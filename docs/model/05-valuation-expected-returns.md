# Layer 05 — Valuation Cycle and the Expected-Return Engine (3–15 years)

**Abstract.** This layer measures how expensive Indian equity is, how far corporate earnings sit above their sustainable path, and converts both into the capital-market-assumption (CMA) vector the Stage-3 optimizer consumes. Five conclusions matter more than the plumbing. **One:** market-cap-to-GDP and CAPE are the same statistic divided by the corporate profit share — `mcap_gdp ≡ PE × φ` — so the profit-share cycle, not the price multiple, is where almost all the information lives. India's listed profit share is at a record ≈5.3% of nominal GDP against a ten-year normal near 4.0%. **Two:** on a Grinold–Kroner build with every term free-sourced, the 7-year expected return on Indian broad equity is **≈10.8% nominal** (90% band ≈7.5–14.0%), against a *frozen* debt assumption of 10.0% at 4% volatility. That comparison implies a debt Sharpe of 1.00 against an equity Sharpe of 0.28 — the optimizer will corner into the 70% debt cap, and the 35–60% CAGR aspiration cannot come from beta. Both are reported as conflicts, not designed around. **Three:** the same build puts **mid/small-cap 7-year expected return at ≈7.5%, some 3.3pp *below* large cap**, because the smid price-to-book premium is ~1.7σ rich. That is a strategic fact about the NIFTY 750 tail the aggressive book lives in. **Four:** India's free history contains fewer than three independent 10-year observations, so the predictive coefficient cannot be estimated here; it is imported from cross-country evidence, frozen in git, and tested only for sign agreement across analog episodes — L01 tier B. **Five:** consequently this layer gets **−9pp / +8pp** of equity authority at **0.143 pp/month**, plus a one-sided extreme override. Valuation sets the strategic centre of gravity; it must not make the cash call. The largest engineering hazard is a data break, not a model error: NSE switched index P/E from standalone to consolidated earnings on **1 April 2021** and the published Nifty P/E fell from **40.1 to 32.7** overnight. Every percentile straddling that date is wrong until spliced.

---

## 1. Scope, and what this layer is not

**Owns.** The 3–15 year mean-reverting valuation state of Indian equity; the aggregate earnings, margin, ROE and profit-share cycle and its structural-versus-cyclical decomposition; the forward expected-return vector and regime-conditioned covariance for equity (large and smid), gold, debt and cash; the cross-sectional value spread; and the size-segment valuation premium.

**Does not own and must not rebuild.** Inflation or growth nowcasts (macro-regime layer). The credit cycle (credit layer). FX and commodity cycles (external layer). The tactical gold view or gold implementation (gold sleeve). Sector-level valuation *scores* — this layer exports the normalisation *method*, the sector model owns the scores. Factor construction and the value factor's weight (factor library). Bottom-up name valuation (bottom-up scoring). The optimizer's objective. The cash call (risk/drawdown engine).

**Numbering note.** Layer numbers are inconsistent across sibling specs already written. Every interface in §10 is keyed by layer **name**; numbers are illustrative only.

**Stage-1 sufficiency.** With the Stage-2 overlay off, this layer emits a complete CMA and a complete tilt from data alone. Every judgement parameter (`f`, `HL_φ`, `λ_PE`) has a computed default. Stage 2 may move exactly one of them (`f`, ±0.25, two signatures, logged) and nothing else. A CI test asserts the tilt is bit-identical with the overlay disabled.

---

## 2. Data spine — free sources, and the four breaks that will ruin you

| Code | Definition | Free source | History | PIT | Lag |
|---|---|---|---|---|---|
| `NSE_PEPB` | Daily P/E, P/B, dividend yield for Nifty 50, 100, 500, Midcap 150, Smallcap 250 | NSE `/reports-indices-yield`; legacy `historical_pepb` archive | Nifty 50 from 1999-01; broad indices ~2005 | `true` (published daily, never revised) | 1d |
| `NSE_IDXMCAP` | Index full and free-float market capitalisation | NSE index factsheets / monthly Market Pulse | 2005– | `true` | 1–30d |
| `MCAP_TOT` | NSE + BSE total listed market capitalisation | BSE daily; NSE Market Pulse monthly | 1995– | `true` | 1d |
| `RBI_CORP` | Quarterly aggregate sales, operating profit, net profit, interest coverage for ~2,700 listed non-government non-financial companies | RBI *Performance of Private Corporate Business Sector* (RBI Bulletin / DBIE) | ~2009– in current form; earlier variants to ~2000 **[verify start]** | `true` (a dated release) | 75d |
| `NGDP`, `RGDP` | Nominal and real GDP/GVA, quarterly and annual | MOSPI National Accounts | 1996– | `lag_approx`; **rebased 2022-23** | 60d |
| `CPI` | All-India CPI combined | MOSPI / RBI DBIE | 2011– (2012=100), **rebased 2024=100**; WPI back-splice to 1994 | `lag_approx` | 12d |
| `Y10`, `TBILL91` | 10y G-sec benchmark yield; 91-day T-bill | RBI DBIE; CCIL | 1996– / 1993– | `true` | 1d |
| `CAPE_IIMA` | CAPE for BSE Sensex and Nifty 500 at 10y, 7y and 5y windows | `capeindia.iima.ac.in` (IIM Ahmedabad India CAPE Data Resource) **[verify download format and history start]** | — | `true` | 30d |
| `NSE_BHAV` | Daily bhavcopy — the survivorship-free spine | NSE all-reports archive | 1994– | `reconstructed` | 1d |
| `SHOUT` | Shares outstanding per name, for the dilution term | NSE/BSE shareholding-pattern filings, corporate-action circulars | 2001– | `lag_approx` | 45d |
| `FIL_PL`, `FIL_BS` | Per-name quarterly P&L and half-yearly balance sheet | NSE/BSE corporate-filings archive (own scrape, forward-archived with true knowledge dates) | 2001– | `lag_approx` | 45–60d |
| `GOLD_USD`, `USCPI`, `USDINR` | LBMA gold, US CPI, rupee | World Gold Council Goldhub / FRED / RBI DBIE | 1968– | `true` | 1–30d |
| `ERP_XC` | Cross-country mature-market ERP and country risk premium | Damodaran free data, `pages.stern.nyu.edu/~adamodar` | 1960– (US), 1998– (country) | `true` | 365d |

**Break 1 — the consolidated-earnings switch, 2021-04-01.** Verified: published Nifty P/E fell from **40.1 (Mar-21) to 32.7 (Apr-21)** with no comparable price move. NSE published no overlap series. MVP splice:

```
ratio_hat = median(PE_pub[2021-04-01 : +20d]) / median(PE_pub[-20d : 2021-03-31])
PE_adj[t < 2021-04-01] = PE_pub[t] * ratio_hat      # expect ratio_hat ~ 0.82; MEASURE it, log it
```

Record `ratio_hat` in the vintage manifest. **Correct fix, deferred:** rebuild index aggregate earnings bottom-up from `FIL_PL` on reconstructed membership and demote `NSE_PEPB` to a validation series with a ±5% tolerance alarm.

**Break 2 — an earnings collapse is not a valuation signal.** Trailing P/E hit ~40 in 2020–21 because the denominator collapsed. Any raw trailing-P/E percentile ranks that as the most expensive moment in Indian history. This is the single strongest argument for GDP-normalised earnings (§3.4), and it is why `pe_500` carries **zero** direct weight in the composite and enters only through `eyg_real` at weight 0.15.

