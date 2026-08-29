# Layer 08 — Momentum, Trend and Technicals (1 month – 2 years)

**Abstract.** This layer is the aggressive book's alpha engine and, simultaneously, the single
largest threat to the owner's drawdown ceiling. It owns two mechanically different things that are
usually confused. The first is **cross-sectional momentum** — which names to own — built as a
six-component composite dominated by *residual* momentum (Blitz–Huij–Martens), because residual
momentum delivers a comparable premium at roughly half the volatility and with a far smaller crash
tail than raw 12-1. The second is **time-series trend** — how much equity to own at all — which
feeds L17's cash-call engine and is the mechanism that actually controls absolute drawdown. Keeping
these separate is the layer's central design decision, because the two risks they address are
different: a long-only momentum sleeve's *absolute* drawdown is a beta problem solved by the trend
gate (a 200-DMA exit on 28 Feb 2020 sidestepped roughly 32 of Nifty's 38 percentage-point fall),
while its *relative* collapse in a rebound is a factor problem solved by Barroso–Santa-Clara
volatility scaling, a Daniel–Moskowitz panic gate and an asymmetric drawdown ladder. Vol targeting
is explicitly **not** a crash predictor and is not sold as one. Every signal here is computable
from NSE bhavcopy archives, `sec_bhavdata_full` delivery files and free niftyindices TRI series —
this is the one layer of the stack with no point-in-time fundamentals problem, which is why it is
the right place to spend the scarce 3–6 month build budget. The layer also delivers the project's
most uncomfortable finding: at ₹1,000 crore, only ~200–350 names clear the liquidity screen, the
momentum premium in that subset is roughly a third to a half of the mid/small-cap spread, and
therefore **the moderate book's 30–40% CAGR aspiration cannot be sourced from momentum.**

---

## 1. Scope, and what this layer is not

**Owns:** price- and volume-derived signals with an information half-life between roughly one month
and two years, for equities, indices and gold; the momentum sleeve's *complete* target portfolio
(Stage-1 sufficiency); the sleeve's own risk scaling; and the trend/breadth state vector that the
cash-call engine consumes. In L01's registry this layer owns `intermediate_momentum_12_1` (MVP),
`short_reversal_1m` (MVP, aggressive only) and `annual_seasonality` (deferred).

**Does not own, and must not rebuild:**

| Belongs to | Do not duplicate here |
|---|---|
| L09 factor library | value / quality / low-vol / size. **L09's blend must not contain a momentum factor** — momentum is mine, and a duplicate would double-count against the L01 budget |
| L10 sector model | sector selection and sector weights. I emit *sector-relative strength* only as a residualisation control and as a diagnostic |
| L11 bottom-up | SUE, fundamentals, the earnings archive. I own the *price-based* PEAD signal (announcement CAR); L11 owns the accounting one |
| L12 special situations / IPO | any name with < 252 trading sessions of history. Those are routed out of my universe, not scored by it |
| L13 gold | gold sizing. I emit `trend_score_gold` only |
| L17 risk engine | the portfolio-level cash call, the de-gearing ladder, the funding-stress trigger. I emit a *recommended* equity scaler; L17 binds |
| L15 execution | tranching, day selection, participation scheduling. I emit hints and hard caps, not schedules |
| L04 macro regime | the nominal-growth nowcast. I consume `m_applied`, I do not compute `NGN_z` |

**Sign convention (L01):** `+1` = state historically favourable to risk assets.

---

## 2. Data spine — all free

| # | Field / series | Source | URL | Freq | History | PIT status |
|---|---|---|---|---|---|---|
| 1 | Daily OHLC, volume, series code (EQ/BE/BZ), ISIN | NSE bhavcopy (legacy `cm{DDMMMYYYY}bhav.csv.zip`; udiff `BhavCopy_NSE_CM_*` from 2024) | nseindia.com/all-reports | D | 1994- | `reconstructed` — a genuine PIT price tape |
| 2 | Delivery quantity and delivery % | NSE `sec_bhavdata_full_DDMMYYYY.csv` (earlier: `MTO_DDMMYYYY.DAT`) | nseindia.com/all-reports | D | ~2011- daily full; MTO earlier **[verify]** | true PIT |
| 3 | Corporate actions (splits, bonus, dividends, mergers) | NSE/BSE corporate action archives | nseindia.com, bseindia.com | event | 1994- | true PIT (ex-date known) |
| 4 | Index levels, PR and **TRI** — Nifty 50, 500, Midcap 150, Smallcap 250, sector indices | niftyindices.com historical data | niftyindices.com | D | 1995-2005 by index | true PIT |
| 5 | Nifty200 Momentum 30, Nifty500 Momentum 50 TRI (**benchmark only**) | niftyindices.com | niftyindices.com | D | base 1-Apr-2005; Momentum 50 launched 4-Jun-2024 | live values PIT; pre-launch is backfilled |
| 6 | India VIX | NSE | nseindia.com | D | Nov 2007- | true PIT |
| 7 | GSM / ASM surveillance lists, price-band and circuit files | NSE daily surveillance reports | nseindia.com | D | ~2017- **[verify]** | true PIT |
| 8 | Index membership history (Nifty 500 / Total Market) | NSE index-maintenance circulars + rebalance press releases | niftyindices.com | semi-annual | 1996- | must be reconstructed (L19) |
| 9 | T-bill 91d yield (risk-free for risk-adjusted momentum) | RBI DBIE / CCIL | data.rbi.org.in | W | 1994- | `lag_approx` |
| 10 | Gold INR: LBMA PM fix × RBI USDINR reference rate; cross-check GOLDBEES adj. close | LBMA/WGC + RBI | — | D | 1994- (ETF 2007-) | true PIT |

Two ingestion facts that must be honoured or every signal below is wrong: (a) the bhavcopy format
changed to udiff in 2024 and both layouts must parse; (b) the universe is the **union across all
dates**, since delisted names simply stop appearing — taking today's listing produces a
survivorship-biased tape that will inflate momentum's backtested return by an amount nobody can
bound.

**No point-in-time fundamentals are required by any MVP signal in this layer.** That is the reason
this layer is first in the build order after the data pipeline.

---

## 3. Universe and eligibility

Applied at each formation date `t`, using only data known at `t`.

```
eligible(i, t) =
    i ∈ nifty_total_market_membership(t)                     # PIT reconstruction, L19
  and trading_history_days(i, t) >= 252                      # else route to L12 (IPO sub-model)
  and series(i, t) == 'EQ'                                   # excludes BE / BZ / T2T
  and traded_sessions(i, [t-60, t]) / 60 >= 0.95
  and median_daily_traded_value(i, [t-60, t]) >= ADV_floor(book)
  and close(i, t) >= 20                                      # tick-size / penny distortion
  and free_float_mcap(i, t) >= 1000e7                        # ₹1,000 cr, aggressive
  and gsm_asm_stage(i, t) < 2
  and circuit_days(i, [t-20, t]) <= 4                        # operator-driven names
  and not (ret(i, [t-63, t]) > 1.00 and max_1d_ret(i, [t-63,t]) > 0.25)   # parabolic filter
```

`ADV_floor`: ₹5 cr (aggressive), ₹33 cr (moderate) — derived in §11, not assumed.

The parabolic filter is India-specific and load-bearing. The small-cap tail of the Nifty 750
contains names whose "momentum" is a manipulated ramp; they rank top-decile on every price signal
and then gap down 20% for five consecutive sessions. Excluding names that have doubled in a quarter
*with* a single-day 25% print costs some genuine winners and removes most of that pathology.

---

## 4. Cross-sectional momentum — the six components

All raw signals are computed on **corporate-action-adjusted total-return prices**. Each raw value is
winsorised at the 1st/99th cross-sectional percentile, then converted to a **normal score**
`z_i = Φ⁻¹((rank_i − 0.5)/N)` within its size bucket (large = top 100 by float mcap, mid = 101–250,
small = 251–750). Rank-based standardisation, not raw z-scoring, because Indian small-cap return
distributions have kurtosis high enough that a raw z-score is dominated by three names.

| id | Formula | Lookback / skip | Update | Evidence | Composite weight |
|---|---|---|---|---|---|
| `mom_12_1` | `P(t−21)/P(t−252) − 1` | 252d, skip 21d | daily, act monthly | Jegadeesh–Titman (1993); Asness–Moskowitz–Pedersen (2013) | 0.20 |
| `mom_6_1` | `P(t−21)/P(t−126) − 1` | 126d, skip 21d | daily | Jegadeesh–Titman (1993); Aziz–Ansari (2013) India | 0.15 |
| `mom_int_12_7` | `P(t−126)/P(t−252) − 1` | intermediate horizon only | monthly | Novy-Marx (2012) — intermediate horizon dominates recent | 0.10 |
| `resmom_12_1` | see below | 252d betas, 12-1 residual window | monthly | **Blitz–Huij–Martens (2011)** | **0.30** |
| `ramom_nse` | `mean_z( r_6m/σ_1y , r_12m/σ_1y )` (excess of 91d T-bill) | 126d & 252d | monthly | NSE Momentum-30/50 index construction | 0.15 |
| `ph_52w` | `P(t) / max(P, [t−252, t])` | 252d | daily | George–Hwang (2004) | 0.10 |

### 4.1 Residual momentum — the component that carries the weight

Blitz, Huij & Martens (2011, *Journal of Empirical Finance* 18(3):506–521) show that momentum
computed on the *residuals* of a factor-model regression earns a comparable mean return with roughly
half the volatility, roughly doubling the information ratio, and — critically for this project —
with far less of the beta asymmetry that produces momentum crashes. Raw 12-1 momentum is partly a
disguised bet on whatever factor recently rose; when that factor reverses, the whole book reverses
at once. Residual momentum strips that out.

The paper's construction uses Fama–French factors. We have no free point-in-time HML for India. The
implementable substitute, using only bhavcopy and free index TRI series:

```
# betas: 252 daily returns ending t-1, Dimson-corrected for thin trading
r_i,d  =  a_i + b0_mkt·r_mkt,d + b1_mkt·r_mkt,d-1 + b0_sec·r_sec,d + b1_sec·r_sec,d-1 + e_i,d
beta_mkt = b0_mkt + b1_mkt ;  beta_sec = b0_sec + b1_sec      # Dimson (1979)

# residual return path over the 12-1 window
e_i,d = r_i,d − beta_mkt·r_mkt,d − beta_sec·r_sec,d ,  d ∈ [t−252, t−21]

resmom_i = ( Σ e_i,d ) / ( sd(e_i,d) · sqrt(n_d) )            # t-statistic form
```

`r_mkt` = Nifty 500 TRI daily return; `r_sec` = the name's NSE sector index TRI return (mapping
consumed from L10). The Dimson lag matters: without it, small-cap betas are biased low by 20–40% and
the "residual" still contains market beta. Minimum 200 valid daily observations, else the name falls
back to `mom_12_1` with a 0.7 confidence haircut.

