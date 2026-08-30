# Layer 15 — Execution Scheduling and the India Transaction Cost Model

**Abstract.** This layer answers the question the whole aggressive mandate stands or falls on: of its 500%/yr turnover ceiling, allocation spends only ~49–65pp (L01/L14), leaving 435–450pp/yr for cross-sectional name selection in the NIFTY 750 tail — does that selection earn more than it costs? Built bottom-up from a full Indian regulatory cost stack (STT, stamp duty, exchange charges, SEBI fees, GST, DP charges, brokerage — with the exercised-ITM-option STT asymmetry stated explicitly) plus a participation-capped square-root impact model calibrated by market-cap decile, the answer is: **at the full 500%/yr ceiling the aggressive book pays ≈3.9% of NAV/yr in round-trip cost; at 100%/yr the moderate book pays ≈0.6%/yr.** The incremental hurdle — the extra gross alpha the aggressive book's cross-sectional engine must clear before its extra churn is worth running at all — is **≈3.3pp/yr at the ceiling, ≈1.3pp/yr at the registry's currently-budgeted turnover.** Independently, this converges with ROADMAP §1.1's top-level placeholder (2.5–4.0% pa drag at 500%) to within the width of its own error bar — a genuine cross-check, not an assumption repeated twice. The layer also specifies the staged-entry scheduler (target weight + ADV + AUM + urgency → tranche dates), the 20%-in-progress queue and its abandonment rule for signals that decay mid-build, the participation-discipline tables that reconcile with L17's liquidity universes, real India execution mechanics (order types, ASM/GSM, T+1, circuit locks), a slippage-feedback loop, and the `CostModel`/`EXEC_COST` contract L14 and L20 already assume exists.

**Scope.** I own: the realised cost function `EXEC_COST.c_j(name, size, urgency)` L14 consumes and never estimates; the staged-entry tranche scheduler; the in-progress queue and abandonment rule; participation discipline and the resulting days-to-build/exit tables; India execution mechanics; slippage TCA and recalibration; the `CostModel` backtest interface. I do **not** own: which names to hold (L08–L12), the target weight itself (L14), ADV/liquidity risk limits at the book level (L17 §6–7, whose `LIQUIDITY(asof)` object I consume rather than recompute), or the free-data pipeline (L19, whose price/volume series feed my ADV and volatility estimators). `expiry_microstructure` was moved here by L01 R6 but is cut (feasible, no allocation authority) — noted, not re-litigated.

---

## 1. The full India cost model

### 1.1 Regulatory, brokerage and DP charges, by instrument

Delivery-equity figures below match L08 §8.4 exactly (frozen there; reused, not re-derived). F&O figures are new to this layer and reflect the Budget 2026 STT revision effective 1-Apr-2026 `[verify against the Finance Act text before go-live]`.

| Component | Equity delivery | Equity intraday | Equity/index futures | Options (premium) | Options (**exercised**) |
|---|---|---|---|---|---|
| STT | 0.10% both legs | 0.025% sell only | 0.05% sell only (↑ from 0.02%, 1-Apr-2026) | 0.15% of premium, sell only (↑ from 0.125%) | **0.15% of settlement/intrinsic value, buyer pays** |
| Stamp duty | 0.015% buy leg | 0.003% buy leg | 0.002% buy leg | ~0.003% buy leg (premium) | 0.015% of delivery value on exercise/assignment |
| Exchange txn charge (NSE) | 0.00297% | 0.00297% | ~0.002% | premium-denominated, higher % of premium but tiny vs notional | as options |
| SEBI fee | ₹10/cr (0.0001%) | same | same | same | same |
| Brokerage (prop desk) | 1.50 bps | 1.50 bps | flat/lot, ≈0.5 bps notional-equiv. | flat/lot | — |
| GST | 18% on (brokerage+exchange) | same | same | same | same |
| DP charge | ~₹18 flat/scrip/sell-day (CDSL/NSDL) | n/a (no delivery) | n/a | n/a | physical delivery only |
| **Explicit total, one leg** | **≈13.0 bps** | ≈4.5 bps | ≈8–9 bps | ≈20–24 bps of premium | see below |