**Break 3 — listing penetration.** Both `mcap_gdp` and the profit share `φ` drift structurally upward as the economy formalises and lists. Reverting either to its own historical mean double-counts a one-way structural shift as cyclical excess. Every use of both is detrended (§3.2, §4.2).

**Break 4 — denominator rebasing.** MOSPI rebased the GDP series (2022-23 base) and CPI (2024=100). Both sit in the denominator of this layer's two most important ratios. The pipeline must store both vintages and splice on log-ratio over a 12-month overlap; a silent rebase is a silent regime break.

---

## 3. Aggregate valuation: definitions, India distributions, and the composite

All z-scores are **one-sided expanding-window** (mean and sd from data available at `asof` only), minimum 10-year burn-in, winsorised at ±3. Percentiles are expanding-window ranks. The distributions below are **priors the pipeline must recompute and may contradict**; a deviation above 0.5σ from these priors raises a review flag rather than silently overwriting.

### 3.1 The measures

| id | Definition | Update | India prior (median / p10 / p90) | 2026-08-28 reading |
|---|---|---|---|---|
| `pe_500` | Nifty 500 trailing P/E, spliced | Daily | 21.5 / 13.5 / 27.0 | **23.1** |
| `pb_500` | Nifty 500 trailing P/B | Daily | 3.00 / 1.85 / 4.20 | **3.51** → z ≈ +0.80 |
| `dy_500` | Nifty 500 dividend yield, % | Daily | 1.35 / 0.80 / 2.10 | **1.04%** |
| `sy_500` | Shareholder yield = `dy_500` − net issuance rate | Quarterly | +0.20 / −1.20 / +1.30 | **−0.26%** → z ≈ −0.28 |
| `mcap_gdp` | (NSE ∪ BSE market cap) / trailing-4q nominal GDP | Monthly | §3.2 | **132.1%** |
| `mcap_gdp_detr_z` | detrended `mcap_gdp` (§3.2) | Monthly | 0 / −1.28 / +1.28 by construction | **+0.55** |
| `eyg_raw` | `1/pe_500 − Y10`, pp — **diagnostic only** | Daily | −2.50 / −5.20 / +1.40 | **−2.52 pp** |
| `eyg_real` | `1/pe_500 − (Y10 − π_exp)`, pp | Daily | +2.00 / −1.00 / +4.50 | **+2.08 pp** → z ≈ +0.10 |
| `cape_gdp` | §3.4 | Quarterly | — | **32.8**, z ≈ **+1.23** |
| `cape7_iima` | IIM-A 7-year CAPE, Nifty 500 | Monthly | — | z ≈ **+1.00** **[verify from source]** |
| `erp_ante` | `E[R_equity] − Y10` from §5 | Quarterly | — | **+3.95 pp** |

Inputs used above: Nifty 500 P/E 23.1, P/B 3.51, DY 1.04%; total listed market cap ≈ $5.18tn; nominal GDP ≈ $3.92tn; `Y10` 6.85%; CPI (Jul-26) 4.5%; `π_exp` 4.60% (consumed from the macro layer). All free-sourced and reproducible.

### 3.2 Market-cap-to-GDP, detrended two ways

India's raw range since 2000: **low ~25–30% (FY2003)**, peak **~149–160% (Dec 2007)**, trough ~55% (Mar 2009) and ~56% (Mar 2020), 124% (FY2024), ~138% (Dec 2025), **132% (Aug 2026)**. Median 2000–2024 ≈ 78%. **[verify — recompute from `MCAP_TOT` and MOSPI; third-party readings for Jun-26 range 120% to 132% depending on GDP vintage and whether BSE-only or NSE∪BSE cap is used. Pin the definition before pinning the percentile.]**

That raw series is non-stationary. Two corrections, both computed, both exposed:

```
# (a) trend residual — cheap, MVP
trend_t         = one-sided OLS of log(mcap_gdp) on t, expanding, min 120 months
mcap_gdp_detr_z = (log(mcap_gdp_t) - trend_t) / sd(residuals up to t)

# (b) fixed-universe version — drift-free, DEFERRED (needs reconstructed membership)
mcap_fixed_t = sum over the top-500-by-cap names at t of (shares_out * price)
mcap_gdp_fx  = mcap_fixed_t / NGDP_trailing4q_t          # constant count => no penetration drift
```

Use `mean(z_a, z_b)` when both are fresh; `z_b` alone if they disagree by >1.0σ, with an alarm. The fitted trend as of 2026 sits at **≈118%** with residual sd ≈ **0.204 in logs**, so 132% is `ln(1.321/1.18)/0.204 = +0.55σ` — mildly expensive, not extreme. Anyone quoting raw 132% against a raw median of 78% and calling it a bubble is reading listing penetration as valuation.

### 3.3 The earnings-yield gap, and why Asness is right and matters more in India

The India Fed model is `eyg_raw = E/P − Y10`. Asness (2003, *Fight the Fed Model*) shows the spread describes investor **inflation illusion** — comparing a real yield (E/P) to a nominal one (Y10) — and that raw E/P forecasts long-horizon returns *better* than the spread.

India makes the objection worse. The 10-year nominal yield fell from ~12% (1996) to 6.85% (Aug 2026) almost entirely on disinflation, so `eyg_raw` is dominated by the inflation trend. A raw-EYG percentile would have shouted "cheap" through the entire high-inflation 1990s–2000s and "expensive" now — a statement about the RBI, not about equities.

**Design decision.** Compute `eyg_real = E/P − (Y10 − π_exp)`, with `π_exp` = 5-year-ahead expected CPI **consumed from the macro layer, never rebuilt here** (MVP proxy: 5y trailing CPI mean clipped to the RBI 4%±2% band; v2 blends the RBI household inflation-expectations survey). Then:

- `eyg_real` enters the composite at weight **0.15** — deliberately low, per Asness's finding that spreads underperform raw yields as forecasters.
- `eyg_raw` is carried as a **diagnostic only**, never in the composite, because the owner will ask for it.
- The correct home for the equity-versus-bond comparison is the **ERP of §5**, where it is an ex-ante risk premium — which is what it actually is — not a timing signal.
- **Deferred (v2):** Asness's own remedy, `E/P_t = a + b·π_exp_t + c·σ²⁰ʸ_equity + d·σ²⁰ʸ_bond + ε_t`, one-sided from 1999, using `z(ε_t)`.

Today: E/P 4.33%, `Y10` 6.85%, `π_exp` 4.60% ⇒ real `Y10` 2.25% ⇒ **`eyg_real` = +2.08pp**, essentially at its own median. *On a real-rate basis Indian equity is not expensive.* All of this layer's expensiveness comes from the profit share and mcap/GDP. That disagreement is real, is logged, and is why the composite reads +0.79 rather than +1.5.

### 3.4 `cape_gdp`, and the identity that motivates it

A Shiller CAPE on India's own EPS history fails three ways: consistent index EPS only from 1999; the 2021 splice; and India's high real earnings trend (~8–11%/yr, 2003–2026), which puts a 10-year backward *average* of real EPS ~30–35% below current normal earnings, mechanically inflating the ratio by ~1.5× and destroying comparability. The IIM-A resource (`capeindia.iima.ac.in`) partly solves this by publishing 5y and 7y windows alongside 10y; use the **7-year** window as primary, since India's earnings cycle is shorter than the US 10-year convention and a 10-year window burns too much of a 27-year sample.

