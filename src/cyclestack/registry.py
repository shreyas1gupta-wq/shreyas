"""Cycle registry: load, validate, and expose the cycle stack's contract.

The registry is DATA, not code. Every threshold, band and influence cap for every
cycle lives in ``config/cycle_registry.yaml`` and is validated here. Nothing in the
model may hardcode a cycle parameter.

The validation rules come from ``docs/model/01-cycle-taxonomy.md`` and exist to stop
the model quietly acquiring more authority than its evidence supports:

    R1  A cycle may claim a circular phase only with >= 4 observed periods.
    R3  Tier-C (narrative) cycles may only REDUCE risk.
    R4  All tier-C cycles combined may move the book at most 150 bps.
    R6  A cycle whose data is infeasible free is cut, or carries a named proxy.
    R7  Cycle budgets govern ADDING risk; the risk engine may cut without limit.

Plus containment (per-bucket budgets), aggregation (3-sigma), turnover, and DAG
acyclicity. A registry that fails any of these does not load.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

BUCKETS = ("B0", "B1", "B2", "B3", "B4", "B5")
BOOKS = ("aggressive", "moderate")
_BOOK_KEY = {"aggressive": "agg", "moderate": "mod"}
TARGETS = ("equity_pp", "gold_pp", "debt_pp")

#: Variance of a signal distributed roughly uniformly on [-1, 1], used in the
#: 3-sigma aggregation test. Buckets are near-independent after orthogonalization,
#: so the worst case (every cycle screaming at once) never occurs and summing
#: budgets linearly would wildly overstate the real exposure.
_UNIFORM_VAR = 0.33


class RegistryError(ValueError):
    """Raised when the registry violates a rule. Never caught in production code."""


@dataclass(frozen=True)
class Influence:
    """One cycle's allocation authority for one book, in percentage points of NAV."""

    equity_pp: tuple[float, float]  # (down, up)
    gold_pp: tuple[float, float]
    debt_pp: tuple[float, float]
    sector_l1_pp: float
    name_l1_pp: float
    leverage_x: tuple[float, float]

    @property
    def allocation_l1(self) -> float:
        """Total allocation authority across asset classes, worst direction each."""
        return sum(max(getattr(self, t)) for t in TARGETS)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Influence":
        return cls(
            equity_pp=tuple(d.get("equity_pp", (0, 0))),
            gold_pp=tuple(d.get("gold_pp", (0, 0))),
            debt_pp=tuple(d.get("debt_pp", (0, 0))),
            sector_l1_pp=float(d.get("sector_l1_pp", 0)),
            name_l1_pp=float(d.get("name_l1_pp", 0)),
            leverage_x=tuple(d.get("leverage_x", (0, 0))),
        )


@dataclass(frozen=True)
class Cycle:
    """A single entry in the cycle registry."""

    id: str
    name: str
    bucket: str
    tau_half_months: float
    phase_repr: str
    evidence_tier: str
    data_tier: str
    status: str
    mvp: bool
    one_sided: bool
    owner_layer: str | None
    parent_id: str | list[str] | None
    family: str
    mechanism: str
    n_effective: float
    proxy_of: str | None
    cut_reason: str | None
    influence: dict[str, Influence] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_cycle_budgeted(self) -> bool:
        """False for risk-engine cycles, which are unbudgeted by rule R7.

        R7 makes authority deliberately asymmetric: cycle signals are budgeted for
        ADDING risk, while the risk engine may cut exposure without limit and at any
        cadence. A funding-stress trigger that could only de-risk by its bucket
        allowance would be useless in exactly the crash it exists for.
        """
        return self.is_active and self.raw.get("authority", "cycle_budget") == "cycle_budget"

    def annual_turnover_pp(self, book: str) -> float:
        """Expected one-way turnover this cycle generates, pp of NAV per year.

        For an Ornstein-Uhlenbeck signal with half-life ``h`` scaled to a +/- b range,
        expected annual one-way turnover is approximately ``1.6 * b * sqrt(12 / h)``.
        Faster signals with the same authority cost proportionally more to trade,
        which is why the moderate book's fast buckets are cut rather than merely damped.
        """
        # Allocation moves are self-funding: raising gold 5pp is paid for by cutting
        # equity 5pp, which is 5pp of one-way turnover, not 10. Summing L1 across
        # asset classes double-counts the trade, so halve it.
        b = self.influence[book].allocation_l1 / 2.0
        return 1.6 * b * math.sqrt(12.0 / max(self.tau_half_months, 0.25))


