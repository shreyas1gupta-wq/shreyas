# Econometric Methods: Estimating Cycles and Signals Without Fooling Ourselves

The methods manual. Every estimation choice in the model is specified here, together with
the failure mode it is guarding against. The organising conviction: **in this problem the
default outcome is a spurious result**, so the burden of proof sits on every signal, and
the methodology exists to make that burden hard to fake.

Three facts frame everything below.

1. **Indian data is short.** Reliable equity data from ~1995 (NSE bhavcopy from 1994),
   usable fundamentals from ~2000–2005. Call it 25 years. That is ~6 Kitchin cycles,
   ~3 Juglar cycles, ~1.5 credit cycles, and less than one of anything longer.
2. **Our fundamentals are lag-approximated, not true point-in-time.** Free sources publish
   restated financials. Every backtest built on them carries a known upward bias.
3. **We will test many hypotheses.** Dozens of signals, each with parameters, across two
   books. Without explicit multiple-testing control, we are guaranteed to find something
   that looks good and is not.

---

## 1. Extracting a cycle from a series

### 1.1 The HP filter, and why we do not use it

The Hodrick–Prescott filter is the default in macroeconomics and is wrong for our purpose.
Hamilton (2018) sets out the objections precisely, and they are decisive:

- It induces **spurious dynamics** not present in the underlying data — the filtered series
  exhibits cyclical behaviour even when applied to a random walk.
- Its **endpoint behaviour is unstable**: the estimate of the current cycle position, which
  is the only estimate we actually need, revises heavily as new data arrives. A signal that
  changes its historical values every month cannot be backtested honestly.
- The smoothing parameter λ is conventional (1600 for quarterly data), not derived.

The endpoint problem alone disqualifies it. We need to know the cycle phase *today*, and
the HP filter is least reliable exactly there.

### 1.2 What we use instead

**The Hamilton regression filter** (Hamilton 2018) is the default. It is a simple
regression of the value at t+h on the values at t, t−1, t−2, t−3:

```
y[t+h] = β0 + β1·y[t] + β2·y[t-1] + β3·y[t-2] + β4·y[t-3] + v[t+h]
cycle[t+h] = residual v[t+h]
```

with h = 8 quarters for business-cycle frequencies and h = 20 quarters for financial-cycle
frequencies. Its virtues are exactly the ones we need: no spurious cycles, no endpoint
revision (it is a one-sided filter by construction), and no arbitrary tuning parameter
beyond h, which is chosen by the economics rather than by fit.

**Band-pass filters** (Baxter–King 1999; Christiano–Fitzgerald 2003) are used for
descriptive work — isolating the 8–30 year financial-cycle band to characterise it — but
never for live signals, because BK is two-sided (it uses future data) and CF's asymmetric
variant still revises at the endpoint. The rule is absolute: **any two-sided filter is a
research tool, never a signal.**

**The BIS credit-to-GDP gap** deserves special mention as the exception that proves the
rule. It uses a one-sided HP filter with λ = 400,000, and we use it *as published by the
BIS* rather than recomputing it — precisely because the published vintage series gives us
what a recomputation cannot: the value as it was known at the time.

### 1.3 Frequency-domain methods

Used for characterisation, not for signals:

- **Spectral analysis** to test whether a claimed periodicity actually has power at that
  frequency. Granger's (1966) "typical spectral shape" result — that economic variables
  have most of their power at low frequencies with no sharp peaks — is itself the strongest
  general argument against discrete cycle theories, and any claimed cycle should be checked
  against it.
- **Wavelet analysis** (Aguiar-Conraria & Soares) for time-varying periodicity, which is
  genuinely useful here because cycle length is not constant — a credit cycle can run 7
  years or 20. Wavelet coherence between credit growth and equity returns is a legitimate
  descriptive exercise.
- **Singular Spectrum Analysis** and **Empirical Mode Decomposition** as robustness checks
  on decomposition, never as primary.

The honest caveat: with 25 years of Indian data, the frequency resolution at the low end is
so poor that spectral evidence for anything longer than ~8 years is uninformative. We say
so rather than reporting a peak.

---

## 2. Estimating the current phase

Knowing a cycle exists is not the same as knowing where we are in it. Phase estimation is
the harder problem and the one that actually drives allocation.

### 2.1 Markov-switching models, and their identifiability limit

Hamilton's (1989) Markov-switching model is the canonical approach: the series is generated
by one of K regimes, regime evolution follows a Markov chain with transition matrix P, and
the output is a **filtered probability of each regime at each date** — which is exactly the
"phase as a distribution, not a point" that the design requires.