**Deferred (v2):** replace the market+sector model with the first 5 principal components of the
252-day return correlation matrix, which needs no classification at all and captures latent style
factors. Deferred because PCA sign/rotation stability across rebalances needs its own test harness.

### 4.2 Risk-adjusted momentum, NSE form

Worth mirroring exactly because it makes the free, published Nifty200 Momentum 30 and Nifty500
Momentum 50 TRI series a *directly comparable* live benchmark for our sleeve — a rare piece of free
external validation:

```
ratio_k = (total return over k) − (91d T-bill return over k)
          ------------------------------------------------------ , k ∈ {126d, 252d}
          sd(daily log returns over 252d) · sqrt(252)
z_k  = cross-sectional z of ratio_k
score = mean(z_126, z_252)
normalised = 1 + score  if score >= 0 ;  else  1/(1 − score)
```

### 4.3 Post-earnings-announcement drift — the price-based version

Analyst estimates are unavailable, so the standardised-unexpected-earnings route is closed for MVP.
The price-based route is not, and Chan, Jegadeesh & Lakonishok (1996) show abnormal-return-based
drift performs comparably to SUE-based drift:

```
CAR_i = Π(1 + r_i,d) − Π(1 + r_mkt,d) ,  d ∈ [t_ann − 1, t_ann + 1]
ARS_i = CAR_i / ( sd(e_i,d over 252d) · sqrt(3) )
pead_i(t) = ARS_i · exp( −(t − t_ann) / 30 ) ,  for t − t_ann ∈ [2, 63] trading days, else 0
```

