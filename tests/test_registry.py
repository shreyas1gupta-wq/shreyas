"""The cycle registry must satisfy its own rules, or it does not load.

These are not incidental unit tests. The registry is the mechanism that stops the
model quietly acquiring more authority than its evidence supports, so each rule
here corresponds to a way the design could fail silently in production.
"""

import pytest

from cyclestack.registry import RegistryError, check, load


@pytest.fixture(scope="module")
def reg():
    return load()


def test_registry_loads_and_satisfies_every_rule():
    assert check(load(validate=False)) == []


def test_narrative_cycles_can_only_reduce_risk(reg):
    """R3. A wrong narrative that de-risks costs carry; one that adds risk costs the mandate."""
    for c in reg.active():
        if c.evidence_tier == "C":
            assert c.one_sided, f"{c.id} is tier C but not one-sided"


def test_all_narrative_cycles_together_move_the_book_less_than_one_good_signal(reg):
    """R4. Ten narrative cycles in unison must move less than a tier-A signal at half strength."""
    cap_pp = reg.meta["tier_c_aggregate_cap_bps"] / 100.0
    for book in ("aggressive", "moderate"):
        total = sum(
            c.influence[book].allocation_l1 for c in reg.active() if c.evidence_tier == "C"
        )
        assert total <= cap_pp + 1e-9


def test_no_cycle_claims_a_clock_it_cannot_observe(reg):
    """R1. A circular phase claim needs at least four observed periods."""
    for c in reg.cycles:
        if c.phase_repr == "circular":
            assert c.n_effective >= 4, f"{c.id} claims a clock on {c.n_effective} observations"


def test_infeasible_data_is_cut_or_proxied(reg):
    """R6. Free-data-only is a design constraint, not an implementation detail."""
    for c in reg.cycles:
        if c.data_tier == "D5":
            assert c.status == "cut" or c.proxy_of, f"{c.id} is D5 but neither cut nor proxied"


def test_mvp_cycles_have_obtainable_data(reg):
    for c in reg.cycles:
        if c.mvp:
            assert c.data_tier != "D5", f"{c.id} is MVP but its data does not exist free"


def test_moderate_book_turnover_fits_its_mandate(reg):
    """The sub-100%/yr cap genuinely binds — this test is why the fast buckets are trimmed."""
    total = sum(c.annual_turnover_pp("moderate") for c in reg.cycles if c.is_cycle_budgeted)
    budget = sum(reg.budget("moderate", b)["turnover_pp"] for b in ("B0", "B1", "B2", "B3", "B4", "B5"))
    assert total <= budget + 1e-9


def test_risk_engine_cycles_are_not_cycle_budgeted(reg):
    """R7. The risk engine may cut without limit; budgeting it would defeat its purpose."""
    unbudgeted = {c.id for c in reg.active() if not c.is_cycle_budgeted}
    assert "funding_stress_spike" in unbudgeted
    assert "volatility_regime_cycle" in unbudgeted


def test_a_broken_registry_refuses_to_load(tmp_path):
    """Validation is on by default and must stay that way."""
    import yaml

    doc = yaml.safe_load(open("config/cycle_registry.yaml"))
    for c in doc["cycles"]:
        if c["id"] == "monetary_order_debasement":
            c["one_sided"] = False  # tier C, now violating R3
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(doc))
    with pytest.raises(RegistryError, match="R3"):
        load(bad)