**The asymmetry that destroys unwary sellers.** A sold option's STT (0.15% of *premium*) is small in absolute terms because premium is small. But if that option is **exercised** — expires in-the-money — STT is charged on the **settlement (intrinsic) value**, not the premium, and physically-settled single-stock F&O additionally trigger a **delivery obligation plus delivery-equivalent STT (0.10%+) on the full contract value**. A trader short a stock-option lot for a ₹2,000 premium who lets it go 8% ITM by expiry can face STT on a settlement value many multiples of that premium, plus an unbudgeted delivery obligation and margin call — the mechanism is real, documented, and is precisely why SEBI mandated physical settlement for ITM stock derivatives in 2018. **Operational rule for this layer:** any options position (L16's book) within 3 sessions of expiry that is ITM or near-the-money by more than 1 standard deviation of the underlying's expected move is flagged for a mandatory close-or-roll decision before expiry; the scheduler never allows an ITM position to drift into automatic exercise/assignment. This is a hard, non-negotiable rule, not a preference.

DP charge is negligible in bps at institutional trade sizes but is a genuine *fixed* per-scrip friction — an argument in §3 against fragmenting a tranche schedule beyond what the participation constraint actually requires.

### 1.2 Spread and market impact — the two that dominate

**Spread.** Modelled as a decile-dependent constant, quoted full spread; charged as half-spread per leg. Calibration source: NSE's own published **impact-cost criterion** for index eligibility (a stock must hold impact cost ≤0.50% on a ₹10cr order, 90% of sessions over 6 months, to qualify for Nifty 50/500 membership) — this is a free, NSE-published, per-constituent liquidity metric that should become the layer's primary live calibration input once the data pipeline exists, and is a better anchor than a hand-assumed spread curve.

**Impact — square-root law, participation-aware.** The functional form is Almgren–Chriss / the Barra practitioner rule, matching L08's own calibration (`η = 0.30`) so the two layers never disagree on the coefficient:

```
impact_bps(Q, ADV, σ_daily, p_max) = η · σ_daily · sqrt( min(Q/ADV, p_max) )   ·10,000
   η = 0.30   (Almgren & Chriss 2000/2001; adopted from L08 §8.4, not re-fit here)
```

The `min(Q/ADV, p_max)` term is the load-bearing addition this layer makes. L08's own worked example (`Q/ADV = 0.25 → ~33bps`) implicitly assumes the whole clip trades in one session — a fair approximation for a liquid name where that's what actually happens. But the owner's frozen staged-entry rule (DECISIONS Q12) caps daily participation at `p_max`; once `Q/ADV > p_max`, the order **must** be split across `N = ceil((Q/ADV)/p_max)` sessions, and for an execution held at a constant participation rate, total impact cost collapses to `η·σ_daily·sqrt(p_max)` — **independent of order size.** This is the entire economic case for staging: it converts an impact cost that would otherwise grow without bound in the illiquid tail into a cost that depends only on the stock's own volatility and the chosen participation rate, at the price of calendar time. Section 3's urgency score is exactly the dial that trades one against the other.

`p_max = 10%` standard, `20%` under the urgent/crisis ceiling (matching L17 §7's own crisis-participation convention, reused rather than re-derived).

### 1.3 The cost table, by market-cap decile, round-trip bps

Deciles of 75 names each across the NIFTY 750. Representative ADV is log-linearly interpolated between L17 §7's five rank-band medians (`[verify against a fresh bhavcopy build]`, per L17's own caveat — this table inherits it). `σ_daily` is an assumed annualised-vol-by-decile prior (large-cap deciles anchored near L05's `equity_large` 17% CMA vol, tail deciles rising toward individual-stock idiosyncratic vol above L05's diversified `equity_smid` 24% basket vol) pending the §7 recalibration loop. Impact columns use the reference position sizes L17 §7 already established: a "full 5% position" = ₹5cr (aggressive) / ₹50cr (moderate).