Requires only announcement *dates*, scraped from NSE/BSE corporate announcements — cheap. Enters as
a bounded tilt of ±0.75pp on names already selected, not as a selection criterion. **Deferred to
v1.5**, gated on L11 delivering a clean announcement-date table; `pead_1_3m` is already `defer` in
the L01 registry and this does not contradict it.

### 4.4 The composite and the sleeve portfolio

```
S_i = 0.30·resmom + 0.20·mom_12_1 + 0.15·mom_6_1 + 0.15·ramom + 0.10·mom_int + 0.10·ph_52w
```

Then hard filters (all must pass, all cheap, all crash-motivated):

- `close > SMA200` and `slope(SMA200, 21d) > 0` — a top-decile name below a falling 200-DMA is a
  name whose momentum has already rolled over.
- `close > SMA50` **or** the name is within 10% of its 52-week high.

Selection: rank by `S_i`, hold the top `N` (aggressive `N = 40`, min 25 / max 60; moderate `N = 30`,
min 20 / max 40).

Weighting: score-tilted inverse-volatility, which is the long-only analogue of volatility scaling and
empirically cuts sleeve volatility 15–25% versus equal weight:

```
w_raw_i  = max(0, S_i − S_threshold) / sigma_i     # sigma_i = 63d realised vol, floored at 15%
w_i      = w_raw_i / Σ w_raw
w_i      = min(w_i, 6% of NAV, ADV_cap_i, 3 × (1/N))      # §11 for ADV_cap
sector_sleeve_cap = 30% of sleeve            # keeps portfolio-level sector cap (25%) reachable
```

Renormalise after capping, iterate to a fixed point (≤ 5 passes). The sleeve emitted is complete and
constraint-satisfying **on its own** — Stage-1 sufficiency is a property of this module, not of the
optimiser.

**India evidence.** Agarwalla, Jacob & Varma (2017, *Vikalpa* 42(4); WP 2013) report a momentum
factor averaging **21.9% p.a. from Jan-1994 to Dec-2014**, against HML 15.3%, SMB ≈ 0% and a market
risk premium of 11.5% — momentum is the strongest documented factor in Indian equities, stronger
than in the US. Their free factor library at faculty.iima.ac.in/iffm/ is built on CMIE Prowess and is
therefore a **validation benchmark only, never a model input** (L01 §14). Sectoral momentum is
documented by Garg & Varshney (2015, *Global Business Review*), and momentum/reversal/liquidity
interactions in India by Bhattacharya et al. (2023, *Pacific-Basin Finance Journal*) [verify exact
authorship]. Third-party backtests of Nifty500 Momentum 50 report ~21.2% p.a. against Nifty 500's
15.0% over ~21 years [verify — blog-sourced; must be reproduced on our own bhavcopy build before it
is quoted anywhere].

---

## 5. Momentum crashes — the binding risk

Daniel & Moskowitz (2016, *JFE* 122(2):221–247) document the mechanism: in a bear market the past
losers have become highly levered, their betas rise toward 3, and the long-short momentum portfolio
becomes a large short position in market beta exactly when the market rebounds. US WML lost 91.6%
(Jul–Aug 1932) and 73% (Mar–May 2009). Barroso & Santa-Clara (2015, *JFE* 116(1):111–120) show that
scaling by the strategy's own realised variance takes the same strategy from Sharpe 0.53 to 0.97 and
maximum drawdown from −91.6% to −45.2%.

**A distinction this project must not blur.** We run a *long-only* sleeve. There is no short leg, so
the classic WML crash mechanism is attenuated. What remains is two separable risks:

| Risk | Mechanism | Hits | Controlled by |
|---|---|---|---|
| **R-A: beta drawdown** | Momentum names are high-beta and extended at tops; they fall harder than the index | *Absolute* drawdown — the binding constraint | §7 trend gate → L17 cash call |
| **R-B: factor rebound loss** | Portfolio is fully invested in the old leaders while the new leaders are the beaten-down names | *Relative* return, and the second leg of drawdown | §5.1–5.3 below |

Selling vol targeting as protection against R-A would be dishonest: realised volatility only rises
*after* the fall. Barroso–Santa-Clara's drawdown improvement comes overwhelmingly from the rebound
leg, not the initial decline.

### 5.1 Sleeve volatility targeting

```
sigma_fast = EWMA vol of sleeve daily returns, lambda = 0.94 (half-life ≈ 11d)
sigma_slow = trailing 126d realised vol
sigma_hat  = sqrt( 0.5·sigma_fast² + 0.5·sigma_slow² ) · sqrt(252)

w_vol = clip( sigma_target / sigma_hat , 0.40 , 1.25 )
sigma_target = 20% (aggressive) , 16% (moderate)
```

Sleeve returns are computed on the *live* weights, backfilled from a simulated sleeve during warm-up.
The fast/slow blend exists to avoid the whipsaw a pure EWMA produces around single-day shocks (e.g.
budget day). Worked example, mid-March 2020: `sigma_fast ≈ 55%`, `sigma_slow ≈ 28%`, blend ≈ 44%,
`w_vol ≈ 0.46`.

### 5.2 Bear / panic gate

```
bear_flag  = 1 if  ret(Nifty500 TRI, 252d) < ret(91d T-bill, 252d)  AND  close < SMA200
vol_pctile = percentile of 21d realised vol of Nifty 500 vs trailing 1260 sessions
panic_flag = bear_flag AND ( vol_pctile > 0.80 OR India VIX > 25 )

w_bear = 1.00  if not bear_flag
       = 0.70  if bear_flag and not panic_flag
       = 0.35  if panic_flag
```

While `panic_flag = 1`, three additional changes apply, all of them targeted at the beta asymmetry
that *is* the crash:

1. Selection switches to **`resmom` only** (weight 1.0), dropping raw price momentum. Residual
   momentum is by construction close to beta-neutral in formation.
2. An **ex-ante sleeve beta cap** of 0.90 is imposed: solve for weights minimising tracking error to
   the unconstrained sleeve subject to `Σ w_i·beta_i ≤ 0.90`; drop any name with `beta_i > 1.6`.
3. `N` is raised to 60 and the max single weight cut to 3% — diversifying into the uncertainty.

Exit requires `bear_flag = 0` for 10 consecutive sessions **and** `vol_pctile < 0.60`. Hysteresis is
not optional; without it this flag flickers weekly through 2011 and 2018.