Independently, normalise price by **GDP-anchored** normal earnings:

```
phi_t       = aggregate listed PAT (ttm) / nominal GDP (ttm)                 # the profit share
coverage_t  = aggregate listed SALES (ttm) / NGDP (ttm)                      # structural; DO NOT revert
margin_t    = phi_t / coverage_t                                             # coverage-free; DO revert
phi_bar_t   = coverage_t * margin_bar_10y_t                                  # judgement-free normal
cape_gdp_t  = mcap_gdp_t / phi_bar_t
```

**Note the identity: `mcap_gdp ≡ PE_market × φ`, hence `cape_gdp = mcap_gdp / φ_bar`.** Market-cap-to-GDP and CAPE are the same statistic once divided by the profit share. This unifies §3.2 and §3.4 and puts the entire informational burden on §4 — measuring the profit share and deciding how much is permanent. That is where the burden belongs.

**Critical: `cape_gdp` uses `φ_bar` (mechanical, judgement-free), never `φ*(f)`.** The structural fraction `f` enters the *expected-return growth term only* (§5). Using `φ*(f)` in the z-score as well would (a) make the historical series depend on a judgement that did not exist historically, and (b) double-count `f`. This is the single easiest error to make in this layer and it is prohibited by a CI assertion.

Today: `φ = 5.27%` (from `MktCap_500/PE_500/NGDP`), `coverage = 62.0%`, `margin = 8.50%`, `margin_bar_10y = 6.50%` ⇒ `φ_bar = 4.03%` ⇒ **`cape_gdp` = 1.321/0.0403 = 32.8** against a trailing P/E of 23.1. GDP normalisation says the market is **~42% more expensive than trailing P/E implies**, because trailing earnings are cyclically high. With trend 23.5 and sd 0.28 in logs, **z = +1.23**.

*Cheap MVP shortcut worth naming:* `φ` needs **no per-name financials**. `aggregate PAT = MktCap_index / PE_index`, both published daily by NSE. This is what makes the earnings module MVP-feasible inside the time budget.

### 3.5 The composite and its bands

```
V_z = 0.30*z(cape_gdp) + 0.25*z(cape7_iima) + 0.20*z(pb_500)
    - 0.15*z(eyg_real)  - 0.10*z(sy_500)
# sign: V_z > 0 == EXPENSIVE.   Exposed as equity_longrun_valuation_z = -V_z.
# Robustness: if any component is stale > 90d, use the MEDIAN of fresh z's, not the weighted mean.
# Require >= 3 of 5 fresh, else emit contribution 0 and raise.
```

Weights are **set from reasoning, then frozen in git** — tier B forbids fitting. Rationale: `cape_gdp` highest, the only measure immune to the earnings-collapse artifact; `cape7_iima` next, an independent free construction that cross-checks it; `pb_500` third because book value does not collapse in recession, making it the most reliable tail measure; `eyg_real` lowest of the price measures per Asness.

| Band | `V_z` | Percentile | Label |
|---|---|---|---|
| 1 | ≤ −1.65 | ≤ 5 | Deep value |
| 2 | −1.65 … −1.05 | 5–15 | Cheap |
| 3 | −1.05 … −0.52 | 15–30 | Mildly cheap |
| 4 | −0.52 … +0.52 | 30–70 | Normal |
| 5 | +0.52 … +1.05 | 70–85 | Expensive |
| 6 | +1.05 … +1.65 | 85–95 | Very expensive |
| 7 | ≥ +1.65 | ≥ 95 | Extreme |

**Hysteresis:** a band change requires crossing the boundary by ≥5 percentile points and holding at two consecutive quarter-ends. `smooth_window_months: 24`, `min_dwell_months: 12`.

**Live reading, 2026-08-28:** `V_z = 0.30(1.23) + 0.25(1.00) + 0.20(0.80) − 0.15(0.10) − 0.10(−0.28) = +0.79` ⇒ percentile ≈ **78** ⇒ **Band 5, "Expensive."**

---

## 4. The earnings cycle

### 4.1 Indicators

| id | Definition | Source | Freq | India prior range |
|---|---|---|---|---|
| `phi` | listed PAT ttm / NGDP ttm — **exposed as `profit_share_gdp_z`** | `NSE_IDXMCAP`+`NSE_PEPB`+`NGDP` | Q | 1.8% (FY20) to **5.3% (FY26, record)** |
| `margin_agg` | aggregate PAT / sales, **non-financials only**, constant-tax-rate basis (§4.3) | `RBI_CORP` | Q | 4.0% (FY20) to 9.0% (FY08, FY25-26) |
| `coverage` | listed sales ttm / NGDP ttm | `RBI_CORP`+`NGDP` | Q | structural drift **+0.5 to +0.8 %/yr in logs [verify]** |
| `eps_gap` | `log(real EPS_ttm) − trend(t)`, one-sided expanding OLS, min 40q | `NSE_PEPB`+`CPI` | Q | −35% (FY20) to +25% (FY08) |
| `roe_agg` | aggregate PAT / opening net worth | `FIL_BS` (deferred) | H | 12% (FY20) to 25% (FY08) **[verify]** |
| `sales_excess` | aggregate nominal sales YoY − nominal GDP YoY | `RBI_CORP`+`NGDP` | Q | −12pp to +14pp |
| `eps_surprise_breadth` | §4.4 — free proxy for the revision cycle | `FIL_PL` (deferred) | Q | −1 to +1 |

Prior on the Nifty-500 profit share by year, to be rebuilt from our own series rather than trusted from broker charts: FY17 2.9, FY18 2.8, FY19 2.9, FY20 ~2.0, FY21 2.7, FY22 4.0, FY23 4.1, FY24 4.8, FY25 4.7, FY26 **5.3** ⇒ 10-year mean **≈3.6%** **[verify]**.

**Mean-reversion half-lives — estimate, do not assume.** For each series fit `Δx_t = α + β(x_{t−1} − x̄_{t−1}) + ε_t` on quarterly data and report `half_life = −ln2/ln(1+β)` **with its standard error and a bootstrap CI**; the CI, not the point estimate, goes into the CMA sensitivity table. Priors: `margin_agg` 10–14q; `roe_agg` 8–12q (Nissim & Penman 2001 find US profitability half-lives of 2–3 years); `eps_gap` 7–10q; `phi` 14–20q. All are far shorter than the ~84-month valuation half-life. **Earnings revert faster than multiples** — which is exactly why a valuation signal built on trailing earnings is unstable and one built on GDP-normalised earnings is not.

### 4.2 Detrending for listing penetration

`phi = coverage × margin`. Mean-revert `margin`; extrapolate `coverage` on its fitted log-linear drift. Reverting `phi` wholesale — what every broker note does — double-counts formalisation as cyclical excess and makes the model permanently too bearish.

### 4.3 Structural upgrade versus cyclical peak — the hardest judgement, made into a number

A four-test discriminator, each scored structural (1) or cyclical (0). All inputs free.

| Test | Structural if | Cyclical if | Data |
|---|---|---|---|
| **T1 Decomposition** | Margin gain sits in gross margin, product mix or opex leverage and has persisted >8 quarters | Gain sits in input-cost deflation, other income, or falling credit costs/provisions | `RBI_CORP` line items; `FIL_PL` for detail |
| **T2 Breadth** | Present in >60% of sectors **and** >55% of names | Concentrated in ≤2 sectors (typically metals, energy, bank provisioning) | own aggregates |
| **T3 Reinvestment** | Asset turns flat/up **and** capex/sales rising — capacity added into demand | Asset turns rising **and** capex/sales falling — sweating capacity, the late-cycle signature | `FIL_BS` (deferred) |
| **T4 Macro anchor** | Matched by a structural fall in the wage or interest share of GVA | Matched by a commodity terms-of-trade move or a one-off tax change | MOSPI NAS; RBI interest coverage |

