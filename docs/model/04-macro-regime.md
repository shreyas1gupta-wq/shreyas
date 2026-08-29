# Layer 04 — Macro Regime: Growth, Inflation, Rates and Liquidity (1–10 years)

**Abstract.** This layer converts free Indian macro data into a *probability distribution over
nine growth × inflation regime cells*, modulated by a continuous financial-conditions scalar, and
emits three things: an asset-class tilt vector, an equity style tilt, and a set of **gates** that
condition faster layers — chief among them the momentum sleeve's weight. Nominal growth is treated
as the primary variable rather than real growth, because every high-frequency series India
publishes for free (GST collections, e-way bills, bank credit, nominal exports) is nominal, and
because the owner's thesis is that momentum works better in higher nominal growth. That thesis is
addressed honestly: the strongest replicated conditioners of momentum in the literature are
**volatility and market state**, not macro growth, and Griffin–Ji–Martin (2003) explicitly fails to
replicate Chordia–Shivakumar (2002) outside the US. The nominal-growth gate is therefore built,
bounded to a multiplier in [0.55, 1.30], and *residualised against L08's own volatility and
market-state gate* so it can only act on what those do not already say. The layer's allocation
authority is not asserted; it is **pre-registered against a measured out-of-sample R²** (§11), with
the honest expectation that macro regime explains 1–3% of forward quarterly Indian equity variance
and therefore earns roughly ±8pp of equity authority, not the ±12pp the L01 B3 budget permits. Two
facts dominate the engineering: free Indian macro is published as *current, revised* data with no
knowledge date, and **all three primary series were rebased between February and June 2026** (CPI to
2024=100, GDP to 2022-23, IIP to 2022-23), so every z-score window in this layer straddles a
definitional break. The layer's genuine value is asymmetric — it is much better at flagging when
*not* to be levered than at forecasting returns, which is exactly what the binding drawdown
constraint needs.

---

## 1. Scope, and what this layer is not

**Owns:** the growth/inflation/rates/liquidity state of the Indian economy on a 1–10 year horizon,
its representation as a probability vector, and the gates it exports downward. In L01's registry
this layer owns `india_business_cycle`, `kitchin_inventory`, `rbi_policy_rate_cycle`,
`inflation_cycle` (all MVP) and `election_policy_cycle` (deferred).

**Does not own, and must not rebuild:**

| Belongs to | Do not duplicate |
|---|---|
| L03 credit/capex | the credit-to-GDP gap and the 8–16y financial cycle. I use *credit impulse* only, as one FCI component, residualised against their `credit_gap_z` |
| L06 external | USDINR cycle, crude cycle, REER, global liquidity/dollar. I consume `oil_shock_flag`, `usdinr_state`, `global_liquidity_z` |
| L02 long wave | the structural gold anchor, the debasement arc, the leverage ceiling floor |
| L13 gold sleeve | gold implementation, ETF-vs-futures, roll. I emit a *cyclical* gold tilt only |
| L17 risk engine | volatility state, funding stress, the drawdown/cash-call ladder. I am budgeted; L17 is not (L01 R7) |
| L05 valuation | equity expected returns. I emit a regime, not a return forecast |

**Sign convention (L01):** `+1` always means "state historically favourable to risk assets".

---

## 2. The state space

Three axes. Two carry the cell structure; the third is deliberately kept continuous.

```
G   real growth z-score          -> 3 bands (LOW / MID / HIGH)   } 9 cells
I   inflation state              -> 3 bands (LOW / MID / HIGH)   }
FCI financial conditions z       -> continuous scalar modifier, NOT a third grid dimension
NG  nominal growth z             -> derived: the gate variable, and the parent of G
```

**Why liquidity is not a third grid dimension.** 3 × 3 × 3 = 27 cells against ~30 years of monthly
data with an 18-month autocorrelation half-life gives roughly 20 independent macro episodes total —
under one observation per cell. Nine cells is already generous (2–4 independent episodes each,
§9.2). The financial-conditions axis therefore enters as an additive, continuous modifier with a
single coefficient per asset class. This is a deliberate dimension reduction, not an oversight.

**Why nominal growth is primary and real growth is derived.** India's free high-frequency data is
nominal by construction. GST collections are rupees collected. Bank credit is rupees lent. E-way
bills are consignments valued in rupees. Deflating them requires a price index that arrives later
and is itself revised. So we nowcast **nominal** GVA growth directly, then subtract a deflator
nowcast to obtain real growth. `G = NG − deflator`, with the deflator's own error carried through.
This is the reverse of the usual construction and it is the right way round for free Indian data.

---

## 3. The data spine

All sources free. Column `PIT` uses L01's D-tier vocabulary: `true` = genuinely point-in-time,
`lag_approx` = published as current/revised, we impose a fixed conservative lag,
`rebased` = definitional break requiring a splice record.

### 3.1 Series table