Cooper, Gutierrez & Hameed (2004, *JF* 59(3)) is the evidence: mean monthly momentum profit of 0.93%
after UP market states versus −0.37% after DOWN states (1929–1995). Large, robust, and — unlike the
nominal-growth hypothesis in §8 — replicated widely.

### 5.3 Drawdown-conditional de-gearing (sleeve level)

`DD_t = sleeve_nav_t / max(sleeve_nav_{≤t}) − 1`

| `DD_t` | `w_dd` |
|---|---|
| > −8% | 1.00 |
| −8% to −15% | 0.85 |
| −15% to −22% | 0.65 |
| −22% to −30% | 0.45 |
| < −30% | 0.30 (floor) |

**Asymmetric timing rule.** De-gearing is applied *the next session*, ignoring all rate limits.
Re-gearing moves at most one rung per rebalance and only after both (a) 15 sessions have elapsed
since the trough and (b) the sleeve has recovered ≥ ⅓ of the drawdown from the trough.

### 5.4 Composition of scalers

```
w_sleeve_mult = clip( m_applied · w_vol · w_bear · w_dd , 0.25 , 1.30 )
sleeve_weight = base_sleeve_weight · w_sleeve_mult
```

Aggressive `base_sleeve_weight = 20pp` of NAV (range 5–26pp). Moderate base = 10pp (range 2.5–13pp).
De-risking bypasses L01's `max_delta_pp_per_month = 1.333` rate limit; re-risking obeys it.

### 5.5 What actually happened in India, Mar–Jun 2020

Nifty 50 peaked at 12,362 (14 Jan 2020), closed below its 200-DMA around 28 Feb at ~11,200 (−9.4%
from peak) and troughed at ~7,610 close on 23 Mar (−38.4%). Nifty Smallcap 250 fell ~46%. Momentum
portfolios entering 2020 were concentrated in private financials and consumer names — precisely the
sectors that fell hardest (Bank Nifty ~−50%) — and the rebound from 24 Mar was led first by pharma
and IT, which momentum did not own, and then by beaten-down high-beta small caps, which momentum
owned least. Momentum therefore lost twice: once on beta and once on rotation. Third-party backtests
put Nifty200 Momentum 30's 2008 peak-to-trough at roughly −70% with a ~65-month recovery [verify].

Against the machinery above: the 200-DMA/trend gate fires around 28 Feb (before 32 of the 38
percentage points of fall); `panic_flag` sets in the week of 9 Mar; `w_vol` reaches ~0.46 by 20 March;
the DD ladder reaches the 0.30–0.45 band by 23 March; the product clips at the 0.25 floor. **The
honest cost:** re-gearing then takes until roughly July–August 2020, and the sleeve participates in
perhaps 60–70% of the Apr–Jun rebound. That is a real, quantifiable loss of 4–8pp of NAV in 2020,
and it is the price of the 30–35% drawdown ceiling. It cannot be avoided by parameter tuning; it is
the constraint doing what the owner asked it to do.

---

## 6. Time-series momentum, trend and the cash-call feed

Moskowitz, Ooi & Pedersen (2012, *JFE* 104(2):228–250) establish time-series momentum across 58
instruments and four decades; Hurst, Ooi & Pedersen (2017, *JPM*) extend it to a century. Neither is
India-specific and India offers only ~25–30 independent 12-month windows since 1994, so the honest
tier is A-by-transfer, B-in-India.

Applied to: Nifty 500 TRI, Nifty 50 TRI, Nifty Midcap 150 TRI, Nifty Smallcap 250 TRI, gold (INR).

```
Family 1 — TSMOM:      s_k = tanh( ret(k) / (sigma_ann · sqrt(k/252)) ),  k ∈ {21, 63, 126, 252}
Family 2 — MA cross:   for (f,s) ∈ {(20,100),(50,200),(100,300)}:
                          m = clip( (EMA_f − EMA_s) / (sigma_daily · sqrt(s)) , −1, +1 )
Family 3 — Breakout:   Donchian d ∈ {63, 126, 252}:
                          +1 if close > max(high, d) ; −1 if close < min(low, d) ; else decay 0.9/day

trend_score = mean( mean(Family 1), mean(Family 2), mean(Family 3) )   ∈ [−1, +1]
```

Two whipsaw controls: the score must hold its sign for **5 consecutive sessions** before the state
label changes, and at least **2 of the 3 families** must agree in sign for a non-neutral label.

**Breadth** (India-specific, cheap, and genuinely informative):
`breadth_200 = fraction of Nifty 500 members trading above their own 200-DMA`. Risk-on > 60%,
risk-off < 30%. Falling breadth with a flat index is the classic pre-2018 and pre-2020 pattern.

**Recommended equity scaler** — a *recommendation*; L17 owns the cash call and may bind tighter:

| `trend_score` | breadth | recommended equity scaler |
|---|---|---|
| > +0.50 | > 50% | 1.00 |
| 0 to +0.50 | any | 0.85 |
| −0.50 to 0 | any | 0.60 |
| < −0.50 | < 30% | 0.40 |

Graded, not binary, deliberately: a marginal signal should produce a marginal de-risking, which is
what keeps whipsaw cost proportionate. Historical behaviour of a 200-DMA rule on the Nifty: exits
around Jan-2008 at ~5,250 (−16% from a 6,288 peak) and re-enters mid-2009 near 4,400 — a large
gain; exits 28-Feb-2020 at ~11,200 and re-enters ~Aug-2020 near 11,100 — roughly flat in price while
avoiding a 32% excursion. It also generates 1–2 false round trips a year in trending bull markets,
each costing 1–3%, for an expected drag of 2–4% p.a. in years like 2017, 2021 and 2023 [all levels
and drags **[verify]** — reproduce on our own tape before quoting].

**Gold:** `trend_score_gold` on INR gold, same ensemble, exported to L13. I do not size gold.

---

## 7. The nominal-growth gate

L04 owns the nowcast and the functional form; I own its application and the residualisation inputs.

**Consumed:** `MACRO_GATES.momentum_weight_multiplier` (`m_applied`), already residualised by L04
against my volatility and market-state gates via
`m_applied = 1 + (m(NG_z) − 1)·sqrt(1 − R²(NG_z ~ [vol_state_z, mkt_state_z]))`, bounded to
[0.55, 1.30].