| Decile | Rank band | ADV (₹cr) | σ_daily | Spread (bps) | Explicit (bps) | Impact, agg. (bps) | Impact, mod. (bps) | **RT, agg. (bps)** | **RT, mod. (bps)** |
|---|---|---|---|---|---|---|---|---|---|
| D1 | 1–75 | 584 | 1.13% | 3 | 13.0 | 3.1 | 9.9 | **35** | **49** |
| D2 | 76–150 | 209 | 1.26% | 5 | 13.0 | 5.9 | 12.0 | **43** | **55** |
| D3 | 151–225 | 108 | 1.39% | 8 | 13.0 | 9.0 | 13.2 | **52** | **60** |
| D4 | 226–300 | 67 | 1.58% | 12 | 13.0 | 13.0 | 15.0 | **64** | **68** |
| D5 | 301–375 | 46 | 1.76% | 18 | 13.0 | 16.7 | 16.7 | **77** | **77** |
| D6 | 376–450 | 30 | 2.02% | 27 | 13.0 | 19.2 | 19.2 | **91** | **91** |
| D7 | 451–525 | 17 | 2.27% | 40 | 13.0 | 21.5 | 21.5 | **109** | **109** |
| D8 | 526–600 | 11 | 2.52% | 60 | 13.0 | 23.9 | 23.9 | **134** | **134** |
| D9 | 601–675 | 7.5 | 2.90% | 90 | 13.0 | 27.5 | 27.5 | **171** | **171** |
| D10 | 676–750 | 5.3 | 3.47% | 130 | 13.0 | 32.9 | 32.9 | **222** | **222** |

**The convergence in D5–D10 is not a coincidence.** Both books' reference positions there exceed the 10% participation cap in one session, so both are forced into the staged regime, and staged cost depends only on `σ_daily` and `p_max` — not on order size. **Past the point where staging is mandatory, the ₹1,000cr book pays exactly the same bps to trade a name as the ₹100cr book; the only thing size buys the smaller book is *time*, not lower cost.** This is a genuinely useful, non-obvious result and it is the mechanical reason L17's liquidity section confines the moderate book to ranks 1–500 rather than raising its cost budget: past that point the marginal cost is flat, but the marginal *days* explode (§5).

---

## 2. The turnover arithmetic — the central go/no-go number

Blended round-trip cost = the decile table weighted by each book's realistic holding mix. Aggressive (40 names, per L08 §10, reaching D1–D10): weights 15/15/15/12/10/10/8/6/5/4 across D1–D10. Moderate (30 names, confined to ranks 1–500 with sizes capped below rank 250, per L17 §7): weights 30/25/20/12/8/4/1/0/0/0.

```
blended_RT_aggressive  = Σ w_i · RT_i  = 78.2 bps
blended_RT_moderate    = Σ w_i · RT_i  = 59.5 bps

annual_cost_drag(book) = (one-way turnover, as multiple of 100%) × blended_RT(book)
```

