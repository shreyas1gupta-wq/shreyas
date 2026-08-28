# Layer 01 — Cycle Taxonomy and the Horizon Ladder

**Abstract.** This layer is the registry, the arithmetic and the rulebook that every other cycle-producing layer conforms to. It enumerates 32 candidate cycles from ~250 years to ~1 month, and reaches an uncomfortable but load-bearing conclusion: **most of what the model calls "cycles" are not periodic and cannot be treated as clocks.** Post-liberalisation India offers three dated recessions (Pandey–Patnaik–Shah), roughly two credit cycles, one incomplete capex swing, one real-estate observation, and zero complete long waves. A registry entry may therefore only claim a *period* if at least four of them have been independently observed; everything else is carried as a persistent **state** with a declared autocorrelation half-life `tau_half`, which becomes the master coordinate of the ladder and mechanically sets smoothing, rate limits and turnover. Phase, where it exists, is carried as a von Mises distribution, and the resulting signal attenuation falls out in closed form as `R = exp(−σ_c²/2)` — so a badly-dated cycle automatically loses influence without any bolted-on penalty. Double-counting is handled by a declared parent–child DAG with slowest-first residualization, shrinkage keyed to the number of *independent cycle observations* rather than data points, and a correlation-cluster cap; the worked example collapses a naive −1,000bps equity call from five credit-family signals to −350bps. Influence is budgeted in percentage points per horizon bucket, separately for the ₹100cr and ₹1,000cr books, and validated against a 3σ aggregation test and an explicit turnover derivation. Fourteen cycles are MVP; nine are cut outright, four of them because their indicators do not exist for free.

---

## 1. The reframe: persistence, not periodicity

The owner's mental model is a stack of clocks of different lengths. The record does not support that model for most of the stack, and pretending otherwise is where cycle-based investing usually dies.

Three claims must be kept apart, because they have wildly different evidence:

| Claim | Example | Estimable in India? |
|---|---|---|
| (a) A **force** exists and moves asset prices | Bank credit expansion inflates collateral values, which inflates credit | Yes — mechanism-level, cross-country |
| (b) The force has a **characteristic persistence** | Credit conditions have a multi-year autocorrelation half-life | Yes — a half-life needs many overlapping windows, not many cycles |
| (c) The force is **periodic and can be phased** | "We are 70% through an 18-year land cycle" | Almost never. Requires ≥4 observed periods |

**Registry rule R1 (the clock test).** A cycle may declare `phase_repr: circular` only if `n_effective ≥ 4` complete observed periods exist *in a regime comparable to today's*. Otherwise it must use `state` (a level, no phase), `ordinal` (a stage posterior with elapsed time, no period), or `calendar` (phase known exactly from the calendar). This is enforced by the registry validator in CI, not by convention.

Under R1, of the 32 candidates only **five** survive as circular clocks, and three of those are calendar-anchored. Everything else is a state variable. This changes what the ladder *is*: it is ordered not by claimed period but by **`tau_half`, the half-life of the signal's own autocorrelation, in months.** `tau_half` is estimable from overlapping windows even with zero complete cycles, and it is what actually determines the three things the portfolio cares about — how hard to smooth, how fast the position may move, and how much turnover the signal will generate.

**Registry rule R2 (phase certainty ≠ effect certainty).** The Indian general election arrives every five years; its phase is known to the day. Whether equities do anything reliable around it is supported by seven observations. These are separate fields (`phase_confidence`, `mapping_confidence`) and the weaker one governs the influence budget.

---

## 2. The horizon ladder

Six buckets. `tau_half` boundaries are the definition; claimed periods are descriptive only.

| Bucket | Name | `tau_half` range | Claimed periods | Role in the portfolio | Rebalance clock |
|---|---|---|---|---|---|
| **B0** | Secular / long wave | ≥ 96 m | 50–250 y | Strategic centre of gravity; floors, ceilings, insurance policy | Annual review, quarterly step |
| **B1** | Generational / structural | 48–96 m | 15–50 y | Slow drift of the centre; commodity and valuation anchors | Quarterly |
| **B2** | Credit and capex long cycle | 24–60 m | 7–16 y | Gross-risk envelope; sector capex tilts; leverage ceiling | Quarterly / monthly |
| **B3** | Business, earnings, policy | 9–30 m | 2.5–7 y | The workhorse. Equity/debt/gold split, sector rotation, cash calls | Monthly |
| **B4** | Intermediate tactical | 3–12 m | 3–18 m | Bounded deviation; name selection; flow and vol overlay | Weekly (aggr.) / monthly (mod.) |
| **B5** | Fast | ≤ 3 m | 1 w – 3 m | Aggressive book only; name-level reversal and event drift | Weekly |

Buckets overlap in `tau_half` deliberately (B2/B3 at 24–30m) because assignment is by *mechanism family* first and `tau_half` second; the overlap is resolved by the parent–child DAG in §6.

---

## 3. The cycle register

Columns: **n(TS)** = independent time-series observations available in a comparable regime; **n(XS)** = independent cross-sectional analogues (other countries/episodes); **E** = evidence tier (§4); **D** = data feasibility tier (§5); **Repr** = phase representation; **Own** = owning layer.

### B0 — Secular (≥96m half-life)