@dataclass(frozen=True)
class Registry:
    cycles: tuple[Cycle, ...]
    meta: dict[str, Any]

    def __getitem__(self, cycle_id: str) -> Cycle:
        for c in self.cycles:
            if c.id == cycle_id:
                return c
        raise KeyError(cycle_id)

    def active(self) -> tuple[Cycle, ...]:
        return tuple(c for c in self.cycles if c.is_active)

    def in_bucket(self, bucket: str, active_only: bool = True) -> tuple[Cycle, ...]:
        pool: Iterable[Cycle] = (
            tuple(c for c in self.cycles if c.is_cycle_budgeted) if active_only else self.cycles
        )
        return tuple(c for c in pool if c.bucket == bucket)

    def budget(self, book: str, bucket: str) -> dict[str, Any]:
        return self.meta["bucket_budgets"][book][bucket]


def load(path: str | Path = "config/cycle_registry.yaml", validate: bool = True) -> Registry:
    """Load and (by default) validate the registry.

    Validation is on by default and should stay that way: a registry that violates
    its own influence budget is worse than no registry, because it looks principled.
    """
    doc = yaml.safe_load(Path(path).read_text())
    cycles = tuple(_parse(entry) for entry in doc["cycles"])
    reg = Registry(cycles=cycles, meta=doc["meta"])
    if validate:
        problems = check(reg)
        if problems:
            raise RegistryError(
                f"{len(problems)} registry violation(s):\n  - " + "\n  - ".join(problems)
            )
    return reg


def _parse(e: dict[str, Any]) -> Cycle:
    influence = {}
    inf = e.get("influence") or {}
    for book in BOOKS:
        influence[book] = Influence.from_dict(inf.get(_BOOK_KEY[book], {}))
    n_obs = e.get("n_obs") or {}
    return Cycle(
        id=e["id"],
        name=e["name"],
        bucket=e["bucket"],
        tau_half_months=float(e["tau_half_months"]),
        phase_repr=e["phase_repr"],
        evidence_tier=e["evidence_tier"],
        data_tier=e["data_tier"],
        status=e["status"],
        mvp=bool(e.get("mvp", False)),
        one_sided=bool(e.get("one_sided", False)),
        owner_layer=e.get("owner_layer"),
        parent_id=e.get("parent_id"),
        family=e.get("family", "unknown"),
        mechanism=e.get("mechanism", ""),
        n_effective=float(n_obs.get("effective", 0.0)),
        proxy_of=e.get("proxy_of"),
        cut_reason=e.get("cut_reason"),
        influence=influence,
        raw=e,
    )


# ---------------------------------------------------------------- rule checks

def check(reg: Registry) -> list[str]:
    """Run every registry rule. Returns a list of human-readable violations."""
    problems: list[str] = []
    for fn in (
        _check_structure,
        _check_r1_clock_test,
        _check_r3_tier_c_one_sided,
        _check_r4_tier_c_aggregate,
        _check_r6_d5_kill_switch,
        _check_mvp_feasible,
        _check_bucket_containment,
        _check_three_sigma,
        _check_turnover,
        _check_dag,
    ):
        problems.extend(fn(reg))
    return problems