| # | Series / field | Source (free) | URL | Freq | Start | Release lag | PIT | Transform used |
|---|---|---|---|---|---|---|---|---|
| 1 | CPI Combined, General Index | MOSPI press release Table 1 | mospi.gov.in | M | 2011-01 (2012=100); **2026-02 (2024=100)** | 12 d (12th of M+1) | lag_approx / **rebased** | YoY; 3m SAAR |
| 2 | CPI 6 groups + 12 sub-groups | same release, Annexure | mospi.gov.in | M | 2011-01 | 12 d | lag_approx | core construction; diffusion index |
| 3 | CPI-IW | Labour Bureau | labourbureau.gov.in | M | 1960s | ~30 d | lag_approx | pre-2011 back-cast of headline |
| 4 | WPI all-commodities + groups | Office of the Economic Adviser | eaindustry.nic.in | M | 1994 (spliced) | 14 d; **final at +10 weeks** | revised | YoY; WPI–CPI wedge; **our only genuine vintage pair** |
| 5 | IIP general / mfg / use-based | MOSPI | mospi.gov.in | M | 1994-04; **new 2022-23 base from 2026-06** | 42 d (12th of M+2) | lag_approx / **rebased** | YoY; 3m/12m ratio |
| 6 | GDP + GVA, nominal and real, quarterly | MOSPI NAD press note | mospi.gov.in | Q | 1996-Q2; **new 2022-23 base from 2026-02-27** | ~60 d | revised PE→3RE / **rebased** | YoY nominal (target of the bridge) and real |
| 7 | PMI manufacturing / services / composite output | S&P Global (headline free) | pmi.spglobal.com | M | mfg 2005-03, svc 2005-12 | 1–3 business days | true | level − 50; 3m MA |
| 8 | Gross GST collections | GST portal news PDFs | tutorial.gst.gov.in/downloads/news/ | M | 2017-07 | **1 day** | true | YoY of 3m MA |
| 9 | E-way bills generated | NIC / GSTN | ewaybillgst.gov.in | M | 2018-04 | ~10 d | true | YoY of 3m MA |
| 10 | Repo rate; MPC stance text | RBI press releases | rbi.org.in | event | 2000-06 | 0 | true | level; Δ6m; Δ12m; stance dummy |
| 11 | Net LAF / daily money-market operations | RBI MMO page + Weekly Statistical Supplement | rbi.org.in, data.rbi.org.in | D / W | 2004 | 1 d | true | net absorption as % of NDTL; 20d MA; z(5y) |
| 12 | M3 | RBI WSS | data.rbi.org.in | fortnightly | 1970 | ~10 d | lag_approx | YoY minus nominal GDP YoY |
| 13 | SCB non-food credit; sectoral deployment | RBI WSS + monthly sectoral release | data.rbi.org.in | fortnightly / M | 1972 | ~10 d / 30 d | lag_approx | YoY; credit impulse |
| 14 | 10y benchmark GSec yield | FBIL / CCIL | fbil.org.in, ccilindia.com | D | 1997 | 0 | true | level; term spread |
| 15 | 91-day T-bill yield | RBI auction results / FBIL | data.rbi.org.in | W | 1993 | 0 | true | term spread base |
| 16 | USDINR reference rate | RBI | data.rbi.org.in | D | 1993 | 0 | true | 3m Δlog (into imported inflation) |
| 17 | Brent crude | FRED `DCOILBRENTEU` (also EIA) | fred.stlouisfed.org | D | 1987 | 1 d | true (ALFRED) | INR-converted; 3m Δlog; z |
| 18 | Indian crude basket | PPAC | ppac.gov.in | D | 2005 | 1 d | true | cross-check on #17 |
| 19 | US 10y TIPS real yield | FRED `DFII10` | fred.stlouisfed.org | D | 2003-01 | 1 d | true (ALFRED) | z(10y); Δ6m — **the gold driver** |
| 20 | All-India SW monsoon rainfall vs LPA | IMD | mausam.imd.gov.in | W in JJAS | 1901 | 1–3 d | true | cumulative % departure |
| 21 | Sub-division rainfall, 36 subdivisions | IMD / OGD | mausam.imd.gov.in, data.gov.in | W | 1901 | 3 d | true | **fraction of subdivisions deficient (< −20% LPA)** |
| 22 | Gridded daily rainfall 0.25° | IMD Pune | imdpune.gov.in/cmpg/Griddata | D | 1901–2024 | annual | true | deferred: district-level stress index |
| 23 | Oceanic Niño Index (ENSO) | NOAA CPC | cpc.ncep.noaa.gov | M | 1950 | ~5 d | true | 3m mean; **6–9m lead on monsoon** |
| 24 | Live reservoir storage | CWC weekly bulletin / India-WRIS | cwc.gov.in | W | 2010 | 5 d | true | % of 10-year average |
| 25 | Kharif / rabi sowing area | Ministry of Agriculture weekly | agriwelfare.gov.in | W | 2010 | 7 d | true | % of normal area |
| 26 | FX reserves | RBI WSS | data.rbi.org.in | W | 1998 | 5 d | true | 12-week Δ (intervention proxy) |
| 27 | Merchandise + services trade | Ministry of Commerce | commerce.gov.in | M | 1996 | ~15 d | lag_approx | nominal exports YoY |

Series 22, 24, 25 are deferred (§12). Everything else is MVP-eligible.

### 3.2 The two-clock rule and revision handling

Every series is stored bitemporally as `(event_date, knowledge_date, value, vintage_id)`. A read at
simulated date *t* returns only rows with `knowledge_date <= t`. Final-vintage reads raise at the
API boundary (L19 contract). Three revision classes, three treatments:

**Class 1 — never revised.** Market prices, repo rate, LAF, exchange rates, GST collections as
published, IMD rainfall, ONI. `knowledge_date = event_date + lag_days` from the table. No further
treatment. **This class is the backbone of the layer and it is why FCI is more trustworthy than
the growth nowcast.**

**Class 2 — revised on a known schedule.** WPI (provisional → final at +10 weeks); IIP (revised at
+1m and +3m); GDP (PE → FRE → 1st/2nd/3rd RE over ~3 years). We hold only the *final* print
historically. Two mitigations, both required:

1. **Conservative fixed lag** from the table, applied to the *final* value. This is the standard
   dodge and it is insufficient on its own, because the final value is not what was known.
2. **Revision-noise injection in backtest.** Add `N(0, σ_rev)` to every historical Class-2 value
   before it enters a signal. `σ_rev` is estimated from the vintage pairs we *can* obtain — the
   WPI provisional/final pair (a true, free, ~20-year vintage panel), the "revisions" statement in
   each MOSPI quarterly GDP press note, and successive annual editions of the **RBI Handbook of
   Statistics on Indian Economy**, each edition of which is a dated vintage of ~200 series going
   back to the 1950s. That Handbook is the single most under-used free vintage source in Indian
   macro and it should be archived in full on day one. Working priors, to be replaced by measured
   values: IIP YoY first-print vs final σ ≈ 1.0–1.5 pp [verify]; quarterly real GDP YoY first-print
   vs 3rd RE σ ≈ 0.5–1.0 pp [verify]; WPI YoY provisional vs final σ ≈ 0.2–0.4 pp [verify].
   **Every backtest is run twice, with and without injection, and both are reported.** A signal
   whose Sharpe halves under injection was never a signal.

**Class 3 — rebased or discontinued.** Splice at the **growth-rate level, never at the index level**,
and record a `series_break` entry `{series, break_date, old_base, new_base, overlap_months,
splice_method}`. A backtest at simulated date *t* must use the definition in force at *t*.

> **The 2026 problem, stated plainly.** CPI moved to 2024=100 on 12 Feb 2026, with food & beverages
> reweighted from 45.86% to 36.75%. GDP moved to base 2022-23 on 27 Feb 2026. IIP moves to base
> 2022-23 with effect from 1 June 2026. All three of this layer's primary inputs were redefined
> inside four months, immediately before this build. Consequences: (a) a food-inflation module
> calibrated on the old weights is not the same object as one calibrated on the new; (b) any
> rolling z-score with a window longer than ~6 months currently straddles a break; (c) the new IIP
> incorporates GST data, so IIP and GST are no longer independent nowcast inputs after mid-2026 and
> the bridge must down-weight one of them. All three are handled by the splice registry, and (c) is
> handled by dropping IIP's bridge coefficient by half from 2026-06 onward. This is a hard-coded,
> dated, git-logged adjustment, not a fitted one.

### 3.3 Standardisation policy

Every z-score in this layer uses an **expanding window with a 60-month minimum, capped at 180
months, computed strictly on data with `knowledge_date <= t`**, using median and 1.4826·MAD rather
than mean and standard deviation. Rationale: Indian macro series contain COVID observations that
are 6–10σ under a Gaussian estimator and would permanently distort any mean/SD window. Winsorise
inputs at ±3.5 MAD-σ before aggregation. The 2020-04 to 2020-09 window is additionally flagged
`covid_exclusion` and excluded from *parameter estimation* while remaining present in *simulation*.

---

## 4. Axis 1 — the nominal growth nowcast (NGN)

### 4.1 Construction

Target: **quarterly nominal GVA growth, YoY, at basic prices** (MOSPI). Monthly indicators are
aggregated to the quarter and mapped by a ridge-regularised bridge regression.