**Exported for that residualisation:** `mom_vol_state_z` (z of `sigma_hat` against its own trailing
5-year distribution) and `mom_mkt_state` (the §5.2 `bear_flag` / `panic_flag` pair). **Interface
risk:** L04's spec currently sources `vol_state_z` and `mkt_state` from L17. If L17's definitions
differ from mine, the residualisation removes the wrong variance and the gate is not orthogonal to
what it claims. One of the two must be canonical — recommend L17's, with L08 consuming rather than
computing, and a CI test asserting the series used by L04 is bit-identical to the one gating my
sleeve.

**Application:**

```
sleeve_weight  = base · clip(m_applied · w_vol · w_bear · w_dd, 0.25, 1.30)
interval_weeks = clip(round(base_weeks / m_applied), lo, hi)
                    aggressive: base 2, lo 1, hi 4 ;  moderate: base 4, lo 4, hi 12
band_mult      = clip(1 / m_applied, 0.80, 1.60)      # widens no-trade bands when down-weighted
```

**What the evidence supports, stated plainly.** Chordia & Shivakumar (2002, *JF* 57(2)) is the
strongest citation for the owner's hypothesis — US momentum payoffs are predictable by lagged macro
variables. Griffin, Ji & Martin (2003, *JF* 58(6)) is the direct rebuttal: macroeconomic risk
variables do not explain momentum profits internationally and the Chordia–Shivakumar result does not
replicate outside the US. I am aware of **no published study conditioning Indian momentum on nominal
growth**. The strongly evidenced conditioners are volatility (Barroso–Santa-Clara) and market state
(Cooper–Gutierrez–Hameed), both already implemented in §5 and both of which the L04 residualisation
explicitly subtracts from the gate. What remains for the NG gate to act on is, by construction, the
slow non-volatile growth slowdown — 2012–13, 2019 — where an independent macro read has something to
add and where the vol gate is silent.

**Pre-registered kill rule.** If L20 measures the residualised gate's contribution to sleeve Sharpe
at < 0.05 with a stationary-bootstrap p > 0.20, `m_applied` is set to a constant 1.0 in production
and the code is retained but disabled. This is registered *before* the backtest is run.

---

## 8. Rebalance design, turnover and what it costs in India

### 8.1 Tiered clock

| Tier | Cadence | Scope | Trade direction allowed |
|---|---|---|---|
| **T0** | Daily, pre-open | `panic_flag`, DD ladder, drift-cap (10%) breach, liquidity/GSM breach, delisting | **De-risking and breach repair only** |
| **T1** | Weekly (Fri close, execute Mon–Wed) | One of the four staggered sub-portfolios; reversal entry-timing tilts | Both |
| **T2** | Monthly (last Fri) | Sleeve weight from `m_applied`/`w_vol`, universe refresh, sector-cap repair | Both |
| **T3** | Quarterly | Universe reconstruction, factor-model re-estimation, parameter review | Both |

Moderate book: T1 becomes monthly (three staggered sub-portfolios on a quarterly cycle), T2 becomes
quarterly. That satisfies the frozen "monthly/quarterly" cadence with a 3-month average holding
period.

### 8.2 Staggered sub-portfolios (rebalance timing luck)

The sleeve is split into **4 overlapping tranches**, each holding 25% of sleeve capital, each formed
on its own date and rebalanced monthly, staggered one week apart. Aggregate cadence is weekly; each
*name's* holding period is monthly. This is an accounting device only: tranche targets are netted to
a single per-name target before anything reaches L15.

Benefit: rebalance timing luck — the dispersion in outcome attributable purely to *which day* you
reconstitute — falls roughly as `1/sqrt(n_tranches)`, so 4 tranches cut it by ~50% (Hoffstein,
Sibears & Faber on rebalance timing luck [verify exact outlet]). Secondary benefit: weekly trade
volume is a quarter of a monthly cliff, which is worth 5–15% of impact cost. Cost: negligible extra
turnover.

### 8.3 Buffer zones (the single highest-value engineering choice in this layer)

**Rank band.** Buy when rank ≤ `N`; sell only when rank > `N × (1 + b)`, `b = 0.50`. With `N = 40`,
buy at rank ≤ 40, hold until rank > 60.

**Weight band (proportional).** Trade a held name only if
`|w_target − w_current| > max(0.50pp, 0.25 × w_target)`.

**Score band on the sleeve scaler.** Only act on `w_sleeve_mult` if it moves more than 0.05 —
except for T0 de-risking.

### 8.4 Turnover and cost arithmetic

Cost stack, Indian equity delivery, per side of traded value:

| Component | bps per side |
|---|---|
| STT (delivery, both legs @ 0.10%) | 10.0 |
| Stamp duty (buy leg only, 0.015%) | 0.75 (avg) |
| Exchange transaction charge (NSE, ₹2.97/lakh) | 0.30 |
| SEBI turnover fee (₹10/cr) | 0.01 |
| Institutional brokerage (prop) | 1.50 |
| GST @18% on brokerage + exchange | 0.33 |
| **Explicit total** | **≈ 12.9 ≈ 13** |

Impact, square-root law `impact ≈ 0.3 · sigma_daily · sqrt(Q / ADV)`: at ₹100 cr with a ₹5 cr
position in a ₹20 cr ADV name, `Q/ADV = 0.25`, `sigma_daily = 2.2%` → ~33 bps/side; in a ₹200 cr ADV
name → ~10 bps/side. Blended aggressive book ≈ **20 bps/side**.

Define turnover `T` as one-way (₹ bought per year / NAV; sells ≈ buys). Total traded value = `2T`.
**Cost per 100% of one-way turnover ≈ 2 × (13 + 20) = 66 bps of NAV.**

| Config | Avg holding | Rank band | Weight band | One-way T | Explicit | Impact | **Total drag** |
|---|---|---|---|---|---|---|---|
| A weekly, strict top-40 | ~1.5m | none | none | ~600% | 1.56% | 2.40% | **3.96%** |
| B monthly, strict top-40 | ~3m | none | none | ~330% | 0.86% | 1.32% | **2.18%** |
| C B + rank band 40/60 | ~5m | 1.5× | none | ~190% | 0.49% | 0.76% | **1.25%** |
| D C + weight band | ~5.5m | 1.5× | 25% / 0.5pp | ~160% | 0.42% | 0.64% | **1.06%** |
| **E D + 4 staggered tranches (recommended)** | ~5.5m | 1.5× | 25% / 0.5pp | ~165% | 0.43% | 0.55% | **0.98%** |