**But it must be identifiable.** A two-regime model on a single series requires estimating
2 means, 2 variances and 2 transition probabilities — 6 parameters — and needs a
meaningful number of *observed transitions*, not merely a long series. India's credit cycle
offers perhaps 3 transitions in 25 years. **A Markov-switching model on Indian credit data
alone is not identifiable, and fitting one would produce parameters driven by noise.**

We therefore apply a hard rule:

> A regime-switching model may be fitted only where at least **10 regime transitions** are
> observed in the estimation sample. Below that threshold, we use a rule-based scorecard
> with thresholds set from theory and cross-country evidence, not from Indian data.

In practice this means: Markov-switching is permitted for volatility regimes and for
monthly-frequency growth/inflation regimes pooled across countries; it is **forbidden** for
the credit cycle, the capex cycle, the property cycle, and everything longer.

### 2.2 Rule-based scorecards — the workhorse

For every cycle that fails the identifiability test, phase is estimated by a transparent
scorecard: a set of indicators, each mapped to a −1..+1 score by a threshold rule whose
levels come from theory or cross-country evidence, then averaged with theory-set weights.

This is deliberately less sophisticated than a fitted model, and that is the point. A
scorecard has **no free parameters estimated from the outcome we are predicting**, so it
cannot overfit. Its thresholds are pre-registered and versioned in `config/cycles.yaml`, and
changing one is a reviewable event with a written justification.

### 2.3 State-space models and the Kalman filter

Where a cycle has a latent state with multiple noisy indicators, a state-space
representation with the Kalman filter is the natural tool: it produces a filtered estimate
of the latent state *and its variance*, which maps directly to our requirement that phase
carries an uncertainty band. Used for the nominal-growth nowcast, where many
high-frequency indicators (GST collections, IIP, PMI, credit growth, e-way bills) are noisy
measurements of one latent quantity, with different publication lags — a problem the
Kalman filter handles natively via missing-observation updates.

### 2.4 The cross-country pooling trick

This is the most important methodological device in the project, and it is what makes the
mid- and long-cycle layers estimable at all.

India has 1.5 credit cycles. The Jordà–Schularick–Taylor Macrohistory Database has 18
advanced economies from 1870, giving on the order of 150–250 country-cycles. **A credit-cycle
phase classifier estimated on that panel and then applied to Indian indicators has a real
statistical foundation, where one estimated on Indian data alone has none.**

The method: fit the relationship on the international panel with country fixed effects,
using variables that are comparable across countries (credit-to-GDP gap, real credit growth,
property-price gap, real rate deviation), and validate it out-of-sample on countries held
out of the fit. Then apply the fitted rule to India as an out-of-sample country.

The honest caveats, which must be reported wherever this is used:

- India in 2026 is a middle-income economy with a different financial structure from the
  advanced economies in the panel. External validity is an assumption, not a fact.
- Cycles are correlated across countries, so 200 country-cycles are **not** 200 independent
  observations. The effective sample is far smaller — cluster standard errors by year, and
  treat the effective N as closer to the number of global cycles than to the raw count.
- Where emerging-market data exists (the IMF and BIS EM panels are shorter but more
  relevant), fit on both and report both.

---

## 3. Predictive regressions and their pathologies

Most of our slow signals amount to a predictive regression: does variable X today predict
returns over the next h periods? This is among the most treacherous exercises in empirical
finance, and every one of the following traps has produced published results that later
failed out of sample.

### 3.1 Stambaugh bias

When the predictor is persistent (dividend yield, PE, credit-to-GDP — all of ours) and its
innovations are correlated with returns, the OLS coefficient is **biased upward in small
samples** (Stambaugh 1999; Nelson & Kim 1993). The bias is approximately

```
E[β̂ - β] ≈ -(σ_uε / σ_u²) · E[ρ̂ - ρ]
```

where ρ is the predictor's autocorrelation. Since ρ̂ is itself downward-biased, and σ_uε is
typically strongly negative for valuation ratios, the return-predictability coefficient is
inflated.

**Remedy, applied to every persistent-predictor regression:** report the bias-adjusted
coefficient, and compute p-values by bootstrap under the null of no predictability with the
predictor's autocorrelation preserved. Never report a raw OLS t-statistic for a persistent
predictor.

### 3.2 Overlapping observations

Predicting 5-year returns from 25 years of monthly data does not give 300 observations; it
gives roughly 5 independent ones. Overlapping windows induce severe serial correlation, and
naive standard errors overstate significance by a factor that grows with the horizon.

**Remedies, in order of preference:**
1. Report the number of **non-overlapping** windows alongside every long-horizon result. If
   that number is under 5, the result is descriptive and is labelled as such.