```
S = number of tests scoring structural                # 0..4
f = clip((S - 1) / 3, 0, 1)                           # S<=1 -> 0 ;  S=4 -> 1
margin_star = f * margin_current + (1 - f) * margin_bar_10y
phi_star_T  = coverage_extrapolated_T * margin_star
```

**Two rules that stop this being hand-waving.**

1. **Statutory tax changes are level shifts, not cycles.** Recompute all margins on a constant effective tax rate: `PAT_adj = PBT × (1 − τ_ref)`, `τ_ref = 25.17%` (India's post-Sept-2019 concessional regime). The Sept-2019 cut from ~30% to 22% raised PAT ~11% permanently and once. On a raw series it reappears every year as "margin expansion"; on the adjusted series it appears once, as a logged level break, and never again.
2. **The credit-cost cycle belongs to the credit layer and must be netted out here.** System GNPA fell from 11.2% (FY18) to ~2.3% (FY25) — a very large, very cyclical contribution to financial-sector PAT. Financials are excluded from `margin_agg` for exactly this reason (which `RBI_CORP` does for us: it covers non-government **non-financial** companies), and `phi_financials` is flagged separately and residualised against the credit layer's `s_credit` with a declared `beta_prior = 0.55`.

**Live application, 2026-08-28.** T1: much of the FY21–26 margin expansion is falling bank credit costs plus the 2019 tax cut — **cyclical** (the tax cut is now netted out). T2: broad, with mid-caps at a 15-year-high contribution — **structural**. T3: capex/sales rising on the public-capex push — **structural**. T4: interest share of GVA fell structurally on corporate deleveraging, but the commodity terms-of-trade also helped — **cyclical**, marginal. **S = 2 ⇒ f = 0.33.** With `margin_current = 8.50%`, `margin_bar_10y = 6.50%`: `margin_star = 7.16%`; `coverage` extrapolated 7y at +0.65%/yr ⇒ 0.649; **`phi_star_T` = 4.65%** against `phi` = 5.27%.

**This is the layer's central live call.** It is exposed as `structural_fraction_f` with the four test scores attached, and it is the only parameter Stage 2 may move (±0.25, two signatures, logged, with a stated falsification condition).

### 4.4 Earnings revisions: the cut signal and its free replacement

Analyst estimates and revision breadth do not exist free for India. The registry's D5 rule requires a named proxy with a one-tier evidence downgrade. Build the surprise against a **seasonal random walk with drift** (Foster 1977; Foster, Olsen & Shevlin 1984), needing only our own scraped results:

```
E_hat[i,q] = E[i,q-4] + delta_i,  delta_i = mean(E[i,k] - E[i,k-4]) over the last 8 quarters
SUE[i,q]   = (E[i,q] - E_hat[i,q]) / sd(E[i,k] - E_hat[i,k]) over the last 8 quarters
eps_surprise_breadth_t = 2 * frac(universe with SUE > 0) - 1        # in [-1, +1]
```

Also emit `realised_eps_breadth` (fraction whose trailing-4q EPS exceeds the value four quarters earlier) so the registry entry resolves.

**State the loss plainly.** This is entirely backward-looking. It tells you the earnings cycle turned 45–60 days *after* the quarter closed. It has none of the forward content of estimate revisions, which is the whole point of a revision signal. It is therefore **tier B→C, one-sided, with near-zero allocation budget**; its real uses are as the T2 breadth input and as a bottom-up PEAD input. **Deferred to v2** — per-name quarterly parsing is the most expensive item in the layer.

---

## 5. Predictive power, and the exact horizon this layer may act over

The evidence, stated honestly:

| Horizon | US/DM evidence | India | This layer's authority |
|---|---|---|---|
| 1 month | R² ≈ 0 | none | **None** |
| 12 months | in-sample R² ~2–6% for D/P and E/P (Fama–French 1988); **out-of-sample R² negative** (Goyal & Welch 2008) | not estimable | **None** |
| 3 years | in-sample R² ~10–20% | ~9 independent windows | Partial — via slow drift only |
| 7–10 years | in-sample R² ~30–45% (Campbell & Shiller 1988, 1998) | **<3 independent windows** | **Primary** |

Four qualifications that must not be dropped:

1. **Goyal & Welch (2008)** is the load-bearing negative result: essentially every classical valuation predictor fails to beat the trailing historical mean out of sample. Cochrane (2008, 2011) rebuts on economic grounds — predictability must exist somewhere, and it shows up in returns rather than dividend growth — but the practical implication survives: a valuation signal deserves a *small, slow* position, not a market-timing rule.
2. **Boudoukh, Richardson & Whitelaw (2008)** show the rise of R² with horizon is largely mechanical under the null, because overlapping windows share data. A high 7-year R² is not evidence.
3. **Stambaugh (1999)** bias: the regressor is highly persistent, so the slope is biased upward and t-statistics overstated. **Valkanov (2003)**: long-horizon t-statistics do not converge; use rescaled `t/√T` statistics or don't report significance at all.
4. **India has no usable sample.** 1999–2026 is ~27 years, i.e. **fewer than 3 independent 7-year windows** and **<3 independent 10-year windows**. Any India-fitted long-horizon coefficient is a curve fit. The one relevant free academic resource is the IIM-A CAPE India work (IIMA working paper, 2022, on CAPE and Indian market characteristics) **[verify authors/title]**.

**Design consequences, binding:**

- The predictive coefficient is **imported and frozen**, not fitted. Working value: a 1σ increase in `V_z` reduces the subsequent 7-year annualised return by **1.8pp/yr** (cross-country panel prior; consistent with 10.8% central and the §5.4 sensitivity table). Frozen in `config/valuation.yaml` at inception, changed only under two-signature control.
- **Validation is sign-agreement only**, not Sharpe: across the analog episodes (Dec-2007 peak, Mar-2009 trough, Nov-2010 peak, Aug-2013 trough, Jan-2018 smid peak, Mar-2020 trough, Dec-2024 smid peak), did `V_z` have the right sign 12–36 months ahead of the subsequent 5-year return being above or below the sample median? Report the count, not a t-statistic.
- **The exact horizon over which this signal may act is 24–60 months.** The rate limiter enforces it mechanically (§8). This layer has **zero tactical authority** and must never be the reason for a cash call. The cash call belongs to the risk/drawdown engine, informed by the credit and macro layers.

---

## 6. The expected-return model — the layer's most important output

### 6.1 Indian equity, Grinold–Kroner

```
E[R]_H = (DY - dS) + i + g + m_phi + m_PE

DY    dividend yield, 12m trailing, index-level
dS    net share issuance rate (positive = dilution), from SHOUT; MVP proxy = 3y mean
i     expected CPI over H, consumed from the macro layer
g     expected real GDP growth over H (IMF WEO / RBI potential; free)
m_phi = (1/H) * [ dlog(coverage) + lambda_phi * ln(margin_star / margin_t) ]
        lambda_phi = 1 - 0.5^(H / HL_phi),   HL_phi = 54 months
m_PE  = (1/H) * lambda_PE * ln(PE_trend / PE_t)
        lambda_PE  = 1 - 0.5^(H / HL_PE),    HL_PE  = 84 months
```

**Internal-consistency constraint (mandatory).** Because `mcap_gdp ≡ PE_market × φ`, the three trends must satisfy `trend(log mcap_gdp) ≡ trend(log PE) + trend(log φ)`. Fit `trend(log mcap_gdp)` and `trend(log φ)` directly — both from cheap, robust series — and **derive** `trend(log PE)` as the residual. This removes a free parameter and guarantees that the mcap/GDP route and the PE×φ route give the same answer. A CI test asserts agreement within 0.15pp/yr.

**H = 7 years. India, 2026-08-28:**

| Term | Value | Derivation |
|---|---|---|
| `DY` | **+1.05%** | Nifty 500 dividend yield |
| `−dS` | **−1.30%** | India is a net issuer; shareholder yield = −0.26% **[verify from `SHOUT`]** |
| `i` | **+4.60%** | 7y expected CPI, macro layer |
| `g` | **+6.30%** | real GDP growth, medium-term; band 5.3–7.3% |
| `m_phi` | **−0.96%** | `(1/7)[ln(0.649/0.620) + 0.660·ln(7.16/8.50)]`, `λ_φ = 0.660` |
| `m_PE` | **+1.11%** | `PE_t = 1.321/0.0527 = 25.1`; `PE_trend = 1.18/0.0403 = 29.3`; `λ_PE = 0.50` |
| **E[R] nominal** | **+10.80%** | |
| **E[R] real** | **+5.93%** | deflating by `i` |
| **`erp_ante`** | **+3.95pp** | over `Y10` = 6.85% |

The positive `m_PE` deserves explanation, because it looks wrong. It is the §3.4 identity in action: today's trailing P/E of 25.1 is *below* its consistency-implied trend of 29.3 **because trailing earnings are cyclically inflated**. The market is expensive on `mcap_gdp` and on `cape_gdp`, and that expensiveness is carried by `φ` (5.27% vs a 4.03% normal), not by the multiple. Reverting `φ` (a −0.96% drag) and reverting the multiple (a +1.11% tailwind) are two sides of one −0.11%/yr net `mcap_gdp` reversion. Reverting `cape_gdp` *and* `φ` — the naive build — would double-count `φ` and understate the equity CMA by roughly 2pp/yr. This is the error the §3.4 prohibition exists to prevent.

**Cross-checks.** (a) The `mcap_gdp` route with a single `λ = 0.50` gives **10.5%**. (b) A Damodaran-style build-up — mature-market ERP ~4.2% (2026) plus an India country risk premium of ~3.4% (Baa3 default spread × 1.55 equity multiplier), in USD, converted at ~3.0%/yr rupee drift — gives roughly **10–11%** in INR **[verify India CRP from the free workbook]**. Three independent routes within 0.8pp is as much agreement as this exercise ever gets.

### 6.2 Sensitivity — where the number actually comes from

| Parameter | Low | Central | High | E[R] low | E[R] high |
|---|---|---|---|---|---|
| `f` structural fraction | 0.00 | 0.33 | 1.00 | 9.9% | 12.4% |
| `g` real GDP | 5.3% | 6.3% | 7.3% | 9.8% | 11.8% |
| `i` expected CPI | 3.6% | 4.6% | 5.6% | 9.8% | 11.8% |
| `λ_PE` (multiple reversion) | 0.00 | 0.50 | 1.00 | 9.7% | 11.9% |
| `dS` dilution | 2.0% | 1.3% | 0.8% | 10.1% | 11.3% |
| `trend(mcap_gdp)` | 1.10 | 1.18 | 1.28 | 9.6% | 12.0% |

`dE[R]/df ≈ 2.5pp` per unit `f`, so the ±0.25 Stage-2 band is worth ±0.63pp. Combining independent terms, the honest **90% band is ≈7.5% to 14.0% nominal**. Report the band, never the point estimate alone; the optimizer must consume `mu` *and* `confidence_band`.

### 6.3 Mid/small cap

```
E[R]_smid = E[R]_large + g_premium - dS_extra - (1/H)*lambda_smid*z_smid*sd_smid
```

With `z(SMID_VAL) = +1.71`, `sd_smid = 0.22` in logs, `HL_smid = 36m` ⇒ `λ = 0.802`, drag = **−4.32%/yr**; `g_premium = +2.0%`, `dS_extra = −1.0%`:

**E[R]_smid ≈ 7.5% nominal, 3.3pp below large cap, at 24% volatility versus 17%.**

This is a strategic statement about the *segment beta*, not about cross-sectional alpha within the segment — those are different objects and the optimizer must not conflate them. But it is a direct, uncomfortable input to a NIFTY 750 mandate: the CMA says the tail the aggressive book reaches into currently offers the worst 7-year risk-adjusted beta in the opportunity set.

### 6.4 Gold

Gold has no cash flow; the decomposition is inflation plus real-price drift plus currency.

```
E[R]_gold_INR = US_CPI_exp + (1/H)*lambda_g*ln(real_gold_anchor / real_gold_t) + INR_depreciation
```

At ~$4,500/oz (Aug-26) and US CPI ≈ 335, the gold-to-CPI ratio is ≈**13.4** — an all-time real high, roughly 60% above the 2011 and 2024 peaks (~8.3–8.4) and far above the floating-era mean. Erb & Harvey (2013, *The Golden Dilemma*; 2024 update) show the real gold price mean-reverts and that at elevated real prices subsequent real returns have been strongly negative; their 2024 update put the forward real return at about **−4%/yr on reversion, −12%/yr on overshoot**.

| Anchor | `real_gold_anchor` | `HL` | drag/yr | E[R]_gold_INR |
|---|---|---|---|---|
| Floating-era mean (1975–) | 5.5 | 180m | −3.5% | **+2.0%** |
| Modern mean (2005–) | 7.5 | 180m | −2.3% | **+3.2%** |
| Structural break, no reversion | — | ∞ | 0.0% | **+5.5%** |

Using `US_CPI_exp = 2.5%` and `INR_depreciation = 3.0%` (relative-PPP: India CPI − US CPI ≈ 2.1%, realised ≈3.0–3.5%; consumed from the external layer, never built here). **Central: shrink 50% toward the no-reversion case, giving `E[R]_gold_INR ≈ 4.0% nominal, 16% vol`** — because the central-bank reserve-diversification argument is a genuine structural candidate, not a rationalisation, and Erb & Harvey themselves frame it as an unresolved dilemma.

**Interface warning.** This is an *unconditional* expected return. The long-wave layer's case for a 5% gold floor rests on gold's *conditional* payoff in a monetary-disorder state, which a low unconditional mean does not defeat. The optimizer must be told which object it is consuming; a mean-variance optimizer fed 4.0% will hold the minimum gold, which is the intended behaviour only if the tail scenario is entered separately.

### 6.5 Debt and cash

The 10% return is **frozen** and used as given. Two variants are published; the optimizer must run both.

| | `debt_frozen` (mandated) | `debt_stressed` (robustness) |
|---|---|---|
| E[R] | 10.0% | 8.6% (10% gross coupon − ~1.4% expected credit loss for an AA/A short-duration book) |
| Vol | 4.0% | 6.5% |
| Worst DD | 6.0% | 14.0% |
| Basis | owner-frozen | IL&FS (Sep-2018), DHFL (2019), and the April-2020 wind-up of six Franklin Templeton India debt schemes — several Indian credit-risk funds fell 8–15% in weeks. All free to verify. |

Cash: 91-day T-bill, **6.0%**, vol 1.0%.

### 6.6 The CMA vector

**Expected returns and volatility, H = 7y, nominal INR:**

| Asset | μ | σ | 90% band on μ | Sharpe vs cash |
|---|---|---|---|---|
| `equity_large` (Nifty 100) | 10.8% | 17% | 7.5–14.0% | **0.28** |
| `equity_smid` (Mid150+Small250) | 7.5% | 24% | 3.5–12.0% | **0.06** |
| `gold` (INR) | 4.0% | 16% | 2.0–5.5% | **−0.13** |
| `debt` (frozen) | 10.0% | 4% | frozen | **1.00** |
| `debt` (stressed) | 8.6% | 6.5% | — | 0.40 |
| `cash` | 6.0% | 1% | — | — |

**Correlation matrices, regime-conditioned.** Regime cells come from the macro layer's growth × inflation posterior; this layer never estimates the regime.

Unconditional (2005–2026 monthly INR, prior to be recomputed):

```
          EqL    EqS   Gold   Debt   Cash
EqL      1.00   0.88   0.05  -0.10   0.00
EqS      0.88   1.00   0.00  -0.12   0.00
Gold     0.05   0.00   1.00   0.15   0.00
Debt    -0.10  -0.12   0.15   1.00   0.20
Cash     0.00   0.00   0.00   0.20   1.00
```

Conditional cells (equity–debt honours the frozen −0.2 / +0.4 flip exactly at the poles):

| Cell | EqL–Debt | EqL–Gold | EqL–EqS | Gold–Debt |
|---|---|---|---|---|
| Disinflation + growth up | **−0.20** | −0.10 | 0.85 | 0.20 |
| Disinflation + growth down | −0.35 | −0.05 | 0.90 | 0.30 |
| Inflation shock + growth up | +0.25 | +0.15 | 0.88 | 0.05 |
| Inflation shock + growth down (stagflation) | **+0.40** | +0.30 | 0.92 | −0.05 |
| **Crisis / funding-stress overlay** | +0.35 | +0.25 | **0.97** | +0.20 |

The crisis row is an **overlay, not a fifth cell**: when the risk engine's funding-stress trigger fires, substitute this row and multiply every volatility by **1.8**. It matters more than the rest of the table, because it says an AA/A credit sleeve loses its diversification in exactly the state the drawdown objective is written for.

```
corr_t   = sum over cells of p_cell * corr_cell            # p from the macro layer
corr_mix = 0.5 * corr_t + 0.5 * corr_sample_120m
corr_out = ledoit_wolf_shrink(corr_mix, target=equicorrelation)
corr_out = psd_project(corr_out, eig_floor=1e-6)           # clip and renormalise diagonal
```

---

## 7. Cross-sectional valuation dispersion — the value spread

```
Universe: book-specific investable set.  Sector-neutralise within 11 sectors.
BY[i]     = book / price            # book yield, not P/B: handles negative book cleanly
Rank BY within sector; form quintiles.
VS_log_t  = ln(median BY of Q1) - ln(median BY of Q5)
z(VS)     = expanding-window z, min 10y burn-in
Also emit VS by sector and a P/S-based variant (robust to loss-makers).
```

India history to be constructed from `NSE_BHAV` + `FIL_BS`; expect peaks around 2000, Mar-2020 and mid-2018 (smid distress), troughs around 2007 and 2017 **[verify — this series does not exist free and must be built]**.

Evidence: Asness, Friedman, Krail & Liew (2000, *Style Timing: Value versus Growth*) and Cohen, Polk & Vuolteenaho (2003, *The Value Spread*) find the spread predicts value-minus-growth returns. Asness (2016, *The Siren Song of Factor Timing*) warns that in practice the effect is weak once you control for the value factor's own valuation, and that factor timing on spreads is much harder than it appears.

**Ownership decision: this layer exposes `value_spread_z` and takes zero budget for it.** The factor library owns the value factor's weight. Recommended mapping for them to accept or reject: `z(VS) > +1.0` ⇒ raise value's weight by up to +25% relative; `z(VS) < −1.0` ⇒ cut by up to 25%; linear in between; no change inside ±0.5. **Deferred to v2** — it requires the per-name financials archive.

---

## 8. Size-segment valuation and the mapping to weights

### 8.1 The smid premium

```
PB_smid = cap-weighted P/B of (Nifty Midcap 150 + Nifty Smallcap 250)     # NSE, daily, free
PB_large = P/B of Nifty 100
SMID_VAL = ln(PB_smid / PB_large)
```

**P/B, not P/E**, because smallcap index P/E is destroyed by loss-making constituents and by the Break-2 earnings-collapse artifact; book value does neither. Emit a median-name P/E variant as a cross-check only.

India prior: `SMID_VAL` has ranged roughly **−0.60 (Mar-2020, ~45% discount)** to **+0.30 (Jan-2018 and Dec-2024, ~35% premium)**, median ≈ **−0.05**, sd ≈ **0.22**, half-life ≈ **30–40 months** **[verify — recompute; this is the single cheapest high-value series in the layer, one NSE endpoint]**. Aug-2026: `PB_smid ≈ 4.3`, `PB_large ≈ 3.1` ⇒ `SMID_VAL = +0.327` ⇒ **z = +1.71**.

### 8.2 The mapping, with explicit numbers

Neutral policy portfolio (set by the taxonomy layer): **equity 60% · gold 12% · debt 28%.** All figures are deviations in pp of NAV, applied to the composite `V_z`, not to any single measure.

| Band | `V_z` | pct | Δequity agg | Δequity mod | Δgold | Δdebt | Δsmid share of equity |
|---|---|---|---|---|---|---|---|
| 1 Deep value | ≤ −1.65 | ≤5 | **+8.0** | +6.0 | −1.0 | −7.0 | +5.0 |
| 2 Cheap | −1.65…−1.05 | 5–15 | +5.5 | +4.0 | −0.5 | −5.0 | +3.0 |
| 3 Mildly cheap | −1.05…−0.52 | 15–30 | +2.5 | +2.0 | 0.0 | −2.5 | +1.5 |
| 4 Normal | −0.52…+0.52 | 30–70 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 5 Expensive | +0.52…+1.05 | 70–85 | **−3.0** | −2.0 | +0.5 | +2.5 | −2.0 |
| 6 Very expensive | +1.05…+1.65 | 85–95 | −6.0 | −4.5 | +1.5 | +4.5 | −3.5 |
| 7 Extreme | ≥ +1.65 | ≥95 | **−9.0** | −7.0 | +2.5 | +6.5 | −5.0 |

Single-measure reference table (diagnostic; the composite governs in production):

| `mcap_gdp_detr_z` | raw ≈ (trend 118%) | pct | implied equity |
|---|---|---|---|
| ≤ −1.65 | ≤ 85% | ≤5 | 68% |
| −1.05 | ~98% | 15 | 65.5% |
| −0.52 | ~110% | 30 | 62.5% |
| 0.00 | 118% | 50 | 60% |
| **+0.55** | **132% (today)** | **71** | **57%** |
| +1.05 | ~144% | 85 | 54% |
| +1.65 | ~166% | 95 | 51% |

`eyg_real` reference: p10 −1.0pp ⇒ equity 54%; median +2.0pp ⇒ 60%; p90 +4.5pp ⇒ 66%. Today +2.08pp ⇒ 60%. The two single measures disagree (57% vs 60%); the composite resolves to **57%** and the disagreement is logged.

**Rate limits.** Per the ladder's derivation `max_delta = 2b / max(2·tau_half, min_traverse_by_tier)`:

| Registry entry | Bucket | `tau_half` | budget (agg) | pp/month |
|---|---|---|---|---|
| `equity_valuation_reversion` | B1 | 84m | ±5.0 | 0.060 |
| `corporate_profit_share_cycle` | B2 | 48m | ±4.0 (post-residualisation) | 0.083 |
| **Combined** | | | **−9 / +8** | **0.143** |

At 0.143 pp/month a full 9pp traverse takes **63 months**. That is uncomfortably slow and is stated as a risk, not hidden. The proposed resolution is a **one-sided extreme override**: when `V_z ≥ +1.65` (band 7) for two consecutive quarter-ends, `max_delta` rises to **0.50 pp/month in the de-risking direction only**, consistent with the taxonomy's asymmetric-authority rule. Risk-adding moves are never accelerated. Proposed as new registry entry `valuation_extreme_trigger` (B2, tier B, one-sided).

**Today's output (aggressive):** Band 5 ⇒ equity **−3.0pp**, gold **+0.5pp**, debt **+2.5pp**, smid share of equity **−2.0pp** (reinforced by `z(SMID_VAL) = +1.71` under `smid_valuation_premium`, which is residualised against the credit layer's `L03_SIZE_TILT` before it lands). Target equity ≈ **57%**.

