# Layer 05 — Valuation Cycle and the Expected-Return Engine (3–15 years)

**Abstract.** This layer measures how expensive Indian equity is, how far corporate earnings sit above or below their sustainable path, and converts both into the capital-market-assumption (CMA) vector the Stage-3 optimizer consumes. It reaches four conclusions that matter more than its plumbing. **First**, market-cap-to-GDP and CAPE are the same statistic divided by the corporate profit share — so the profit-share cycle, not the price multiple, is where almost all the information lives, and India's profit share is at a record 5.2% of GDP (FY26, Nifty-500 basis). **Second**, on a Grinold–Kroner build with every term sourced free, the 7-year expected return on Indian equity is **≈7.9% nominal** (bear 5.2%, bull 10.5%), against a reverse-optimised equilibrium of 10.8% and a *frozen* debt assumption of 10%. That arithmetic says the owner's 35–60% CAGR aspiration cannot come from beta, and that an unshrunk optimizer will corner into the 70% debt cap. Both are stated as conflicts, not designed around. **Third**, India's free valuation history contains fewer than three independent 10-year observations, so the predictive coefficient cannot be estimated here; it is imported from a cross-country panel, frozen in git, and the layer is tested only for sign agreement across analog episodes — L01 tier B. **Fourth**, and consequently, this layer is given **±9pp down / +7pp up** of equity authority with a combined rate limit of **0.193 pp/month**, meaning a full traverse takes ~47 months. Valuation sets the strategic centre of gravity. It cannot and must not make the cash call; that is L03/L04/L18's job. The single largest engineering hazard is not the model but a data break: NSE switched index P/E from standalone to consolidated earnings on **1 April 2021**, moving the published Nifty P/E from ~40 to ~32 overnight. Every percentile that straddles that date is wrong until spliced.

---

## 1. Scope, and what this layer is not

**Owns.** The 3–15 year mean-reverting valuation state of Indian equity; the aggregate earnings/margin/ROE cycle and its structural-versus-cyclical decomposition; the forward expected-return vector and regime-conditioned covariance for equity (large and smid), gold and the debt sleeve; the cross-sectional value spread; and the size-segment valuation premium. In L01's registry it owns `equity_valuation_reversion` (B1, MVP) and `corporate_profit_share_cycle` (B2, MVP), and proposes two new entries, `valuation_extreme_trigger` (B2, one-sided) and `smid_valuation_premium` (B2).

**Does not own and must not rebuild.** Inflation or growth nowcasts (L04). The credit cycle (L03). FX and commodity cycles (L06). The tactical gold view or gold implementation (L13). Sector-level valuation, which consumes my *method* and normalisation but is scored by L09. Factor construction and the value factor's weight (L10). Bottom-up name valuation (L11). The optimizer's objective function (L14). The cash call (L18).

**The load-bearing claim.** Stage 1 must produce a complete portfolio alone. This layer's contribution to that is a fully determined CMA vector and an allocation tilt, with zero human inputs required. Every judgement parameter (`f`, `θ`, `ω`) has a computed default; Stage 2 may move two of them within a declared band and nothing else.

---

## 2. Data spine — free sources, and the three breaks that will ruin you