| id | Claimed period (CV) | Generating mechanism | n(TS) | n(XS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|---|
| `monetary_order_debasement` | 60–90y (—) | Sovereign debt build-up → negative real rates / monetisation → liquidation or reset | 2–3 global, **0 India** | ~8 repression episodes | C | D1 | ordinal | L02 | consume |
| `reserve_currency_succession` | 80–120y (—) | Network externalities in invoicing, settlement and reserves; slow, contestable | **2** | 2 | C | D1 | ordinal | L02 | defer |
| `india_development_arc` | monotone, not cyclic | Per-capita income S-curve → consumption mix and financial deepening | 1 | ~15 (KR, TW, JP, CN, TH, MY, BR…) | B | D2 | state | L02 | MVP (static prior) |
| `demographic_transition` | 60–80y half-arc | Cohort mechanics; dependency ratio; savings rate | 1 | ~20 | B | D1 | state | L02 | defer |

*Note on `demographic_transition`:* it is the one B0 variable whose **state** is near-deterministic 15 years ahead — the 2036–41 working-age peak is made of people already born. Its uncertainty is entirely in the *mapping* to returns, not the *phase*. Rule R2 in action.

### B1 — Generational (48–96m)

| id | Claimed period (CV) | Mechanism | n(TS) | n(XS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|---|
| `commodity_supercycle` | 15–35y (CV≈0.40) | Long extraction capex lead times vs demand shocks from industrialising blocs | 4–5 since 1900 | — | B | D1 | circular (marginal) | L06 | defer |
| `long_capex_swing` (Kuznets) | 15–25y | Infrastructure/building stock, migration, corporate capacity | 5–6 global, **1.5 India** | 6 | C | D2 | state | L03 | defer |
| `equity_valuation_reversion` | half-life 7–10y, **not periodic** | Mean reversion of market-cap/GDP and long-window earnings yield | ~2 India swings | ~20 | B | D2/D4 | state | L05 | MVP |
| `household_financialisation` | 20–30y | Savings migrate physical → financial as income and formalisation rise | 1 | ~12 | C | D2 | state | L02 | defer |
| `real_estate_long_cycle_18y` | 18y | Land-price/credit feedback (Harrison/Hoyt narrative) | **≈1 for India** | contested | C | **D5** | — | — | **CUT** |

### B2 — Credit and capex (24–60m)

| id | Claimed period (CV) | Mechanism | n(TS) | n(XS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|---|
| `india_credit_financial_cycle` | 8–16y (Drehmann et al. ≈16y) | Credit ↔ collateral-value feedback; bank capital and risk appetite | **2** | 17 (BIS panel) | B | D1 | state | L03 | **MVP** |
| `global_liquidity_cycle` | 4–8y | Fed policy and the dollar → global risk appetite (Rey's "global financial cycle") | 5–6 | — | B | D1 | state | L04/L06 | **MVP** |
| `corporate_profit_share_cycle` | 7–12y | Margin mean reversion via capacity, wage share and competitive entry | 1.5 India | ~20 | B | D2/D4 | state | L05 | MVP (simple) |
| `npa_provisioning_cycle` | 8–16y, lagged 2–4y | **Child of `india_credit_financial_cycle`** — the accounting echo | 2 | 17 | B | D2 | state | L03 | defer (aliased) |
| `juglar_fixed_investment` | 7–11y | Machinery replacement and capacity | 15 global, 2–3 India | — | C | D2 | state | L03 | defer (aliased) |
| `em_capital_flow_cycle` | 7–12y | Risk-appetite waves, rating migration, index inclusion | 2 India | ~25 EMs | C | D1/D3 | state | L06 | defer |

### B3 — Business, earnings, policy (9–30m)

| id | Claimed period (CV) | Mechanism | n(TS) | n(XS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|---|
| `india_business_cycle` | ≈5.25y (exp. 12q, rec. 9q) | Inventory + investment + external demand | **3 recessions since 1996** | 17 | B | D1/D2 | **state** (fails R1) | L04 | **MVP** |
| `kitchin_inventory` | 3–5y (CV≈0.25) | Inventory over/undershoot against demand | 6–8 | many | B | D1/D3 | **circular** | L04 | **MVP** |
| `rbi_policy_rate_cycle` | 3–5y | Monetary reaction function to inflation and output gap | 5–6 since 2000 | many | B | D1 | circular (marginal) | L04 | **MVP** |
| `inflation_cycle` | 3–5y | Food (monsoon), fuel (crude/INR), core (output gap) | ~7 | many | B | D1 | state | L04 | **MVP** |
| `smallcap_breadth_cycle` | 3–5y | Retail flow, float and issuance dynamics; liquidity premium swings | **4** | ~10 | B | D1 | circular (marginal) | L07/L09 | **MVP** |
| `sector_rotation_cycle` | 3–6y | Sector-level capex, margin and credit cycles running out of phase | ~4 | many | B | D2/D4 | state | L09 | **MVP** |
| `election_policy_cycle` | 5y exact (GE) + state density | Pre-election fiscal impulse; post-election reform window | 7 GE since 1996 | ~40 EM elections | B (phase exact, effect weak) | D1 | **calendar** | L04 | defer |
| `earnings_revision_cycle` | 2–4y | Analyst anchoring and revision drift | — | — | — | **D5** | — | — | **CUT → proxy** |

### B4 — Intermediate tactical (3–12m)

| id | Claimed period | Mechanism | n(TS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|
| `intermediate_momentum_12_1` | none; `tau_half` ≈ 6m | Underreaction plus flow-driven continuation (Jegadeesh–Titman) | ~30 independent factor episodes; thousands of stock-months | **A** | D1/D4 | state | L08 | **MVP** |
| `flows_positioning_cycle` | 6–18m | FPI/DII/retail flow waves and positioning extremes | 10–12 | B | D1/D3 | state | L07 | **MVP** |
| `volatility_regime_cycle` | 1–9m clustering | Volatility clustering; leverage and margin feedback | ~15 India episodes (VIX 2008–), realised vol 1996– | **A** | D1 | state | L18 | **MVP** |
| `annual_seasonality` | 12m exact | Union Budget (Feb 1), fiscal Q4 (Mar), monsoon (Jun–Sep), festive (Oct–Nov) | ~30 | B (multiple-testing risk) | D1 | **calendar** | L08 | defer |
| `crude_cycle_short` | 6–18m | Inventory, OPEC policy, refining margins | ~12 | B | D1 | state | L06 | defer |

### B5 — Fast (≤3m)

| id | Claimed period | Mechanism | n(TS) | E | D | Repr | Own | MVP |
|---|---|---|---|---|---|---|---|---|
| `short_reversal_1m` | ≈1m | Compensation for liquidity provision; overreaction (Jegadeesh 1990) | very large | **A** | D1/D4 | state | L08 | **MVP (aggressive only)** |
| `pead_1_3m` | 1–3m post-results | Underreaction to earnings surprise | large; India evidence moderate | A/B | D2/D4 | state | L11 | defer |
| `funding_stress_spike` | days–weeks, **not periodic** | Margin spirals, dealer balance-sheet withdrawal | ~6 India episodes | B | D1 | state (trigger) | L18 | **MVP (as trigger)** |
| `expiry_microstructure` | 1m | F&O expiry positioning and roll | ~300 | B | D1 | calendar | L15 | **CUT** (execution-only, no allocation authority) |

**Register totals:** 32 candidates → **14 MVP**, 13 deferred, 5 cut.

---

## 4. Honesty tiering (A / B / C)

Tier is assigned on **independent observations of the effect**, not on rows of data.

| Tier | Admission test | Parameter policy | Backtest test | Influence multiplier | Authority |
|---|---|---|---|---|---|
| **A** | ≥30 independent effect observations, out-of-sample testable, cross-sectionally replicated | May be **fitted**, with purged/embargoed CV | Sharpe and IR are meaningful | **×1.00** | Two-sided |
| **B** | 4–30 independent observations, **or** n<4 with strong cross-country replication (n(XS) ≥ 10) | Set from published literature or economic reasoning, then **frozen in git at inception** | "Did it move in the right direction in each analog episode?" — not Sharpe | **×0.60** | Two-sided |
| **C** | <4 observations and no cross-sectional replication | Frozen; two-signature change control | Constraint tests and analog replays only | **×0.30** | **One-sided (see below)** |

**Rule R3 (tier-C one-sided authority).** Tier-C cycles may only take actions that *reduce* risk: raise gold (within its sub-cap), raise cash, buy hedges, lower the gross-leverage ceiling, tighten a concentration cap. They may **not** raise equity weight, raise gross leverage, or loosen any concentration limit. Rationale: a wrong narrative that de-risks costs carry; a wrong narrative that adds risk costs the mandate. Gold and cash are exempt from "risk-adding" for this purpose.

**Rule R4 (aggregate tier-C cap).** The combined L1 allocation influence of all tier-C cycles is capped at **150 bps** of NAV for both books, before any other cap applies. Ten narrative cycles screaming in unison move the book by less than a single tier-A signal at half strength.

**Rule R5 (ratchet).** Tier may be **downgraded** by any reviewer at any time. An **upgrade** requires a written case, a fresh out-of-sample window not used in the original assessment, and two signatures. Reviewed annually; the review is logged.

---

## 5. Data feasibility tiering (D1–D5)

Under free-sources-only, feasibility is a first-class design constraint, not an implementation detail.

| Tier | Definition | Backtest label | Examples |
|---|---|---|---|
| **D1** | Free, long history, **genuinely point-in-time** (market prices, or vintaged releases) | `pit=true` | NSE/BSE bhavcopy (1994–), RBI policy rate, BIS `TOTAL_CREDIT`/`CREDIT_GAPS` (India 1951–), IMF WEO/COFER/IFS, FRED **ALFRED** vintages, World Bank Pink Sheet (1960–), UN WPP |
| **D2** | Free, adequate history, **lag-approximated PIT** — published as current/restated with no knowledge date; we impose a fixed conservative publication lag | `pit=lag_approx` | Company financials from exchange filings, GDP/IIP levels, RBI household savings, sector aggregates |
| **D3** | Free but **short** (<10y or <4 cycle observations) | `pit=true, short` | GST collections (2017–), UPI (2016–), India VIX (2008–), NSDL FPI detail, NHB Residex (2007–) |
| **D4** | **Reconstructable with our own engineering** | `pit=reconstructed` | NIFTY 750 historical membership from NSE circulars; delisted-name prices from bhavcopy archives; corporate-action adjustment; own forward-archived filings with true knowledge dates |
| **D5** | **Infeasible free** | — | Analyst estimates and revisions; long-dated option surfaces; tick order-book history; rating-bucket credit-spread history; commercial real estate |

**Rule R6 (D5 kill switch).** A cycle whose primary indicator is D5 is **cut**, or replaced by a *named* proxy. A proxy inherits an automatic **one-tier evidence downgrade** (A→B, B→C) and carries `proxy_of` in the registry.

**D5 casualties and their disposition:**

| Cut | Why | Disposition |
|---|---|---|
| `earnings_revision_cycle` | I/B/E/S-style estimate revisions do not exist free for India | **Proxy:** `realised_eps_breadth` = fraction of the investable universe whose trailing-4q EPS exceeds the value four quarters earlier, from scraped exchange results. Lag 45–60 days, D2, tier B→C. Loses the *forward* content entirely — say so. |
| `real_estate_long_cycle_18y` | NHB Residex from 2007, RBI HPI from 2010 ⇒ ≈1 observation. No free long series exists | **CUT, not proxied.** Housing credit growth already enters `india_credit_financial_cycle`; a separate 18-year clock would be pure narrative with zero incremental data. |
| `expiry_microstructure` | Feasible (D1) but has no business setting allocation | **Moved to execution (L15).** Registry keeps a `status: cut, reason: wrong_layer` stub so it is not re-proposed. |
| `pead_1_3m` | Needs a clean PIT surprise definition; without estimates, surprise must be defined against a time-series model | Deferred to v2 with a Foster–Olsen–Shevlin-style seasonal random walk surprise. |
| `em_capital_flow_cycle` (rating/spread leg) | Rating-bucket spread history not free | Proxy with CCIL G-sec yields + NSDL FPI debt flows; tier C. |

**Non-negotiable engineering consequence:** three D4 items — survivorship-free bhavcopy history, NIFTY 750 membership reconstruction, and forward-archiving of filings with our own knowledge dates — are prerequisites for *any* backtest above B2. They belong to L17 and must start on day 1. This layer's build plan assumes them.

---

## 6. Aliasing and double-counting

Ten measurements of one force must not become a ten-times bet. Three mechanisms, applied in order.

### 6.1 A declared parent–child DAG

With two observed Indian credit cycles you cannot *learn* the dependency structure; you must *declare* it. Each registry entry carries `parent_id`. Declared families:

```
india_credit_financial_cycle  (B2, parent)
   ├── npa_provisioning_cycle            (lag 2–4y)
   ├── bank_nim_cycle                    (lag 0–2y)
   ├── juglar_fixed_investment
   └── real_estate_activity              (housing credit leg only)
india_business_cycle  (B3, parent)
   ├── kitchin_inventory
   ├── inflation_cycle
   ├── rbi_policy_rate_cycle             (reaction function ⇒ child, not sibling)
   └── corporate_profit_share_cycle      (cross-parent: also child of B2)
global_liquidity_cycle  (B2, parent)
   ├── flows_positioning_cycle
   ├── crude_cycle_short
   └── em_capital_flow_cycle
```

A node may have two parents (`corporate_profit_share_cycle`); residualization then runs against both, in horizon order.

### 6.2 Slowest-first residualization with observation-count shrinkage

Order all cycles by `tau_half` descending. For cycle *i* with ancestor set A(i):

```
z_i_orth = z_i_raw − Σ_{j ∈ A(i)}  β_ij · z_j_orth

β_ij      = λ_ij · β̂_ij + (1 − λ_ij) · β_prior_ij
λ_ij      = n_eff_ij / (n_eff_ij + 60)
n_eff_ij  = overlap_months / (0.5 × period_months of the SLOWER of i, j)
retained_variance_i = Var(z_i_orth) / Var(z_i_raw)
```

Two points that are easy to get wrong and matter enormously:

1. **The shrinkage denominator counts independent cycle observations, not months.** A 15-year parent measured over a 30-year window gives `n_eff = 30/7.5 = 4`, hence `λ = 4/64 = 0.0625` — the OLS estimate is 94% shrunk toward the declared prior. That is correct. Regressing on 360 monthly points and believing the standard error is the single most common way to fake precision at long horizons.
2. **Do not renormalise the residual to unit variance.** Rescaling re-inflates a signal that has nothing left. Instead the *cap* is scaled: a child that retains 11% of its variance gets `sqrt(0.11) = 33%` of its nominal budget. The signal keeps its natural, honestly-shrunken size.

The parent keeps the shared variance by construction. This is intentional: the slower, more structural cycle has the causal story and moves the strategic centre; the faster child only gets what is left over to move the tactical overlay.

### 6.3 Worked arithmetic — the credit family

Suppose the credit complex is uniformly late-cycle. Raw standardised signals, each nominally allowed ±250bps of equity weight, gain `k = −1.50 pp of equity per unit z`:

| Signal | `z_raw` | β to parent (shrunk) | `z_orth` | retained var | budget × √rv | contribution |
|---|---|---|---|---|---|---|
| `india_credit_financial_cycle` (parent) | +1.60 | — | +1.60 | 1.00 | ±250 bps | **−240 bps** |
| `npa_provisioning_cycle` | +1.40 | 0.85 | +0.04 | 0.11 | ±83 bps | −6 bps |
| `bank_nim_cycle` | +1.20 | 0.70 | +0.08 | 0.20 | ±112 bps | −12 bps |
| `juglar_fixed_investment` | +1.30 | 0.55 | +0.42 | 0.42 | ±162 bps | −63 bps |
| `real_estate_activity` | +1.50 | 0.65 | +0.46 | 0.35 | ±148 bps | −69 bps |

- **Naive stacking:** 5 × (−1.50 × z/2 × 100) ≈ **−1,000 bps** of equity from what is one force observed twice.
- **After residualization:** −240 − 6 − 12 − 63 − 69 = **−390 bps**.
- **After the cluster cap (§6.4):** cluster L1 cap = 1.4 × 250 = 350 bps; 390 > 350, so scale by 350/390 = 0.897 ⇒ **−350 bps final**.

A 6.5 kg to 3.5 kg reduction, and the residual weights are now telling you something real: after the credit cycle is accounted for, capex and real-estate activity are running *hotter* than credit alone implies, while NPAs and margins are exactly where credit says they should be.

### 6.4 Correlation-cluster audit (the safety net)

Structural declaration cannot catch cross-family correlation (commodity supercycle and credit cycle both load on global liquidity). Monthly, on the **final orthogonalised** signal vector:

```
1. ρ = 60-month rolling correlation matrix of the final signals
2. d_ij = sqrt(2(1 − ρ_ij));  average-linkage hierarchical clustering
3. cut at ρ = 0.50  (d = 1.00)
4. for each cluster C:  L1_C = Σ_{i∈C} |contribution_i| per asset class
   cap_C = 1.40 × max_{i∈C} (budget_i)
   if L1_C > cap_C:  scale every member by cap_C / L1_C
5. log every scaling event with cluster membership — this is the primary
   early-warning that the taxonomy has grown a redundant limb
```

The 1.40 multiplier is the concession that a cluster of genuinely-related-but-not-identical signals carries slightly more information than its largest member. It is set, not fitted; there is no way to fit it honestly.

**CI assertion.** The test suite constructs a synthetic panel where five signals are exact copies of one factor plus 10% noise and asserts total allocation impact ≤ 1.4 × single-signal budget. This test must never be relaxed.

---

## 7. Phase estimation with tolerance

### 7.1 Four representations

| `phase_repr` | Used when | Carried as | Consumed as |
|---|---|---|---|
| `circular` | R1 satisfied (n_eff ≥ 4 periods) | von Mises `VM(μ, κ)` over θ ∈ [0, 2π) | Attenuated projection (§7.2) |
| `calendar` | Phase is exogenous and exact | θ from the calendar, `σ_c = 0` | `κ → ∞`, `R = 1`; all uncertainty sits in the mapping |
| `ordinal` | Long arcs with no estimable period | Stage posterior `P(S₁..Sₖ)` + elapsed `τ` | Expectation over stages |
| `state` | Not periodic; a persistent level | `z`, `tau_half`, and a two-sided band | Direct, with hysteresis |

### 7.2 Circular phase and the attenuation identity

Carry phase as `VM(μ, κ)`. Define the circular standard deviation `σ_c` (radians). Almost every cycle's effect on an asset is modelled as `g(θ) = cos(θ − φ)`, where `φ` is the phase at which that asset historically peaks. The expectation under the posterior has a closed form:

```
E_θ~VM(μ,κ) [ cos(θ − φ) ]  =  R · cos(μ − φ)        with   R = I₁(κ)/I₀(κ)
and, by definition of circular SD,   R = exp(−σ_c² / 2)
```

**This is the elegant part: phase uncertainty attenuates the signal multiplicatively, in closed form, with no extra machinery.** A cycle you cannot date simply cannot move the book, and nobody had to remember to penalise it.

Set the tolerance from evidence, not taste:

```
σ_c = clip( 0.25 + 0.60/sqrt(n_eff) + 0.40·(1 − R²_fit) , 0.25 , 2.20 )   radians
phase_tolerance_years = (period_years / 2π) · σ_c
attenuation R = exp(−σ_c² / 2)
```

| Cycle | n_eff | R²_fit | σ_c (rad) | **R** | Tolerance |
|---|---|---|---|---|---|
| `annual_seasonality` (calendar) | 30 | — | 0.00 | **1.000** | 0 |
| `intermediate_momentum` (state, shown for scale) | 30 | 0.35 | 0.62 | **0.825** | — |
| `kitchin_inventory` (3.8y) | 7 | 0.30 | 0.76 | **0.751** | ±0.46 y |
| `smallcap_breadth_cycle` (4.2y) | 4 | 0.25 | 0.85 | **0.696** | ±0.57 y |
| `commodity_supercycle` (24y) | 4.5 | 0.15 | 0.87 | **0.683** | ±3.3 y |
| `india_business_cycle` (5.25y) | **3.0** | 0.30 | 0.87 | — | **fails R1 ⇒ `state`, no clock** |

The last row is the most useful output of this section. **India's business cycle cannot be used as a clock.** Three dated recessions since 1996 (1999Q4–2003Q1, 2007Q2–2009Q3, 2011Q2–2012Q4 per Pandey–Patnaik–Shah, plus the 2020 COVID contraction which is a shock, not a cycle) is not a basis for phasing. It is used as a *nowcast* of expansion/contraction with a `tau_half` of 18 months — which is genuinely useful and honestly scoped.

### 7.3 Ordinal phase (B0/B1) and the trigger slide

For arcs with no estimable period, carry `P(stage)` plus elapsed time `τ` in the modal stage, exactly as L02 does with its P1–P5 clock. Triggers act on `τ`, and must also act on *confidence*, because a regime break destroys information:

```
On a pre-registered event firing:
   μ  ← μ + Δθ,       Δθ = 2π · Δτ_years / period      (circular)
   τ  ← τ + Δτ_years                                    (ordinal)
   σ_c ← sqrt( σ_c² + w_e² )                            w_e ∈ [0.20, 0.60] rad
   then σ_c decays back:  σ_c(t) = σ_base + (σ_post − σ_base)·exp(−t / h),  h = period/8

Bounds (hard, CI-asserted):
   B1  cumulative |Σ Δτ| over any rolling 2 periods ≤ 0.25 × period
   B2  each event class fires at most once per 0.40 × period
   B3  applied with a 1-month lag, then amortised linearly over min(6 m, period/20)
   B4  each logged slide decays 20%/yr after 5 years
```

**Worked example — an 18-year cycle takes a +3.0y slide.** `Δθ = 2π·3/18 = 1.047 rad` (60° of arc). Cumulative bound = 0.25 × 18 = 4.5y over 36 years, so this consumes two-thirds of the allowance. Event refractory = 7.2 years. Amortised over `min(6, 10.8) = 6` months, so 0.175 rad/month. Confidence: `σ_c` goes from 0.87 to `sqrt(0.87² + 0.45²) = 0.98`, dropping attenuation from 0.686 to **0.618** — the slide moves the estimate *and* costs the cycle 10% of its influence for the next ~27 months, which is exactly right. A trigger is evidence that you were wrong before, not proof that you are right now.

**Governance.** The trigger table is a versioned YAML file. A backtest at simulated date *t* may only read the version tagged at or before *t*. Adding an event after observing an outcome is the single most seductive form of hindsight available in this design, and version pinning is the only defence.

### 7.4 State representation

For `phase_repr: state`, carry `z`, `tau_half`, and a **two-sided hysteresis band**: enter a directional state at `|z| ≥ 0.75`, exit only below `|z| ≤ 0.45`, minimum dwell `max(2, tau_half/6)` months. Smoothing window is set mechanically at `w = round(tau_half / 3)` months, median not mean.

---

## 8. Influence budgeting

### 8.1 The neutral policy portfolio

The zero-signal state, against which all budgets are deviations:

**Equity 60% · Gold 12% · Debt 28% · gross 1.00x · sector weights = benchmark.**

Every cycle contribution is a signed deviation in percentage points of NAV from this point. The debt sleeve's assumed 10% return with 4% vol is deliberately *not* allowed to set the neutral point — that is an optimizer corner-solution waiting to happen (see DECISIONS.md open item 3).

### 8.2 Bucket budgets — Aggressive (₹100 cr)

Values are ±pp of NAV of allocation authority for that bucket, **after** tier multipliers and phase attenuation.

| Bucket | `tau_half` | Equity dn/up | Gold dn/up | Debt dn/up | Sector L1 | Name-level L1 | Leverage dn/up | Turnover pp/yr |
|---|---|---|---|---|---|---|---|---|
| B0 | 120 m | 5 / 5 | 3 / 14 | 8 / 10 | 4 | 0 | −0.25 / 0.00 | 2.5 |
| B1 | 84 m | 5 / 5 | 2 / 8 | 6 / 6 | 5 | 0 | −0.10 / 0.00 | 3.0 |
| B2 | 48 m | 10 / 8 | 2 / 4 | 8 / 10 | 8 | 0 | −0.20 / +0.10 | 8.0 |
| B3 | 18 m | 12 / 12 | 2 / 6 | 10 / 10 | 12 | 6 | −0.15 / +0.15 | 15.7 |
| B4 | 6 m | 8 / 8 | 1.5 / 4 | 6 / 6 | 10 | 25 | −0.10 / +0.10 | 18.1 |
| B5 | 1.5 m | 4 / 4 | 1 / 2 | 3 / 3 | 5 | 40 | −0.05 / +0.05 | 18.1 |
| **Σ (worst case)** | | 44 / 42 | 11.5 / 38 | 41 / 45 | 44 | 71 | −0.85 / +0.40 | **65.4** |

### 8.3 Bucket budgets — Moderate (₹1,000 cr)

| Bucket | `tau_half` | Equity dn/up | Gold dn/up | Debt dn/up | Sector L1 | Name-level L1 | Leverage dn/up | Turnover pp/yr |
|---|---|---|---|---|---|---|---|---|
| B0 | 120 m | 5 / 5 | 3 / 14 | 8 / 10 | 3 | 0 | −0.25 / 0.00 | 2.5 |
| B1 | 84 m | 4 / 4 | 2 / 8 | 5 / 5 | 4 | 0 | −0.10 / 0.00 | 2.4 |
| B2 | 48 m | 8 / 7 | 2 / 4 | 7 / 8 | 6 | 0 | −0.20 / +0.05 | 6.4 |
| B3 | 18 m | 9 / 9 | 2 / 5 | 8 / 8 | 8 | 3 | −0.15 / +0.10 | 11.8 |
| B4 | 6 m | 4 / 4 | 1 / 3 | 3 / 3 | 5 | 10 | −0.10 / +0.05 | 9.1 |
| B5 | — | **0** | 0 | 0 | 0 | 0 | 0 | 0 |
| **Σ** | | 30 / 29 | 10 / 34 | 31 / 34 | 26 | 13 | −0.80 / +0.20 | **32.2** |

### 8.4 The two consistency tests the budgets must pass

**Test 1 — 3σ aggregation.** Buckets are near-independent after §6, so the worst case Σb never occurs. Require, for each asset class:

```
3 · sqrt( 0.33 · Σ_i b_i² )  ≤  headroom to the mandate cap (up) or floor (down)
```
(0.33 is Var of a signal roughly uniform on [−1, 1].)

| Check (aggressive) | Σb² | 3σ | Headroom | Pass |
|---|---|---|---|---|
| Equity **down** (b = 5,5,10,12,8,4) | 374 | **33.3 pp** | 60 → 15% floor = 45 pp | ✅ |
| Equity **up** (b = 5,5,8,12,8,4) | 338 | 31.7 pp | 60 → 110% (1.5x gross) = 50 pp | ✅ |
| Gold **up** (b = 14,8,4,6,4,2) | 332 | 31.4 pp | 12 → 50% cap = 38 pp | ✅ |
| Gold **down** (b = 3,2,2,2,1.5,1) | 24.25 | 8.5 pp | 12 → 4% L02 floor = 8 pp | ⚠️ binds at 2.8σ |
| Debt **up** (b = 10,6,10,10,6,3) | 381 | 33.6 pp | 28 → 70% cap = 42 pp | ✅ |

The gold-downside line is flagged, not fixed: L02's 4% insurance floor binds at 2.8σ. That is acceptable — the floor is a hard mandate backstop and clipping there is the intended behaviour, not a bug. It is recorded so nobody later "discovers" it and loosens the floor.

**Test 2 — turnover.** For an OU signal with half-life `h` months scaled to a ±b range:

```
annual_one_way_turnover_i  ≈  1.6 · b_i · sqrt(12 / h_i)
```

Aggressive: **65 pp/yr** of asset-allocation turnover, ~13% of a 500% budget — leaving the rest for name selection. Moderate: **32 pp/yr**, ~32% of a 100% budget, leaving ~68 pp for name selection. This is precisely why the moderate book's B4 budget is halved and B5 is zero: not squeamishness, arithmetic.

### 8.5 The rate limiter, derived not asserted

Every cycle's per-month allocation authority follows mechanically from its half-life:

```
max_delta_pp_per_month_i  =  2 · b_i / max(2 · tau_half_i , min_traverse_by_tier_i)
min_traverse_by_tier = { A: 6 m , B: 12 m , C: 36 m }
```

**B0 check against L02:** `b = 10pp` (equity+debt+gold net authority), `tau_half = 120m` ⇒ `2×10/240 = 0.083 pp/month` net directional. With an L1 allowance of 4× (offsetting moves across asset classes), that is **100 bps/quarter L1**, versus the 300 bps/quarter L02 proposes for itself. **The ladder is tighter and the ladder binds** — `effective_limit = min(L01_rate_limit, layer_self_limit)`. This is an interface conflict that must be resolved in L02's favour or L01's, not left ambiguous; L01's recommendation is L01 binds, and L02 is asked to re-derive.

### 8.6 The asymmetry that resolves the leverage-vs-drawdown tension

**Rule R7.** Cycle signals are budgeted for *adding* risk. The risk and drawdown engine (L18) is **not budgeted** and may cut gross exposure, equity weight and leverage without limit and at any cadence. Authority is deliberately asymmetric.

Quantitatively: at 3σ the aggressive cycle stack alone takes equity from 60% to ~27% and the leverage ceiling from 1.50x to 0.65x-of-ceiling. That is the honest answer to "can cash calls deliver a sub-Nifty-50 drawdown?" — **the machinery exists and is large enough, provided the signals fire in time.** For a slow bear market (2000–03, 2008, 2011–13, 2018–20 small-caps) they plausibly do. For March 2020 — a 38% index fall in five weeks with no cycle signal in the preceding quarter — **they do not, and this layer cannot pretend otherwise.** That drawdown must be met by the options overlay (L14) and the fast vol/funding triggers (L18), not by the cycle stack. The moderate book is weaker still: its 3σ equity de-risking authority is only 24.5pp (60% → 35.5%), which is a direct, unavoidable consequence of the sub-100% turnover constraint.

---

## 9. Conflict resolution

When the 100-year signal says "risk off" and the 3-month signal says "risk on":

**A1 — Additive by default.** Contributions add. No cycle holds a veto over another's direction. A B0 contribution of −5pp and a B4 contribution of +8pp nets to +3pp before A3.

**A2 — Slow cycles set the centre and the bounds, never the direction.** When the aggregate B0+B1 signal exceeds `|s| > 0.70` in the risk-off direction, the *upside* budgets of B4 and B5 are scaled by `(1 − 0.5·|s|)`, floored at 0.50. The fast cycle may still be positive — just less so. Downside budgets are never scaled down.

**A3 — Disagreement haircut.** For contributions `c_i` to the same asset from buckets **two or more rungs apart**:

```
D = 1 − |Σ c_i| / Σ |c_i|        ∈ [0, 1]
net_final = (Σ c_i) · (1 − 0.35 · D)
```
*Worked:* `c = (−5, +8)` ⇒ `Σc = +3`, `Σ|c| = 13`, `D = 0.769`, haircut `0.269` ⇒ **net = +2.19 pp**. Perfect agreement (`D = 0`) is unpenalised; heavy disagreement shrinks an already-small net. Continuous, monotone, no discontinuity to game.

**A4 — Precedence is emergent, not declared.** Every contribution has already been multiplied by its tier factor (§4), its phase attenuation `R` (§7.2) and `sqrt(retained_variance)` (§6.2). A poorly-dated tier-C 100-year cycle arrives at the arbitration with roughly `0.30 × 0.30 × 1.00 ≈ 9%` of its nominal size; a tier-A momentum state arrives with `1.00 × 0.83 × 0.80 ≈ 66%`. **The fast, well-evidenced signal wins on merit, without any rule saying so.** Deleting A4 and hard-coding a precedence order would be worse: it would hide the reason.

**A5 — Hard vetoes, exhaustively.** Only three things veto: (i) L18 de-risking; (ii) B0 leverage-ceiling modifiers; (iii) liquidity/tradability constraints from L15. Nothing else.

**A6 — No-trade band.** If `|net_final| < 1.0 pp` (aggressive) or `< 1.5 pp` (moderate) for an asset class, or `< 0.5 pp` for a single name, emit zero. Noise is not a signal.

**A7 — Every arbitration is logged**: contributions in, D, haircut, clipping, cluster scaling, final. The log is the explainability artefact Stage 2 and the owner read.

---

## 10. The canonical registry schema

Machine-readable, git-versioned, at `config/cycle_registry.yaml`, JSON-Schema validated in CI.

```yaml
# --- schema (field list the codebase reads) -------------------------------
id:                    str          # snake_case, unique, immutable
name:                  str
family:                str          # for cluster reporting
parent_id:             str | [str] | null
bucket:                B0|B1|B2|B3|B4|B5
claimed_period_years:  [lo, hi] | null
period_dispersion_cv:  float | null
tau_half_months:       float        # THE ladder key
phase_repr:            circular|calendar|ordinal|state
mechanism:             str          # one sentence, causal
n_obs: {timeseries: int, cross_sectional: int, effective: float}
evidence_tier:         A|B|C
evidence_note:         str          # citations; [verify] where unconfirmed
data_tier:             D1|D2|D3|D4|D5
proxy_of:              str | null
indicators: [ {code, definition, source_name, source_url, freq,
               history_start, pit_status, lag_days} ]
phase_state: {mu_rad|stage_posterior|z, sigma_c_rad, attenuation_R, asof}
triggers: [ {event_id, definition, delta_tau_years, sigma_inflation_rad,
             refractory_years} ]
gain: {target, k_pp_per_unit, mapping_fn: cos|linear|logistic|table, peak_phase_rad}
influence:
  agg: {equity_pp: [dn,up], gold_pp: [dn,up], debt_pp: [dn,up],
        sector_L1_pp, name_L1_pp, leverage_x: [dn,up]}
  mod: {…same…}
rate_limit:            {max_delta_pp_per_month, min_traverse_months}
hysteresis:            {enter_z, exit_z, min_dwell_months, smooth_window_months}
one_sided:             bool         # true ⇒ may only reduce risk (R3)
orthogonalization:     {beta_prior, beta_used, shrinkage_lambda, retained_variance}
owner_layer:           L02…L19
mvp:                   bool
status:                active|deferred|cut
cut_reason:            str | null
version, last_reviewed, signoff: […]
```

**Validator rules enforced in CI:** R1 (circular ⇒ n_eff ≥ 4) · R3 (tier C ⇒ `one_sided: true`) · R4 (Σ tier-C L1 ≤ 150 bps) · R6 (D5 ⇒ status cut or `proxy_of` set) · budget 3σ test · turnover test · DAG acyclicity · `mvp: true` ⇒ `data_tier ≤ D4` · every `source_url` syntactically valid and every indicator resolvable against a committed fixture.

**Note on URL reachability.** Per `ENVIRONMENT-CONSTRAINTS.md`, the build session's egress is allowlisted and cannot reach NSE, RBI, BIS, FRED, Kaggle or Hugging Face. Reachability is therefore **not** a CI assertion here; it runs as a separate `make verify-sources` target in the owner's ingestion environment. In this repo every registry indicator must instead resolve against a committed fixture, so the whole layer is exercisable with zero live data. This is a hard requirement, not a convenience: a cycle whose indicator has no fixture cannot be merged.

### Worked entries

```yaml
- id: monetary_order_debasement
  bucket: B0 ; tau_half_months: 120 ; phase_repr: ordinal
  claimed_period_years: [60, 90] ; period_dispersion_cv: null
  parent_id: null ; family: long_wave
  mechanism: "Sovereign debt accumulates until service crowds out fiscal space; resolved
              by negative real rates, monetisation, or reset."
  n_obs: {timeseries: 2, cross_sectional: 8, effective: 2.0}
  evidence_tier: C            # mechanism is B (Reinhart–Sbrancia); the CLOCK is C
  data_tier: D1
  indicators:
    - {code: GDS,  source_name: "IMF WEO GGXWDG_NGDP + CBO", source_url: "https://www.imf.org/en/Publications/WEO", freq: A, history_start: 1980, pit_status: lag_approx, lag_days: 180}
    - {code: RPR,  source_name: "BIS policy rates + FRED/OECD CPI", source_url: "https://data.bis.org/", freq: M, history_start: 1960, pit_status: true, lag_days: 30}
    - {code: CBGS, source_name: "WGC Goldhub + IMF IFS", source_url: "https://www.gold.org/goldhub", freq: Q, history_start: 1948, pit_status: true, lag_days: 60}
  phase_state: {stage_posterior: {P3: 0.35, P4: 0.55, P5: 0.10}, tau_years: 6.0, sigma_c_rad: null, asof: 2026-08-28}
  gain: {target: gold_weight, k_pp_per_unit: 5.5, mapping_fn: linear}
  influence: {agg: {equity_pp: [5,0], gold_pp: [3,14], debt_pp: [8,10], sector_L1_pp: 4, name_L1_pp: 0, leverage_x: [-0.25, 0.0]},
              mod: {equity_pp: [5,0], gold_pp: [3,14], debt_pp: [8,10], sector_L1_pp: 3, name_L1_pp: 0, leverage_x: [-0.25, 0.0]}}
  one_sided: true             # R3: equity_up forced to 0
  rate_limit: {max_delta_pp_per_month: 0.083, min_traverse_months: 36}
  owner_layer: L02 ; mvp: true ; status: active

- id: india_credit_financial_cycle
  bucket: B2 ; tau_half_months: 48 ; phase_repr: state
  claimed_period_years: [8, 16] ; period_dispersion_cv: 0.35
  parent_id: null ; family: credit
  mechanism: "Bank credit growth raises collateral values, which relaxes constraints and
              raises credit further; unwinds through capital impairment."
  n_obs: {timeseries: 2, cross_sectional: 17, effective: 2.4}
  evidence_tier: B            # n(XS)=17 via the BIS panel rescues it from C
  evidence_note: "Drehmann, Borio & Tsatsaronis (2012): financial cycle ~16y vs business
                  cycle 1–8y. BIS credit-gap ~10pp distress threshold."
  data_tier: D1
  indicators:
    - {code: CGAP, definition: "credit-to-GDP gap, one-sided HP λ=400000", source_name: "BIS CREDIT_GAPS India", source_url: "https://data.bis.org/topics/CREDIT_GAPS", freq: Q, history_start: 1951, pit_status: true, lag_days: 150}
    - {code: DBCG, definition: "SCB non-food credit YoY − nominal GDP YoY", source_name: "RBI DBIE + MOSPI", source_url: "https://dbie.rbi.org.in", freq: M, history_start: 1972, pit_status: lag_approx, lag_days: 45}
    - {code: GNPA, definition: "system GNPA ratio, 4q change", source_name: "RBI Financial Stability Report", source_url: "https://rbi.org.in", freq: SA, history_start: 1997, pit_status: true, lag_days: 90}
  phase_state: {z: null, sigma_c_rad: null, asof: null}
  hysteresis: {enter_z: 0.75, exit_z: 0.45, min_dwell_months: 8, smooth_window_months: 16}
  gain: {target: equity_weight, k_pp_per_unit: -1.50, mapping_fn: linear}
  influence: {agg: {equity_pp: [10,8], gold_pp: [2,4], debt_pp: [8,10], sector_L1_pp: 8, name_L1_pp: 0, leverage_x: [-0.20,0.10]},
              mod: {equity_pp: [8,7],  gold_pp: [2,4], debt_pp: [7,8],  sector_L1_pp: 6, name_L1_pp: 0, leverage_x: [-0.20,0.05]}}
  one_sided: false
  rate_limit: {max_delta_pp_per_month: 0.104, min_traverse_months: 96}
  owner_layer: L03 ; mvp: true ; status: active

- id: india_business_cycle
  bucket: B3 ; tau_half_months: 18 ; phase_repr: state     # FAILS R1 — not a clock
  claimed_period_years: [4.5, 6.0] ; period_dispersion_cv: 0.30
  parent_id: null ; family: business
  mechanism: "Inventory, fixed investment and external demand co-move; amplified post-1991
              by financial globalisation and private investment decisions."
  n_obs: {timeseries: 3, cross_sectional: 17, effective: 3.0}
  evidence_tier: B
  evidence_note: "Pandey, Patnaik & Shah (2017), Indian Growth and Development Review 10(1).
                  Three recessions 1999Q4–2003Q1, 2007Q2–2009Q3, 2011Q2–2012Q4; mean
                  expansion 12q, recession 9q. n_eff=3 ⇒ R1 fails ⇒ nowcast, not clock."
  data_tier: D1
  indicators:
    - {code: IIP,  definition: "IIP SA, CF-filtered cyclical component", source_name: MOSPI, source_url: "https://mospi.gov.in", freq: M, history_start: 1994, pit_status: lag_approx, lag_days: 42}
    - {code: GVA,  definition: "real GVA YoY, seasonally adjusted", source_name: "MOSPI NAD", source_url: "https://mospi.gov.in", freq: Q, history_start: 1996, pit_status: lag_approx, lag_days: 60}
    - {code: GST,  definition: "gross GST collections, 3m/12m ratio", source_name: "GST Council", source_url: "https://gstcouncil.gov.in", freq: M, history_start: 2017, pit_status: true, lag_days: 3}
    - {code: EWB,  definition: "e-way bill volume YoY", source_name: NIC/GSTN, source_url: "https://ewaybillgst.gov.in", freq: M, history_start: 2018, pit_status: true, lag_days: 10}
  hysteresis: {enter_z: 0.75, exit_z: 0.45, min_dwell_months: 4, smooth_window_months: 6}
  gain: {target: equity_weight, k_pp_per_unit: 2.20, mapping_fn: linear}
  influence: {agg: {equity_pp: [12,12], gold_pp: [2,6], debt_pp: [10,10], sector_L1_pp: 12, name_L1_pp: 6, leverage_x: [-0.15,0.15]},
              mod: {equity_pp: [9,9],   gold_pp: [2,5], debt_pp: [8,8],   sector_L1_pp: 8,  name_L1_pp: 3, leverage_x: [-0.15,0.10]}}
  one_sided: false
  rate_limit: {max_delta_pp_per_month: 0.667, min_traverse_months: 36}
  owner_layer: L04 ; mvp: true ; status: active

- id: kitchin_inventory
  bucket: B3 ; tau_half_months: 11 ; phase_repr: circular   # PASSES R1 (n_eff = 7)
  claimed_period_years: [3.0, 5.0] ; period_dispersion_cv: 0.25
  parent_id: india_business_cycle ; family: business
  mechanism: "Production over- and under-shoots demand because inventory decisions are made
              on lagged information; the correction is the cycle."
  n_obs: {timeseries: 7, cross_sectional: 20, effective: 7.0}
  evidence_tier: B
  data_tier: D1
  indicators:
    - {code: IIPQ, definition: "IIP manufacturing vs 24m trend, CF-filtered", source_name: MOSPI, source_url: "https://mospi.gov.in", freq: M, history_start: 1994, pit_status: lag_approx, lag_days: 42}
    - {code: PMII, definition: "S&P Global India Mfg PMI, stocks-of-purchases sub-index", source_name: "S&P Global (headline free)", source_url: "https://www.pmi.spglobal.com", freq: M, history_start: 2005, pit_status: true, lag_days: 1}
    - {code: INVS, definition: "aggregate inventory/sales, listed non-fin universe", source_name: "NSE/BSE filings (own archive)", source_url: "https://nseindia.com", freq: Q, history_start: 2001, pit_status: reconstructed, lag_days: 55}
  phase_state: {mu_rad: null, sigma_c_rad: 0.76, attenuation_R: 0.751, asof: null}
  gain: {target: cyclical_sector_tilt, k_pp_per_unit: 4.0, mapping_fn: cos, peak_phase_rad: 1.05}
  influence: {agg: {equity_pp: [4,4], gold_pp: [0,0], debt_pp: [3,3], sector_L1_pp: 6, name_L1_pp: 3, leverage_x: [0,0]},
              mod: {equity_pp: [3,3], gold_pp: [0,0], debt_pp: [2,2], sector_L1_pp: 4, name_L1_pp: 1.5, leverage_x: [0,0]}}
  orthogonalization: {beta_prior: 0.55, retained_variance: 0.45}
  rate_limit: {max_delta_pp_per_month: 0.364, min_traverse_months: 22}
  owner_layer: L04 ; mvp: true ; status: active

- id: intermediate_momentum_12_1
  bucket: B4 ; tau_half_months: 6 ; phase_repr: state
  claimed_period_years: null ; parent_id: null ; family: price_persistence
  mechanism: "Slow diffusion of information plus flow-driven continuation; decays and
              crashes after sharp market reversals."
  n_obs: {timeseries: 30, cross_sectional: 40, effective: 30.0}
  evidence_tier: A
  evidence_note: "Jegadeesh & Titman (1993). India: Agarwalla, Jacob & Varma (2013) publish
                  a free four-factor WML series — NOTE their construction uses CMIE Prowess,
                  so it is usable as a BENCHMARK for our own factor, never as an input."
  data_tier: D1/D4
  indicators:
    - {code: R12_1, definition: "cum. return t−12m to t−1m, skip 1m, corporate-action adjusted", source_name: "NSE/BSE bhavcopy archive (own build)", source_url: "https://www.nseindia.com/all-reports", freq: D, history_start: 1994, pit_status: reconstructed, lag_days: 0}
    - {code: WMLX,  definition: "IIM-A WML factor, validation reference only", source_name: "IIMA IFFM", source_url: "https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/", freq: D, history_start: 1993, pit_status: true, lag_days: 30}
  hysteresis: {enter_z: 0.50, exit_z: 0.25, min_dwell_months: 1, smooth_window_months: 2}
  influence: {agg: {equity_pp: [8,8], gold_pp: [1.5,4], debt_pp: [6,6], sector_L1_pp: 10, name_L1_pp: 25, leverage_x: [-0.10,0.10]},
              mod: {equity_pp: [4,4], gold_pp: [1,3],   debt_pp: [3,3], sector_L1_pp: 5,  name_L1_pp: 10, leverage_x: [-0.10,0.05]}}
  rate_limit: {max_delta_pp_per_month: 1.333, min_traverse_months: 12}
  owner_layer: L08 ; mvp: true ; status: active
```

---

## 11. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L02–L14 (every signal layer) | `CycleSignal{cycle_id, z or phase, asof, vintage, confidence}` | Must validate against the registry entry the layer owns; a signal for an unregistered `cycle_id` is rejected, not warned |
| L17 data pipeline | `pit_store(series, asof)`, `universe(asof)`, `membership(asof)` | Point-in-time only; final-vintage reads raise |
| L16 backtest/validation | `n_eff_estimate(cycle_id)`, `fit_r2(cycle_id)`, `retained_variance(cycle_id)` | Feeds §4 tiering and §7.2 attenuation; recomputed annually, never mid-backtest |
| L15 Stage-2 AI+human overlay | `trigger_nomination`, `phase_override_proposal`, `tier_downgrade` | Overlay may **downgrade** a tier or fire a **pre-registered** trigger. It may **not** create a cycle, upgrade a tier, or raise a budget |
| L19 governance | `registry_version`, `signoff_log` | Backtest at date *t* reads the registry version tagged ≤ *t* |

**Exposes**

```python
CYCLE_REGISTRY   # config/cycle_registry.yaml — the canonical file
HORIZON_LADDER   # bucket definitions, tau_half boundaries, budgets per book
SIGN_CONVENTION  # +1 ALWAYS means "phase historically favourable to risk assets"

orthogonalize(panel, asof)   -> {z_orth, beta_used, retained_variance, cluster_map}
phase_posterior(cycle_id, asof) -> {repr, params, attenuation_R, tolerance_years}
influence_budget(cycle_id, book) -> {caps, rate_limit, one_sided}
resolve(contributions, asof) -> {net_by_asset, D, haircut, clip_log, cluster_scaling}
CYCLE_STATE(asof) -> full snapshot for Stage 2 review and Stage 3 optimizer
```

Stage 3 (optimizer) consumes only `resolve()` output plus `CYCLE_STATE`; it must never read a raw layer signal. Stage 2 reads `CYCLE_STATE` and writes only into the four nomination channels above. **Switching Stage 2 off must leave `resolve()` output unchanged** — this is asserted by a CI test, and it is what makes quant-only vs quant-plus-overlay measurable.

---

## 12. MVP vs deferred, and the build plan

**MVP registry (14 cycles):** `india_development_arc` (static prior) · `monetary_order_debasement` (consumed) · `equity_valuation_reversion` · `india_credit_financial_cycle` · `global_liquidity_cycle` · `corporate_profit_share_cycle` (simple) · `india_business_cycle` · `kitchin_inventory` · `rbi_policy_rate_cycle` · `inflation_cycle` · `smallcap_breadth_cycle` · `sector_rotation_cycle` · `intermediate_momentum_12_1` · `volatility_regime_cycle` · `flows_positioning_cycle` · `short_reversal_1m` (aggressive only) · `funding_stress_spike` (trigger only).

**Deferred to v2:** all B0 entries beyond the two above; `commodity_supercycle`; `long_capex_swing`; `household_financialisation`; `npa_provisioning_cycle`; `juglar_fixed_investment`; `em_capital_flow_cycle`; `election_policy_cycle`; `annual_seasonality`; `crude_cycle_short`; `pead_1_3m`; `demographic_transition`.

**Cut:** `real_estate_long_cycle_18y` · `earnings_revision_cycle` (proxied) · `expiry_microstructure` (wrong layer) · plus the rating-spread leg of `em_capital_flow_cycle`.

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Registry schema + JSON-Schema validator | `cycle_registry.schema.json`, CI rules R1/R3/R4/R6, DAG acyclicity, URL reachability | 3 | ✅ |
| 2 | Populate 14 MVP entries | `config/cycle_registry.yaml` with sources, bands, budgets, both books | 4 | ✅ |
| 2b | Indicator fixtures | One committed sample file per registry indicator, so every rule above runs offline | 2 | ✅ |
| 3 | `tau_half` estimator | Overlapping-window AR(1)/OU half-life with block bootstrap CI | 2 | ✅ |
| 4 | Orthogonalizer | Slowest-first residualization, `n_eff` shrinkage, retained-variance caps | 3 | ✅ |
| 5 | Cluster audit | Rolling correlation, average-linkage clustering, 1.4× cap, scaling log | 2 | ✅ |
| 6 | Phase engine | von Mises state, `R = exp(−σ_c²/2)`, ordinal posterior, calendar phase, state+hysteresis | 4 | ✅ |
| 7 | Trigger-slide machinery | Versioned event YAML, bounds B1–B4, σ inflation and decay, two-signature hook | 3 | ✅ |
| 8 | Budget allocator + rate limiter | Per-book caps, 3σ test, turnover test, `max_delta_pp_per_month` | 3 | ✅ |
| 9 | Conflict resolver | A1–A7 including disagreement haircut and arbitration log | 2 | ✅ |
| 10 | Constraint test suite | Synthetic panels: 5-copies test, turnover bound, flip frequency, budget sums | 3 | ✅ |
| 11 | Explainability report | One page per rebalance: every cycle, state, attenuation, contribution, clip reason | 2 | ✅ |
| 12 | Tier review procedure + freeze | Git tag, sign-off record, annual review checklist | 1 | ✅ |
| 13 | Deferred-cycle entries (13) | Registry rows with `status: deferred` and full sourcing, so v2 is a config change | 3 | ⬜ |
| **Total MVP** | | | **34 days** | |

Thirty-two engineer-days for the layer everything else conforms to, and it must land in the first six weeks or twenty layers will each invent their own conventions.

---

## 13. Risks and constraint conflicts

1. **The premise is partly wrong, and the design says so.** Most of the stack is not periodic. If the owner's conviction is specifically in *clocks* — "we are at year 14 of an 18-year cycle" — then R1 will delete most of that conviction, and that disagreement should surface now rather than after the build.
2. **n_eff for almost everything in India is under 8.** Post-1991 India offers ~35 years: 3 dated recessions, ~2 credit cycles, 1.5 capex swings, 1 housing observation, 0 long waves. No amount of monthly data changes this. Every long-horizon parameter in the model is a prior wearing an estimate's clothes.
3. **Degrees of freedom overwhelm the sample.** 32 cycles × ~10 tunable parameters ≈ 320 knobs against perhaps 8 independent macro observations. Overfitting here is not *measurable*, only *preventable* — by freezing thresholds in git at inception and requiring two signatures plus a written case to change one. That discipline is the only defence and it will be tested the first time a frozen parameter looks stupid.
4. **The cycle stack cannot stop a March-2020 drawdown.** A 38% fall in five weeks with no macro deterioration in the preceding quarter is outside what any B0–B3 signal can see. The drawdown objective therefore rests on L14 (options) and L18 (fast vol/funding triggers), and this layer's budgets should not be read as a drawdown solution. Stated plainly so it is not quietly assumed elsewhere.
5. **The moderate book's de-risking authority is structurally weaker** (24.5pp vs 33.3pp at 3σ), a direct consequence of the sub-100% turnover cap. The ₹1,000cr book will find "max drawdown below Nifty 50" materially harder, and needs a larger standing hedge to compensate.
6. **The 25%/20% sector cap conflicts with the "fully sector-active" decision more than it appears.** Financials are roughly 30–35% of the Nifty 500 by weight [verify current]. A 25% cap is therefore not a concentration limit — it is a permanent, forced 5–10pp *underweight* to the largest sector, active whether or not the sector model wants it. Either the cap is expressed relative to benchmark weight (`min(25%, benchmark + 10pp)`), or the owner should accept a standing structural short of Indian financials. This must be resolved before the sector model is built.
7. **Tier-C cycles will attract disproportionate attention.** Reserve-currency succession is far more interesting to discuss than inventory-to-sales, and it is capped at 150bps for the whole tier. Expect pressure to loosen R4; the answer is no.
8. **The 35–60% CAGR aspiration is not reachable from this layer, and probably not from the architecture.** Cycle-driven asset allocation contributes perhaps 100–300bps/yr of the total; the rest must come from selection and leverage. Concurring with L02: a realistic full-cycle range is ~18–24% (aggressive) and ~14–18% (moderate). Designing the ladder to chase 35–60% would mean removing exactly the caps that make it safe.
9. **Free-data PIT contamination is the silent killer.** Every D2 indicator (`corporate_profit_share_cycle`, `sector_rotation_cycle`, `realised_eps_breadth`) uses restated financials with an imposed lag. Backtests using them are `pit=lag_approx` and must be labelled as such in every output, not just in a footnote.
10. **The taxonomy will become a dumping ground.** Momentum is not a cycle; volatility clustering is not a cycle; funding stress is not a cycle. They are in the registry because they need budgets and rate limits, and the registry is where those live. The risk is conceptual drift into "everything is a cycle". R1, R6 and the `status: cut` stubs are the guard rails.

---

## 14. References

1. Pandey, R., Patnaik, I. & Shah, A. (2017). "Dating business cycles in India." *Indian Growth and Development Review* 10(1), 32–61. Also NIPFP WP 175 (2016). — Three recessions since 1996; mean expansion 12q, recession 9q.
2. Drehmann, M., Borio, C. & Tsatsaronis, K. (2012). "Characterising the financial cycle: don't lose sight of the medium term!" BIS Working Paper 380. — Financial cycle ≈16y vs business cycle 1–8y.
3. Borio, C. (2014). "The financial cycle and macroeconomics: What have we learnt?" *Journal of Banking & Finance* 45.
4. Jegadeesh, N. & Titman, S. (1993). "Returns to Buying Winners and Selling Losers." *Journal of Finance* 48(1). Jegadeesh, N. (1990). "Evidence of Predictable Behavior of Security Returns." *Journal of Finance* 45(3).
5. Agarwalla, S. K., Jacob, J. & Varma, J. R. (2013). "Four factor model in Indian equities market." IIMA WP 2013-09-05. Free factor library: <https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/>. **Constructed from CMIE Prowess — usable as an external validation benchmark, never as a model input.**
6. Rey, H. (2013). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." Jackson Hole / NBER WP 21162.
7. Reinhart, C. & Sbrancia, M. B. (2011). "The Liquidation of Government Debt." NBER WP 16893. — The strongest empirical plank under B0.
8. Jordà, Ò., Schularick, M. & Taylor, A. — Macrohistory Database, 17 countries, 1870–. <https://www.macrohistory.net/database/>
9. Bry, G. & Boschan, C. (1971). *Cyclical Analysis of Time Series*. NBER. Christiano, L. & Fitzgerald, T. (2003). "The Band Pass Filter." *International Economic Review* 44(2). — The dating and filtering methods used by ref. 1.
10. Mardia, K. V. & Jupp, P. E. (2000). *Directional Statistics*. Wiley. — von Mises distribution; `R = I₁(κ)/I₀(κ)` and `R = exp(−σ_c²/2)`.
11. Harvey, C. R., Liu, Y. & Zhu, H. (2016). "…and the Cross-Section of Expected Returns." *Review of Financial Studies* 29(1). — Multiple-testing discipline; why 320 knobs against 8 observations is not estimation.
12. Garvy, G. (1943). "Kondratieff's Theory of Long Cycles." *Review of Economic Statistics* [verify volume]. Solomou, S. (1987). *Phases of Economic Growth, 1850–1973*. Cambridge UP. — Why no Kondratiev clock is implemented.
13. Foster, G., Olsen, C. & Shevlin, T. (1984). "Earnings Releases, Anomalies, and the Behavior of Security Returns." *The Accounting Review* 59(4). — Seasonal-random-walk surprise, the free-data substitute for analyst estimates.
14. Free-source index: RBI DBIE <https://dbie.rbi.org.in> · MOSPI <https://mospi.gov.in> · BIS <https://data.bis.org> · IMF WEO/IFS/COFER · FRED/ALFRED <https://alfred.stlouisfed.org> (vintages) · World Bank Pink Sheet · CCIL <https://www.ccilindia.com> · NSE reports <https://www.nseindia.com/all-reports> · NSDL FPI <https://www.fpi.nsdl.co.in> · AMFI · GST Council · UN WPP.

*Items marked [verify] require confirmation against the primary source before circulation.*