2. Use **Hodrick (1992) standard errors**, which are better behaved than Newey–West in this
   setting.
3. Newey–West with lag = 1.5 × horizon as a cross-check, never as the primary.
4. Valkanov (2003) shows that long-horizon t-statistics do not converge to standard
   distributions when the horizon grows with the sample; use his rescaled t/√T statistic
   for long-horizon claims.

**Standing rule:** no long-horizon predictive result enters the model on statistical
significance alone. It must also have a mechanism and cross-country support.

### 3.3 The Goyal–Welch problem

Goyal & Welch (2008) tested essentially every published equity-premium predictor out of
sample and found that almost none beat the historical mean forecast. This is the single most
important negative result in the field and it constrains our valuation layer directly.

The constructive responses we adopt:

- **Campbell & Thompson (2008):** impose economically motivated restrictions — set a
  negative equity-premium forecast to zero, and constrain coefficient signs to theory. These
  restrictions materially improve out-of-sample performance.
- **Rapach, Strauss & Zhou (2010):** **combination forecasts** — a simple average of many
  individual predictors — consistently beat individual predictors out of sample. This
  directly justifies our composite-score architecture over any single-signal timing rule.
- Report **out-of-sample R²** against the historical mean benchmark, not in-sample R². An
  in-sample R² is not evidence.

### 3.4 Cross-sectional regressions

For stock-level signals, the standard is **Fama–MacBeth (1973)**: run a cross-sectional
regression each period, then test the time-series mean of the coefficients. With the
corrections that matter:

- Fama–MacBeth standard errors do not correct for cross-sectional correlation in residuals;
  follow Petersen (2009) and cluster by time, or use both time and firm clustering where
  panel structure warrants.
- Winsorize characteristics at the 1st/99th percentile before regressing; Indian small-caps
  produce extreme ratios that otherwise dominate the fit.
- Report both the raw and the sector-neutralised version. A signal that only works because
  it is a disguised sector bet should be known to be one.

---

## 4. Shrinkage, regularisation and the small-sample regime

With 25 years of data and hundreds of candidate parameters, unregularised estimation is
guaranteed to overfit. Shrinkage is not optional.

- **Covariance:** Ledoit–Wolf shrinkage toward a structured target as the default. For a
  750-name universe with fewer usable daily observations per name than names, the sample
  covariance is singular and unusable. A factor-model covariance (statistical PCA on 10–20
  components, or a fundamental factor model) is the alternative; we use factor-model
  covariance for risk decomposition and Ledoit–Wolf for optimisation inputs.
- **Signal weights:** shrink toward equal weight. DeMiguel, Garlappi & Uppal (2009) showed
  the naive 1/N portfolio beats optimised portfolios out of sample across many datasets,
  because estimation error swamps the optimisation gain. The practical implication for us:
  **the prior for combining signals is equal weight, and any deviation must be justified.**
- **Coefficients:** ridge rather than lasso where predictors are correlated (which ours are
  — the whole aliasing problem). Lasso's variable selection is unstable under
  multicollinearity and will select a different signal each refit, which is
  indistinguishable from noise.
- **Bayesian shrinkage toward theory:** where a coefficient's sign and rough magnitude are
  known from theory or from the international panel, use that as the prior mean, with prior
  variance reflecting how confident the theory is. This is the formal version of "don't let
  25 years of Indian data overturn 150 years of cross-country evidence".

---

## 5. Validation and multiple testing

### 5.1 Cross-validation for time series

Standard k-fold CV is invalid on serially correlated data with overlapping labels. We use
López de Prado's (2018) framework:

- **Purging:** remove from the training set any observation whose label period overlaps the
  test set.
- **Embargo:** additionally drop a buffer after the test set to prevent leakage through
  serial correlation. Embargo length = the label horizon.
- **Combinatorial Purged CV** for generating multiple backtest paths rather than a single
  historical path, which gives a distribution of outcomes instead of one number.
- **Walk-forward** with expanding windows as the primary reported result, because it is the
  only scheme that mimics live operation.

### 5.2 Multiple-testing control

This is where most quant projects quietly fail. The discipline:

- **Log every backtest run.** An append-only trial register recording the hypothesis, the
  parameters, the date, and the result — written *before* the result is seen. Without a
  known trial count, no deflation is possible and no result is interpretable.
- **Harvey, Liu & Zhu (2016)** show that with the number of factors tested in the
  literature, a t-statistic of ~3.0 rather than 2.0 is the appropriate threshold for a new
  factor. We adopt **t > 3.0** as the bar for any new signal, and higher where the trial
  count is large.
- **Deflated Sharpe Ratio** (Bailey & López de Prado 2014): adjusts the observed Sharpe for
  the number of trials, the skew and kurtosis of returns, and the sample length. Reported
  for every strategy variant.