---

## 9. MVP versus deferred

Honest total ≈ **30 engineer-days**. MVP target was 13; the achievable MVP is **15**.

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Valuation ingester + 2021 splice + rebase handling | NSE PE/PB/DY, index mcap, MCAP_TOT, MOSPI NGDP, RBI yields, vintage manifest | 2.5 | ✅ |
| 2 | `mcap_gdp` trend residual | one-sided expanding trend + z | 1.0 | ✅ |
| 3 | `eyg_real` consuming `π_exp` | plus `eyg_raw` diagnostic | 0.5 | ✅ |
| 4 | `φ` from `MktCap/PE`, coverage/margin split, `cape_gdp` | the §3.4 block, incl. the `φ_bar`-only CI assertion | 2.0 | ✅ |
| 5 | `RBI_CORP` ingester | quarterly aggregate sales, OPM, NPM, interest coverage | 2.0 | ✅ |
| 6 | `CAPE_IIMA` ingester | 7y CAPE, Nifty 500 | 0.5 | ✅ |
| 7 | Composite `V_z`, bands, hysteresis, mapping table | `VAL_STATE`, `VAL_TILT` | 1.5 | ✅ |
| 8 | Discriminator **T2 + T4 only**, `f` | `structural_fraction_f` with test scores | 1.0 | ✅ |
| 9 | Grinold–Kroner CMA engine + consistency constraint | equity L/S, gold, debt (both variants), cash; full decomposition and bands | 2.0 | ✅ |
| 10 | Regime-conditioned correlation, shrinkage, PSD | `CMA.corr` | 1.5 | ✅ |
| 11 | `SMID_VAL` from NSE segment P/B | one endpoint, high value | 0.5 | ✅ |
| — | **MVP subtotal** | | **15.0** | |
| 12 | Half-life harness + analog sign-agreement replay | bootstrap CIs feeding the sensitivity table | 1.5 | ⬜ |
| 13 | Discriminator T1 + T3 (needs `FIL_PL`/`FIL_BS`) | full four-test `f` | 2.0 | ⬜ |
| 14 | Value spread | `VAL_XS.value_spread_z`, sector-neutral | 2.5 | ⬜ |
| 15 | `eps_surprise_breadth` (seasonal random walk) | per-name quarterly parsing | 3.0 | ⬜ |
| 16 | Bottom-up rebuilt index EPS ⇒ own `cape_trend`, kills Break 1 | replaces the splice with a real series | 3.0 | ⬜ |
| 17 | Asness residual `E/P` model | `z(ε_t)` | 1.5 | ⬜ |
| 18 | Fixed-universe `mcap_gdp_fx` | needs reconstructed membership | 1.5 | ⬜ |