def _check_structure(reg: Registry) -> list[str]:
    out = []
    seen = set()
    for c in reg.cycles:
        if c.id in seen:
            out.append(f"{c.id}: duplicate id")
        seen.add(c.id)
        if c.bucket not in BUCKETS:
            out.append(f"{c.id}: unknown bucket {c.bucket!r}")
        if c.evidence_tier not in ("A", "B", "C"):
            out.append(f"{c.id}: evidence_tier must be A/B/C, got {c.evidence_tier!r}")
        if c.status not in ("active", "deferred", "cut"):
            out.append(f"{c.id}: unknown status {c.status!r}")
        if c.status == "cut" and not c.cut_reason:
            out.append(f"{c.id}: status 'cut' requires cut_reason")
        if not c.mechanism:
            out.append(f"{c.id}: mechanism is required — a cycle with no causal story is numerology")
    return out


def _check_r1_clock_test(reg: Registry) -> list[str]:
    """R1: a circular phase claim needs >= 4 observed periods."""
    return [
        f"R1 violated — {c.id}: phase_repr 'circular' with only "
        f"{c.n_effective} effective observations (need >= 4). "
        f"Use 'state', 'ordinal' or 'calendar' instead."
        for c in reg.cycles
        if c.phase_repr == "circular" and c.n_effective < 4
    ]


def _check_r3_tier_c_one_sided(reg: Registry) -> list[str]:
    """R3: narrative cycles may only reduce risk.

    A wrong narrative that de-risks costs carry. A wrong narrative that adds risk
    costs the mandate.
    """
    return [
        f"R3 violated — {c.id}: evidence_tier C must set one_sided: true"
        for c in reg.cycles
        if c.evidence_tier == "C" and c.status == "active" and not c.one_sided
    ]


def _check_r4_tier_c_aggregate(reg: Registry) -> list[str]:
    """R4: all tier-C cycles together may move the book at most 150 bps."""
    cap_pp = reg.meta["tier_c_aggregate_cap_bps"] / 100.0
    out = []
    for book in BOOKS:
        total = sum(
            c.influence[book].allocation_l1
            for c in reg.active()
            if c.evidence_tier == "C"
        )
        if total > cap_pp + 1e-9:
            out.append(
                f"R4 violated — {book}: tier-C cycles claim {total:.2f}pp of "
                f"allocation authority, cap is {cap_pp:.2f}pp"
            )
    return out


def _check_r6_d5_kill_switch(reg: Registry) -> list[str]:
    """R6: a cycle whose data is infeasible free is cut, or carries a named proxy."""
    return [
        f"R6 violated — {c.id}: data_tier D5 requires status 'cut' or a proxy_of"
        for c in reg.cycles
        if c.data_tier == "D5" and c.status != "cut" and not c.proxy_of
    ]


def _check_mvp_feasible(reg: Registry) -> list[str]:
    return [
        f"{c.id}: mvp: true but data_tier {c.data_tier} — MVP requires D1-D4"
        for c in reg.cycles
        if c.mvp and c.data_tier == "D5"
    ]


def _check_bucket_containment(reg: Registry) -> list[str]:
    """Cycles in a bucket may not, together, exceed that bucket's budget."""
    out = []
    for book in BOOKS:
        for bucket in BUCKETS:
            cycles = reg.in_bucket(bucket)
            if not cycles:
                continue
            budget = reg.budget(book, bucket)
            for target, key in (("equity_pp", "equity"), ("gold_pp", "gold"), ("debt_pp", "debt")):
                for idx, direction in ((0, "down"), (1, "up")):
                    claimed = sum(getattr(c.influence[book], target)[idx] for c in cycles)
                    allowed = budget[key][idx]
                    if claimed > allowed + 1e-9:
                        out.append(
                            f"budget overrun — {book}/{bucket} {key} {direction}: "
                            f"cycles claim {claimed:.2f}pp, bucket allows {allowed:.2f}pp"
                        )
            for attr, key in (("sector_l1_pp", "sector_l1"), ("name_l1_pp", "name_l1")):
                claimed = sum(getattr(c.influence[book], attr) for c in cycles)
                allowed = budget[key]
                if claimed > allowed + 1e-9:
                    out.append(
                        f"budget overrun — {book}/{bucket} {key}: "
                        f"cycles claim {claimed:.2f}pp, bucket allows {allowed:.2f}pp"
                    )
    return out


