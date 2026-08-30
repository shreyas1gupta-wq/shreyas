# Layer 09 — Cross-Sectional Factor Library for the NIFTY 750

**Abstract.** This layer converts free Indian accounting and price data into one signed score per name, and on the current arithmetic it is where the return actually comes from — the cycle stack contributes only 100–300bps/yr of allocation alpha (L01 §13), so cross-sectional selection has to carry the rest. Its organising conclusion: **the fundamental half of a factor library cannot be built point-in-time from free Indian data, and a backtest of it is biased upward by an amount we can bound but not remove.** The response is two books — a genuinely point-in-time **price-only factor book (PO-FL)**, buildable in four engineer-days from bhavcopy alone and a real strategy in its own right, and a fundamental book (FUND-FL) whose performance gap against PO-FL is reported as the upper bound on data artefact, sharpened after 2028 by a forward-archive replay that isolates the artefact exactly. Scores are computed **within sector**, because Indian accounting ratios are not comparable across sectors and a raw cross-sector value score would double-count L10's `sector_rotation_cycle` budget; the sector tilt stays L10's explicit decision. Factors combine into a **single integrated composite** — except momentum, excluded and left to L08 so its crash machinery can act on that exposure alone. Timing runs in three narrow, hard-capped, killable channels. Financials get their own pool with a substituted factor set. The composite is a clipped sigma score, never a weight, which is how it survives the 5.7× difference in L14's per-book score-to-weight gain without any change here. And at ₹1,000 crore, capacity is *not* the binding constraint — breadth and turnover are — so with quality and value running roughly five times momentum's `tau_half`, **the factor book, not momentum, is the moderate book's primary name-level engine.**

---

## 1. Scope and the interface boundary

**Owns.** Definition, construction, normalisation, compositing and disciplined timing of cross-sectional *characteristic* factors over the NIFTY 750 — value, quality, low-risk, size (and size×quality), yield — plus the negative forensic factor and the price-only factor book. Delivers a Stage-1-sufficient per-name `FACTOR_SCORE` and `FACTOR_SLEEVE`.

| Belongs elsewhere | Not duplicated here |
|---|---|
| **L08 momentum** | Anything built from `t−12m→t−1m`, `t−1m`, 52-week-high, or trend/breadth. My composite carries **no momentum factor**; my long-horizon reversal uses the disjoint `t−60m→t−13m` window |
| **L10 sector model** | Sector weights. I emit sector-*neutral* scores plus a zero-budget `lowvol_sector_component` recommendation |
| **L11 bottom-up** | Reverse-DCF, incremental ROIC narrative scoring; L11 orthogonalises against my `qual_z` |
| **L05 valuation** | The aggregate CMA and `value_spread_z`, which I consume, never compute |
| **L12 special situations** | Any name with < 252 sessions or < 8 filed quarters, routed out entirely |
| **L17 risk engine** | The risk covariance. I own *return* factors; L17 owns the risk model and consumes my exposures |
| **L14 optimizer** | Target weights, the entry/drift bands, netting across sleeves |
| **L19 data pipeline** | Raw ingestion, the bitemporal store, corporate actions, membership. I consume a `pit_store` interface only |