**If MVP must fit 13 days**, cut #11 and #10's shrinkage machinery (use the four fixed regime matrices without sample blending): 13.0 days. Do not cut #4 or #9 — they are the layer.

---

## 10. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| Free-data pipeline | `pit_store(series, asof)` | Bitemporal; final-vintage reads raise. All series in §2 |
| Cycle taxonomy | registry entries, `influence_budget()`, `orthogonalize()`, `resolve()`, rate limiter | Output must validate; unregistered ids rejected |
| Macro regime | `MACRO_INFL.pi_exp_5y` (or `I_level_pct`), `regime_probs`, `regime_label` | Inflation and regime are **consumed, never rebuilt** |
| Credit cycle | `s_credit`, `L03_STATE.phase_posterior` | Nets the credit-cost cycle out of financial-sector margins (`beta_prior = 0.55`) |
| External / currency | `usdinr_state`, long-run INR drift, `commodity_supercycle_state` | Gold CMA's currency term and the T4 terms-of-trade test |
| Long wave | `LW_RISK_INPUTS.debt_corr_state`, `disaster_prob_annual` | Crisis-overlay row and tail scenario |
| Backtest validation | `sign_agreement_valuation` | **Sets this layer's budget** via a pre-registered rule |

**Exposes**

```python
VAL_STATE = {V_z, V_percentile, band, band_label,
             components: {cape_gdp_z, cape7_iima_z, pb_z, eyg_real_z, sy_z},
             mcap_gdp, mcap_gdp_detr_z, eyg_raw, eyg_real, pe_500, pb_500, dy_500, sy_500,
             months_in_band, staleness_days, asof, vintage_id}

EARNINGS_STATE = {phi, phi_z, coverage, coverage_drift_pct_yr, margin_agg, margin_bar_10y,
                  margin_star, eps_gap, roe_agg, sales_excess, structural_fraction_f,
                  discriminator: {T1,T2,T3,T4}, half_lives: {series: (point, lo, hi)},
                  eps_surprise_breadth}

CMA = {horizon_years: 7,
       mu_nominal, mu_real, vol, confidence_band,
       corr_unconditional, corr_by_regime_cell, corr_crisis_overlay, vol_crisis_multiplier: 1.8,
       decomposition: {asset: {dy, issuance, inflation, real_growth, phi_reversion, pe_reversion}},
       debt_variant: {'frozen': {...}, 'stressed': {...}},
       asof, vintage_id}

VAL_TILT = {equity_pp, smid_pp, gold_pp, debt_pp,
            max_delta_pp_per_month: 0.143,
            extreme_override_pp_per_month: 0.50,     # de-risking direction ONLY
            book_scale: {aggressive: 1.00, moderate: 0.75}}

VAL_XS = {value_spread_log, value_spread_z, value_spread_by_sector,
          smid_val_log, smid_val_z}                  # recommendation only, zero own budget

VAL_METHOD = {normalise_valuation(series, asof) -> z}    # method export to the sector model

# Contracts already claimed by sibling specs and honoured verbatim:
equity_longrun_valuation_z = -V_z         # consumed by the long-wave layer
profit_share_gdp_z         = z(phi)       # consumed by the credit layer
```