| Book | Turnover | Round trips/yr | Blended RT | **Annual cost drag** |
|---|---|---|---|---|
| Aggressive | **500%/yr (full mandate ceiling)** | 5.00 | 78.2 bps | **391 bps ≈ 3.91% of NAV/yr** |
| Moderate | **100%/yr (full mandate ceiling)** | 1.00 | 59.5 bps | **59.5 bps ≈ 0.60% of NAV/yr** |
| Aggressive | 194.4pp/yr (L14's *measured* budgeted turnover) | 1.944 | 78.2 bps | 152 bps ≈ 1.52%/yr |
| Moderate | 41.2pp/yr (L14's rate-limited budgeted turnover) | 0.412 | 59.5 bps | 24.5 bps ≈ 0.25%/yr |

**State both plainly: at the mandate ceiling, the aggressive book pays ~3.9% of NAV per year to trade; the moderate book pays ~0.6%.** This independently reproduces ROADMAP §1.1's own top-down placeholder — "5 round trips × ~0.5–0.8% all-in ⇒ ~2.5–4.0% pa drag" — to within its stated range, which is a real cross-check: one estimate came from a flat assumption at the whole-book level, this one from decile-level ADV, volatility and participation-capped impact, and they agree. It is **materially higher than L14 §5.2's own figure of 170bps/yr at the 500% ceiling**, because L14's two-bucket (large/mid-small) blend, at a flat 45bps assumption for the whole mid/small tail, understates the deep tail (D8–D10, 171–222bps round-trip) that the aggressive mandate's mid/small reach specifically exists to access. **Flagged as an interface finding, not silently reconciled**: L14 §5.2 should treat this layer's `EXEC_COST` output, not its own placeholder blend, as authoritative — which is exactly what L14's own text says it intends ("Impact is the only calibrated term and it belongs to L15").

**The hurdle.** The gross, pre-cost alpha the aggressive book's cross-sectional engine must clear before its extra 400pp/yr of turnover over the moderate book is worth running at all:

```
incremental_hurdle = annual_cost_drag(aggressive) − annual_cost_drag(moderate)
   at the ceiling:            3.91% − 0.60% = 3.31 pp/yr
   at current registry budgets: 1.52% − 0.25% = 1.27 pp/yr
```

**This is the project's central go/no-go number.** ROADMAP's engineered targets (22–28% aggressive vs 15–19% moderate CAGR) imply a headline gap of roughly 7–13pp, most of which the shared allocation machinery, cash-call engine and leverage policy do not produce (they are near-identical across books). The bulk of that gap has to come from cross-sectional selection, and it has to clear a real, non-trivial hurdle of **1.3pp/yr at today's budgeted turnover, rising to 3.3pp/yr if the aggressive book ever trades at its full ceiling.** The targets are consistent with clearing the lower number with real margin; they are not obviously consistent with clearing the upper one, which is exactly why L14's finding that both books run at ~40% of ceiling (influence-constrained, not turnover-constrained) matters — the honest reading is: **stay influence-constrained, and the arithmetic works; chase the full turnover ceiling, and the hurdle roughly doubles for no independently-demonstrated alpha gain.**

---

## 3. The staged-entry scheduler

**Strict separation, stated once and enforced everywhere below:** L14 emits a *target weight*, already cap-projected (entry/drift ratchet, sector caps, in-progress budget). This layer never alters that target. It only decides the *path* — how many tranches, what size, on what calendar.

**Inputs:** target weight `w*` (L14), current weight `w0`, name ADV, book AUM, urgency `u ∈ [0,1]`.

```
Δw       = w* − w0 ;  Q_total = |Δw| · AUM
p_max    = 0.10                                    # standard; 0.20 under urgency-driven override, hard ceiling
N_min    = ceil( (Q_total/ADV) / p_max )            # physical minimum sessions at the participation cap
N_default = max(3, ceil(|Δw| / 1.0%))               # owner's frozen default: ~1% clips, floor of 3 for thin names
N_tranches      = max(N_min, round(N_default · (1 − 0.6·u)))
spacing_days    = round(base_spacing · (1 − 0.7·u)) ,  base_spacing = 8 trading days
participation   = min(0.20, 0.10 · (1 + u))
```

**Urgency, generalised beyond momentum.** The task's own framing — a fast momentum signal is urgent, a slow valuation signal is not — is exactly what L01's `tau_half` already encodes, so urgency reuses it rather than inventing a parallel concept:

```
U_signal(name) = clip( 1 − tau_half_effective(name) / TAU_REF , 0, 1 ) ,  TAU_REF = 24 months
tau_half_effective = the contribution-weighted average tau_half of the cycles/factors that moved this
                      name's target weight this rebalance, read from L14's CONSTRAINT_LOG / arbitration log
```

`intermediate_momentum_12_1` (τ=6m) → `U=0.75`; `short_reversal_1m` (τ=1m) → `U=0.96`; `equity_valuation_reversion` (τ=84–120m) → `U=0`. Where L08 already publishes a per-name urgency in `EXEC_HINTS.urgency` (momentum-attributed trades only), that value is consumed **directly** — this layer never recomputes it. `U_signal` is used only for trades attributed to every other signal family (L09–L12), which L08 does not score.

**Worked example — L14 §9.6's own flagged case, resolved.** Name N3 (mid-cap metal), aggressive book, target 3.5%, current 0%, ADV ₹15cr.

| Case | `U` | `N_tranches` | Spacing | Participation | Schedule |
|---|---|---|---|---|---|
| Momentum-driven (τ=6m) | 0.667 | round(4×0.60)=**2** | round(8×0.533)=**4** trading days | 16.7% | 2 tranches of 1.75% each, ~1 week total |
| Valuation-driven (τ=90m) | 0.00 | **4** | **8** trading days | 10.0% | 4 tranches of ~0.875%, ~5 weeks total |

The urgent case matches the physical minimum almost exactly (a genuinely fast signal decays faster than the default cadence would respect, so the scheduler compresses toward it); the patient case reproduces the owner's literal description — "roughly three buys... several weeks" — closely, with one extra tranche because 3.5% is larger than a minimal thin-name entry.

---

## 4. The 20% in-progress budget: queue, priority, and the abandonment rule

L14's linear constraint (`Σ max(0, w*_j − w0_j)` over incomplete names `≤ 20%`) is consumed as a hard ceiling; this layer owns what happens when demand for construction exceeds it.

**Priority score**, admitted greedily until the cap binds:

```
priority(name) = |contribution to expected active return| × (0.5 + 0.5·U_signal)
              ÷ remaining_gap_pp(name)
```

Higher urgency and higher expected-return contribution move a name up the queue; a larger remaining gap (more budget consumed per name admitted) moves it down — the queue prefers to *finish* cheap, high-conviction, urgent positions over *starting* expensive ones. Ties broken toward higher ADV (a more liquid name vacates its queue slot faster, recycling budget sooner).

**The abandonment rule — the failure mode people miss.** A name mid-build whose driving signal changes while `w_current < w*` splits into two cases, not one:

| Case | Trigger | Action |
|---|---|---|
| **FADE** | `z` crosses the registry's `exit_z` (L01 §7.4 hysteresis) but keeps its sign, or `w*` shrinks by <50% | **Freeze.** Stop building at the current partial weight. Do not sell. Redefine `w* ← w_current` **for in-progress-budget accounting only**, immediately releasing the remaining gap back to the queue. The position's *actual* target stays flagged `stale_pending_refresh` and is re-read fresh next rebalance. This is the direct fix to L17 §12 risk 9 (orphaned frozen positions silently consuming budget forever) |
| **REVERSAL** | `z` crosses zero (sign flip), or `w*` collapses ≥50% toward zero, or a hard L17 limit (17: single-name days-to-liquidate) is breached | **Abandon.** Queue an immediate unwind of the partial position using the §3 schedule with urgency inherited from the reversal itself — a signal reversal is typically a *fast* event and is scored accordingly, not defaulted to patient |

A frozen (not abandoned) position is never sold on this rule alone; it is re-underwritten as a normal holding at its partial weight and re-enters the ordinary scoring cycle. This is deliberate: freezing avoids selling into the exact illiquidity that made the position slow to build in the first place, while abandonment exists precisely for the case where holding is now actively wrong, not just less urgent.

---

## 5. Participation discipline, and days-to-build/exit by decile

`days = Q / (p · ADV)`, using the §1.3 decile ADV table and the reference position sizes (₹5cr agg / ₹50cr mod).

| Decile | ADV (₹cr) | Days @10%, agg. | Days @20%, agg. | Days @10%, mod. | Days @20%, mod. |
|---|---|---|---|---|---|
| D1 | 584 | 0.09 | 0.04 | 0.86 | 0.43 |
| D2 | 209 | 0.24 | 0.12 | 2.39 | 1.20 |
| D3 | 108 | 0.46 | 0.23 | 4.63 | 2.31 |
| D4 | 67 | 0.75 | 0.37 | 7.46 | 3.73 |
| D5 | 46 | 1.09 | 0.54 | 10.87 | 5.43 |
| D6 | 30 | 1.67 | 0.83 | 16.67 | 8.33 |
| D7 | 17 | 2.94 | 1.47 | 29.41 | 14.70 |
| D8 | 11 | 4.55 | 2.27 | 45.45 | 22.73 |
| D9 | 7.5 | 6.67 | 3.33 | 66.67 | 33.33 |
| D10 | 5.3 | 9.43 | 4.72 | 94.34 | 47.17 |

This is a finer-grained restatement of L17 §7's own rank-band table (which used 5 bands, not 10 deciles) and L08 §10's fixed-build-days design point (5 days agg / 15 days mod at 10% participation) — both reproduce as special cases rather than being contradicted: L17's "251–500 band, mod: 12.5 days" sits between my D4 (7.5d) and D6 (16.7d), exactly where the band's width implies it should. **The reconciliation with L17's finding:** the aggressive book's days-to-build stay single-digit through D9 and only reach ~9.4 days at the very tail (D10) — consistent with "the ₹100cr book can hold the full NIFTY 750." The moderate book's days-to-build cross into the tens by D5 and the tens-of-**weeks** by D7 (29 days ≈ 6 trading weeks for a single name) — the arithmetic reason L17 confines it to ranks 1–500 and caps sizes below rank 250 is visible directly in this table, not asserted separately.

---

## 6. Rebalance execution — 200–400 names, real India mechanics

**Order types available on retail/prop infrastructure.** NSE natively supports **disclosed-quantity (iceberg) orders** — the right primitive for tail names, since it avoids signalling the full clip; broker APIs (Kite Connect, ICICI Direct API, and prime/DMA desks for larger books) support **basket/bulk order upload** for a 200–400-name rebalance in one submission, and **POV (percent-of-volume) or VWAP-benchmarked algos** for names where the scheduler's tranche should itself be spread across the session rather than dropped as one clip.

**ASM/GSM.** L08 already excludes GSM/ASM stage ≥2 from its universe (`gsm_asm_stage(i,t) < 2`). Stage-0/1 names still eligible get: limit-only orders (never market — ASM often carries trade-for-trade settlement, removing intraday netting), the daily participation cap halved, and immediate re-queue into the §4 abandonment path the session a name escalates to stage 2 (a forced exit, executed per L17 §8's own prescription for a trapped tail position: hedge in index/sector futures rather than chase a locked book).

**Circuit limits.** Individual bands are typically 2/5/10/20%, tighter for surveillance names. A circuit-locked order **does not chase**: the unfilled tranche carries forward unmodified to the next session; three consecutive locked sessions escalate the name into the §4 queue at elevated priority (it is now effectively untradeable at any reasonable participation and should either wait or convert to a futures-hedged exposure per L17 §8's liquidity-event playbook).

**T+1 settlement.** Sale proceeds and shares settle T+1, not same-day. A rebalance that funds buys from sells must therefore either draw on existing cash/margin headroom for same-day fills, or explicitly schedule the funded buy leg for T+1 — the scheduler sequences multi-name rebalances so this never silently creates an unplanned one-day leverage gap; it is a scheduling constraint, not a risk-engine matter (L17 owns actual leverage/margin limits; this layer only avoids tripping them through poor sequencing).

**Intraday schedule.** Standard participation avoids the first and last ~15 minutes (opening/closing auction volatility); tranches execute via POV/VWAP through the middle of the session. High-urgency trades (u→1) are explicitly permitted to trade into the open/close if needed for certainty of fill — the urgency score trades benchmark-tracking for speed, consistent with §3.

---

## 7. Slippage measurement and feedback

Every execution logs an **implementation-shortfall decomposition** (Perold 1988): `decision_price → arrival_price` (delay cost, owned by the scheduler's queueing decisions) and `arrival_price → average_fill_price` (impact/timing, owned by the cost model's calibration). Monthly:

```
bias_ratio = realised_cost_bps / model_predicted_cost_bps     (per decile, pooled)
```

If `bias_ratio` sits outside `[0.80, 1.25]` for **3 consecutive months** in a given decile, `η` (the impact coefficient) is re-estimated by rolling regression of realised impact on `σ_daily·sqrt(Q/ADV)` for that decile, and the change is logged with before/after values — the same discipline L14 §1.5 and L17 §5 already apply to their own bias-ratio checks, reused rather than reinvented. Every recalibration event is written to the same append-only register `02-ECONOMETRIC-METHODS.md §5.3` mandates for signals, because a cost-model parameter that is quietly tuned to make a backtest look better is exactly the fitted-threshold failure mode that document forbids.

---

## 8. The backtest interface

```python
class CostModel(Protocol):
    def estimate(self, symbol: str, side: Literal["buy","sell"], notional_inr: float,
                 asof: date, urgency: float = 0.0) -> CostEstimate: ...

CostEstimate = {
    explicit_bps: float,     # §1.1, instrument-specific
    spread_bps: float,       # half-spread, one leg
    impact_bps: float,       # eta * sigma_daily * sqrt(min(Q/ADV, p_max)), staged-execution-aware
    total_bps: float,        # one-way = explicit + spread + impact
    round_trip_bps: float,   # 2 x total_bps
    days_to_fill: float,     # at the urgency-implied participation rate
}

EXEC_COST.c_j(name, size, urgency) -> total_bps      # exact name L14 §11 already assumes

SCHEDULE     = {symbol, target_weight, tranches: [{date, size_pp, participation_pct}],
                urgency, days_to_complete}
IN_PROGRESS  = {aggregate_pct, queue: [...], frozen: [...], abandoned_log: [...]}
SLIPPAGE_REPORT = {bias_ratio_by_decile, recalibration_events, decomposition}
```

**Fixtures.** Reuses L14's planned synthetic 750-name panel (its MVP step 12) rather than building a second one: the same seeded 12-factor process already carries an 8%-illiquid tail, and this layer adds only a committed `{decile, adv_cr, sigma_daily, spread_bps}` panel (§1.3's table, plus a "stressed" variant at half ADV / 2–3× spread, per L17's crisis-haircut convention) and a synthetic order-flow generator driving the scheduler end-to-end. Zero live data required, per `ENVIRONMENT-CONSTRAINTS.md`. Actual trade fills (for §7's TCA loop) come from the owner's own broker/OMS export, not a free market-data source — flagged as a distinct, always-available-once-live input rather than a data-feasibility problem.

---

## 9. MVP versus deferred

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Cost model core | §1 explicit-cost table by instrument, spread/impact formulas, decile calibration table | 2.5 | ✅ |
| 2 | `CostModel` / `EXEC_COST` interface + fixtures | §8 contract, decile panel fixture, reuse of L14's synthetic universe | 1.5 | ✅ |
| 3 | Turnover arithmetic report | §2 as a runnable report, both books, ceiling and measured-budget variants | 1.0 | ✅ |
| 4 | Staged-entry scheduler | §3 tranche/spacing/participation formulas, urgency scoring, `EXEC_HINTS` consumption | 3.0 | ✅ |
| 5 | In-progress queue + abandonment | §4 priority score, freeze/abandon state machine, budget release logic | 2.0 | ✅ |
| 6 | Participation/DTL tables | §5 decile tables, reconciliation checks against L17 §7 and L08 §10 | 1.0 | ✅ |
| 7 | Execution mechanics rules | §6 ASM/GSM handling, circuit no-chase, T+1 sequencing, order-type routing | 2.0 | ✅ |
| 8 | Slippage TCA + feedback | §7 implementation-shortfall logging, bias-ratio monitor, recalibration trigger | 2.0 | ✅ |
| 9 | Property tests | For any target-weight vector: in-progress cap never breached, no circuit-chase, urgency bounds respected | 2.0 | ✅ |
| **MVP total** | | | **17.0** | |
| 10 | Live broker-API integration (order routing, real fills) | Deferred until the owner has live capital; not needed to validate the model | 4 | ⬜ |
| 11 | Options-exercise auto-close/roll automation | v1 is a flagged manual check (§1.1); automation is v1.5 | 2 | ⬜ |
| 12 | NSE-published impact-cost ingestion (replacing the assumed spread curve) | Needs the live data pipeline (L19); the assumed table is the MVP substitute | 2 | ⬜ |

---

## 10. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L14 | `TARGET_PORTFOLIO`, `CONSTRAINT_LOG` (for signal attribution), `IMPLIED_RETURNS` | Target weights are final; never altered here |
| L08 | `EXEC_HINTS.{urgency, max_daily_participation_pct, est_days_to_fill, tom_window_flag}` | Consumed directly for momentum-attributed trades; never recomputed |
| L01 | `tau_half_months` per registry entry | Drives `U_signal` for every non-momentum trade |
| L17 | `LIQUIDITY(asof)` (adv60, dtl fields), `fast_trigger_flags`, `gross_ceiling` | Canonical ADV source — never recomputed independently; fast/crisis de-risking stays in index futures per L17 §3.2 and is out of this layer's scope |
| L19 | `adj_prices(asof)`, `universe(asof)` | For `σ_daily` estimation and decile assignment |
| Owner's OMS/broker | Trade fills, timestamps | For §7 TCA; not a free-data-pipeline object |

**Exposes:** `CostModel` / `EXEC_COST.c_j` (to L14), `SCHEDULE` and `IN_PROGRESS` (to the execution desk and to L17's in-progress limit), `SLIPPAGE_REPORT` (to L20).

---

## 11. Risks and constraint conflicts

1. **L14 §5.2's cost figures should be superseded by this layer's, not averaged with them.** The gap (170 vs 391 bps/yr at the aggressive ceiling) is large enough to change the central hurdle number by roughly 2×; L14's own text already defers to L15 on impact, so this is a completion of that deferral, not a dispute.
2. **The decile ADV/vol/spread table is an assumption pending live calibration**, exactly like L17 §7's rank-band table it extends. Both should be replaced by the same fresh bhavcopy build the moment L19 exists.
3. **The exercised-option STT trap is an operational rule, not yet automated.** Until step 11 (deferred) ships, a human must action the mandatory close-or-roll flag inside the 3-session pre-expiry window; a missed flag is a real capital-loss event, not a modelling nicety.
4. **Fixed per-scrip friction (DP charge, minimum brokerage ticket) is not yet in the tranche-count optimisation.** For the smallest thin-name entries this could argue for fewer, larger tranches than §3's formula alone implies; flagged for v1.5, not expected to change any number by more than a few bps.
5. **The urgency framework assumes attribution to a single dominant signal family.** A name whose weight change is genuinely split across a fast and a slow signal in comparable magnitude gets a blended `tau_half_effective` that may under- or over-state true urgency in either direction; this is the same aggregation problem L01 §6 solves for allocation and is not yet solved here for execution.

---

## References

1. Almgren, R. & Chriss, N. (2000). "Optimal execution of portfolio transactions." *Journal of Risk* 3(2), 5–39; and (2001) *ibid.* — square-root impact law, participation-rate cost scaling; coefficient adopted from L08 §8.4.
2. Kyle, A. (1985). "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1315–1335. — theoretical grounding for linear/square-root price impact.
3. Perold, A. (1988). "The Implementation Shortfall: Paper versus Reality." *Journal of Portfolio Management* 14(3), 4–9. — the §7 TCA decomposition.
4. Grinold, R. & Kahn, R. (2000). *Active Portfolio Management*, 2nd ed. — the fundamental-law framing behind §2's hurdle.
5. Novy-Marx, R. & Velikov, M. (2016). "A Taxonomy of Anomalies and Their Trading Costs." *Review of Financial Studies* 29(1). — real-world anomaly cost fragility, already used by L14 §5.1 for the short-reversal hurdle.
6. NSE — Methodology Document for Equity Indices (impact-cost eligibility criterion, ≤0.50% on a ₹10cr basket), <https://www.niftyindices.com/Methodology/Method_NIFTY_Equity_Indices.pdf>. Free, per-constituent liquidity metric; the recommended future calibration anchor for §1.2's spread curve.
7. STT rates effective 1-Apr-2026 (Budget 2026–27 F&O revision): [Zerodha — STT calculation](https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated), [VRD Nation — STT rates 2026](https://www.vrdnation.com/stt-cash-fno-intraday/). `[verify against the Finance Act text before circulation]`.
8. Exercised-option STT and physical settlement of ITM stock derivatives: [Upstox — how options are settled](https://upstox.com/learning-center/futures-and-options/how-are-options-settled/article-525/); SEBI circular mandating physical settlement of stock F&O (2018) `[verify circular number]`.
9. `docs/model/08-momentum-technical.md` §8.4, §10 — the frozen delivery-equity cost stack and the ADV-participation position-cap formula this layer implements the execution path for.
10. `docs/model/17-risk-drawdown-cash-engine.md` §7 — the rank-band ADV/DTL table this layer's decile table refines and reconciles against.
11. `docs/model/14-allocation-optimizer.md` §5.2, §11 — the `EXEC_COST.c_j` interface contract and the turnover figures this layer supersedes with a calibrated impact term.

*Items marked `[verify]` require confirmation against the primary source before circulation.*