```
NGN_q  =  a  +  Σ_k  b_k · x_k,q
```

Fitted by ridge (λ from 5-fold *blocked* CV, blocks = 8 consecutive quarters to respect
autocorrelation), refit **annually only** and frozen between refits, with the fit date recorded.
Coefficients are never refit mid-backtest.

Because GST history begins 2017-07 and e-way bills 2018-04, a single bridge cannot span the
backtest. **Two nowcasts, explicitly:**

| | `NGN_long` | `NGN_short` |
|---|---|---|
| Span | 1996-Q2 → | 2018-Q2 → |
| Indicators | IIP YoY; WPI-manufactured YoY; SCB non-food credit YoY; nominal exports YoY; PMI composite (from 2005, zero before) | all of the above **plus** GST YoY, e-way bill YoY |
| Coefficients | equal-weight on standardised inputs, **frozen at inception**, not fitted | ridge-fitted, refit annually |
| Use | the **only** series a backtest may read | live blending only |

```
live:      NGN = 0.50 · NGN_long + 0.50 · NGN_short
backtest:  NGN = NGN_long                       # enforced by the data layer, CI-asserted
log:       divergence = NGN_short − NGN_long, monitored; > 1.5σ for 2 months raises an alert
```

This is not conservatism for its own sake. Blending a 2018-start series into a 1996-start backtest
is exactly the leak that makes a nowcast look prescient. The cost — the backtest does not see the
best data we have — is accepted and stated.

`NGN_z = z_expanding(NGN)`. Real growth `G_z = z_expanding(NGN − deflator_nowcast)`, where
`deflator_nowcast = 0.6 · CPI YoY + 0.4 · WPI YoY` (a crude but stable free proxy for the GVA
deflator; the true deflator is only known with GDP itself).

**Nowcast standard error** `σ_G` is the blocked-CV residual SD of the bridge inflated by the
revision variance of the target: `σ_G = sqrt(σ_cv² + σ_rev,GVA²)`. Expect 0.35–0.55 in z units.
This is the number that drives the soft-membership width in §9.1, so it is a first-class output,
not a diagnostic.

### 4.2 The momentum gate — functional form

This is the layer's most consequential export. Bounded logistic:

```
m(NG_z) = m_min + (m_max − m_min) / (1 + exp(−s · (NG_z − c)))

m_min = 0.55    m_max = 1.30    s = 1.20    c = −0.25
```

| `NG_z` | −3.0 | −2.0 | −1.5 | −1.0 | −0.5 | 0.0 | +0.5 | +1.0 | +1.5 | +2.0 | +3.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `m` | 0.58 | 0.63 | 0.69 | 0.76 | 0.86 | 0.98 | 1.09 | 1.17 | 1.22 | 1.25 | 1.28 |

`m` multiplies the **momentum sleeve's target weight**, not individual name scores — L08 owns name
selection; I only scale the sleeve.

**The orthogonalisation requirement (non-negotiable).** L08 already runs a volatility-scaling and
market-state gate (Barroso–Santa-Clara; Cooper–Gutierrez–Hameed). Those are the *strongly evidenced*
conditioners. My gate must act only on the residual:

```
m_applied = 1 + (m(NG_z) − 1) · sqrt(1 − R²(NG_z ~ [vol_state_z, mkt_state_z]))
```

with `R²` estimated on a 120-month rolling window and shrunk per L01 §6.2. Empirically `R²` will be
high in crises (nominal growth collapses exactly when volatility spikes), so the gate will
*correctly* contribute almost nothing in March 2020 — L08's own vol gate is already doing the work —
and will contribute most in slow, non-volatile nominal-growth slowdowns such as 2019 and 2012–13,
which is precisely where an independent macro signal has something to add.

**Rebalance intensity.** The sleeve's rebalance interval and no-trade band scale inversely with `m`:

```
interval_weeks = clip(round(base_weeks / m), lo, hi)
   aggressive: base 2, lo 1, hi 4        moderate: base 4, lo 4, hi 12
no_trade_band_multiplier = clip(1 / m, 0.80, 1.60)
```

Rationale is cost, not alpha: when the sleeve is down-weighted there is less to be gained from
trading it, and churning a de-emphasised sleeve is pure cost. This is a defensible engineering
rule; there is, to my knowledge, **no published evidence on the optimal rebalance frequency of
momentum conditional on macro state in India**, and none is claimed.

### 4.3 What the evidence does and does not support

**Supports macro conditioning of momentum:**

- **Chordia & Shivakumar (2002)**, *JF* 57(2):985–1019. US momentum payoffs are predictable by
  lagged macro variables (dividend yield, default spread, term spread, short rate) and *disappear*
  once returns are adjusted for macro-predicted expected returns. The strongest single citation for
  the owner's thesis.
- **Cooper, Gutierrez & Hameed (2004)**, *JF* 59(3):1345–1365. Mean monthly momentum profit
  following positive market returns 0.93%, following negative market returns −0.37% (1929–1995).
  Large and robust — but this is a **market-state** conditioner, not a nominal-growth one.
- **Daniel & Moskowitz (2016)**, *JFE* 122(2):221–247. Momentum crashes cluster in panic states
  (bear market plus high volatility) during rebounds. Again volatility and market state.
- **Barroso & Santa-Clara (2015)**, *JFE* 116(1). Scaling momentum by its own realised volatility
  roughly doubles its Sharpe ratio. The single most effective conditioner known, and it uses no
  macro data at all.

**Cuts against it:**

- **Griffin, Ji & Martin (2003)**, *JF* 58(6):2515–2547, "Momentum Investing and Business Cycle Risk:
  Evidence from Pole to Pole." Macroeconomic risk variables **do not** explain momentum profits
  internationally; the Chordia–Shivakumar result does not replicate outside the US. This is the
  direct rebuttal and it must not be omitted from any presentation of this layer.