- **Probability of Backtest Overfitting** via combinatorially symmetric CV: the fraction of
  splits where the in-sample-best configuration underperforms the median out of sample. A
  PBO above ~0.5 means the selection procedure has no skill.
- **White's Reality Check (2000)** and **Hansen's SPA test (2005)** where a best-of-N
  selection is being made.
- **Clark–West (2007)** for comparing nested forecast models, since Diebold–Mariano is
  mis-sized for nested comparisons.

### 5.3 The pre-registration protocol

Operationally, the single most effective anti-overfitting device is procedural rather than
statistical:

1. Write the hypothesis, the exact signal definition, the parameter values, and the success
   criterion into `research/register/` **before** running the backtest.
2. Run it once.
3. Record the result against the registration.
4. **A rejected hypothesis may not be re-tested with tweaked parameters.** If a variant is
   genuinely warranted, it is a new registration and it increments the trial count.

This is the rule that costs the most to follow and saves the most.

### 5.4 The point-in-time haircut

Because our fundamentals are restated rather than true point-in-time, backtested
fundamental signals carry a known upward bias: the data reflects what companies *later said*
their financials were, and restatements systematically remove bad news. Every backtest using
lag-approximated fundamentals is labelled as such, and results are reported alongside a
**price-only variant** — a version of the strategy using only price and volume data, which
has genuine point-in-time integrity. The gap between the two is an upper bound on how much
of the apparent alpha could be a data artefact.

---

## 6. Signal construction standards

Applied uniformly, so that signals are comparable and composable:

| Step | Rule |
|---|---|
| **Outliers** | Winsorize at 1st/99th percentile cross-sectionally, or ±3 MAD for time series |
| **Normalisation** | Cross-sectional rank → normal score for stock signals; expanding-window z-score for macro signals (never full-sample, which leaks) |
| **Missing data** | Explicit: neutral score (0) plus a missingness flag; never mean-imputed, which fabricates information |
| **Lag** | Fundamentals lagged by a fixed conservative number of days from period end; macro lagged by its actual publication delay |
| **Neutralisation** | Report raw and sector-neutral; the book is deliberately sector-active so the sector tilt is a separate explicit decision, not an accident of stock scores |
| **Smoothing** | Slow signals use an exponential smoother whose half-life is a stated fraction of the cycle period; fast signals are unsmoothed but subject to no-trade bands |
| **Combination** | Equal weight within family by default; family composites via first principal component or theory weights; deviations require written justification |

---

## 7. What we will not do

- **No neural networks or gradient boosting on 25 years of data for return prediction.** Gu,
  Kelly & Xiu (2020) show machine learning helps in US equities — with 60 years, thousands of
  stocks and clean point-in-time data. We have a quarter of the history and worse data. The
  capacity of these models to fit noise exceeds our ability to detect that they have.
  *Permitted exception:* ML for non-return tasks where labels are objective — text
  extraction from filings, entity resolution, data-quality anomaly detection.
- **No optimisation of thresholds against portfolio outcomes.** Thresholds come from theory,
  from distributional percentiles, or from cross-country evidence. The moment a threshold is
  tuned to maximise backtest Sharpe, it stops being a threshold and becomes a fitted
  parameter that must be counted in the trial register.
- **No in-sample performance reported as evidence.** Out-of-sample or nothing.
- **No "the model would have worked if not for" adjustments.** A failed backtest is a
  result, and it goes in the register.

---

## 8. The reported-result template

Every signal that enters the model carries this record, and no signal enters without it:

```yaml
signal_id: credit_gap_bis_india
hypothesis: "Elevated credit-to-GDP gap predicts lower forward 3y equity returns
             and higher drawdown risk"
registered: 2026-09-14
mechanism: "Minsky/Borio financial cycle; credit booms precede banking stress"
estimation:
  method: rule_scorecard          # not fitted — thresholds from BIS/JST panel
  fitted_on: JST_panel_18_countries_1870_2020
  applied_to: India_out_of_sample
  transitions_observed_india: 2   # below the 10-transition bar -> no MS model
validation:
  oos_r2_vs_mean: <value>
  non_overlapping_windows: <n>
  t_stat: <value>                 # bar is 3.0
  deflated_sharpe: <value>
  pbo: <value>
  trials_to_date: <n>
data:
  source: BIS credit-to-GDP gap (published vintage series)
  pit_integrity: true             # BIS publishes vintages
limits:
  max_influence_pp: 8
  evidence_tier: B
  min_dwell_months: 12
```

---

*References consolidated in `03-BIBLIOGRAPHY.md`.*