Turnover figures are engineering estimates from the momentum decile's known ~30%/month raw churn and
must be **measured**, not assumed — L20 owns the measurement. The literature prior for the alpha cost
of the band is 0.5–1.5pp of gross return (momentum's information half-life is ~6 months, so extending
the holding period from 1 to ~5 months costs surprisingly little; Novy-Marx & Velikov 2016 and
Frazzini, Israel & Moskowitz on real-world anomaly trading costs). **Net of that, A → E is worth
roughly +2.0pp p.a.** That is the arithmetic that says the frozen 500%-turnover allowance should
*not* be spent on the core momentum sleeve. Reserve it for the fast overlays.

---

## 9. Additional technical modules, with honest evidence grades

| Module | Definition | Evidence | Grade | Status |
|---|---|---|---|---|
| Relative strength vs sector | `ret(i,126d) − ret(sector,126d)` | Subsumed by `resmom`; kept as a diagnostic only to avoid double-counting | B | diagnostic |
| Volume-confirmed breakout | `close > max(close, [t−252, t−5])` **and** `mean(traded value, 20d) > 2 × mean(100d)` **and** `deliv%_20d − deliv%_100d > 5pp` | Gervais, Kaniel & Mingelgrin (2001) high-volume return premium (US, weeks-to-months). India **[verify]** | B | defer to v1.5 |
| Delivery-percentage accumulation | `z(deliv%_20d − deliv%_252d)` | India-specific; distinguishes delivery accumulation from intraday churn. No academic evidence found | C | defer |
| MA structure filter | `close > SMA50 > SMA200`, `slope(SMA200,21d) > 0` | Weak standalone evidence; strong as a *filter* on momentum names | B | **MVP (as filter, §4.4)** |
| Turn-of-month | Window `[−1, +3]` around month end | Ariel (1987); Lakonishok & Smidt (1988); McConnell & Xu (2008). India **[verify]** | B | **MVP but routed to L15 as an execution tilt, not an allocation signal** |
| India calendar seasonality | Budget (1 Feb), fiscal Q4, monsoon (Jun–Sep), festive (Oct–Nov) | ~30 non-independent observations; severe multiple-testing risk | C | **defer** (matches L01 `annual_seasonality: defer`) |
| Short-horizon reversal | §9.1 | Jegadeesh (1990); Lehmann (1990); India: Deb, Banerjee & Chakrabarti (2008) find 3–6m reversals with 1y persistence | A (US), B (India) | **MVP, aggressive only** |

### 9.1 Short-horizon mean reversion — how it coexists with 12-1 momentum

```
rev_i = − ( Σ e_i,d over d ∈ [t−21, t] ) / ( sd(e_i,d) · sqrt(21) )    # residual, not raw
```

Residual reversal (market and sector removed) rather than raw reversal, so the signal is not
implicitly shorting the index after a market fall.

Four mechanisms keep it from cancelling 12-1 momentum. All four are enforced, not just described:

1. **Mechanical horizon separation.** Every momentum component skips the most recent 21 sessions.
   The reversal window *is* those 21 sessions. Their return windows do not overlap at all — that is
   what the "−1" in 12-1 has always been for.
2. **Different job in the pipeline.** Momentum answers *which names*. Reversal answers *at what
   weight and on what day*. Reversal never adds or removes a name from the sleeve. Formally,
   `w_i ← w_i + clip(0.35 × rev_z_i, −0.75pp, +0.75pp)`, applied after selection and before caps.
3. **Sequential gating.** Within the selected top-`N`, prefer names that have pulled back — buy-the-
   dip-within-an-uptrend. Symmetrically, never sell a held name because of a one-week spike unless
   it breaches the 10% drift cap.
4. **Explicit conflict rule.** If `sign(rev) ≠ sign(mom_composite)` and `|rev_z| > 2`, defer the
   trade by one rebalance cycle rather than netting to zero. A 3-sigma one-week move is usually
   news, and trading into it is how a quant book gets picked off.

Honest scope note: at ₹1,000 cr this signal is untradeable — it needs weekly turnover in mid and
small caps — which is why L01 marks `short_reversal_1m` aggressive-only. That stands.

---

## 10. Liquidity reality and capacity

Position cap from participation, not from a fixed ADV number (per Q13):

```
ADV_cap_i = participation_pct · ADV_i · build_days / AUM
   aggressive: participation 10%, build_days 5     moderate: participation 10%, build_days 15
w_i = min(entry_cap 6%, ADV_cap_i, 3/N)
```

| | Aggressive ₹100 cr | Moderate ₹1,000 cr |
|---|---|---|
| Full 5% position | ₹5 cr | ₹50 cr |
| ADV needed for a 5-day build @10% | ₹10 cr | ₹100 cr |
| ADV needed for a 15-day build @10% | ₹3.3 cr | ₹33 cr |
| **Screen used** (median 60d traded value) | **≥ ₹5 cr** | **≥ ₹33 cr** |
| Est. Nifty-750 names passing, normal market | **~550–620** [verify] | **~250–350** [verify] |
| Est. names passing, stressed market (ADV halves) | ~400–450 | ~150–220 |
| Names held | 40 | 30 |
| One-way turnover target | 150–250% | 60–90% |
| Blended impact | ~20 bps/side | ~30 bps/side |
| Cost per 100% one-way turnover | ~66 bps | ~86 bps |
| Sleeve cost drag at target turnover | ~1.0–1.6% | ~0.5–0.8% |

**Sleeve capacity** = `Σ over held names of (participation × ADV × build_days)`. Aggressive: 40 names
at ₹25 cr average ADV → ₹500 cr of sleeve capacity against a ≤ ₹26 cr sleeve. Comfortable. Moderate:
30 names at ₹150 cr ADV, 15 build days → ₹6,750 cr nominal, but the binding constraint is not build
capacity, it is *universe breadth* — 250–350 eligible names is roughly the Nifty 350, and the
momentum sleeve is then choosing 30 from a large-cap set.