**Ownership conflict to resolve:** the credit-cycle spec also publishes `DEBT_SLEEVE_RISK = {e_return, vol, worst_dd, corr_equity}`. Two publishers of one object is a bug. Recommendation: **this layer is the sole publisher of the CMA**, and consumes the credit layer's regime-conditional correlation state as an input to it.

---

## 11. Risks and constraint conflicts

1. **The frozen debt assumption breaks the optimizer.** 10% at 4% vol is a Sharpe of 1.00 — roughly 3.5× Indian equity's ex-ante Sharpe of 0.28, and higher than any liquid asset class has sustained anywhere over a long sample. A mean-variance optimizer fed this vector holds 70% debt at every rebalance, and the 70% cap stops being a risk limit and becomes the permanent solution. **Mitigation, not a fix:** publish `debt_stressed` (8.6% / 6.5% vol / 14% worst DD, grounded in IL&FS, DHFL and the April-2020 Franklin Templeton India wind-up) and require the optimizer to run both. If the two produce materially different portfolios, the frozen assumption is doing the work, not the model.
2. **The 35–60% / 30–40% CAGR aspirations cannot come from beta.** At a 10.8% large-cap CMA and 1.25× average gross, the asset-allocation layer contributes ~13.5% before costs. Reaching 35% net requires roughly **22pp/yr of cross-sectional alpha** on the equity sleeve, sustained. Long-run top-decile India long-only alpha is more like 5–8pp. This layer cannot close that gap and should not be asked to.
3. **Fewer than three independent long-horizon observations in India.** The predictive coefficient is imported and frozen, and cannot be validated in-sample. Sign-agreement replay across seven analog episodes is the only honest test available.
4. **The 2021 consolidated-earnings splice is a live data hazard**, verified at 40.1 → 32.7. Until step 16 is built, every pre-2021 percentile carries a measured but estimated `ratio_hat`.
5. **`f` is the largest unhedged judgement.** ±0.25 moves the 7-year equity CMA by ±0.63pp and the tilt by ~1pp. Four qualitative tests reduced to one number is a real epistemic compromise; it is exposed with its component scores so it can be argued with.
6. **The rate limiter may make this layer inert.** 63 months for a full traverse means the signal will rarely reach its stated extent, and a 3–6 month build cannot observe it working. The extreme override is proposed precisely because the base limiter is too slow to matter at the tails.
7. **The gold CMA is hostile to the gold sleeve.** At a gold/CPI ratio of ~13.4 the reversion drag is large, and even the shrunk central estimate (4.0% nominal INR) is below cash. This will fight the long-wave layer's 5% gold floor and the gold sleeve's tactical case. The reconciliation — unconditional mean versus conditional crisis payoff — must be made explicit in the optimizer, or gold will be sized wrongly in both directions.
8. **Denominator rebasing.** MOSPI's GDP rebase and CPI's 2024=100 rebase both sit under this layer's key ratios. A silent rebase is a silent regime break.
9. **Listing-penetration extrapolation is one-sided.** If formalisation stalls, `coverage_T` overstates future earnings and this layer is systematically too bullish. Cap the extrapolation at +0.8%/yr and re-fit annually.
10. **Goyal & Welch is not refuted, only survived.** Out-of-sample, valuation predictors fail. The only defence is that the position taken is small, slow and one-way-asymmetric at the extremes. If the tilt is ever widened beyond −9/+8pp, that defence is gone.
11. **Smid CMA versus mandate design.** The CMA says the NIFTY 750 tail currently offers the worst 7-year segment beta in the opportunity set. That is an argument about beta, not about the alpha the aggressive book is built to harvest — but it should be an explicit, argued decision rather than an accident.