| Code | Definition | Free source | History | PIT | Lag |
|---|---|---|---|---|---|
| `NSE_PEPB` | Daily P/E, P/B, dividend yield for Nifty 50, 100, 500, Midcap 150, Smallcap 250 | NSE `reports-indices-yield`; legacy `products/content/equities/indices/historical_pepb.htm` | Nifty 50 from 1999-01-01; broad indices from ~2005 | `true` (published daily, never revised) | 1d |
| `NSE_BHAV` | Daily bhavcopy: close, shares traded, delivery; the survivorship-free spine | NSE all-reports archive | 1994- (NSE), 2007- (BSE) | `reconstructed` | 1d |
| `SHOUT` | Shares outstanding per name, for the dilution term | NSE/BSE shareholding-pattern filings, corporate-action circulars | 2001- | `lag_approx` | 45d |
| `FIL_PL` | Quarterly standalone + consolidated P&L: sales, EBITDA, PBT, tax, PAT, interest | NSE/BSE corporate-filings archive (own scrape) | 2001- | `lag_approx` (forward-archived from today with true knowledge dates) | 45–60d |
| `FIL_BS` | Half-yearly balance sheet: net worth, gross block, total assets | same | 2001- | `lag_approx` | 60d |
| `NGDP`, `RGDP` | Nominal and real GDP/GVA, quarterly and annual | MOSPI National Accounts | 1996- | `lag_approx`, **rebased 2022-23 in 2026** | 60d |
| `CPI` | All-India CPI combined | MOSPI / RBI DBIE | 2011- (2012=100), **rebased 2024=100 in Feb 2026**; WPI back-splice to 1994 | `lag_approx` | 12d |
| `Y10` | 10-year G-sec benchmark yield | RBI DBIE; CCIL | 1996- | `true` | 1d |
| `TBILL91` | 91-day T-bill yield (the cash rate) | RBI DBIE | 1993- | `true` | 1d |
| `MCAP_TOT` | NSE + BSE total market capitalisation | NSE Market Pulse monthly; BSE daily | 1995- | `true` | 1d |
| `GOLD_USD`, `USCPI` | LBMA gold and US CPI, for the real gold price | FRED / World Gold Council Goldhub / World Bank Pink Sheet | 1968- | `true` | 30d |
| `IESH` | RBI household inflation-expectations survey, 1y ahead | RBI DBIE | 2005- | `true` | 45d |
| `CAPE_XC` | Cross-country CAPE panel, for the imported coefficient | Siblis Research free tier; Barclays/StarCapital public tables; `capeindia.iima.ac.in` (IIM-A India CAPE resource) **[verify — reachable from the owner's machine only]** | 1980- | `true` | 90d |

**Break 1 — the consolidated-earnings switch, 2021-04-01.** NSE moved index P/E from standalone to consolidated earnings; published Nifty P/E fell ~20% overnight with no change in price. NSE published no overlap series. Splice rule for MVP:

```
ratio_hat = median(PE_pub[2021-04-01 : +20d]) / median(PE_pub[-20d : 2021-03-31])
PE_adj[t < 2021-04-01] = PE_pub[t] * ratio_hat        # ratio_hat ≈ 0.80  [measure, do not assume]
```
Log the estimated `ratio_hat` in the vintage record. **Deferred fix, and the correct one:** rebuild index aggregate P/E bottom-up from `FIL_PL` on the L17-reconstructed membership, consolidated where filed and standalone before, and demote `NSE_PEPB` to a validation series with a ±5% tolerance alarm.

**Break 2 — index-level earnings collapses are not valuation signals.** Trailing P/E hit ~40 in 2020–21 because the denominator collapsed, not because the market was at a record. Any trailing-P/E percentile treats that as the most expensive moment in Indian history. This is the single strongest argument for GDP-normalised earnings (§3.4) and it is why trailing P/E carries only 0.15 of the composite weight, entering through `eyg_real` rather than on its own.

**Break 3 — listing penetration.** Both market-cap/GDP and listed-profit/GDP drift structurally upward as more of the economy formalises and lists. Reverting either to its own historical mean double-counts a one-way structural shift as a cyclical excess. Every use of these two series in this layer is detrended (§3.4, §4.2).

---

## 3. Aggregate valuation: definitions, India distributions, and the composite

All z-scores are **one-sided expanding-window** (mean and sd computed only on data available at `asof`), minimum 10-year burn-in, winsorised at ±3. Percentiles are expanding-window ranks. Bands and distributions below are stated as **priors to be recomputed by the pipeline**, not as measured constants; the code must emit its own distribution table and any deviation from these priors above 0.5σ raises a review flag.

### 3.1 The measures

| id | Definition | Update | India prior distribution (median / 10th / 90th) | Aug-2026 reading |
|---|---|---|---|---|
| `pe_500` | Nifty 500 trailing P/E, spliced | Daily | 21.5 / 13.5 / 27.0 | **22.65** (Jul-26); 5y median 23.90 |
| `pb_500` | Nifty 500 trailing P/B | Daily | 3.00 / 1.85 / 4.20 | ≈3.6 **[verify]** → z ≈ +0.85 |
| `dy_500` | Nifty 500 dividend yield, % | Daily | 1.35 / 0.80 / 2.10 | ≈1.15% |
| `sy_500` | **Shareholder yield** = `dy_500` − net issuance rate | Quarterly | +0.20 / −1.20 / +1.30 | **−0.15%** → z ≈ +0.50 |
| `mcap_gdp` | (NSE ∪ BSE market cap) / trailing-4q nominal GDP | Monthly | see §3.2 | **132%** |
| `mcap_gdp_detr_z` | detrended `mcap_gdp` (§3.2) | Monthly | 0 / −1.28 / +1.28 by construction | **+0.55** |
| `eyg_raw` | `1/pe_500 − Y10`, pp | Daily | −2.50 / −5.20 / +1.40 | **−2.49 pp** |
| `eyg_real` | `1/pe_500 − (Y10 − π_exp)`, pp | Daily | +2.00 / −1.00 / +4.50 | **+2.11 pp** → z ≈ +0.10 |
| `cape_gdp` | §3.4 | Quarterly | — | z ≈ **+1.20** |
| `cape_trend` | §3.5 | Quarterly | — | z ≈ **+1.00** (deferred; prior used in v1) |
| `erp_ante` | `E[R_equity] − Y10`, from §5 | Quarterly | — | **+3.0 pp** (model) / +5.9 pp (shrunk) |

### 3.2 Market-cap-to-GDP, detrended two ways

India's raw range, 2000–2026: **low ~25–30% (FY2003)**, **peak ~149–160% (Dec 2007)**, trough ~55% (Mar 2009), ~56% (Mar 2020), 124% (FY2024), ~138% (Dec 2025), **132% (Aug 2026)**. Median over 2000–2024 ≈ 78%, min–max 30.7%–161.2% **[verify — recompute from `MCAP_TOT` and MOSPI]**.

That raw series is non-stationary. Two corrections, both computed, both exposed:

```
# (a) trend residual — cheap, MVP
trend_t   = one-sided OLS fit of log(mcap_gdp) on t, expanding window, min 120 months
mcap_gdp_detr_z = (log(mcap_gdp_t) - trend_t) / sd(residuals up to t)

# (b) fixed-universe version — drift-free, MVP if L17 membership lands on time
mcap_fixed_t = sum over the top-500-by-mcap names at t of (shares_out * price)
mcap_gdp_fx  = mcap_fixed_t / NGDP_trailing4q_t     # constant count, so no listing-penetration drift
```
Use `mean(z_a, z_b)` when both are fresh; `z_b` alone if they disagree by more than 1.0σ, with an alarm. Fitted trend as of 2026 sits at ≈118% of GDP, so 132% is **+0.55σ** — mildly expensive, not extreme. Anyone quoting the raw 132% against a raw median of 78% and calling it a bubble is reading listing penetration as valuation.

### 3.3 The earnings-yield gap, and why Asness is right and matters more in India

The India Fed model is `eyg_raw = E/P − Y10`. Asness (2003, *Fight the Fed Model*, JPM 30(1)) shows the spread is a description of investor **inflation illusion** — comparing a real yield (E/P) to a nominal one (Y10) — and that raw E/P forecasts long-horizon returns *better* than the spread does.

India makes the objection worse, not better. Indian 10-year nominal yields fell from ~12% (1996) to 6.91% (Aug 2026) almost entirely on disinflation, so `eyg_raw` is dominated by the inflation trend. A raw-EYG percentile would have shouted "cheap" through the entire high-inflation 1990s–2000s and "expensive" now — a statement about the RBI, not about equities.

**Fix, and the design decision.** Compute `eyg_real = E/P − (Y10 − π_exp)`, with `π_exp` = 5-year-ahead expected CPI taken from **L04**, never rebuilt here (MVP proxy: 5y trailing CPI mean, clipped to RBI's 4%±2% band; v2: blended with RBI IESH). Then:

- `eyg_real` enters the composite with weight **0.15** — deliberately low, per Asness's finding that spreads underperform raw yields as forecasters.
- `eyg_raw` is carried as a **diagnostic only**, never in the composite. It is exposed because Stage 2 and the owner will ask for it.
- The genuinely correct home for the earnings-yield-vs-bond comparison is the **ERP term of §5**, where it is an ex-ante risk premium — which is what it actually is — not a timing signal.
- **Deferred (v2):** Asness's own remedy, `E/P_t = a + b·π_exp_t + c·σ^{20y}_{equity,t} + d·σ^{20y}_{bond,t} + ε_t` fitted one-sided from 1999, using `z(ε_t)`.

Today: E/P 4.42%, Y10 6.91%, π_exp 4.60% → real Y10 2.31% → **`eyg_real` = +2.11pp**, essentially at its own median. *On a real-rate basis Indian equity is not expensive.* The expensiveness in this layer comes entirely from the profit share and market-cap/GDP. That disagreement is real, is logged, and is why the composite reads +0.85 rather than +1.5.

### 3.4 `cape_gdp` — the layer's primary measure, and the identity that motivates it

A Shiller CAPE built on India's own EPS history fails three ways: consistent index EPS only from 1999; the 2021 splice; and India's high real earnings trend (~8–11%/yr over 2003–2026), which makes a 10-year backward *average* of real EPS sit ~30–35% below current normal earnings and so inflates the ratio mechanically by ~1.5×, destroying comparability with its own early history and with other countries.

Sidestep it. Normalise price by **GDP-anchored** normal earnings:

```
phi_t      = aggregate listed PAT (trailing 4q) / nominal GDP (trailing 4q)      # the profit share
phi_bar_t  = detrended trailing 10y mean of phi (listing-penetration corrected, §4.2)
E_norm_t   = NGDP_t * phi_star_t                    # phi_star from the structural discriminator, §4.3
cape_gdp_t = MktCap_t / E_norm_t
```

Note the identity: **`cape_gdp` = `mcap_gdp` / `phi_star`.** Market-cap-to-GDP and CAPE are the same statistic once you divide by the profit share. This unifies §3.2 and §3.4 and puts the entire informational burden on §4 — measuring the profit share and deciding how much of it is permanent. That is exactly where the burden belongs, and it is why the earnings-cycle module, not the multiple, is the heart of this layer.

Today: `mcap_gdp` 1.32, `phi_star` 4.13% (§4.3) → `cape_gdp` = 32.0, against a trailing P/E of 22.65. The GDP normalisation says the market is **~41% more expensive than trailing P/E implies**, because trailing earnings are cyclically high. z ≈ +1.20.

### 3.5 `cape_trend` — deferred, and the right way to build it

Not a 10-year mean; a 10-year **trend value**, which removes the growth bias while keeping the cyclical smoothing:

```
fit log(real EPS_index) on t over a trailing 10y window, one-sided
E_star_t     = exp(fitted value at t)
cape_trend_t = P_real_t / E_star_t
```
Also compute a 7-year variant (`cape7`) — India's earnings cycle is shorter than the US 10-year convention, and a 10-year window burns too much of a 27-year sample. Both are **deferred to v2** because they need the bottom-up rebuilt index EPS series (Break 1). In v1 the composite carries `cape_trend` at a frozen prior of z = +1.00 with `stale=true`, and the code must degrade gracefully to a 4-component composite if the owner prefers.

### 3.6 The composite and its bands

```
V_z = 0.30*z(cape_gdp) + 0.25*z(cape_trend) + 0.20*z(pb_500)
    + 0.15*z(eyg_real, sign-flipped)  + 0.10*z(sy_500, sign-flipped)
# sign: V_z > 0 == EXPENSIVE.  Exposed to L01 as equity_longrun_valuation_z = -V_z.
# Robustness: if any component is stale > 90d, use the MEDIAN of the fresh z's instead of the
# weighted mean. Require >= 3 of 5 fresh, else emit contribution 0 and raise.
```
Weights are **set from reasoning, then frozen in git** — L01 tier B forbids fitting them. Rationale: `cape_gdp` highest because it is the only measure immune to the earnings-collapse artifact; `pb_500` next because book value does not collapse in a recession, making it the most reliable tail measure; `eyg_real` lowest of the price measures per Asness.

| Band | `V_z` | Percentile | Label |
|---|---|---|---|
| 1 | ≤ −1.65 | ≤ 5 | Deep value |
| 2 | −1.65 … −1.05 | 5–15 | Cheap |
| 3 | −1.05 … −0.52 | 15–30 | Mildly cheap |
| 4 | −0.52 … +0.52 | 30–70 | Normal |
| 5 | +0.52 … +1.05 | 70–85 | Expensive |
| 6 | +1.05 … +1.65 | 85–95 | Very expensive |
| 7 | ≥ +1.65 | ≥ 95 | Extreme |

**Hysteresis:** a band change requires the percentile to cross the boundary by ≥5 percentile points and hold at two consecutive quarter-ends. `smooth_window_months: 24`, `min_dwell_months: 12`.

**Live reading, 2026-08-28:** `V_z = 0.30(1.20) + 0.25(1.00) + 0.20(0.85) + 0.15(0.10) + 0.10(0.50) = +0.85` → percentile ≈ **80** → **Band 5, "Expensive."**

---

## 4. The earnings cycle

### 4.1 Indicators

| id | Definition | Source | Freq | India prior range |
|---|---|---|---|---|
| `eps_gap` | `log(real EPS_ttm) − trend(t)`, one-sided expanding OLS, min 40q | `FIL_PL` + `CPI` | Q | −35% (FY20) to +25% (FY08) |
| `margin_agg` | aggregate PAT / Sales, **non-financials only**, constant-tax-rate basis (§4.3) | `FIL_PL` | Q | 4.0% (FY20) to 9.0% (FY08, FY25-26) |
| `roe_agg` | aggregate PAT / opening net worth | `FIL_PL`+`FIL_BS` | H | 12% (FY20) to 25% (FY08) **[verify]** |
| `sales_excess` | aggregate nominal sales YoY − nominal GDP YoY | `FIL_PL`+`NGDP` | Q | −12pp to +14pp |
| `phi` (`profit_share_gdp`) | listed PAT ttm / NGDP ttm — **exposed to L03** | `FIL_PL`+`NGDP` | Q | 1.8% (FY20) to **5.2% (FY26, record)** |
| `eps_surprise_breadth` | §4.4 — the free proxy for the cut revision cycle | `FIL_PL` | Q | −1 to +1 |

Prior on the Nifty-500 profit share by year, to be rebuilt from our own archive rather than trusted from broker charts: FY17 2.9, FY18 2.8 (lowest since 2003), FY19 2.9, FY20 ~2.0, FY21 2.7, FY22 4.0, FY23 4.1, FY24 4.8, FY25 4.7, FY26 **5.2** → 10-year mean **≈3.6%** **[verify]**.

**Mean-reversion half-lives — estimate, do not assume.** For each series fit `Δx_t = α + β(x_{t−1} − x̄_{t−1}) + ε_t` on quarterly data and report `half_life = −ln2 / ln(1+β)` with its standard error. Priors: `margin_agg` 10–14 quarters; `roe_agg` 8–12 quarters (Nissim & Penman 2001 find US profitability half-lives of 2–3 years); `eps_gap` 7–10 quarters; `phi` 14–20 quarters. Note these are **all much shorter than the valuation half-life of 84 months** — earnings revert faster than multiples, which is precisely why a valuation signal built on trailing earnings is unstable and one built on GDP-normalised earnings is not.

### 4.2 Detrending the profit share for listing penetration

The same drift that corrupts `mcap_gdp` corrupts `phi`. Correct it by separating coverage from margin:

```
coverage_t = aggregate listed SALES (ttm) / NGDP (ttm)          # rises structurally; DO NOT revert it
margin_t   = aggregate listed PAT (ttm) / aggregate listed SALES (ttm)   # coverage-free; DO revert it
identity:  phi_t = coverage_t * margin_t
```
`coverage` carries a structural drift of **+0.5 to +0.8 %/yr** in log terms **[verify from our archive; this is a measurement, not a guess]**. Mean-revert `margin`, extrapolate `coverage`. Reverting `phi` wholesale — which is what every broker note does — double-counts formalisation as a cyclical excess and makes the model permanently too bearish.

### 4.3 Structural upgrade versus cyclical peak — the hardest judgement, made into a number

A four-test discriminator, each scored structural (1) or cyclical (0). All inputs free.

| Test | Structural if | Cyclical if | Data |
|---|---|---|---|
| **T1 Decomposition** | Margin gain sits in gross margin, product mix, or opex leverage, and has persisted >8 quarters | Gain sits in input-cost deflation, other income, or falling credit costs/provisions | `FIL_PL` line items |
| **T2 Breadth** | Present in >60% of sectors **and** >55% of names | Concentrated in ≤2 sectors (typically metals, energy, bank provisioning) | own aggregate |
| **T3 Reinvestment** | Asset turns flat/up **and** capex/sales rising — capacity added into demand | Asset turns rising **and** capex/sales falling — sweating capacity, the classic late-cycle signature | `FIL_PL`+`FIL_BS` |
| **T4 Macro anchor** | Matched by a structural fall in the wage or interest share of GVA (formalisation, deleveraging) | Matched by a commodity terms-of-trade move or a one-off tax change | MOSPI NAS; RBI interest coverage |

```
S = number of tests scoring structural            # 0..4
f = clip((S - 1) / 3, 0, 1)                       # structural fraction. S<=1 -> 0 ; S=4 -> 1
margin_star  = f * margin_current + (1 - f) * margin_bar_10y
phi_star     = coverage_extrapolated * margin_star
```

**Two rules that stop this being hand-waving.**

1. **Statutory tax changes are level shifts, not cycles.** Recompute all margins on a constant effective tax rate: `PAT_adj = PBT * (1 − τ_ref)`, `τ_ref = 25.17%` (India's post-Sept-2019 concessional regime). India's Sept-2019 cut from 30% to 22% raised PAT ~11% permanently and once. On a raw series it reappears every year as "margin expansion." On the adjusted series it appears once, as a level break in the splice record, and never again.
2. **The credit-cost cycle is L03's, and it must be netted out here.** Bank system GNPA fell from 11.2% (FY18) to ~2.3% (FY25). That is a very large, very cyclical contribution to financial-sector PAT. Financials are excluded from `margin_agg` for exactly this reason, and their contribution to `phi` is flagged separately as `phi_financials`, residualised against L03's `s_credit` with a declared `beta_prior = 0.55`.

**Live application, 2026-08-28.** T1: much of the FY21–26 margin expansion is falling bank credit costs plus the 2019 tax cut — **cyclical** (the tax cut is a level shift, now netted out). T2: broad, with mid-caps at a 15-year-high contribution — **structural**. T3: capex/sales rising on the public-capex push — **structural**. T4: interest share of GVA fell structurally on corporate deleveraging, but the commodity terms-of-trade also helped — **cyclical**, marginal. **S = 2 → f = 0.33.** With `margin_current ≈ 8.5%` and `margin_bar_10y ≈ 6.5%` **[verify]**: `margin_star = 7.16%`; with `coverage` extrapolated, `phi_star = 4.13%` against `phi = 5.20%`.

**This is the layer's central live call and its largest single unhedged risk.** An error of ±0.5 in `f` moves the 7-year equity expected return by roughly ±2pp/yr and flips the strategic tilt. It is exposed as `structural_fraction_f` with the four test scores attached, and it is one of only two parameters Stage 2 may move (±0.25, two signatures, logged).

### 4.4 Earnings revisions: the cut signal and its free replacement

Analyst estimates and revision breadth are D5 — not freely available for India. L01 R6 requires a named proxy with a one-tier evidence downgrade. Build the surprise against a **seasonal random walk with drift** (Foster 1977; Foster, Olsen & Shevlin 1984), which needs only our own scraped results:

```
E_hat[i,q]  = E[i,q-4] + delta_i,   delta_i = mean(E[i,k] - E[i,k-4]) over the last 8 quarters
SUE[i,q]    = (E[i,q] - E_hat[i,q]) / sd(E[i,k] - E_hat[i,k]) over the last 8 quarters
eps_surprise_breadth_t = 2 * (fraction of universe with SUE > 0) - 1      # in [-1, +1]
```
Also emit the simpler `realised_eps_breadth` that L01 §5 names verbatim (fraction whose trailing-4q EPS exceeds the value four quarters earlier), so the registry entry resolves.

**State the loss plainly.** This is entirely backward-looking. It tells you the earnings cycle turned 45–60 days *after* the quarter closed. It has none of the forward content of estimate revisions, which is the whole point of a revision signal. Tier **B → C** by R6, one-sided under R3, and its allocation budget is therefore near-zero; its real use is as a **T2 breadth input to the discriminator** and as an L11 input for name-level PEAD. Deferred to v2 — it needs per-name quarterly parsing, the most expensive item in the layer.