**India:** Agarwalla, Jacob & Varma (2013 WP; 2017, *Vikalpa*/*Journal of Emerging Market Finance*
[verify outlet]) document a large Indian momentum premium (~21.9% p.a. over their sample) and
publish a free four-factor library at faculty.iima.ac.in/iffm/. **That library is built from CMIE
Prowess and is therefore a validation benchmark only, never a model input** (L01 §14 ref. 5). I am
aware of **no published study conditioning Indian momentum on nominal growth.** If one exists it
should be found; absent it, this gate is an untested hypothesis.

**Honest conclusion.** The owner's thesis is plausible and worth building, but the strongly
evidenced conditioners are volatility and market state, and nominal growth's incremental content
beyond them is unproven anywhere and untested in India. The design response is the three
constraints above: bounded multiplier [0.55, 1.30], residualisation against L08's own gates, and a
pre-registered authority rule (§11). If the residualised gate adds nothing measurable in L20's
validation, it should be set to a constant 1.0 and the code kept.

---

## 5. Axis 2 — inflation regime and its sub-cycles

### 5.1 The state variable

Anchored to the RBI's target, not purely statistical — the 4% ± 2% band is a *policy-relevant*
threshold and behaves as a structural break in the reaction function:

```
I_level   = 3m MA of CPI Combined YoY
I_gap     = I_level − 4.0                                   # target midpoint
core_saar = 3m annualised SA change in core CPI
I_z       = 0.60 · clip(I_gap / 1.5, −3, 3)  +  0.40 · z_expanding(core_saar)
```

Bands: `HIGH` if `I_z > +0.5`, `LOW` if `I_z < −0.5`, else `MID`. Hysteresis per L01 §7.4: enter a
directional inflation state at `|I_z| ≥ 0.75`, exit only below `0.45`, minimum dwell 4 months.
A headline print above 6.0% (the upper tolerance band) for two consecutive months sets a hard
`inflation_breach` flag regardless of `I_z`, because that is the level at which RBI behaviour
changes discretely.

**Core is computed, not downloaded.** MOSPI does not publish a core CPI. Construct:
`core = CPI excluding "Food and beverages", "Fuel and light", and "Pan, tobacco and intoxicants"`,
re-weighted to sum to 1. This requires the sub-group index table from each monthly release
annexure — a real, recurring PDF-scraping job with an annual format-change risk, and it is a named
line item in the build plan, not a footnote.

**Core stickiness** is measured by diffusion, not level:
`core_diffusion = fraction of the 12 CPI sub-groups with YoY > 4.0%`, 3m MA. A diffusion above 0.60
with a flat headline is the signature of broad-based, sticky inflation and is materially more
informative about RBI behaviour than the headline number alone.

**WPI–CPI wedge** = `WPI YoY − CPI YoY`. Wide positive wedge = producer margin compression ahead
(input costs outrunning consumer prices); wide negative = margin expansion. Feeds the equity style
tilt, not the asset-class tilt.

### 5.2 The monsoon / food module

India-specific and genuinely predictive, because the physical driver leads the price by two to three
quarters and the physical driver is free daily data.

```
subdiv_deficient_frac  = (# of 36 IMD subdivisions with cumulative JJAS rainfall < −20% LPA) / 36
allindia_departure     = cumulative all-India JJAS rainfall as % departure from LPA
reservoir_z            = z of (live storage as % of 10-year average)      [deferred]
sowing_gap             = (kharif sown area / normal area) − 1             [deferred]
oni_lead               = 3-month mean Oceanic Niño Index, lagged 6 months  # ENSO leads monsoon

food_pressure_z = 0.45 · z(subdiv_deficient_frac)
                + 0.25 · z(−allindia_departure)
                + 0.20 · z(oni_lead)
                + 0.10 · z(3m momentum of SA food CPI)
```

**Spatial diffusion matters more than the all-India number.** A national departure of −8% that is
concentrated in a few subdivisions is a non-event; the same −8% spread across half the country is a
food-price shock. The all-India figure is what the press reports and it is the weaker of the two
variables. `subdiv_deficient_frac > 0.35` is the working trigger threshold.

**Empirical expectation, to be measured not assumed.** Monsoon deficits transmit to food CPI with a
2–3 quarter lag, concentrated in vegetables, pulses and cereals. Deficit years to use as the
in-sample analogue set: 2002, 2004, 2009, 2014, 2015, 2018 and the 2023 El Niño year [verify each
departure figure against IMD's own time series before use]. With seven episodes, `n_eff ≈ 7`, this
is an L01 **tier B** signal — parameters set from reasoning and frozen, tested by "did it move in
the right direction in each analog episode", never by Sharpe ratio.

**Seasonality.** Food CPI has strong, stable seasonality (vegetable prices peak roughly July–
November). All food-CPI transforms use an X-13-style seasonal adjustment estimated on a rolling
120-month window **with the seasonal factors themselves lagged one year** so the current year's
observation does not participate in estimating its own seasonal factor.

**Policy floor.** Minimum Support Price announcements (CACP, free, annual, June and October) set a
floor under cereal inflation independent of the monsoon. Carried as a deferred additive term.

### 5.3 Imported inflation

```
brent_inr        = Brent USD/bbl × USDINR
imported_infl_z  = z_expanding( 3m Δlog(brent_inr) )
oil_shock        = imported_infl_z > +1.5   (consumed from L06 as `oil_shock_flag`; not rebuilt)
```

Pass-through is asymmetric and administered: to CPI "Fuel and light" it is muted and delayed by
excise and retail-price management; to WPI it is fast and large. So the *first* place an oil shock
shows up in free data is the WPI–CPI wedge, typically one to two months before CPI moves. That
wedge is therefore the early-warning variable, and it is free and unrevised-ish (WPI provisional).

---

## 6. Axis 3 — financial conditions (FCI)

Sign-oriented so **positive = easy**. All components z-scored on 5-year windows, then weighted:

| Component | Definition | Source | Weight |
|---|---|---|---|
| Real policy rate | repo − 3m MA of CPI YoY | RBI + MOSPI | **−0.25** |
| System liquidity | net LAF absorption as % of NDTL, 20d MA (sign: surplus positive) | RBI MMO / WSS | **+0.20** |
| Credit impulse | `(ΔCredit_{t,12m} − ΔCredit_{t−12,12m}) / nominal GDP_t` | RBI WSS + MOSPI | **+0.20** |
| Term spread | 10y GSec − 91d T-bill | FBIL / CCIL / RBI | **+0.15** |
| Excess money | M3 YoY − nominal GDP YoY | RBI + MOSPI | **+0.10** |
| Corporate spread | AAA 5y − GSec 5y (inverted) | FBIL valuation yields [verify free tenor coverage] | **−0.10** |

`FCI_z = Σ w_i · z_i`, weights sum to 1.0 in absolute value, **frozen at inception**. Credit impulse
is residualised against L03's `credit_gap_z` before entry (L01 §6.2 slowest-first: the 8–16y credit
cycle is the parent, the 1–2y impulse is the child, and only the child's residual is mine).

Global financial conditions are consumed from L06 as `global_liquidity_z` and enter as a separate,
declared input — not folded into `FCI_z` — so that the domestic and global legs can be attributed
separately in the arbitration log.

**As at 2026-08-28** the domestic liquidity leg is in deficit — reported net system liquidity
deficit of roughly ₹3.4 lakh crore on 22 Aug 2026 [verify against RBI's own MMO page; the figure is
from a secondary source]. That is a materially tight reading and, if confirmed, pushes `FCI_z`
negative regardless of the growth/inflation cell.

---

## 7. The rate cycle

The debt sleeve has **no duration overlay** (frozen decision Q17). The rate cycle therefore expresses
itself through exactly three channels and no others.

### 7.1 RBI policy phase — a rule-based state machine

```
d6  = repo(t) − repo(t−6m)          d12 = repo(t) − repo(t−12m)
rr  = repo − 3m MA CPI YoY          rr_z = z_expanding(rr)
stance ∈ {accommodative, neutral, withdrawal_of_accommodation, calibrated_tightening}
         parsed from the MPC resolution text (RBI press release, free, scrapeable)

TIGHTENING      if d6 > +25 bp
EASING          if d6 < −25 bp
ON_HOLD_TIGHT   if |d6| <= 25 bp and rr_z > +0.5
ON_HOLD_EASY    if |d6| <= 25 bp and rr_z < −0.5
NEUTRAL_DRIFT   otherwise
```

Minimum dwell 3 months. The stance string is carried but does not override the rate arithmetic in
MVP; a stance/arithmetic disagreement raises a flag for the Stage-2 overlay to look at.

**Turn detection is deliberately weak.** A logit for `P(first cut within 2 quarters)` on
`{rr_z, I_gap, G_z, term_spread_z, stance_dummy}` has roughly 5–6 rate cycles since 2000 to learn
from — `n_eff ≈ 5`, hence **L01 tier C**, hence **one-sided authority under rule R3: it may only
reduce risk.** It is deferred to v2 and, when built, may raise gold or cash but may not raise
equity or leverage. Predicting RBI turns is the most seductive and least supportable thing this
layer could do.

### 7.2 Real rates and gold

For a rupee investor, gold return = USD gold return + USDINR return. The dominant driver of the USD
leg is the **global** real rate, not India's:

```
real_rate_z_global = z_10y( US 10y TIPS yield, FRED DFII10 )      # 2003–; pre-2003 proxy below
d_real_rate_6m     = DFII10(t) − DFII10(t−6m)
gold_tilt_pp       = clip( −1.5 · z(d_real_rate_6m), −2.0, +6.0 )   # aggressive; ×0.75 moderate
```

Pre-2003 proxy: `US 10y nominal (DGS10) − Cleveland Fed 10y expected inflation (FRED EXPINF10YR)`,
spliced at growth-rate level with a `series_break` record. The rupee leg belongs to L06 and the
gold sleeve to L13; I contribute a *cyclical* tilt inside my B3 gold budget of [−2, +6] pp, on top
of L02's structural anchor, and I am subject to L02's hard 4% gold floor and 30% ceiling.

### 7.3 Equity duration and cyclicality — two orthogonal style axes

The common error is to collapse "rates" into one style call. There are two independent channels:

```
duration_tilt    = clip( −0.8 · z(Δ real 10y GSec yield, 6m)  −  0.4 · I_z , −1, +1 )
                   #  +1 = favour LONG-duration (high P/E, back-loaded cash flow, growth, quality)
                   #  −1 = favour SHORT-duration (high FCF yield, low P/E, value)
cyclicality_tilt = clip( +0.9 · NG_z  +  0.3 · FCI_z , −1, +1 )
                   #  +1 = favour cyclicals, operating leverage, capex beneficiaries
                   #  −1 = favour defensives, staples, low-beta
```

2020 is the worked case that shows why they must be separate: real rates collapsed (`duration_tilt`
strongly positive → growth and quality won, correct) while nominal growth also collapsed
(`cyclicality_tilt` negative → defensives, correct); then through 2021–22 nominal growth surged and
real rates rose, flipping both. A single "rates" axis gets 2020 and 2021 wrong in opposite
directions. Both are emitted to L09 (factor library) and L10 (sector model) as *priors on style
exposure*, never as name-level trades.

### 7.4 The cash call

The rate cycle's third channel. `FCI_z < −1.25` combined with `G_z < −0.5` is this layer's
contribution to the cash-call ladder — but L17 owns the ladder and is unbudgeted (L01 R7). I emit
`gross_leverage_cap_modifier ∈ [−0.25, 0.00]` — **one-sided, may only reduce** — and a
`macro_derisk_score ∈ [0, 1]`; L17 decides what to do with them.

---

## 8. The mapping: nine cells

Tilts are **deviations in percentage points of NAV from the L01 §8.1 neutral policy portfolio
(Equity 60 / Gold 12 / Debt 28, gross 1.00x)**, for the **aggressive** book. Moderate book =
× 0.75 (its B3 budget is 9pp vs 12pp). Every row sums to zero.

| Cell | G | I | Equity | Gold | Debt | Cash | Equity style tilt | Momentum `m` prior | Reliability |
|---|---|---|---|---|---|---|---|---|---|
| **Goldilocks** | HIGH | LOW | **+10** | −1.5 | −8.5 | 0 | long-duration growth, quality; small-cap OK | 1.20 | med-high |
| **Boom** | HIGH | MID | **+9** | 0 | −7 | −2 | cyclical value, operating leverage | 1.20 | med-high |
| **Overheat** | HIGH | HIGH | **+2** | +4 | −6 | 0 | energy/materials, short-duration value, pricing power | 1.10 | medium |
| **Disinflation drift** | MID | LOW | **+4** | 0 | −4 | 0 | quality, long-duration, rate-sensitives | 1.00 | medium |
| **Muddle-through** | MID | MID | 0 | 0 | 0 | 0 | neutral | 1.00 | n/a |
| **Stagflation-lite** | MID | HIGH | **−4** | +3 | 0 | +1 | short-duration value, low-vol, pricing power | 0.90 | low-med |
| **Deflationary bust** | LOW | LOW | **−10** | +2 | +8 | 0 | quality, low-vol, defensives, balance-sheet strength | 0.70 | medium |
| **Slowdown** | LOW | MID | **−8** | +1.5 | +6.5 | 0 | quality, low-vol | 0.80 | medium |
| **Stagflation** | LOW | HIGH | **−11** | +6 | +2 | +3 | gold, energy, low-vol; avoid leverage entirely | 0.60 | low |

**Budget check against L01 §8.2 (aggressive B3: equity ±12, gold −2/+6, debt ±10, sector L1 12):**
max |equity| = 11 ≤ 12 ✓; gold up 6 ≤ 6 ✓; gold down 1.5 ≤ 2 ✓; max |debt| = 8.5 ≤ 10 ✓.

**Why Stagflation adds cash rather than debt.** The frozen debt assumption is 10% return, 4% vol,
6% worst drawdown, with equity correlation flipping from about −0.2 in disinflation to about **+0.4
in an inflation shock** (DECISIONS Q16). In the Stagflation cell that correlation flip removes the
hedge exactly when it is needed, and a 10% return implies AA/A credit, whose drawdown in an
inflation shock is materially worse than 6%. So Stagflation gets +2 debt and +3 true cash, not +5
debt. **This is the single most important interaction between this layer and the frozen debt
assumption, and getting it wrong would put the optimizer into leveraged credit in the one regime
that kills leveraged credit.**

**Financial-conditions modifier**, applied additively after cell blending:

```
equity_pp += clip( 3.0 · FCI_z , −4.0, +4.0 )
gold_pp   += clip( −1.5 · z(d_real_rate_6m) , −2.0, +6.0 )
debt_pp    = −(equity_pp + gold_pp + cash_pp)          # residual, then clipped to budget
```

The resulting vector is then handed to L01's `resolve()`, which applies tier multipliers, the
disagreement haircut, the cluster cap, the rate limiter and the no-trade band. **This layer never
writes a portfolio weight; it writes a contribution.**

---

## 9. Transitions: probability, not switching

### 9.1 Soft membership

No hard classification anywhere in the production path. `(G_z, I_z)` is treated as a draw from a
bivariate normal with the nowcast's own standard errors and the 120-month rolling correlation
`ρ_GI`:

```python
def regime_probs(G_z, I_z, sig_G, sig_I, rho, cut=0.5):
    """Return P(cell) for the 9 growth x inflation cells."""
    S = np.array([[sig_G**2, rho*sig_G*sig_I], [rho*sig_G*sig_I, sig_I**2]])
    mvn = multivariate_normal(mean=[G_z, I_z], cov=S)
    gb = [(-np.inf, -cut), (-cut, cut), (cut, np.inf)]      # LOW / MID / HIGH
    P = np.zeros((3, 3))
    for i, (g0, g1) in enumerate(gb):
        for j, (i0, i1) in enumerate(gb):
            P[i, j] = mvn_rect_prob(mvn, (g0, g1), (i0, i1))   # inclusion-exclusion on the CDF
    return P / P.sum()

tilt = sum(P[i, j] * TILT_TABLE[i][j] for i in range(3) for j in range(3))
```

`sig_G`, `sig_I` come from §4.1 and the inflation nowcast's residual — typically 0.35–0.55 and
0.25–0.40 respectively. Note that the tilt is **continuous and differentiable in `(G_z, I_z)`**;
there is no threshold to whipsaw across.

### 9.2 Diffuseness penalty

Averaging over a diffuse posterior shrinks the tilt automatically, but not enough when the mass sits
on two adjacent same-signed cells. So an explicit confidence multiplier on top:

```
H          = −Σ p log p / log 9                  # normalised entropy, 0 = certain, 1 = uniform
confidence = clip(0.40 + 0.80 · (1 − H), 0.40, 1.00)
tilt_final = tilt · confidence · book_scale
```

| `H` | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|---|
| `confidence` | 1.00 | 1.00 | 0.80 | 0.60 | 0.40 |

### 9.3 Label, dwell and confirmation

The **reported regime label** (what humans and the Stage-2 overlay read) and the **allocation tilt**
are different objects with different update rules, and conflating them is a common failure:

- **Tilt:** updates every rebalance from the current probability vector. No dwell, no confirmation —
  the probabilities already encode the uncertainty.
- **Label:** `argmax P`, changes only after **two consecutive months** with the new argmax and
  `max P > 0.30`, and carries a **minimum dwell of 4 months**. The label exists for explanation and
  for Stage-2 review; it has no allocation authority.

### 9.4 Regime break

```
if max(P) < 0.35 for 2 consecutive months:
    regime_break_flag = True
    layer_influence_multiplier = 0.60   for 3 months, then linear recovery over 3 more
    band widths (enter/exit z) widened by 50%
```

This is L01 §7.3's "a trigger is evidence you were wrong before, not proof you are right now"
applied to state rather than phase: when the classifier stops being able to tell where it is, it
loses influence rather than picking a cell at random.

### 9.5 Staleness

Every output carries `staleness_days = t − max(knowledge_date over MVP inputs)`. If any Class-2
input is more than 1.5 × its nominal lag overdue (a delayed MOSPI release, a government-shutdown-
style data gap), that component drops out of the composite and its weight is redistributed, and
`confidence` is multiplied by `sqrt(remaining_weight)`.

---

## 10. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L19 free-data pipeline | `pit_macro_store(series, asof)` | Bitemporal; final-vintage reads raise. All 27 series in §3.1 |
| L01 cycle taxonomy | registry entries for `india_business_cycle`, `kitchin_inventory`, `rbi_policy_rate_cycle`, `inflation_cycle`; `influence_budget()`, `resolve()`, rate limiter | Output must validate against the registry; unregistered ids rejected |
| L03 credit / capex | `credit_gap_z` | Credit impulse is residualised against it. I never emit a credit-cycle view |
| L06 external | `oil_shock_flag`, `usdinr_state`, `global_liquidity_z`, `reer_z` | Consumed, never rebuilt. The FX and crude cycles are theirs |
| L02 long wave | `LW_CONSTRAINTS` (gold floor 5%, gold ceiling 30%, leverage ceiling), `debt_corr_state` | My gold tilt is additive on their anchor and clipped by their floor/ceiling |
| L17 risk engine | `vol_state_z`, `mkt_state`, `current_drawdown` | Used only for the §4.2 residualisation, so my gate does not duplicate theirs |
| L20 validation | `oos_r2_macro_regime` | **Sets my equity budget via the pre-registered rule in §11** |

**Exposes**

```python
MACRO_STATE = {NGN_z, NGN_level_pct, G_z, I_z, I_level_pct, I_gap, FCI_z,
               regime_probs: {cell: p}, regime_label, entropy_H, confidence,
               months_in_label, regime_break_flag, staleness_days, asof, vintage_id}

MACRO_TILT  = {equity_pp, gold_pp, debt_pp, cash_pp,
               style: {duration_tilt, cyclicality_tilt},
               book_scale: {aggressive: 1.00, moderate: 0.75},
               max_delta_pp_per_month: 0.667}          # L01 §8.5, tau_half = 18m, tier B

MACRO_GATES = {momentum_weight_multiplier,             # m_applied, §4.2
               momentum_rebalance_interval_weeks,
               no_trade_band_multiplier,
               gross_leverage_cap_modifier,            # ONE-SIDED: <= 0 always
               macro_derisk_score}

MACRO_RATES = {policy_phase, real_repo_z, term_spread_bps,
               real_rate_z_global, d_real_rate_6m}

MACRO_INFL  = {food_pressure_z, monsoon_departure_pct, subdiv_deficient_frac,
               oni_lead, imported_infl_z, core_diffusion, wpi_cpi_wedge,
               inflation_breach}
```

**Stage-1 sufficiency.** With the Stage-2 overlay switched off, this layer emits a complete
`MACRO_TILT` and `MACRO_GATES` from data alone. The Stage-2 overlay may write only into
`nowcast_override_proposal` (a signed adjustment to `NGN_z`, capped at ±0.75σ, two-signature,
logged with a falsification condition) and `tier_downgrade`. It may not change the tilt table, the
cell boundaries, or any weight. A CI test asserts that disabling Stage 2 leaves `MACRO_TILT`
bit-identical.

---

## 11. How much authority this layer deserves

### 11.1 What the evidence says

Contemporaneous macro news explains far less of equity return variance than intuition suggests.
Cutler, Poterba & Summers (1989) find identified macroeconomic news explains only a modest fraction
of monthly US return variance. Chen, Roll & Ross (1986) find industrial production growth, inflation
surprises, the term spread and the default spread are priced, but with low contemporaneous R².
Flannery & Protopapadakis (2002) find 6 of 17 macro announcement series move US market returns.
Rapach, Wohar & Rangvid (2005) find interest rates the most consistent international macro
predictor. Regime-switching allocation adds value (Ang & Bekaert 2002; Guidolin & Timmermann 2007)
but the gains come mostly from **avoiding the bad regime**, not from ranking the good ones.

For **India specifically I know of no published, credible estimate** of the share of Nifty return
variance explained by a macro regime classifier, and I will not invent one.

### 11.2 The pre-registered authority rule

Rather than assert a number, measure it and bind the budget to the measurement. L20 runs, **before
any allocation code is written and with the result recorded in git**:

> Regress forward 3-month Nifty 500 TRI excess return on the 9-element regime probability vector
> plus `FCI_z`, on 1996-07 → present, with purged and embargoed k-fold CV (embargo 6 months, purge
> 3 months), Newey–West standard errors at lag 6, and a block bootstrap (24-month blocks, 5,000
> draws) for the confidence interval on **out-of-sample** R².

| Measured OOS R² | This layer's equity budget (aggressive) | Gold | Debt |
|---|---|---|---|
| < 1% | ±4 pp | −1 / +3 | ±4 |
| 1–3% | ±8 pp | −2 / +4 | ±7 |
| > 3% | ±12 pp (full L01 B3 budget) | −2 / +6 | ±10 |
| < 0% (OOS R² negative) | **±2 pp, one-sided (de-risk only)** | −0 / +3 | ±3 |

The tilt table in §8 is written to the ±12pp column; a lower measured R² scales the whole table
linearly. **My honest prior is 1.5–3%, so the realistic outcome is the ±8pp row.** The owner should
expect this layer to be intellectually central and allocationally modest, and that is not a
contradiction.

### 11.3 The asymmetry that actually earns the layer its keep

The measured R² on forward returns understates this layer's value, because its real contribution is
conditional and one-sided. Split the same regression by outcome quantile: macro state has far more
information about the **left tail** than about the mean. Tight financial conditions plus decelerating
nominal growth is a genuinely informative joint state about *drawdown*, and it is the state in which
running 1.5x gross leverage is most expensive. Given the binding constraint is "maximum drawdown
below the Nifty 50's, ceiling 30–35%", the correct use of this layer is:

1. **De-gearing** — `gross_leverage_cap_modifier`, one-sided, unbudgeted-adjacent (feeds L17).
2. **The cash call** — `macro_derisk_score`.
3. **Style rotation** — `duration_tilt`, `cyclicality_tilt`, which are lower-variance calls than
   the equity/debt split and are consumed by layers with their own evidence.

and only fourth, the asset-class tilt itself. L20 should therefore additionally measure the layer
against **forward 3-month drawdown** and **forward 3-month realised volatility**, not just forward
return, and I expect the R² there to be materially higher (5–15%). If it is, that — not return
prediction — is the case for the layer.

---

## 12. MVP versus deferred

Honest total for a complete build: ~30 engineer-days. **MVP must fit 15.**

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Series adapters + fixtures | Adapters for the 14 MVP series in §3.1; one committed fixture per series so the whole layer runs offline (mandatory per ENVIRONMENT-CONSTRAINTS) | 3.0 | ✅ |
| 2 | Bitemporal + splice layer | Two-clock reader, fixed-lag table, `series_break` registry with the three 2026 rebases pre-loaded, growth-rate splicing | 2.0 | ✅ |
| 3 | CPI annexure scraper | Sub-group index extraction from the monthly MOSPI PDF; core construction; diffusion index | 1.5 | ✅ |
| 4 | `NGN_long` bridge | Equal-weight frozen bridge, expanding MAD z, `sig_G` from blocked CV | 2.0 | ✅ |
| 5 | Inflation state | `I_z` target-anchored, hysteresis, `inflation_breach`, WPI–CPI wedge | 1.5 | ✅ |
| 6 | FCI | Six components, credit-impulse residualisation against L03, frozen weights | 1.5 | ✅ |
| 7 | Regime classifier | Bivariate soft membership, 9-cell tilt table, entropy confidence, label dwell, regime-break | 2.0 | ✅ |
| 8 | Gates | `m(NG_z)` with L08 residualisation, rebalance interval, no-trade band, one-sided leverage modifier | 1.0 | ✅ |
| 9 | Minimal monsoon module | All-India LPA departure + `subdiv_deficient_frac` + ONI lead only | 0.5 | ✅ |
| 10 | RBI phase state machine | Rule-based, repo arithmetic + `rr_z`; stance parsed but non-binding | 1.0 | ✅ |
| 11 | Registry entries + explainability | Four L01 registry rows; one-page per-rebalance report: cell probabilities, contributions, clip reasons | 1.5 | ✅ |
| | **MVP total** | | **17.5** | |
| 12 | `NGN_short` + live blend | GST, e-way bill, divergence monitor | 1.5 | ⬜ |
| 13 | Revision-noise injection | RBI Handbook vintage archive, WPI prov/final panel, `σ_rev` estimation, dual backtest | 3.0 | ⬜ |
| 14 | Full monsoon module | Reservoirs, sowing, gridded district stress, MSP floor | 2.5 | ⬜ |
| 15 | Rate-turn logit | Tier C, one-sided; `P(cut within 2q)` | 1.5 | ⬜ |
| 16 | MPC stance NLP | Text classification of the resolution, hawkish/dovish scoring | 2.0 | ⬜ |
| 17 | Sector hint vector | Per-cell sector prior handed to L10 | 1.0 | ⬜ |
| 18 | Corporate spread component | FBIL valuation yields, AAA-GSec | 1.0 | ⬜ |

At 17.5 days MVP is 2.5 days over its budget. The cut, if forced: step 3 (CPI annexure scraper,
1.5d) — substitute RBI's published core-CPI-equivalent commentary or use headline-only inflation
with `core_saar` set from headline, at the cost of losing the stickiness diffusion. That is a real
loss and it should be the last thing cut, ahead of steps 9 or 10.

---

## 13. Risks and constraint conflicts

1. **All three primary series were rebased in 2026.** CPI (2024=100, 12 Feb 2026, food weight
   45.86% → 36.75%), GDP (2022-23 base, 27 Feb 2026), IIP (2022-23 base, effective 1 Jun 2026).
   Every long z-score window straddles a definitional break, the food module's weights changed by a
   fifth, and the new IIP incorporates GST data so two nowcast inputs stopped being independent.
   Handled by the splice registry and a dated coefficient adjustment, but this is a live source of
   error for the next 3–5 years and it cannot be engineered away.
2. **The nowcast's best inputs cannot be backtested.** GST has 9 years of history, e-way bills 8.
   That is one cycle. The `NGN_long` / `NGN_short` split is the honest answer, and its cost is that
   the backtest evaluates a *weaker* nowcast than the one that will run live — so live behaviour
   will differ from backtested behaviour in a direction we cannot measure.
3. **We have almost no real vintages.** Backtests use revised data with an imposed lag. Revision-
   noise injection (deferred, step 13) is the mitigation and it is deferred, which means the MVP
   backtest is optimistic by an unmeasured amount. Every MVP output must be labelled
   `pit=lag_approx`.
4. **The momentum-macro thesis may simply be false.** Griffin–Ji–Martin (2003) fails to replicate
   the Chordia–Shivakumar result outside the US, the strongly evidenced conditioners are volatility
   and market state, and there is no Indian study on nominal-growth conditioning. The residualised,
   bounded gate is designed so that a false thesis costs little; but if L20 finds the residual gate
   adds nothing, the owner should accept `m ≡ 1.0` rather than tune it until it works.
5. **Nine cells × four assets × two books is 72 numbers set by judgement.** This is the single
   easiest place in the entire model to overfit, and the overfitting would be invisible because
   there are only ~20 independent macro episodes to check against. The defences are: freeze the
   table in git at inception, require two signatures to change one number, and bind the whole
   table's scale to the pre-registered OOS R² (§11.2). Expect pressure to "just adjust" a cell the
   first time it looks wrong.
6. **Cell reliability is low everywhere.** With ~360 months and an 18-month autocorrelation
   half-life, each cell holds 2–4 independent episodes. `Deflationary bust` holds roughly one
   (2008–09, arguably 2020). Under L01 R3, any cell with fewer than two independent episodes must
   be marked `one_sided: true` — it may de-risk but not add risk. That applies to
   `Deflationary bust` today.
7. **This layer cannot prevent a March-2020 drawdown.** Indian macro data through February 2020 was
   unremarkable; `G_z`, `I_z` and `FCI_z` were all mid-range. A 38% index fall in five weeks is
   invisible to a layer whose fastest genuinely informative input has a 12-day publication lag.
   Concurring with L01 §8.6: the drawdown objective rests on L16 (options) and L17 (fast vol and
   funding triggers), not here. This layer helps with 2000–03, 2008 (from mid-2008), 2011–13 and
   2018–19; it does not help with a five-week gap-down.
8. **The moderate book's macro tilt can only genuinely update quarterly.** Its rebalance cadence is
   monthly/quarterly and its budget is 0.75×; combined with a 42–60 day data lag, the ₹1,000cr book
   receives a macro signal that is at best two months old and at worst five. That is not a design
   flaw to fix, it is a capacity constraint to state.
9. **Conflict with the frozen debt assumption.** A flat 10% return at 4% vol makes debt the
   optimizer's preferred asset in seven of nine cells. My tilt table partially counteracts this by
   adding *cash* rather than debt in Stagflation, but the deeper problem is L14's, not mine: the
   frozen assumption will corner-solution unless the regime-dependent correlation flip (−0.2 → +0.4)
   is implemented as a *state variable this layer sets*. I therefore expose `I_z` and
   `inflation_breach` explicitly so the optimizer can switch the correlation on my inflation state
   rather than on a static parameter. If L14 does not consume it, the flip does not happen and the
   book will be long leveraged credit into an inflation shock.
10. **Return aspiration.** This layer contributes perhaps 50–150 bps/yr of the total under the
    ±8pp authority I expect it to earn. It is not a route to 35–60% CAGR and should not be
    presented as one. Concurring with L01 §13.8 and L02.

---

## 14. References

1. Chordia, T. & Shivakumar, L. (2002). "Momentum, Business Cycle, and Time-Varying Expected
   Returns." *Journal of Finance* 57(2), 985–1019.
2. Griffin, J. M., Ji, X. & Martin, J. S. (2003). "Momentum Investing and Business Cycle Risk:
   Evidence from Pole to Pole." *Journal of Finance* 58(6), 2515–2547. — The direct rebuttal to (1)
   outside the US.
3. Cooper, M. J., Gutierrez, R. C. & Hameed, A. (2004). "Market States and Momentum." *Journal of
   Finance* 59(3), 1345–1365. — 0.93%/month after up markets vs −0.37% after down markets, 1929–1995.
4. Daniel, K. & Moskowitz, T. J. (2016). "Momentum Crashes." *Journal of Financial Economics*
   122(2), 221–247.
5. Barroso, P. & Santa-Clara, P. (2015). "Momentum has its moments." *Journal of Financial
   Economics* 116(1), 111–120.
6. Chen, N-F., Roll, R. & Ross, S. A. (1986). "Economic Forces and the Stock Market." *Journal of
   Business* 59(3), 383–403.
7. Cutler, D. M., Poterba, J. M. & Summers, L. H. (1989). "What Moves Stock Prices?" *Journal of
   Portfolio Management* 15(3), 4–12.
8. Flannery, M. J. & Protopapadakis, A. A. (2002). "Macroeconomic Factors Do Influence Aggregate
   Stock Returns." *Review of Financial Studies* 15(3), 751–782.
9. Rapach, D. E., Wohar, M. E. & Rangvid, J. (2005). "Macro variables and international stock
   return predictability." *International Journal of Forecasting* 21(1), 137–166. [verify journal]
10. Ang, A. & Bekaert, G. (2002). "International Asset Allocation With Regime Shifts." *Review of
    Financial Studies* 15(4), 1137–1187. Guidolin, M. & Timmermann, A. (2007). "Asset allocation
    under multivariate regime switching." *Journal of Economic Dynamics and Control* 31(11).
11. Pandey, R., Patnaik, I. & Shah, A. (2017). "Dating business cycles in India." *Indian Growth and
    Development Review* 10(1), 32–61. — Three recessions since 1996; the reason `india_business_cycle`
    is a state, not a clock.
12. Agarwalla, S. K., Jacob, J. & Varma, J. R. (2013). "Four factor model in Indian equities market."
    IIMA WP 2013-09-05; and the free factor library at
    <https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/>. **Built from CMIE Prowess —
    validation benchmark only, never a model input.**
13. Harvey, C. R., Liu, Y. & Zhu, H. (2016). "…and the Cross-Section of Expected Returns." *Review
    of Financial Studies* 29(1). — Why 72 hand-set cell numbers against 20 macro episodes is not
    estimation.
14. **Free-source index (verified reachable as of Aug 2026 by search; not fetchable from the build
    session per ENVIRONMENT-CONSTRAINTS):**
    MOSPI <https://mospi.gov.in> ·
    RBI DBIE <https://data.rbi.org.in/DBIE/> (the old `dbie.rbi.org.in` redirects here) ·
    RBI Handbook of Statistics on Indian Economy (annual, = a dated vintage) <https://rbi.org.in> ·
    Office of the Economic Adviser (WPI) <https://eaindustry.nic.in> ·
    GST monthly collections <https://tutorial.gst.gov.in/downloads/news/> ·
    E-way bill <https://ewaybillgst.gov.in> ·
    S&P Global India PMI <https://www.pmi.spglobal.com> ·
    CCIL <https://www.ccilindia.com> · FBIL <https://www.fbil.org.in> ·
    FRED / ALFRED <https://alfred.stlouisfed.org> (`DCOILBRENTEU`, `DFII10`, `DGS10`, `EXPINF10YR`) ·
    IMD rainfall statistics <https://mausam.imd.gov.in/imd_latest/contents/rainfall_statistics.php> ·
    IMD gridded rainfall 0.25° 1901–2024 <https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html> ·
    NOAA CPC ONI <https://www.cpc.ncep.noaa.gov> ·
    PPAC <https://www.ppac.gov.in> · CWC <https://cwc.gov.in> ·
    Open Government Data India <https://www.data.gov.in>
15. MOSPI base-year revisions, 2026: CPI 2024=100 released 12 Feb 2026 (food & beverages weight
    45.86% → 36.75%, per HCES 2023-24); GDP base 2022-23 released 27 Feb 2026; IIP base 2022-23
    effective 1 Jun 2026. Primary source: MOSPI press notes and PIB releases. **[verify each against
    the MOSPI press note PDFs before any code depends on the exact dates.]**

*Items marked [verify] require confirmation against the primary source before circulation.*