---

## 12. References

1. Grinold, R. C. & Kroner, K. F. (2002). *The Equity Risk Premium.* Investment Insights, Barclays Global Investors. See also Grinold, Kroner & Siegel (2011), "A Supply Model of the Equity Premium," in *Rethinking the Equity Risk Premium*, CFA Institute Research Foundation.
2. Campbell, J. Y. & Shiller, R. J. (1988). "Stock Prices, Earnings, and Expected Dividends." *Journal of Finance* 43(3).
3. Campbell, J. Y. & Shiller, R. J. (1998). "Valuation Ratios and the Long-Run Stock Market Outlook." *Journal of Portfolio Management* 24(2).
4. Fama, E. F. & French, K. R. (1988). "Dividend Yields and Expected Stock Returns." *Journal of Financial Economics* 22(1).
5. Goyal, A. & Welch, I. (2008). "A Comprehensive Look at the Empirical Performance of Equity Premium Prediction." *Review of Financial Studies* 21(4).
6. Boudoukh, J., Richardson, M. & Whitelaw, R. (2008). "The Myth of Long-Horizon Predictability." *Review of Financial Studies* 21(4).
7. Stambaugh, R. F. (1999). "Predictive Regressions." *Journal of Financial Economics* 54(3).
8. Valkanov, R. (2003). "Long-horizon regressions: theoretical results and applications." *Journal of Financial Economics* 68(2).
9. Cochrane, J. H. (2008). "The Dog That Did Not Bark: A Defense of Return Predictability." *RFS* 21(4); and (2011) "Presidential Address: Discount Rates." *Journal of Finance* 66(4).
10. Asness, C. S. (2003). "Fight the Fed Model." *Journal of Portfolio Management* 30(1).
11. Asness, C. S., Ilmanen, A. & Maloney, T. (2017). "Market Timing: Sin a Little." *Journal of Investment Management* **[verify venue]**.
12. Asness, C. S. (2016). "The Siren Song of Factor Timing." *Journal of Portfolio Management* 42(5).
13. Asness, C. S., Friedman, J., Krail, R. & Liew, J. (2000). "Style Timing: Value versus Growth." *Journal of Portfolio Management* 26(3).
14. Cohen, R. B., Polk, C. & Vuolteenaho, T. (2003). "The Value Spread." *Journal of Finance* 58(2).
15. Erb, C. B. & Harvey, C. R. (2013). "The Golden Dilemma." *Financial Analysts Journal* 69(4); NBER WP 18706. And Erb & Harvey (2024), "Is There Still a Golden Dilemma?", SSRN.
16. Bernstein, W. J. & Arnott, R. D. (2003). "Earnings Growth: The Two Percent Dilution." *Financial Analysts Journal* 59(5).
17. Nissim, D. & Penman, S. H. (2001). "Ratio Analysis and Equity Valuation." *Review of Accounting Studies* 6.
18. Foster, G. (1977). "Quarterly Accounting Data: Time-Series Properties and Predictive-Ability Results." *The Accounting Review* 52(1). Foster, G., Olsen, C. & Shevlin, T. (1984). "Earnings Releases, Anomalies, and the Behavior of Security Returns." *The Accounting Review* 59(4).
19. Ledoit, O. & Wolf, M. (2004). "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices." *Journal of Multivariate Analysis* 88(2).
20. Damodaran, A. (2026). *Equity Risk Premiums: Determinants, Estimation and Implications — 2026 Edition.* SSRN. Free country ERP data at `pages.stern.nyu.edu/~adamodar`.
21. IIM Ahmedabad (2022). *Cyclically Adjusted PE Ratio (CAPE) and Stock Market Characteristics in India*, IIMA working paper; data resource at `capeindia.iima.ac.in` **[verify authors and title]**.
22. NSE India, *Price Earnings Ratio* methodology page — the April-2021 standalone-to-consolidated change; verified effect 40.1 (Mar-21) → 32.7 (Apr-21).