**The finding the owner needs to see.** Momentum's premium in India, as everywhere, is concentrated
where liquidity is worst. Israel & Moskowitz (2013, *JFE*) show momentum survives in large caps but
is materially weaker there. If the ₹1,000 cr book's momentum universe is effectively the Nifty 200-350,
a reasonable prior is that it captures **a third to a half** of the mid/small-cap momentum spread —
roughly 2–3pp of gross excess return, not the 6pp the broad indices suggest, and ~0.6pp of that goes
to costs. **The moderate book can run momentum, but momentum cannot be the source of a 30–40% CAGR
there.** That has to be sourced from allocation, gold and the debt sleeve, or the target has to move.
This is stated in `risks`, not designed around.

---

## 11. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L19 data pipeline | `adj_prices(asof)`, `delivery(asof)`, `universe(asof)`, `membership(asof)`, `index_tri(asof)`, `corp_actions` | Bitemporal; final-vintage reads must raise |
| L01 taxonomy | registry entries `intermediate_momentum_12_1`, `short_reversal_1m`; `influence_budget()`, rate limiter | Output validates against the registry or is rejected |
| L04 macro regime | `MACRO_GATES.momentum_weight_multiplier` (`m_applied`), `momentum_rebalance_interval_weeks`, `no_trade_band_multiplier`, `NGN_z` | Consumed as given; I never recompute the nowcast |
| L17 risk engine | `vol_state_z`, `mkt_state`, `current_drawdown`, `cash_call_level` | Canonical source for the vol/market state used in L04's residualisation (§7 interface risk) |
| L10 sector model | `sector_map(symbol, asof)`, sector index TRI returns | Used only to residualise. I emit no sector view |
| L11 bottom-up | `earnings_announcement_dates`, later `sue_z` | Gates the PEAD module (v1.5) |
| L12 special situations | list of names with < 252 sessions of history | Excluded from my universe |
| L09 factor library | factor exposures, for overlap diagnostics | **L09 must not include a momentum factor** |
| L20 validation | `turnover_measured`, `band_alpha_cost`, `ng_gate_contribution` | Drives the §7 kill rule and the §8.4 band calibration |

**Exposes**

```python
MOM_SLEEVE  = {target_weights: {symbol: pct_nav}, sleeve_weight_pct, n_names,
               sleeve_beta_exante, sleeve_vol_ann_exante, est_turnover_pct,
               sector_exposure: {sector: pct}, asof, vintage_id}

MOM_SCORES  = {symbol: {composite_z, resmom_z, mom_12_1_z, mom_6_1_z, mom_int_z,
                        ramom_z, ph52_z, rev_z, trend_filter_ok, beta_exante,
                        adv_cap_pct, confidence}}

TREND_STATE = {trend_score_nifty500, trend_score_nifty50, trend_score_midcap,
               trend_score_smallcap, trend_score_gold, breadth_200dma_pct,
               mkt_state, bear_flag, panic_flag, days_in_state,
               recommended_equity_scaler}

MOM_RISK    = {sleeve_dd, w_vol, w_bear, w_dd, w_sleeve_mult, crash_alert,
               mom_vol_state_z, mom_mkt_state}

EXEC_HINTS  = {symbol: {entry_timing_z, max_daily_participation_pct,
                        est_days_to_fill, urgency, tom_window_flag}}
```

**Stage-1 sufficiency.** With Stage 2 off, `MOM_SLEEVE` is a complete, cap-satisfying portfolio from
price data alone. The Stage-2 overlay may write only `name_veto` (remove a name, with a logged
reason and a falsification condition) and `tier_downgrade`. It may not add a name, change a weight,
or move `sleeve_weight_pct`. A CI test asserts that disabling Stage 2 leaves `MOM_SLEEVE`
bit-identical.

**Double-counting guard.** My `w_vol · w_bear · w_dd` scales the sleeve's share *within* the equity
budget; L17's cash call scales the equity budget itself. L20 must report total de-gearing in the
Mar-2020 and Oct-2008 windows and assert it does not exceed the L17 ladder's intended floor.

---

## 12. MVP versus deferred

**MVP (must exist in v1, ~24 engineer-days):**

1. Adjusted-price and universe layer with the eligibility screen (§3) — 4d
2. `mom_12_1`, `mom_6_1`, `mom_int_12_7`, `ramom_nse`, `ph_52w` + rank standardisation — 3d
3. `resmom_12_1` with Dimson-corrected market+sector betas — 4d
4. Composite, MA-structure filter, inverse-vol score-tilted weighting, cap iteration — 3d
5. Crash machinery: `w_vol`, `bear_flag`/`panic_flag`, DD ladder, asymmetric rate limiting — 4d
6. TSMOM/MA/breakout ensemble + breadth + `TREND_STATE` export — 3d
7. Rank buffer, weight band, 4 staggered tranches, tiered clock — 2d
8. `m_applied` consumption with the pre-registered kill rule — 0.5d
9. Residual 1-month reversal as a bounded entry-timing tilt (aggressive only) — 0.5d

**Deferred (v2+):** PEAD (price-based, then SUE); PCA-residualised momentum; volume/delivery
breakout; delivery-accumulation z; India calendar seasonality; weekly-frequency reversal;
frog-in-the-pan information discreteness (Da, Gurun & Warachka 2014); momentum crowding /
valuation-spread monitor; sector-level TSMOM for L10.

---

## 13. Risks and honest assessment

1. **The moderate book's return target is not reachable from momentum.** At ₹1,000 cr the eligible
   universe is ~250–350 names and the accessible premium is plausibly 2–3pp gross. A 30–40% CAGR
   cannot be built on that. Flagged as a constraint conflict.
2. **The drawdown ceiling costs rebound participation, and the cost is large.** In a V-shaped
   recovery like Apr–Jun 2020, the composed de-gearing (trend gate + vol target + panic + DD ladder)
   plausibly gives up 4–8pp of NAV. Any presentation that shows the drawdown benefit without this
   cost is dishonest.
3. **Vol targeting does not prevent the initial fall.** Realised volatility is a lagging measurement.
   Absolute drawdown control comes from the trend/breadth gate, and that gate whipsaws 1–2 times a
   year at 1–3% each.
4. **The nominal-growth gate is an untested hypothesis.** Griffin–Ji–Martin (2003) is the direct
   international rebuttal of Chordia–Shivakumar; there is no Indian study. The kill rule in §7 is the
   design response.