**Registry position.** This layer owns no cycle entry. It consumes `equity_valuation_reversion` (via L05's `value_spread_z`), `smallcap_breadth_cycle` (L07), `sector_rotation_cycle` (L10) and `india_business_cycle` (L04). The strategic composite is a Block-B alpha input to L14, not a cycle contribution routed through `resolve()`; only the §7 *timing tilts* are charged against those cycles' `name_l1_pp` budgets. No new registry entry, no new budget.

**Sign convention (L01).** `+1` = characteristic historically associated with higher forward risk-adjusted return.

---

## 2. Data feasibility — the decisive filter

| # | Object | Free route | History | Coverage | PIT | Tier |
|---|---|---|---|---|---|---|
| 1 | Daily OHLC, volume, ISIN | NSE bhavcopy (legacy + udiff from 2024) | 1994– | full, incl. delisted | true (reconstructed tape) | **D1/D4** |
| 2 | Free-float market cap | Shareholding pattern (LODR Reg 31) × price | 2001– | ~full | 21-day filing deadline | **D2** |
| 3 | Quarterly P&L (standalone + consolidated) | NSE/BSE XBRL results filings | XBRL ~2017–; PDF 2001– | ~full XBRL era; parse-dependent before | restated, no knowledge date | **D2→D4** |
| 4 | Balance sheet + cash-flow statement | Half-yearly (Reg 33) + annual audited | 2001– (half-yearly BS/CFS from ~2019 **[verify]**) | full annual, weaker half-yearly | restated | **D2** |
| 5 | Bulk historical fundamentals | Kaggle/HuggingFace scrapes (~4,000–4,500 names) | 10–15y typical | broad but survivorship-contaminated | restated, degraded | **D2, degraded** |
| 6 | Promoter pledge | Reg 31 shareholding pattern | 2009– | full | 21-day deadline | **D2** |
| 7 | Auditor resignation / change, audit qualification | Reg 30 announcements; Reg 33 impact statement | 2016– | full | **true PIT** (24h) | **D1** |
| 8 | ASM/GSM surveillance, circuits | NSE/BSE daily surveillance files | ~2017– **[verify]** | full | true PIT | **D1** |
| 9 | Related-party transactions, contingent liabilities, subsidiaries | Annual report PDF notes; Reg 23 | 2001– | parse-dependent, poor | restated | **D4** |
| 10 | Intangibles decomposition (R&D, SG&A split) | Directors' Report (Cos Act 8(3)) | patchy | poor | — | **D5** |
| 11 | Sector classification | niftyindices factsheets; history D4 | current free | full | current-as-of-today | **D2/D4** |
| 12 | IIM-A Fama-French + momentum factors | `faculty.iima.ac.in/iffm/` | 1993– | index-level | true PIT | **D1 — benchmark only** |

Three non-negotiable consequences. **Row 3 is the whole game and it is D2**: quarterly XBRL gives P&L and little else, so ROIC, asset growth, accruals, leverage and cash conversion are **half-yearly, not quarterly**. **Row 10 is D5**: intangibles-adjusted book value (Peters–Taylor 2017) cannot be built free for India; we route around it (§4.1), not fake it. **Row 12 may never enter the signal path**: the IIM-A library is built on CMIE Prowess, which we do not license; it is a committed fixture for validation only (§5), CI-enforced by an import ban from `src/cyclestack/factors/`.

---

## 3. The point-in-time bias, quantified, and the price-only book

Free Indian fundamentals are as-restated, published with no knowledge date. Restatements are not symmetric noise — they systematically move bad news (an impairment, a related-party write-off) out of the record or into a later period. A backtest reading restated data declines to buy names that looked cheap and clean in real time and then blew up. The bias is **upward, and concentrated in exactly the value-and-quality composite this layer sells** — Banz & Breen (1986) is the canonical demonstration that an E/P effect significant in ex-post data was *absent* point-in-time.

| Component | Derivation | Estimate (bps/yr drag) | Removable? |
|---|---|---|---|
| Survivorship / delisting | ~1–2%/yr involuntary exits; a value/small tilt ~2× overweight them; terminal loss ~70% | **150–300** | Yes — L19's union-of-bhavcopy universe |
| Restatement look-ahead | ~3% of long-book name-years hide a disqualifying real-time figure that restatement later removed; those names lose ~50% the following year | **100–300** | No — irreducible until the forward archive matures |
| Reporting-lag error | ~30% of names file at 45–90d against an imposed 45d lag, conferring ~15d of unearned foresight on a third of the book at ~1.5% relative | **50–150** | Mostly — the conservative lag table in §6.3 |
| **Total, uncontrolled / after D4 engineering** | | **300–750 / 150–450** | |

**PO-FL — a required deliverable, not a placeholder.** A complete, tradeable book touching no accounting data whatsoever, built in week one:

| Component | Definition | Sign |
|---|---|---|
| `lowbeta` | 24m weekly beta vs Nifty 500 TRI, Dimson-corrected, Vasicek-shrunk `β* = 0.60β̂ + 0.40·1.0` | − |
| `idiovol` | Annualised residual σ, market+size regression, 250 daily obs | − |
| `maxret` | Mean of 5 largest daily returns, trailing 21 sessions (Bali–Cakici–Whitelaw) | − |
| `size` | `log(free_float_mcap)` | − (weak alone) |
| `size_x_lowrisk` | `z(−size) × z(lowbeta+idiovol)` — the price-only stand-in for §4.4 | + |
| `lt_rev` | `−`cum. return `t−60m→t−13m` (De Bondt–Thaler), disjoint from L08 | + |
| `illiq` | Amihud `mean(|r|/turnover)`, 250d, capacity-gated | + |
| `forensic_px` | ASM/GSM stage, circuit-day count | one-sided − |

Two measurements. **`pit_gap`** (immediate): `IR(FUND-FL) − IR(PO-FL)`, same window/universe/cost model, reported on the cover page of every backtest as an *upper bound* on artefact. **`restatement_delta`** (~2028): once the forward archive holds both as-first-reported and current-restated values, replaying FUND-FL on both isolates the artefact exactly — free beyond L19's ingestion to start now, unknowable if not.

---

## 4. The factor set

Scores are within-sector normal scores (§6.2). `MVP` = v1, `DEF` = v1.5/v2, `CUT` = not built.

### 4.1 Value (`W_val` 0.25 both books)

| Factor | Definition | Tier | Status |
|---|---|---|---|
| `ey` | Trailing-4q PAT (consol., pre-exceptional) / mcap | B/D2 | MVP — missing, not bottom-ranked, if PAT ≤ 0 |
| `sp` | Trailing-4q net sales / mcap | B/D2 | MVP — always defined, the loss-maker anchor |
| `ebit_ev` | Trailing-4q EBIT / (mcap + debt − cash) | B/D2 | MVP — preferred over EV/EBITDA, which flatters capital-intensive names |
| `bp` | Book value / mcap | B/D2 | MVP, **gated** — dropped in low-tangibility sectors |
| `fcfy` | (CFO − capex, trailing 4 half-years) / EV | B/D2 | MVP, half-yearly, lag 75/105d |
| `ibp` | Intangibles-adjusted book/price | B/**D5** | **CUT** — R&D/SG&A split not free; replaced by the tangibility gate |

**B/P and the tangibility gate.** B/P misprices asset-light businesses because the balance sheet omits their real capital — not a fringe case in India, where IT services, pharma, exchanges and platform names are a large, growing share of the Nifty 500. The literature's fix (Peters & Taylor 2017; Eisfeldt & Papanikolaou 2013; Arnott, Harvey, Kalesnik & Linnainmaa 2021 [verify]) needs an SG&A decomposition India does not disclose. **Our fix:** compute each sector pool's trailing-3y median `net fixed assets/total assets`; where **< 0.20**, drop `bp` for every name in the pool, re-weighting remaining legs by §6.5's coverage rule. Crude, cheap, frozen at inception, and it removes the largest known defect in a free-data India value factor.

### 4.2 Quality (`W_qual` 0.30 aggressive / 0.35 moderate)

| Factor | Definition | Tier | Status |
|---|---|---|---|
| `gpoa` | Gross profit / total assets (Novy-Marx) | A/D2 | MVP, weight ×1.5 |
| `roe` | Trailing-4q PAT / avg net worth | B/D2 | MVP |
| `roic` | NOPAT / (net worth + debt − cash), half-yearly | B/D2 | MVP |
| `accruals` | (ΔCA−ΔCash)−(ΔCL−ΔSTD)−Dep, /avg assets (Sloan); or `(PAT−CFO)/assets` | A/D2 | MVP, half-yearly |
| `asset_growth` | −YoY total-asset growth (Cooper–Gulen–Schill) | A/D2 | MVP |
| `earn_stab` | −σ(YoY PAT growth, 5y)/\|mean\| | B/D2 | MVP |
| `leverage` | −(debt/EBITDA); −(net debt/net worth) | B/D2 | MVP |
| `cash_conv` | 3y cum. CFO / 3y cum. PAT | B/D2 | MVP, weight ×1.5 — India's single most informative leg (§5) |
| `piotroski_f` | 9-point F-score | B/D2 | DEF — spanned by legs above |
| `qmj_full` | AQR profitability+growth+safety+payout | A/D2 | DEF |

Family weights equal (methods §4) except the two ×1.5 legs, frozen at inception.

### 4.3 Low-risk (`W_lowrisk` 0.20 aggressive / 0.25 moderate)

`lowbeta`, `idiovol`, `maxret` exactly as §3, D1 in both PO-FL and FUND-FL. Frazzini–Pedersen's leverage-constraint mechanism applies with extra force in India, where the retail tail is leverage-constrained but lottery-seeking and F&O concentrates what leverage exists into a few hundred names. **Sector carve-out:** FMCG and pharma are structurally low-beta, so sector-neutralising destroys part of the premium. We compute both; within-sector enters the composite, and the cross-sector residual is exported to L10 as `lowvol_sector_component` — zero own budget, exactly like L05's `value_spread_z`.

### 4.4 Size and size×quality (`W_size` 0.15 aggressive / 0.05 moderate)

Raw size is weak in India — the IIM-A SMB averaged ≈0%/yr, 1994–2014. It enters at weight 0.25 within family; the family is dominated by `size_x_qual = z(−size)×z(qual_composite)` at 0.75, following Asness, Frazzini, Israel, Moskowitz & Pedersen (2018): small caps earn a premium once junk is controlled for, and the Indian micro tail is where junk concentrates. The moderate book's `W_size = 0.05` reflects that its universe (§10) has almost no small-cap tail for the tilt to express.

### 4.5 Yield (`W_yield` 0.10 both books)

`net_payout = (dividends + buybacks − issuance)/mcap`, trailing 12m, from corporate-action and Reg 30 filings. Issuance is the load-bearing leg — dilution via preferential allotments and QIPs is common in India and is the cleanest free proxy for growth financed externally. Dividend yield alone is **not** used standalone: post-2020 it is a tax-regime artefact and a value proxy, not a factor.

### 4.6 Growth — deliberately absent

No standalone growth factor. Sustainable growth enters through `roic` and `asset_growth` (negative sign), L11's bottom-up score, and L04's `duration_tilt`. A positively-signed growth factor has no robust cross-market premium and would double-count momentum. **DEF, with prejudice.**

---

## 5. India-specific evidence and the IIM-A benchmark

Agarwalla, Jacob & Varma's Fama-French-momentum library (1994–2014, free, survivorship-corrected): Market 11.5%, **WML 21.9%** (L08's, not mine), **HML 15.3%**, SMB ≈0%. Four places India genuinely differs: **(1) quality is stronger, value lumpier** — a long 2013–2020 drought, then a violent 2021–2023 recovery, so `W_qual > W_val` in both books and value's only timing channel is T1 below; **(2) promoter holding and governance have no developed-market analogue** — ~50% average promoter ownership makes pledge, dilution and related-party extraction the dominant idiosyncratic risk, so §9 is a factor family with its own weight, not an add-on; **(3) the small-cap tail is wide and partly synthetic** — 12m-return dispersion is roughly 1.6–1.9× larger in the Smallcap 250 than the Nifty 100 [verify], which is where alpha and operator-driven ramps both live, so the aggressive book gets the tail and the moderate book gets neither; **(4) cross-sector accounting comparability is worse than the US**, making within-sector scoring a correctness requirement, not a refinement.

**The rule: if our value factor does not broadly reconcile with theirs, our construction is wrong, not theirs.** A CI test against a committed fixture (`fixtures/iima_iffm_monthly.csv`) asserts, for `F ∈ {HML, SMB, WML_ref}` (WML_ref built only for this test, never traded): `corr(ours, theirs) ≥ 0.75` over ≥120 overlapping months; `|mean_ann(ours)−mean_ann(theirs)| ≤ 4.0pp`; `beta(ours~theirs) ∈ [0.65,1.40]`; max rolling-12m `|cum(ours)−cum(theirs)| ≤ 20pp`; annual sign agreement `≥ 70%`. A failure is build-blocking with a fixed diagnostic ladder (universe, size breakpoint, rebalance lag, survivorship, definition) — in practice universe and survivorship, both L19 defects, explain most divergence. Their series is never an input to a score or a fitted parameter (CI-asserted import ban), and passing reconciliation validates our *plumbing*, not our *alpha*.

---

## 6. Construction mechanics

### 6.1 Universe

Consume `L08.eligible(i,t)` verbatim (ADV floor, 252-session history, EQ-series, GSM/ASM, parabolic filter). Add: `filed_quarters(i,t) ≥ 8` (else → L12 IPO sub-model); `newest_statement_age(i,t) ≤ 400 days` (stale filers excluded, not neutral-scored); `sector_pool(i,t)` defined.

### 6.2 Sector pools — the neutralisation decision

**Decision: all factor scores are computed within sector; the sector tilt is L10's separate, explicit, budgeted decision.** Three reasons: **(1) comparability** — a 4% net margin is excellent for a distributor, catastrophic for a software exporter, so a cross-sector rank on a margin ratio is a sector score with noise, not a factor score; **(2) double-counting (L01 §6)** — a raw cross-sector value score is ~40–60% a sector bet, and stacking it with L10's `sector_rotation_cycle` (`sector_l1_pp`=4 aggressive) and L03's tilt puts three claims on one force, exactly what L01 §6.3 residualises from −1,000bps to −350bps; **(3) accountability** — the book is deliberately sector-active, and an exposure arriving as a side effect of stock scores is owned by no one.

NSE's ~22 tier-2 sectors collapse to **12 scoring pools** (any sector with N<20 merges into its nearest macro-sector sibling, frozen in `config/factor_pools.yaml`). **Financials are always their own pool** (§6.4), split into Banks/NBFC-HFC/Insurance-AMC at N≥20 each. Sector classification history is D4; v1 applies today's classification backward (induced look-ahead estimated <20bps/yr, logged, scheduled for D4 reconstruction in v2).

**Size neutralisation: no.** Size is a factor we want exposure to via `size_x_qual`; neutralising deletes §4.4. The finished sleeve's size exposure is instead measured and capped — `z(size)` within ±0.75 of benchmark — so the book cannot become a covert micro-cap fund by accident; the intentional small-cap tilt runs through L07's `smallcap_breadth_cycle` budget.

### 6.3 The point-in-time lag, in days

Effective date = `max(imposed_historical_date, first_observed_in_archive)`.

| Object | LODR deadline | Imposed historical lag |
|---|---|---|
| Q1–Q3 results | 45 days | **period_end + 60 cal. days** |
| Q4 / annual audited | 60 days | **period_end + 90 days** |
| Half-yearly BS + CFS | with H1/annual | **+75 / +105 days** — drives `accruals`, `cash_conv`, `fcfy`, `roic` |
| Shareholding pattern, pledge | 21 days | **quarter_end + 30 days** |
| Annual report (RPT, contingent, subsidiaries) | AGM ≤6mo | **FY_end + 210 days** |
| Auditor resignation, audit qualification | 24 hours | **+1 day** — true PIT |
| ASM/GSM, circuits | daily | **file date** — true PIT |

The freshest fundamental input to a January score is the September quarter; the freshest balance sheet is the March or September half-year. The fundamental book is slow by construction — a cost in §10, an advantage for turnover.

### 6.4 Financials

Financials are ~30–35% of the Nifty 500 and their accounting differs in kind: no COGS, no EV, no ordinary working capital, debt as raw material not leverage.

| General pool | Financials substitute |
|---|---|
| `gpoa` | `ppop_a` = pre-provision operating profit / avg assets |
| `ebit_ev`, `fcfy`, `cash_conv` | dropped — undefined |
| `bp` | kept, up-weighted — P/B is the primary bank valuation metric |
| `asset_growth` | `loan_growth` — same mechanism; rapid growth predicts credit cost |
| `leverage` | `car_tier1`; `−(gnpa − pcr_coverage)` |
| `accruals` | `credit_cost_smoothing` = σ(quarterly provisions)/mean — low is suspicious in a rising-NPA cycle |

Insurance/AMC score on `bp`, `roe`, `earn_stab`, `net_payout` until populous enough for their own pool; embedded value and VNB margin are D4/D5, deferred.

### 6.5 Loss-makers and compositing

```
if trailing_4q_PAT <= 0:  ey, roe = MISSING (not 0, not bottom rank); distress_flag = True
if trailing_4q_EBIT <= 0 too:  ebit_ev = MISSING;  forensic penalty += 0.35 sigma
if PAT <= 0 in 3 of 4 quarters and net_debt/equity > 1.0:  HARD EXCLUDE  (zombie filter)
```

Rank-based, not z-score (Indian small-cap ratio tails would otherwise dominate the fit):

```
within pool s:  x_ik = winsorise(1st,99th pctile);  r_ik = avg rank
                n_ik = clip(Φ⁻¹((r_ik-0.5)/N_s), -2.5, +2.5)      # van der Waerden
family:         F_if = Σ w_k·n_ik / Σ w_k (observed);  c_if = coverage in [0,1]
                F_if = MISSING if c_if < 0.50;  re-rank F_if -> Ftil_if
composite:      S_i = Σ_f W_f·sqrt(c_if)·Ftil_if / Σ_f W_f·sqrt(c_if)   (unscored if Σ W_f < 0.60)
                S_i = S_i − P_i (forensic, §9);  clip(S_i, -3.0, +3.0)
```

`sqrt(c)` rather than `c` mirrors L01 §6.2's `sqrt(retained_variance)`: information scales with the square root of coverage, so a name missing half its legs keeps ~71% of its score, not 50%. Winsorise at 1st/99th percentile throughout (methods §6). Strategic family weights (§4) are frozen in git at inception, two signatures to change.

---

## 7. Factor timing: disciplined, limited, killable

Both sides are real. Asness (2016), "The Siren Song of Factor Timing," and Asness, Chandra, Ilmanen & Israel (2017) show value-spread timing is weak, largely a disguised long-value tilt, and has historically hurt when levered onto an already value-tilted book. Arnott, Beck & Kalesnik (2016) [verify exact title] show the opposite: factor valuations do predict factor returns, and ignoring a 95th-percentile spread is its own error. Both are right about *magnitude* — timing exists, and it is smaller than its advocates size it.

Three channels, hard caps, frozen parameters, no fitting:

| # | Channel | Source | Target | Max deviation | Dead band | Min evidence |
|---|---|---|---|---|---|---|
| T1 | Value spread | L05 `value_spread_z` | `W_val` | **±25%** | \|z\|<0.5 | Tier B, ≥8 non-overlapping obs |
| T2 | Macro style prior | L04 `duration_tilt`, `cyclicality_tilt` | `W_qual` vs `W_val` | **±20%** | \|tilt\|<0.25 | Tier B, L04 frozen mapping |
| T3 | Credit phase & smallcap breadth | L03 `s_credit`, L07 breadth | `W_size`, `leverage` leg weight | **±20%** | \|z\|<0.5 | Tier B, charged to those cycles' `name_l1_pp` |

```
HARD CAPS (all CI-asserted):  Σ|W_f(t)−W_f_strategic| ≤ 0.35·Σ W_f_strategic
   |ΔW_f| ≤ 0.03 (agg) / 0.015 (mod) per month;  W_f(t) ∈ [0.5, 1.5]·W_f_strategic
```

**The registry-derived room, checked line by line rather than assumed.** Charging each channel to its cited cycle's `name_l1_pp` (per §1's "no new budget" rule) gives real numbers, not round ones: T2 draws on `india_business_cycle` (name_l1_pp **1pp agg / 0pp mod**); T3 on `smallcap_breadth_cycle` (**3pp agg / 0pp mod**). **T1 has zero registry room in either book** — `equity_valuation_reversion`'s `name_l1_pp` is 0, because L05's cycle was budgeted for asset-class, not name-level, authority. So the honest aggregate ceiling under the current registry is **4pp of name-weight L1, aggressive only**; T1 is inert and moderate's T2/T3 room is zero until L01's next annual review adds a name-level allocation. Nothing here invents new authority to compensate — an unbudgeted cap would itself be a rule violation.

**Kill rule.** L20 reports `timing_contribution` gross and net, rolling 36-month, quarterly. Negative for three consecutive quarters ⇒ timing disabled, `W_f` reverts to strategic permanently, until a written case with a fresh out-of-sample window and two signatures reinstates it. Expected contribution, stated honestly: **0–40bps/yr, aggressive only, plausibly zero** — in the MVP because it costs 1.5 days and to have the machinery ready for the day the value spread hits an extreme or the registry gap closes, not because a return is expected now.

---

## 8. Factor combination — integrate, don't mix

**Decision: a single integrated composite `S_i`; separate sleeves across layers.** Integration dominates mixing at equal tracking error for long-only books (Fitzgibbons, Friedman, Pomorski & Serban 2017 [verify volume]) — a sleeve-of-sleeves happily holds a cheap fraud the value sleeve loves and quality hates; an integrated score never buys it, which matters more in India's forensic-dominated tail than in the US. It also saves turnover (sleeves trading against each other is 100% turnover for zero net position change, unaffordable against the moderate book's ~68pp/yr name budget) and position count (a five-sleeve ₹100cr book of 20 names each is 100 positions averaging 0.3% of NAV).

**The carve-out: momentum stays out.** L08 owns a crash-control apparatus (volatility scaling, a panic gate, an asymmetric ladder) that must act on the momentum exposure in isolation; folding it into `S_i` would hide that exposure at exactly the moment — a rebound off a bottom — it matters most. Architecture: **integrated within L09, mixed across L08/L09/L11/L12**, L14 doing the netting.

**The score, and why it survives the 5.7× book difference.** `S_i` is a clipped sigma score (§6.5), not a weight and not an expected return — a name's rank ordering within its sector pool, identical in construction for both books. L14 §6.2 finds that converting a score to a weight requires a per-book gain `k` that differs 5.7× between books (`name_l1_pp`/names/`E|z|`: 1.755pp/σ aggressive vs 0.306pp/σ moderate), because the two books' capital-per-name-slot differs by design, not because the underlying signal differs. Keeping `S_i` book-agnostic and pushing all of that difference into L14's `k` is deliberate: it means L09 never has to know which book is asking, and a future change to either book's `name_l1_pp` budget requires zero change here.

```python
FACTOR_SCORE[symbol] = { 'S': float, 'S_pofl': float,
  'families': {'value','quality','lowrisk','sizequal','yield': Ftil},
  'coverage': {family: c_if}, 'n_missing_legs': int, 'pool': str, 'pool_n': int,
  'P_forensic': float, 'flags': {...}, 'pit_status': 'lag_approx'|'true' (S_pofl only),
  'confidence': float, 'asof': date, 'vintage_id': str }
```

---

## 9. Forensic and exclusion screens — the negative factor

In India this is not hygiene, it is where the largest single-name losses are avoided: governance failures are slow-then-sudden, years of accumulating flags then a 40–70% fall over days. Every screen is one-sided (`P_i ≥ 0`), mirroring L01 R3.

| Screen | Source | Threshold | Action |
|---|---|---|---|
| Auditor resignation mid-term | Reg 30 (D1) | any | **HARD EXCLUDE 24m** |
| Auditor change ≥2/5y, net of rotation | Reg 30 + s.139 calendar | 2+ unexplained | −1.00σ |
| Audit qualification, quantified | Reg 33 statement (D1) | >5% of PAT | **EXCLUDE** to 2 clean periods |
| Promoter pledge | Reg 31 (D2) | >25% | −0.75σ |
| | | >50% | **HARD EXCLUDE** |
| | | +10pp QoQ | −0.50σ |
| Promoter holding decline | Reg 31 | >5pp/12m ex-offer | −0.50σ |
| CFO-to-PAT divergence | half-yearly CFS (D2) | 3y CFO/PAT <0.50 | −1.00σ |
| | | <0.25 | **EXCLUDE** |
| Receivable-days deterioration | half-yearly BS (D2) | DSO >1.5× own median & >pool p75 | −0.75σ; 2 periods → **EXCLUDE** |
| Contingent liabilities | annual report (D4) | >50% net worth | −0.50σ; >100% → **EXCLUDE** |
| Related-party intensity | Reg 23 + annual report (D4) | >15% of base | −0.50σ; >30% → **EXCLUDE** |
| Subsidiary complexity | annual report (D4) | >25 subs & consol-standalone gap >40% | −0.50σ |
| Independent-director exits | Reg 30 (D1, post-2021) | ≥2/12m | −0.50σ |
| ASM stage≥2 / any GSM | NSE/BSE surveillance (D1) | any | **HARD EXCLUDE** while listed + 60d |
| Zombie filter | §6.5 | PAT≤0 3/4q & net debt/equity>1.0 | **HARD EXCLUDE** |

`P_i = min(Σ applicable penalties, 2.50)` — the cap stops the screen becoming a de-facto short book; hard exclusions are absolute, never auto-reversed. **MVP** = the D1/D2 screens (auditor, qualification, pledge, promoter decline, ASM/GSM, zombie, CFO/PAT, DSO) — also the *cleanest PIT data in the layer*, since Reg 30 and surveillance carry true knowledge dates. D4 screens (contingent liabilities, RPT, subsidiary complexity) need annual-report PDF parsing, **deferred to v1.5**. Financials drop RPT (inter-group lending is their business) for `related_party_advances/net worth > 10%`. An absolute 25% sector cap would make these screens decorative for the largest sector before they can bind — this layer joins L14 and L17 in depending on `min(25%, benchmark+10pp)`.

---

## 10. Capacity, both books

Neutral equity 60%. Recommended equity-sleeve split (a recommendation to L14, which owns the blend): aggressive — factor 40% / momentum 35% / bottom-up 15% / special situations 10%; moderate — factor 55% / momentum 25% / bottom-up 20%.

| | Aggressive ₹100cr | Moderate ₹1,000cr |
|---|---|---|
| Factor sleeve capital | 40% of equity ⇒ **₹24cr** | 55% ⇒ **₹330cr** |
| Eligible names at the ADV floor | **~500 of 750** [verify] | **~275 of 750** [verify] |
| Sleeve holdings | 40 names, avg 0.6% NAV | 30 names, avg 1.1% NAV |
| Implied sleeve capacity | **₹400cr (16× headroom)** | **₹1,980cr (6× headroom)** |

**Finding 1 — capacity does not bind either sleeve.** Factor turnover is low, and capacity scales with trading rate; a book turning over 30%/yr needs a sixth the liquidity of one turning over 200%/yr. **Finding 2 — breadth and dispersion bind instead, costing the moderate book ~45% of factor alpha.** Grinold: `IR ∝ IC·√breadth`; 500 vs 275 names gives `√(500/275)=1.35×`; dispersion in the moderate universe is ~1.3–1.6× narrower (§5); combined, moderate alpha ≈ `1/1.35² ≈ 0.55` of aggressive — gross sleeve alpha 4.5–7.0%/yr aggressive vs 2.5–4.0%/yr moderate, netting to roughly **1.0–1.5pp / 0.7–1.2pp of book CAGR**. **Finding 3 — the factor book is the moderate book's primary name engine.** At an identical 60pp active L1, L01's turnover identity gives momentum (`tau_half`=6m) 67.9pp/yr against factor (`tau_half`≈30m) 30.3pp/yr; against the moderate book's ~68pp/yr name-turnover residual, the recommended 55%/25% split costs ~33.6pp/yr, leaving headroom for L11/L12, while the aggressive book's 500%/yr ceiling carries both at full size without constraint.

Rebalance cadence: aggressive — monthly refresh, monthly rebalance, 1.5× rank buffer; moderate — monthly refresh, **quarterly** rebalance, 2.0× rank buffer, 0.4%-of-sleeve no-trade band. The buffer, not the cadence, does most of the turnover work.

---

## 11. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L19 | `pit_store`, `universe(asof)`, `membership(asof)`, forward-archived filings | Bitemporal; final-vintage reads raise |
| L08 | `eligible(i,t)` | Consumed verbatim, never redefined |
| L05 | `value_spread_z` | Timing input only (T1); never used to compute a score |
| L04 | `duration_tilt`, `cyclicality_tilt` | Timing input only (T2) |
| L03, L07 | `s_credit`, `smallcap_breadth` phase | Timing input only (T3), charged to their `name_l1_pp` |
| L10 | `sector_map(symbol,asof)` | Pool definition only; I emit no sector view |
| L01 | `SIGN_CONVENTION` | `+1` = higher forward risk-adjusted return |

**Exposes**

```python
FACTOR_SLEEVE = {target_weights: {symbol: pct_nav}, sleeve_weight_pct, n_names,
                 sector_exposure: {sector: pct}, size_z_vs_bench, asof, vintage_id}
FACTOR_SCORE  = {symbol: {...}}          # §8
VAL_XS        = {value_spread_z_source: 'L05', W_f_current: {...}, timing_active: bool}
PIT_REPORT    = {pit_gap, restatement_delta (from ~2028), pofl_ir, fund_ir}
```

L14 consumes `FACTOR_SCORE` as a Block-B alpha input (name-level score, never a sleeve weight); L17 consumes exposures for its style-factor risk block; both are read-only against this layer's output.

---

## 12. MVP versus deferred

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | PO-FL | Full price-only book: `lowbeta`, `idiovol`, `maxret`, `size`, `size_x_lowrisk`, `lt_rev`, `illiq`, `forensic_px` | 4.0 | ✅ |
| 2 | Fundamentals adapter | Parse XBRL/Kaggle inputs from L19 into the value/quality legs, half-yearly handling | 5.0 | ✅ |
| 3 | Sector pools + tangibility gate + financials substitution | `config/factor_pools.yaml`, §6.4 substitute set | 2.0 | ✅ |
| 4 | Composite construction | Rank-normal scoring, coverage weighting, loss-maker/zombie handling | 3.0 | ✅ |
| 5 | Forensic screens (D1/D2 set) | Auditor, pledge, promoter decline, ASM/GSM, zombie, CFO/PAT, DSO | 3.0 | ✅ |
| 6 | Factor timing | 3 channels, hard caps, kill rule | 1.5 | ✅ |
| 7 | IIM-A reconciliation | Fixture + CI test, import-ban assertion | 1.5 | ✅ |
| 8 | Capacity + cadence | ADV-derived sleeve construction, per-book rank buffers | 1.0 | ✅ |
| 9 | Property tests + fixtures | Synthetic panel incl. missing-data, financials, illiquid tail | 2.5 | ✅ |
| 10 | Explainability report | Per-rebalance score, coverage, penalty, binding-constraint log | 1.0 | ✅ |
| **MVP total** | | | **24.5** | |
| 11 | D4 forensic screens | RPT, contingent liabilities, subsidiary complexity from annual-report PDFs | 3.0 | ⬜ |
| 12 | `piotroski_f`, `qmj_full` | Largely spanned by MVP legs | 2.0 | ⬜ |
| 13 | PCA sector residual for `resmom`-style factor risk | Replaces market+sector regression | 2.0 | ⬜ |
| 14 | `restatement_delta` measurement | Requires 2 years of forward-archive accumulation | — | ⬜ |

**Cut, not deferred:** `ibp` (intangibles-adjusted book/price) — D5, no free route, replaced permanently by the tangibility gate.

---

## 13. Risks and constraint conflicts

1. **The PIT bias is irreducible in its middle component.** 100–300bps/yr of restatement look-ahead survives every mitigation until the forward archive matures around 2028. Every FUND-FL backtest carries `pit_gap` on its cover page, not in a footnote.
2. **Half-yearly, not quarterly, is the true refresh rate for most of the quality family** — a reviewer assuming quarterly accruals will overstate this layer's responsiveness by 2×.
3. **The sector-cap resolution matters here too.** Financials scored with a substituted set are decorative if the absolute 25% cap forces a permanent underweight before the forensic screens can bind — this layer depends on `min(25%, benchmark+10pp)`, alongside L14 and L17.
4. **D4 screens (RPT, contingent liabilities) are the highest-value deferred item** — structurally India's largest hidden risks, gated on PDF-parsing effort, not evidence quality.
5. **The tangibility gate is blunt.** A single trailing-3y 0.20 threshold will misclassify some asset-heavy but intangible-adjacent businesses; frozen in git so this is revisited on evidence, not vibes.
6. **Factor timing's expected contribution is plausibly zero** — retained for optionality at the next value-spread extreme, not because a positive return is expected; the kill rule stops it becoming a quietly fitted parameter.
7. **T1's value-spread timing channel has no registry budget.** `equity_valuation_reversion` carries `name_l1_pp: 0` in the current registry (it was budgeted for asset-class authority only), so under the "charge to the cited cycle's own budget" rule this layer holds itself to, T1 is currently inert and the moderate book's T2/T3 room is also zero. This is a registry gap for L01 to close, not a use-it-anyway decision.
8. **This layer is the largest single concentration of the stack's `lag_approx` contamination** and must be labelled as such in every output.

---

## 14. References

1. Novy-Marx, R. (2013). "The Other Side of Value: The Gross Profitability Premium." *JFE* 108(1), 1–28.
2. Sloan, R. (1996). "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" *The Accounting Review* 71(3), 289–315.
3. Cooper, M., Gulen, H. & Schill, M. (2008). "Asset Growth and the Cross-Section of Stock Returns." *JF* 63(4), 1609–1651.
4. Frazzini, A. & Pedersen, L. (2014). "Betting Against Beta." *JFE* 111(1), 1–25.
5. Asness, C., Frazzini, A., Israel, R., Moskowitz, T. & Pedersen, L. (2018). "Size Matters, If You Control Your Junk." *JFE* 129(3), 479–509.
6. Asness, C., Frazzini, A. & Pedersen, L. (2019). "Quality Minus Junk." *Review of Accounting Studies* 24(1), 34–112.
7. Piotroski, J. (2000). "Value Investing…" *Journal of Accounting Research* 38, 1–41.
8. Banz, R. & Breen, W. (1986). "Sample-Dependent Results Using Accounting and Market Data." *JF* 41(4), 779–793 — a PIT E/P effect can vanish versus ex-post data.
9. Peters, R. & Taylor, L. (2017). "Intangible Capital and the Investment-q Relation." *JFE* 123(2), 251–272.
10. Eisfeldt, A. & Papanikolaou, D. (2013). "Organization Capital and the Cross-Section of Expected Returns." *JF* 68(4), 1365–1406.
11. Arnott, R., Harvey, C., Kalesnik, V. & Linnainmaa, J. (2021). "Reports of Value's Death May Be Greatly Exaggerated." *FAJ* 77(1) [verify exact venue for the intangibles argument].
12. Bali, T., Cakici, N. & Whitelaw, R. (2011). "Maxing Out." *JFE* 99(2), 427–446.
13. De Bondt, W. & Thaler, R. (1985). "Does the Stock Market Overreact?" *JF* 40(3), 793–805 — the `lt_rev` window.
14. Dimson, E. (1979). "Risk Measurement When Shares Are Subject to Infrequent Trading." *JFE* 7(2), 197–226.
15. Vasicek, O. (1973). "Bayesian Estimation of Security Betas." *JF* 28(5), 1233–1239.
16. Amihud, Y. (2002). "Illiquidity and Stock Returns." *Journal of Financial Markets* 5(1), 31–56.
17. Fitzgibbons, S., Friedman, J., Pomorski, L. & Serban, L. (2017). "Long-Only Style Investing: Don't Just Mix, Integrate." *Journal of Investing* [verify volume].
18. Asness, C. (2016). "The Siren Song of Factor Timing." *JPM*, Special QES Issue, 42(5).
19. Asness, C., Chandra, S., Ilmanen, A. & Israel, R. (2017). "Contrarian Factor Timing Is Deceptively Difficult." *JPM* 43(5).
20. Arnott, R., Beck, N. & Kalesnik, V. (2016). "Timing 'Smart Beta' Strategies?" Research Affiliates wp [verify exact title/venue].
21. Agarwalla, S. K., Jacob, J. & Varma, J. R. (2013). IIMA WP 2013-09-05; (2017) "Size, Value, and Momentum in Indian Equities." *Vikalpa* 42(4). <https://faculty.iima.ac.in/iffm/>. **Prowess-built — benchmark only, never an input.**
22. Fama, E. & MacBeth, J. (1973). "Risk, Return, and Equilibrium." *JPE* 81(3), 607–636.
23. López de Prado, M. (2018). *Advances in Financial Machine Learning.* Wiley — purged/embargoed CV, §5 and §7.
24. DeMiguel, V., Garlappi, L. & Uppal, R. (2009). "Optimal Versus Naive Diversification." *RFS* 22(5), 1915–1953 — equal-within-family weighting.
25. Grinold, R. & Kahn, R. (2000). *Active Portfolio Management*, 2nd ed. McGraw-Hill — the fundamental law (`IR ∝ IC·√breadth`) behind §10's capacity findings.
26. Free-source index: NSE bhavcopy <https://www.nseindia.com/all-reports> · NSE/BSE XBRL filings · SEBI LODR Reg 23/30/31/33 · niftyindices <https://www.niftyindices.com> · Kaggle/HuggingFace fundamentals scrapes · IIM-A IFFM library.

*`[verify]` requires confirmation against the primary source before circulation.*
