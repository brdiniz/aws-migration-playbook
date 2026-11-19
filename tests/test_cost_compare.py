import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import cost_compare as cc  # noqa: E402

DATA = {
    "company": "Test",
    "horizon_months": 24,
    "current_monthly": {"a": 10000},
    "target_monthly": {"b": 5000},
    "ownership_monthly": 1000,
    "one_time": {"x": 20000},
    "double_run_months": 1,
}


def _expected():
    return {s.name: s for s in cc.build_scenarios(DATA)}["expected"]


def test_expected_scenario_math():
    s = _expected()
    assert s.target_monthly == 6000  # 5000 + 1000 ownership
    assert s.monthly_delta == 4000
    assert s.one_time == 30000  # 20000 + one month of double running (10000)
    assert s.break_even_month == 8  # ceil(30000 / 4000)
    assert s.net_at(12) == 4000 * 12 - 30000


def test_pessimistic_is_worse_than_optimistic():
    by_name = {s.name: s for s in cc.build_scenarios(DATA)}
    assert by_name["pessimistic"].monthly_delta < by_name["optimistic"].monthly_delta
    assert by_name["pessimistic"].one_time > by_name["optimistic"].one_time


def test_never_breaks_even_when_aws_costs_more():
    data = dict(DATA, target_monthly={"b": 20000})
    s = {x.name: x for x in cc.build_scenarios(data)}["expected"]
    assert s.break_even_month is None


def test_render_mentions_never_and_checkpoints():
    data = dict(DATA, target_monthly={"b": 20000})
    out = cc.render(data, cc.build_scenarios(data))
    assert "never" in out
    assert "Net @12m" in out


def test_load_rejects_missing_sections(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"current_monthly": {"a": 1}}))
    with pytest.raises(ValueError):
        cc.load(str(bad))


def test_example_file_runs(capsys):
    example = os.path.join(os.path.dirname(__file__), "..", "examples", "acme-saas.json")
    assert cc.main([example]) == 0
    assert "Acme SaaS" in capsys.readouterr().out