5. **Turnover figures in §8.4 are estimates.** They are the basis for a recommendation that
   materially reduces trading, and they must be measured on our own tape before that recommendation
   is trusted.
6. **The 1.5x leverage cap and the drawdown ceiling are in genuine tension in this layer.** A levered
   momentum sleeve is the most drawdown-prone thing in the portfolio. Recommendation: leverage is
   permitted *only* when `trend_score > +0.5`, `panic_flag = 0` and `sleeve_dd > −8%`, and is capped
   at +0.10x from this layer (matching the L01 registry `leverage_x` budget). L17 arbitrates.
7. **Delivery-data history depth is unverified.** `sec_bhavdata_full` may not extend before ~2011;
   every delivery-based module inherits that limit and is therefore correctly deferred.
8. **Survivorship and membership reconstruction are upstream single points of failure.** If L19's
   PIT membership is wrong, this layer's backtest is wrong in the optimistic direction and nothing in
   this layer can detect it.
9. **Multiple testing.** Six momentum components, three trend families and a seasonality module is a
   large search space over ~30 years. All composite weights above are *set a priori from the
   literature*, not fitted. No parameter in this spec may be optimised on the backtest sample; L20
   owns the walk-forward protocol.

---

## 14. References

1. Jegadeesh, N. & Titman, S. (1993). "Returns to Buying Winners and Selling Losers." *Journal of Finance* 48(1):65–91.
2. Jegadeesh, N. (1990). "Evidence of Predictable Behavior of Security Returns." *Journal of Finance* 45(3):881–898.
3. Lehmann, B. (1990). "Fads, Martingales, and Market Efficiency." *Quarterly Journal of Economics* 105(1):1–28.
4. Asness, C., Moskowitz, T. & Pedersen, L. (2013). "Value and Momentum Everywhere." *Journal of Finance* 68(3):929–985.
5. Blitz, D., Huij, J. & Martens, M. (2011). "Residual Momentum." *Journal of Empirical Finance* 18(3):506–521.
6. Barroso, P. & Santa-Clara, P. (2015). "Momentum Has Its Moments." *Journal of Financial Economics* 116(1):111–120.
7. Daniel, K. & Moskowitz, T. (2016). "Momentum Crashes." *Journal of Financial Economics* 122(2):221–247.
8. Cooper, M., Gutierrez, R. & Hameed, A. (2004). "Market States and Momentum." *Journal of Finance* 59(3):1345–1365.
9. George, T. & Hwang, C.-Y. (2004). "The 52-Week High and Momentum Investing." *Journal of Finance* 59(5):2145–2176.
10. Moskowitz, T., Ooi, Y. H. & Pedersen, L. (2012). "Time Series Momentum." *Journal of Financial Economics* 104(2):228–250.
11. Hurst, B., Ooi, Y. H. & Pedersen, L. (2017). "A Century of Evidence on Trend-Following Investing." *Journal of Portfolio Management* 44(1).
12. Novy-Marx, R. (2012). "Is Momentum Really Momentum?" *Journal of Financial Economics* 103(3):429–453.
13. Novy-Marx, R. & Velikov, M. (2016). "A Taxonomy of Anomalies and Their Trading Costs." *Review of Financial Studies* 29(1):104–147.
14. Israel, R. & Moskowitz, T. (2013). "The Role of Shorting, Firm Size, and Time on Market Anomalies." *Journal of Financial Economics* 108(2):275–301.
15. Frazzini, A., Israel, R. & Moskowitz, T. "Trading Costs of Asset Pricing Anomalies" / "Trading Costs." AQR working papers. [verify exact title and year]
16. Chordia, T. & Shivakumar, L. (2002). "Momentum, Business Cycle, and Time-Varying Expected Returns." *Journal of Finance* 57(2):985–1019.
17. Griffin, J., Ji, X. & Martin, J. S. (2003). "Momentum Investing and Business Cycle Risk: Evidence from Pole to Pole." *Journal of Finance* 58(6):2515–2547.
18. Chan, L., Jegadeesh, N. & Lakonishok, J. (1996). "Momentum Strategies." *Journal of Finance* 51(5):1681–1713.
19. Bernard, V. & Thomas, J. (1989). "Post-Earnings-Announcement Drift." *Journal of Accounting Research* 27:1–36.
20. Gervais, S., Kaniel, R. & Mingelgrin, D. (2001). "The High-Volume Return Premium." *Journal of Finance* 56(3):877–919.
21. Da, Z., Gurun, U. & Warachka, M. (2014). "Frog in the Pan: Continuous Information and Momentum." *Review of Financial Studies* 27(7):2171–2218.
22. Dimson, E. (1979). "Risk Measurement When Shares Are Subject to Infrequent Trading." *Journal of Financial Economics* 7(2):197–226.
23. Ariel, R. (1987). "A Monthly Effect in Stock Returns." *Journal of Financial Economics* 18(1):161–174.
24. McConnell, J. & Xu, W. (2008). "Equity Returns at the Turn of the Month." *Financial Analysts Journal* 64(2):49–64.
25. **India** — Agarwalla, S. K., Jacob, J. & Varma, J. R. (2017). "Size, Value, and Momentum in Indian Equities." *Vikalpa* 42(4). WP 2013-09-05. Momentum factor ≈ 21.9% p.a., Jan-1994 to Dec-2014. Free library: <https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/> — **Prowess-built; benchmark only, never an input.**
26. **India** — Garg, A. K. & Varshney, P. (2015). "Momentum Effect in Indian Stock Market: A Sectoral Study." *Global Business Review*.
27. **India** — Deb, Banerjee & Chakrabarti (2008); Aziz & Ansari (2013). Short-horizon reversals and 6-month momentum persistence in India. [verify exact outlets]
28. **India** — "Momentum, reversals and liquidity: Indian evidence." *Pacific-Basin Finance Journal* (2023). [verify authorship]
29. Hoffstein, C., Sibears, J. & Faber, N. "Rebalance Timing Luck: The (Dumb) Luck of Smart Beta." [verify outlet — *Journal of Index Investing* 2020]
30. NSE Indices. *Nifty200 Momentum 30 Index Whitepaper* (Sep 2020) and *Nifty500 Momentum 50 Factsheet* (launched 4-Jun-2024, base 1-Apr-2005). <https://www.niftyindices.com>