def _check_three_sigma(reg: Registry) -> list[str]:
    """3-sigma aggregation must stay inside the mandate caps.

    Buckets are near-independent, so the linear sum of budgets is not the right
    test — it would be absurdly conservative. The right test is whether a 3-sigma
    draw across independent buckets still lands inside the hard caps.
    """
    caps = reg.meta["mandate_caps"]
    neutral = reg.meta["neutral_portfolio"]
    out = []
    headroom = {
        ("equity_pp", 0): neutral["equity_pct"] - caps["equity_floor_pct"],
        ("equity_pp", 1): caps["gross_leverage_max_x"] * 100 - neutral["equity_pct"],
        ("gold_pp", 0): neutral["gold_pct"] - caps["gold_insurance_floor_pct"],
        ("gold_pp", 1): caps["gold_max_pct"] - neutral["gold_pct"],
        ("debt_pp", 0): neutral["debt_pct"],
        ("debt_pp", 1): caps["debt_max_pct"] - neutral["debt_pct"],
    }
    for book in BOOKS:
        for target, idx in headroom:
            per_bucket = [
                sum(getattr(c.influence[book], target)[idx] for c in reg.in_bucket(b))
                for b in BUCKETS
            ]
            sigma3 = 3.0 * math.sqrt(_UNIFORM_VAR * sum(b * b for b in per_bucket))
            room = headroom[(target, idx)]
            if sigma3 > room + 1e-9:
                out.append(
                    f"3-sigma breach — {book} {target} "
                    f"{'down' if idx == 0 else 'up'}: 3sigma={sigma3:.1f}pp "
                    f"exceeds headroom {room:.1f}pp"
                )
    return out


def _check_turnover(reg: Registry) -> list[str]:
    """Asset-allocation turnover must fit inside each book's turnover budget."""
    out = []
    for book in BOOKS:
        total = sum(c.annual_turnover_pp(book) for c in reg.cycles if c.is_cycle_budgeted)
        allowed = sum(reg.budget(book, b)["turnover_pp"] for b in BUCKETS)
        if total > allowed + 1e-9:
            out.append(
                f"turnover overrun — {book}: cycles generate {total:.1f}pp/yr of "
                f"asset-allocation turnover, budget is {allowed:.1f}pp/yr"
            )
    return out


def _check_dag(reg: Registry) -> list[str]:
    """Parent-child relations must form a DAG and resolve to real cycles."""
    ids = {c.id for c in reg.cycles}
    parents: dict[str, list[str]] = {}
    out = []
    for c in reg.cycles:
        p = c.parent_id
        ps = [] if p is None else ([p] if isinstance(p, str) else list(p))
        for parent in ps:
            if parent not in ids:
                out.append(f"{c.id}: parent_id {parent!r} does not exist")
        parents[c.id] = [x for x in ps if x in ids]

    state: dict[str, int] = {}

    def visit(node: str, trail: list[str]) -> None:
        if state.get(node) == 2:
            return
        if state.get(node) == 1:
            out.append(f"cycle in parent DAG: {' -> '.join(trail + [node])}")
            return
        state[node] = 1
        for parent in parents.get(node, []):
            visit(parent, trail + [node])
        state[node] = 2

    for cid in parents:
        visit(cid, [])
    return out


if __name__ == "__main__":  # pragma: no cover
    import sys

    problems = check(load(validate=False))
    for p in problems:
        print(f"FAIL  {p}")
    print(f"\n{len(problems)} violation(s)")
    sys.exit(1 if problems else 0)
