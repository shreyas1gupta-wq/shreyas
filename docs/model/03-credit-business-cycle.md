# Layer 03 — Structural Mid-Cycles: Credit, Capex, Bank Balance Sheets and Real Estate (7–25 years)

**Abstract.** This layer owns the `india_credit_financial_cycle` (bucket B2, `tau_half` = 48m) and everything that is genuinely the same force measured under a different name: the corporate capex/Juglar swing, the NPA/bank-balance-sheet echo, and the housing-and-CRE credit leg. It rejects four things the brief invited: a standalone 18-year real-estate clock (L01 already cut it — one Indian observation), a demographic-dividend signal with allocation authority (L02 owns the arc; a 15-year cohort trend cannot inform a quarterly rebalance), a financialisation signal (same reason), and a commodity supercycle (L06's). What it adds instead is (i) a **deepening-adjusted credit gap** that fixes the well-known upward bias of the raw BIS gap for a rapidly financialising economy, (ii) a credit aggregate built on the **total flow of resources to the commercial sector** rather than bank credit alone — because bank credit alone would have missed IL&FS entirely — and (iii) a six-phase classifier that emits a **probability distribution, never a label**. On the identifiability question the answer is explicit and negative: India offers ~2.4 independent credit-cycle traversals since 1996, a 6-state Gaussian HMM needs ~60 free parameters, so Baum–Welch estimation is **prohibited in code, not merely discouraged**. What is retained is the HMM *filter* — a forward recursion over a hand-declared, git-frozen transition matrix with archetype emissions, likelihood tempering at γ = n_eff/(n_eff+4) = 0.375, and a hard cap of 0.55 on any single phase's posterior. The consequence is deliberate and stated: this layer can only ever use ~60% of its nominal ±10/+8pp equity budget from the classifier alone, and it hands the unused headroom back rather than rescaling into it. Two frozen assumptions are challenged in §12: the debt sleeve's 6% worst drawdown is a mid-cycle number that understates a credit bust by roughly 3x, and the registry's 8-year minimum de-risking traverse is unworkable against a 2008-speed unwind.

---

## 1. Scope, and the five boundaries that stop double-counting

L01 §6 forbids ten measurements of one force becoming a ten-times bet. The DAG handles it arithmetically; this section handles it definitionally. **A variable belongs to exactly one layer.**

| Variable / concept | Owner | This layer's use | Why |
|---|---|---|---|
| BIS credit-to-GDP gap, credit stock, credit impulse | **L03 (mine)** | Budgeted, core | The parent of the credit family in L01's DAG |
| Bank GNPA, SMA-2, credit cost, CRAR, provisioning | **L03** | Budgeted, core | `npa_provisioning_cycle` is my declared child |
| OBICUS capacity utilisation, GFCF/GDP, project sanctions, IIP **capital goods** | **L03** | Budgeted (M-axis + sector) | `juglar_fixed_investment` is my declared child |
| Housing + commercial-real-estate credit, real house prices | **L03** | Budgeted, inside the composite | L01 cut the 18y clock; the *credit leg* survives as my indicator |
| IIP **general**, GVA, GST, e-way bills, repo rate, CPI | **L04** | Not used | L04's business/policy/inflation cycles. I never read the repo rate |
| Corporate profit share of GDP, market-cap/GDP, long-run valuation | **L05** | **Classifier input only, zero budget** (§6.2) | L05 holds the allocation authority on profit-share reversion |
| Commodity supercycle, oil, REER, global liquidity | **L06 / L04** | Consumed as an archetype conditioner (§6.3) | Terms-of-trade is theirs; I only let it shift my late-expansion threshold |
| Demographic arc, household financialisation, development arc | **L02** | **Zero budget. Enters only through GDP-per-capita in my frontier fit** | A 60-year arc with `min_dwell` 45–84m cannot move a quarterly book twice |
| Small-cap breadth (3–5y clock) | **L09** | Residualised against; `beta_prior` = 0.40 requested | Mine is the 8–16y credit conditioning of size, not the breadth clock |
| Final sector weights, name weights | **L09 / L11 / L14** | I emit a tilt *vector*; they own the blend | `name_L1_pp = 0` for B2 by registry |
| Fast vol/funding de-risking | **L18** | Unbudgeted veto (R7) sits above me | I am a quarters-ahead signal, not a crash stop |

**The classifier-input rule.** A variable may feed my *phase posterior* without carrying my *allocation budget*. Profit share enters the L-axis at weight 0.15 within a composite that is itself 0.85 of L — an effective 12.75% loading — and contributes nothing separately to equity weight. This is the only legitimate form of sharing, and L01's cluster audit (§6.4) is the safety net if the residual correlation to L05 exceeds ρ = 0.50.

**Ceded outright.** Demographics and financialisation are *not* signals in this layer. India's working-age share peaks around 2036–41 [verify: UN WPP 2024 revision] and that fact is already true, already known, and already in L02's frozen constant `A = 1.22`. Giving it a second home here would be a pure double-count of a variable that cannot change state inside the model's entire design life.

---

## 2. Mechanism: why these are one force in India, not four

The canonical loop (Kiyotaki–Moore collateral amplification; Borio's financial cycle; Minsky's hedge → speculative → Ponzi progression):

```
bank capital & risk appetite ↑
   → credit supply ↑ → asset & collateral values ↑
      → borrowing capacity ↑ → capex + housing demand ↑
         → capacity utilisation ↑ → profits ↑ → underwriting standards ↓
            → marginal borrower quality ↓  (peak: GNPA at its LOW)
               → shock or rate rise → collateral ↓ → NPAs ↑ → bank capital ↓
                  → credit supply ↓ → capex cancelled → the loop runs backwards
```

Two properties matter for design:

1. **The best-looking indicator is the most dangerous one.** GNPA at a multi-decade low (1.8% in March 2026) is not a statement about future losses; it is a statement that the loans that will go bad were written recently and have not seasoned. GNPA is a *lagging* variable with a 2–3 year lag to the credit that caused it. It belongs in the L-axis as a *lateness* marker, never as a safety marker.
2. **Capex and credit in India are the same series measured twice.** GFCF/GDP and bank credit growth are near-coincident across 2003–08 and 2011–16. L01's worked example already shows `juglar_fixed_investment` residualising to β = 0.55 and 42% retained variance. Hence the MVP decision in §10: capex gets no separate registry cycle, only an M-axis block and a sector channel.

The real-estate leg is a *child*, not a sibling: housing and CRE credit are inside my composite, and Indian house prices are measured too badly and too briefly to carry a clock. Nationally, the RBI HPI rose 4.2% YoY in Q4 FY26 against ~9–10% nominal GDP growth — roughly zero in real terms. There is no national housing bubble in 2026 even though Bengaluru printed +12.7%. A layer that treated Bengaluru as India would be wrong.

---

## 3. The Indian record, dated

Ex-post hand labels. This table is the **ground truth for §11 validation** and must be frozen in git before any classifier is fitted, or it becomes a hindsight device.

| Window | Phase | Markers (numbers marked [v] need verification against source) |
|---|---|---|
| 1996Q2–1998Q4 | late → stress | 1994–96 post-liberalisation credit boom ends; SCB GNPA ≈ 15.7% of advances FY97 [v]; capex stalls |
| 1999–2002 | bust → repair | Corporate deleveraging; GNPA 10–15%; investment rate ~24–26% of GDP; Nifty ≈ −53% Feb-2000→Sep-2001 [v] |
| 2003Q2–2004Q4 | **early expansion** | Non-food credit accelerates past 20% YoY; GNPA falling fast; CU rising off a low base |
| 2005–2006 | mid expansion | Credit 28–30% YoY; GFCF/GDP climbing through 30% |
| 2007–2008Q2 | **late expansion** | Investment rate peaks ~35.6% of GDP FY08 [v]; listed corporate profit ≈ 7.8% of GDP [v]; CU > 80% |
| 2008Q3–2009Q2 | **bust** | Nifty 6,357 → 2,524 ≈ −60%; credit growth halves within four quarters |
| 2009Q3–2010 | early (false start) | Stimulus-led rebound to ~22% credit growth; **the classifier's hardest historical case** |
| 2011–2013Q3 | stress | Stagflation (CPI ~10%), stalled projects, CAD 4.8% of GDP FY13 [v], taper tantrum Aug 2013 |
| 2013Q4–2015Q2 | repair (**false**) | INR and inflation stabilise, but NPAs are *unrecognised* — the indicator set was lying |
| 2015Q4–2018Q1 | stress (recognition) | RBI AQR Oct 2015; GNPA 4.6% → 11.2% peak Mar-2018 [v]; IBC May 2016; demonetisation Nov 2016; ₹2.11 lakh cr recap Oct 2017 |
| 2018Q2–2019Q4 | stress (funding) | **IL&FS default Sep 2018** → NBFC/CP freeze → DHFL 2019; small-caps ≈ −40% with no earnings recession |
| 2020Q1–Q2 | bust | COVID; Nifty 12,430 → 7,511 ≈ −39.6%. **Exogenous — no credit indicator saw it** |
| 2020Q3–2021 | repair → early | Moratorium, ECLGS; corporate deleveraging completes; GNPA falls |
| 2022–2024 | early → mid | Credit 15–16%; GNPA to ~2.8%; capex **public**-led (central capex ₹11.21 lakh cr FY26 BE ≈ 3.1% of GDP) |
| 2025 | mid (soft patch) | Credit decelerates to ~9–10% after the Nov-2023 unsecured/NBFC risk-weight increase; GNPA ~2.3% |
| **2026** | **mid (re-acceleration)** | Risk weights rolled back Apr 2025 + repo cuts; **non-food credit 18.3% YoY (Jun-2026)** vs 9.3% a year earlier; GNPA **1.8%** (Mar-2026), CRAR 17.7%, CET1 15.3%; CU-SA **74.8%**; credit/GDP **97.4%** (Q3-2025) |

**The two lessons the design is built around.** 2013Q4–2015 is the *false repair*: every headline indicator improved while the balance sheet damage was simply unrecognised — which is why SMA-2 and credit cost, not GNPA, are the primary bank-stress inputs post-2015. 2018Q2 is the *non-bank bust*: bank credit growth was ~13% and healthy while the marginal lender froze — which is why the M-axis uses total flow of resources, not bank credit.

---

## 4. Indicator set — definitions and free sources

All sources free. `pit` column: `true` = genuinely vintaged; `lag` = current/restated value with an imposed publication lag; `recon` = we reconstruct.

### Block A — credit stock (the **L** axis: how extended)

| Code | Definition | Free source | Freq / lag | pit | w |
|---|---|---|---|---|---|
| `CGAP_bis` | Credit-to-GDP gap, one-sided HP λ=400,000 | BIS `CREDIT_GAPS`, India (`data.bis.org/topics/CREDIT_GAPS`) | Q / ~150d | true | 0.25 |
| `CGAP_deep` | **Deepening-adjusted gap** (§4.1) | BIS `TOTAL_CREDIT` panel + World Bank `NY.GDP.PCAP.PP.KD` | Q / ~150d | true | 0.30 |
| `CDR` | SCB credit-deposit ratio, 13-week MA | RBI **Weekly Statistical Supplement**, Table 5 (`dbie.rbi.org.in`) | Fortnightly / ~10d | true | 0.15 |
| `HPI_r5` | 5-yr change in real house prices (nominal deflated by CPI-C) | BIS Residential Property Prices for India (FRED `QINN628BIS`); cross-check RBI HPI + NHB Residex | Q / ~120d | true | 0.15 |
| `LEV_corp` | Aggregate debt/equity, non-govt non-financial public ltd cos | RBI annual study *Finances of Non-Government Non-Financial Public Limited Companies* (RBI Bulletin) | A / ~12m | lag | 0.15 |

Overlay: `L = 0.85·z(A-composite) + 0.15·z(PROF_GDP)` where `PROF_GDP` = trailing-4q listed non-financial PAT / nominal GDP, from RBI's quarterly *Performance of Private Corporate Business Sector* release (~2,700 listed non-govt non-financial companies, RBI Bulletin, ~2-month lag). **Classifier input only — L05 owns its allocation authority.**

### Block B — credit flow (the **M** axis: which way)

| Code | Definition | Free source | Freq / lag | pit | w |
|---|---|---|---|---|---|
| `CIMP` | Credit impulse = [ΔCredit₄q − ΔCredit₄q(t−4)] / **trailing-4q** nominal GDP | RBI WSS + MOSPI NAS | M / ~15d | true | +0.25 |
| `TFR` | **Total flow of financial resources to the commercial sector**, YoY − nominal GDP YoY | RBI *Monetary Policy Report* / Annual Report standing table (bank + non-bank domestic + foreign) | H / ~60d | lag | +0.25 |
| `SPRD` | AAA 3y corporate yield − 3y GSec, 13-week change | FBIL / CCIL curves; long history from RBI *Handbook of Statistics on the Indian Economy* | W / ~7d | true | −0.15 |
| `SMA2` | SCB SMA-2 ratio (61–90 dpd), 2-half change | RBI **Financial Stability Report** | H / ~90d | true | −0.15 |
| `dGNPA` | SCB GNPA ratio, 2-half change | RBI FSR + *Trend and Progress of Banking in India* (long history) | H / ~90d | true | −0.20 |

`M_credit = Σ w·z`, `Σ|w| = 1.00`. Signs are set so **+M always means "credit conditions easing"** — consistent with L01's global convention that +1 favours risk assets.

### Block C — real-side capex (25% of M, and the sector channel)

| Code | Definition | Free source | Freq / lag |
|---|---|---|---|
| `CU_SA` | OBICUS seasonally-adjusted capacity utilisation, deviation from own 10y mean | RBI OBICUS quarterly release (`rbi.org.in` → Publications → Survey) | Q / ~120d |
| `GFCF_gap` | Real GFCF/GDP − 10y trailing mean | MOSPI National Accounts, quarterly NAS | Q / ~60d |
| `CAPG` | IIP capital-goods index, 3m/12m ratio | MOSPI IIP | M / ~42d |
| `PROJ` | Cost of new projects sanctioned by banks/FIs, 4q sum YoY | RBI Bulletin, *Private Corporate Investment: Performance and Near-term Outlook* [verify current cadence] | A/Q / ~90d |
| `GCAP` | Central-government capital expenditure, 12m rolling YoY | Controller General of Accounts monthly accounts (`cga.nic.in`) | M / ~30d |

`M_real = 0.35·z(ΔCU_SA) + 0.25·z(CAPG) + 0.25·z(PROJ) + 0.15·z(GCAP)`; `M = 0.75·M_credit + 0.25·M_real`.

### Block D — composition (this cycle's specific risk; §4.3)

`PERS` unsecured personal-loan + credit-card growth, `NBFC` bank credit to NBFCs YoY, `CRE` commercial-real-estate credit YoY — all from RBI **Sectoral Deployment of Bank Credit** (monthly, ~30d lag). Retail delinquency by product from the RBI FSR. TransUnion CIBIL's quarterly *Credit Market Indicator* summary is partially free [verify].

### 4.1 The deepening-adjusted gap — the one non-obvious construction

The raw BIS gap is a one-sided HP filter on a series that has risen from ~35% of GDP in 1990 to 97.4% in Q3-2025. On a trending series the filter's trend lags mechanically, so the gap is **biased positive in any rapidly financialising economy** — the BIS itself flags the buffer guide's weakness for EMs. Using it naked would have this layer permanently late-cycle.

Fix — an exogenous frontier, which also breaks a would-be DAG cycle with L02:

```
Annually, on a ~40-country BIS TOTAL_CREDIT panel (excluding India), fit
    (credit/GDP)_it = a + b·log(GDPpc_PPP_it) + c·log(GDPpc)²  + country RE
Refit with a 5-year embargo; freeze coefficients in git with the fit date.

CGAP_deep_t = (credit/GDP)_India,t  −  fitted(log GDPpc_PPP_India,t)
```

`CGAP_deep` answers "is India over-levered *for its income level*", which is the economically meaningful question, while `CGAP_bis` answers "is credit above its own recent trend", which is the cyclical question. Both are kept, weighted 0.30/0.25. **They disagree right now and that disagreement is informative**: at ~97% of GDP with GDP-per-capita PPP around US$12,000 [verify], India sits roughly *on* the cross-country frontier (`CGAP_deep` ≈ +0.1σ) while the HP gap is turning sharply positive (≈ +0.7σ) because credit is compounding at 18.3% against ~9–10% nominal GDP. Reading: **the flow is hot, the stock is not yet extreme.**

Critically, the frontier is fitted on a *foreign* panel and World Bank income data. It does not read L02's `FINDEEP` composite, so the L02↔L03 relationship stays acyclic: I supply them the 10-year trailing slope of `CGAP_bis` (their contract), they supply me nothing that enters my arithmetic.

### 4.2 Why bank credit alone is the wrong aggregate

In FY19 SCB non-food credit grew ~13% while CP issuance, NBFC bond access and developer funding froze after IL&FS. A bank-credit-only M-axis would have printed *mid-expansion* through the single worst small-cap drawdown of the last decade. `TFR` is the correction and is non-negotiable in the MVP. Its cost is a semi-annual frequency and a ~60-day lag; `CIMP` and `SPRD` carry the higher-frequency load between prints.

### 4.3 This cycle is not the last one, and the indicator set knows it

2026's credit growth is led by services +21.4% (NBFCs, CRE, trade) and personal loans +15.8%, with corporate leverage at 20-year lows. The historical transmission channel — large-corporate capex → large-corporate NPAs → PSU bank capital — is largely absent. Two consequences:

- `LEV_corp` and corporate `GNPA` will **under-read** the risk in this cycle. Block D exists to catch what they miss.
- The stress, when it comes, is more likely to look like 2018 (a funding/NBFC event, fast, non-bank) than 2015 (an asset-quality recognition event, slow, bank). The trigger table (§8) is weighted accordingly: `T1` and `T2` fire on funding, not on GNPA.

### 4.4 PIT and splice hazards — must be handled, not noted

1. **GNPA is not a continuous series.** The Oct-2015 AQR changed what "NPA" meant. Splice: use `GNPA` pre-2015Q3 and `SMA2 + credit cost` post-2015Q3, z-scored within each regime, with the splice date and method in the fixture. Never regress across it.
2. **RBI released a new HPI series in 2026** with a different base and coverage [verify]. Prefer BIS `QINN628BIS` (break-adjusted) as the primary, RBI HPI as a cross-check.
3. **Bust-quarter denominator contamination.** In 2020Q1–Q2 the credit/GDP ratio spiked because GDP collapsed, not because credit grew. Every ratio in Blocks A and B uses a **trailing-4-quarter nominal GDP denominator**, not the spot quarter. This is the difference between reading 2020Q2 as "dangerously extended" and reading it correctly.
4. **Release-date calendar is mandatory.** OBICUS lands ~4 months after quarter-end, the FSR twice a year. A backtest that reads Q2 CU in Q2 is a fiction. The `pit_store` must refuse a read whose `knowledge_date` is after `asof`.

---

## 5. What is deliberately *not* built

`real_estate_long_cycle_18y` (L01: cut, ~1 observation, D5) · `household_financialisation` and `demographic_transition` (L02) · `commodity_supercycle` (L06) · a standalone `juglar_fixed_investment` registry cycle (folded into M and sector) · unsold-housing-inventory (Knight Frank/ANAROCK are paid or partial — **INFEASIBLE**) · rating-bucket credit-spread history (**INFEASIBLE** free; `SPRD` uses the AAA–GSec spread only).

---

## 6. The phase classifier

### 6.1 Is a Markov-switching model or HMM identifiable here? No — with arithmetic

| Model | Free parameters | Independent observations available |
|---|---|---|
| 6-state Gaussian HMM, 2-dim observation | 6×2 means + 6×3 covariances + 6×5 transitions = **60** | ≈ 2.4 cycle traversals (1996–2026) |
| 2-state MS-AR(1), Hamilton (1989) | ≈ 9 | 4–5 regime switches |

Quarterly data since 1996Q2 gives 120 rows, but 120 highly autocorrelated rows contain roughly `120 / (0.5 × period_quarters)` ≈ 2.4 independent cycle observations at a ~50-quarter period — exactly L01's `n_eff` shrinkage denominator, and exactly why `india_credit_financial_cycle` carries `n_obs.effective = 2.4`. A 2-state MS-AR would be identified almost entirely by 2008 and 2020, i.e. by two months.

**Decision: Baum–Welch / ML estimation of transition or emission parameters is prohibited, and the prohibition is a unit test** (`test_no_em_fitting`: asserts the transition matrix hash equals the git-frozen value at every backtest step). What is retained is the **forward filter**, whose arithmetic is valid for *any* declared Π. The filter is a smoother with a directional prior, not an estimator. This distinction is the whole design.

To make the honesty testable rather than merely asserted, L16 runs an MS-AR(1) as a **diagnostic** and reports the 95% CI on the persistence parameter. The expectation is an interval spanning roughly [0.3, 0.99]; if it does, that interval *is* the published evidence for the prohibition.

### 6.2 Two axes, six archetypes

The credit cycle traces a counter-clockwise loop in (**L** = stock of imbalance, **M** = direction of flow). Archetype coordinates are **declared from the §3 record and frozen**, not fitted:

| Phase | L* | M* | Value `v_k` | Implied mean dwell | India analogues |
|---|---|---|---|---|---|
| `repair` | −1.10 | −0.30 | **+0.70** | 12.5 q | 2002–03, 2013–14, 2020H2 |
| `early_expansion` | −0.70 | +0.90 | **+1.00** | 10.0 q | 2003–04, 2014–15, 2021 |
| `mid_expansion` | +0.10 | +1.05 | **+0.55** | 10.5 q | 2005–06, 2016–17, 2023–24, **2026** |
| `late_expansion` | +1.15 | +0.35 | **−0.25** | 7.7 q | 2007–08H1, 2018H1 |
| `stress` | +0.95 | −1.05 | **−0.80** | 5.0 q | 2008H2–09, 2011–13, 2018H2–19 |
| `bust` | +0.60 | −1.70 | **−1.00** | 4.3 q | 1998–2001, 2009H1, 2020H1 |

Implied full loop ≈ 12.5 years — inside the claimed 8–16y band and consistent with Drehmann, Borio & Tsatsaronis (2012)'s ~16-year financial cycle. `bust` sits at L* = +0.60 rather than low because the ratio is denominator-contaminated in a collapse even after the trailing-GDP fix; `repair` is the phase where the stock has genuinely worked off.

`v_k` is the phase's favourability to risk assets on [−1, +1]. `repair` is high (+0.70) because the price damage has already happened — 2003, 2009 and 2020H2 were the best Indian entry points of the last 25 years — and `mid_expansion` is only +0.55 because by then the return has been earned.

### 6.3 Emission, transition, tempering, cap

```python
# --- frozen constants (config/l03_phase.yaml, git-tagged, two-signature change) ---
SIGMA_L = SIGMA_M = 0.75
GAMMA   = 0.375          # = n_eff/(n_eff+4), n_eff = 2.4
P_MAX   = 0.55           # hard cap on any single phase posterior
PI = [  # quarterly, DECLARED. rows=from, cols=to, order as in §6.2
 [0.920, 0.060, 0.005, 0.000, 0.010, 0.005],   # repair
 [0.010, 0.900, 0.075, 0.005, 0.010, 0.000],   # early
 [0.000, 0.020, 0.905, 0.055, 0.015, 0.005],   # mid
 [0.000, 0.005, 0.045, 0.870, 0.065, 0.015],   # late
 [0.050, 0.010, 0.020, 0.030, 0.800, 0.090],   # stress
 [0.150, 0.030, 0.005, 0.000, 0.045, 0.770]]   # bust

def step(P_prev, L, M, tau_in_modal_phase, trigger_multipliers):
    Pi = duration_hazard(PI, tau_in_modal_phase)   # see below
    prior = Pi.T @ P_prev

    d2  = ((L - L_star)/SIGMA_L)**2 + ((M - M_star)/SIGMA_M)**2
    lik = np.exp(-d2/2) ** GAMMA                   # tempered emission
    lik = lik * trigger_multipliers                # §8, default all-ones

    post = normalise(prior * lik)
    return confidence_cap(post, P_MAX)

def duration_hazard(Pi, tau):
    # stop the filter getting stuck: if elapsed quarters in the modal phase
    # exceed 1.5x its implied mean dwell, shrink that diagonal by 0.75
    # and redistribute pro-rata across the row's off-diagonals.
    ...

def confidence_cap(P, p_max):
    # bisect eps in [0,1] on  P_f = (1-eps)*P + eps*u  (u = stationary dist of PI)
    # returning the SMALLEST eps with max(P_f) <= p_max.
    ...
```

**Why the cap exists and what it costs.** With 2.4 observed cycles, a posterior placing 0.80 on one of six phases is not a belief anyone is entitled to. `P_MAX = 0.55` is an epistemic constraint, stated, not fitted. Its cost is exact and must not be hidden: the achievable range of the exposed signal `s` is roughly **[−0.75, +0.50]** rather than [−1, +1], so the classifier alone can reach only ≈ −6.0 / +4.0 pp of equity against a nominal ±10 / +8 budget. Per L01 §6.2 ("do not renormalise the residual"), the mapping is **not** rescaled to recover the headroom — the unused budget is reported back to L01 so the 3σ aggregation test uses the effective figure, not the nominal one. The `bust` end recovers most of the range because the trigger multipliers (§8) act on the likelihood *before* the cap.

### 6.4 Exposed signal, and a sign-convention bug in the registry

```
s_credit = Σ_k P_k · v_k        ∈ [−1, +1],  +1 = favourable to risk assets
```

`config/cycle_registry.yaml` currently sets `india_credit_financial_cycle.gain.k_pp_per_unit = −1.50`, and L01 §6.3's worked example uses `z_raw = +1.60` to mean *late-cycle*. That is the opposite of the file's own stated `SIGN_CONVENTION: +1 ALWAYS means "phase historically favourable to risk assets"`. **Registry patch requested (§13):** this layer exposes `s_credit` in the favourability convention with a positive gain. Left unpatched, this layer's equity call arrives at the optimizer with the sign inverted — a silent, catastrophic, and entirely plausible bug.

### 6.5 Worked example — 28 August 2026

Inputs (z-scores, from §3's 2026 row; each marked [verify] against the live store):

| Axis | Components | Value |
|---|---|---|
| **L** | `CGAP_bis` +0.7 (0.25), `CGAP_deep` +0.1 (0.30), `CDR` +1.2 (0.15), `HPI_r5` −0.6 (0.15), `LEV_corp` −1.2 (0.15) → A = +0.115; `PROF_GDP` +0.8 (0.15 overlay) | **+0.22** |
| **M** | `CIMP` +1.6, `TFR` +1.2, `SPRD` 0.0, `SMA2` −0.4, `dGNPA` −1.0 → M_credit = +0.96; M_real = +0.59 | **+0.87** |

Tempered likelihoods `ℓ^0.375`: repair 0.354 · early 0.754 · **mid 0.985** · late 0.685 · stress 0.245 · bust 0.105. With a mid-heavy prior (0.02, 0.08, 0.72, 0.12, 0.04, 0.02), the raw posterior is mid = 0.814 — which trips the cap (ε = 0.430), giving:

| | repair | early | mid | late | stress | bust |
|---|---|---|---|---|---|---|
| **P(phase), 28-Aug-2026** | 0.108 | 0.121 | **0.550** | 0.118 | 0.062 | 0.040 |

`s_credit = +0.38`. **Aggressive book: equity +3.0pp, gold −0.9pp, debt −2.1pp, leverage ceiling 1.37x.**

**The narrative read, stated plainly.** India in 2026 is mid-expansion with the flow running well ahead of the stock and well ahead of the real economy: credit compounding at 18.3% against ~9–10% nominal GDP, capacity utilisation only ~1pp above its long-run average, private capex still ~12% of GDP, house prices flat in real terms. The imbalance is not yet in the stock — it is in the *composition*. Services credit +21.4% led by NBFCs, CRE and trade, with unsecured personal at +15.8%, against GNPA at a multi-decade 1.8% low, is the 2017–18 signature, and 2017–18 ended in September 2018. The layer is therefore modestly long and explicitly *not* adding. The named watch condition is in §8 as `T7`.

---

## 7. Mapping to the portfolio

### 7.1 Asset weights (post-tier, tier-B multiplier `m = 0.60`)

```
equity_pp = clip( m · (16.7·s if s<0 else 13.3·s), −10, +8 )      # aggressive
equity_pp = clip( m · (13.3·s if s<0 else 11.7·s),  −8, +7 )      # moderate
gold_pp   = clip( m · (6.7·(P_stress+P_bust) − 3.3·(P_early+P_mid)), −2, +4 )
debt_pp   = clip( −(equity_pp + gold_pp), −8, +10 )
```

The coefficients are set so the budget binds exactly at |s| = 1. **Residual routing rule:** when `debt_pp` clips at +10, or whenever `P(stress) + P(bust) ≥ 0.35`, the de-risked capital goes to **true cash / T-bills, not the 10% credit sleeve** — see §7.5 for why.

Realised by phase (aggressive, pure-phase corners, before the confidence cap):

| Phase | equity pp | gold pp | debt pp | leverage ceiling |
|---|---|---|---|---|
| repair | +5.6 | −2.0 | −3.6 | 1.50x |
| early_expansion | +8.0 | −2.0 | −6.0 | 1.50x |
| mid_expansion | +4.4 | −2.0 | −2.4 | 1.40x |
| late_expansion | −2.5 | 0.0 | +2.5 | 1.25x |
| stress | −8.0 | +3.2 | +4.8 → **cash** | 1.10x |
| bust | −10.0 | +4.0 | +6.0 → **cash** | 1.00x |

### 7.2 Sector tilts — pp of NAV vs benchmark, L1 ≤ 8 (agg) / 6 (mod)

Emitted as a *vector* to L09, which owns the blend against sector momentum, sector PE and sector growth. Aggressive figures; moderate = ×0.75.

| Sector | repair | early | mid | late | stress | bust |
|---|---|---|---|---|---|---|
| Banks (private, well-capitalised) | +1.5 | +2.0 | +1.0 | −0.5 | −1.0 | −1.5 |
| Banks (PSU) / NBFC | −1.0 | +1.5 | +1.0 | −1.0 | **−2.0** | **−2.0** |
| Industrials / capital goods | 0.0 | +1.5 | +1.5 | 0.0 | −1.0 | −1.5 |
| Materials (metals, cement) | −0.5 | +1.5 | +1.0 | −0.5 | −1.0 | −1.0 |
| Real estate | −0.5 | +1.0 | +1.0 | −0.5 | −1.5 | −1.5 |
| Auto / consumer discretionary | 0.0 | +0.5 | +0.5 | 0.0 | −1.0 | −1.0 |
| Consumer staples | +1.0 | −1.5 | −1.5 | +1.0 | +2.0 | +2.5 |
| Pharma / healthcare | +1.0 | −1.0 | −1.0 | +0.5 | +1.5 | +2.0 |
| IT services | +1.0 | −1.5 | −1.5 | +1.0 | +1.5 | +2.0 |
| Utilities / telecom | +0.5 | −1.0 | −1.0 | +0.5 | +1.5 | +1.0 |
| **L1** | 7.0 | 13.0 | 11.0 | 5.5 | 14.0 | 16.0 |

Rows are normalised to the L1 budget after the posterior-weighted blend: `tilt = m · Σ_k P_k · tilt_k`, then scaled so `L1 ≤ 8`. The posterior blend alone shrinks L1 substantially — at the Aug-2026 posterior the raw L1 is ≈ 10.4, scaled by `min(1, 8/10.4) × 0.60` → an effective ≈ 4.6pp of active sector risk.

**PSU banks and NBFCs are the sharp end.** They carry the highest credit-cycle beta in both directions: the 2018–19 drawdown was an NBFC funding event, and 2003–07 PSU banks were the single best expression of the upswing. **IT is a joint signal** — my phase term is defensive-in-stress; L06 owns the INR/REER term. I emit only my half, and L09 must not add them twice.

### 7.3 Factor and size tilts — target active exposure, **zero allocation budget**

Emitted as a recommendation vector in units of active factor beta (σ of the cross-sectional factor). L10 owns the translation to names and its own budget. Evidence: the early-recovery "junk rally" — high-beta, high-leverage, low-quality names leading off the trough — is well documented globally and is visible in India in 2003–04, 2009 and 2020H2; the flight to quality/low-vol in 2011–13 and 2018–19 is equally visible.

| Factor | repair | early | mid | late | stress | bust |
|---|---|---|---|---|---|---|
| Value | +0.15 | **+0.45** | +0.15 | −0.10 | −0.30 | −0.10 |
| Quality | +0.30 | **−0.30** | 0.00 | +0.35 | +0.60 | +0.55 |
| Low volatility | +0.20 | −0.35 | −0.15 | +0.20 | +0.50 | +0.60 |
| Momentum | 0.00 | +0.10 | +0.35 | +0.20 | +0.15 | **−0.20** |
| Leverage (high D/E) | −0.10 | +0.25 | +0.10 | −0.20 | −0.45 | −0.50 |
| Size (small tilt) | +0.10 | **+0.40** | +0.25 | −0.25 | −0.55 | −0.60 |

The `bust` momentum entry is negative on purpose: momentum crashes at cycle turns (Daniel & Moskowitz on momentum crashes), and a credit bust is precisely where the turn arrives.

**Size gets a budgeted channel, subject to a registry patch (§13).** The credit cycle is the best-evidenced Indian driver of the small-cap premium — 2018–19 delivered a ~40% small-cap drawdown on a *funding* event with no earnings recession. Requested: `size_tilt_pp` for B2 at ±5pp of the equity sleeve (aggressive) / ±3pp (moderate), residualised against L09's `smallcap_breadth_cycle` with `beta_prior = 0.40`. Phase values (aggressive, pp of the equity sleeve vs benchmark smid weight): repair +2, early +8, mid +5, late −3, stress −8, bust −10, times `m = 0.60`. The moderate book gets half, because at ₹1,000cr the bottom ~250 names of the NIFTY 750 are untradeable and the tilt has nowhere to go.

### 7.4 Leverage — the cheapest drawdown insurance in the stack

`gross_leverage_ceiling_L03 = Σ_k P_k · ceiling_k` from the §7.1 table → **1.37x at the Aug-2026 posterior.** Ceilings compose across layers by `min()`, which is idempotent and therefore cannot double-count — a formal point worth stating, because it is the only case in the whole stack where two layers may speak to the same number without residualisation. The final ceiling is `min(L02_ceiling, L03_ceiling, L18_ceiling)`.

This channel is close to free. It costs +0.06x of forgone leverage in the good phases and removes 0.12–0.50x exactly when equity/credit/gold correlations converge to one. Against the frozen "max drawdown below Nifty 50" objective, running 1.5x gross into a credit bust is the single most reliable way to fail; making the ceiling phase-conditional is the direct answer.

### 7.5 The debt sleeve's credit risk is a credit-cycle output — and DECISIONS.md open item 3 is under-specified

Instrument selection is out of scope, but the *risk of the sleeve* is not: a genuine 10% short-duration Indian return implies AA/A credit, and AA/A credit is the credit cycle. The frozen working assumption (4% vol, 6% worst drawdown, correlation flipping −0.2 → +0.4) is a **mid-cycle** parameterisation. Exposed as `DEBT_SLEEVE_RISK`:

| Phase | E[12m return] | vol | worst DD | corr to equity | max debt weight from L03 |
|---|---|---|---|---|---|
| repair | 10.5% | 4.0% | 5% | −0.15 | 70% |
| early_expansion | 10.0% | 3.5% | 3% | −0.20 | 70% |
| mid_expansion | 9.5% | 3.5% | 3% | −0.10 | 70% |
| late_expansion | 9.0% | 4.5% | 6% | +0.10 | 65% |
| stress | 6.5% | 7.0% | 11% | +0.35 | 50% |
| bust | 3.0% | 10.0% | 18% | +0.50 | 40% |

The bust row is the important one. Indian AA/A paper does not mark down gracefully in a credit bust — it *gates*. Franklin Templeton wound up six debt schemes in April 2020; IL&FS, DHFL, Reliance Capital and the Yes Bank AT1 write-off (March 2020) are the precedents. A realised drawdown in that state includes an illiquidity discount that a 6% assumption does not contain. 18% is an estimate [verify], but the direction is not in doubt, and it is the number that stops the optimizer cornering into the 70% debt cap precisely when the sleeve is most correlated with the equity book.

---

## 8. Being wrong: what forces re-classification, and how fast the book unwinds

Pre-registered in `config/l03_triggers.yaml`, versioned; a backtest at date *t* reads only the version tagged ≤ *t*. Triggers act as **multipliers on the emission likelihood**, before the confidence cap — so a trigger can move the posterior hard without any layer overriding the filter.

| ID | Condition | Free source | Effect |
|---|---|---|---|
| **T1** | A bank or NBFC with > ₹25,000cr borrowings defaults, is placed under moratorium, or enters RBI PCA | RBI press releases; exchange filings | ×3.0 on `stress`, `bust` |
| **T2** | AAA-3y − GSec-3y spread > 150bp for 2 consecutive weeks, **or** the AA−AAA spread widens > 100bp | FBIL / CCIL | ×2.0 on `stress`, `bust` |
| **T3** | 3m-annualised non-food credit growth falls > 500bp below its 12m average for 2 consecutive months | RBI WSS | ×1.6 on `stress` |
| **T4** | System GNPA rises > 40bp over two consecutive half-years after a declining run | RBI FSR | ×1.8 on `stress`; ×0.4 on `early`, `mid` |
| **T5** | An AQR-type recognition exercise is announced (cf. Oct 2015) | RBI | **Not deterioration — information.** Fire L01's trigger slide: `Δτ = +1.5y`, `σ_c` inflation 0.40 rad. We were later in the cycle than we measured |
| **T6** | L04's business-cycle nowcast has been in contraction ≥ 2 quarters while `P(mid) + P(late) > 0.50` | L04 | Cut this layer's influence by 40% until they agree, and log it. A "you are probably wrong" detector |
| **T7** | Non-food credit growth > 16% for 4 consecutive quarters **while** `CU_SA < 76%` **and** the private share of GFCF has not risen | RBI WSS + OBICUS + MOSPI | ×1.5 on `late`; ×0.6 on `mid`. **The named 2017–18-signature watch condition, live in 2026** |

**Unwind speed — and a registry conflict.** `cycle_registry.yaml` currently sets `rate_limit: {max_delta_pp_per_month: 0.104, min_traverse_months: 96}` for this cycle. Symmetric, that means a full −10pp de-risk takes **eight years**. In 2008 the cycle went from late-expansion to bust in roughly three quarters. The rate limit as written is unworkable in the only direction that matters.

Requested asymmetric replacement, and the justification: the cost of being slow to de-risk is a drawdown against a binding drawdown mandate; the cost of being slow to re-risk is forgone return against an aspirational return target.

| Path | Condition | Max Δequity | Full −10pp in |
|---|---|---|---|
| Re-risking (always) | any | **+0.104 pp/m** + min. 2-quarter dwell in the new phase | 96 m |
| Normal de-risking | `P(stress)+P(bust) < 0.45` | −0.104 pp/m | 96 m |
| **Break-glass** | `P(stress)+P(bust) ≥ 0.45` and rising 2 quarters | **−1.25 pp/m** | 8 m |
| **Hard trigger** | T1 or T2 fired within 3 months | **−3.00 pp/m**, decaying to break-glass after 3 m | 3.3 m |

Turnover impact: the OU estimate `1.6·b·√(12/h) = 1.6×10×0.5 = 8.0 pp/yr` matches the registry's B2 budget, but it prices a diffusion, not a jump. A full down-and-back round trip is ~20pp of equity turnover at roughly one per 8 years ≈ +2.5 pp/yr of event turnover. Requested B2 turnover budget: **10.5 pp/yr** (aggressive), 8.4 (moderate) — still ~16% of the aggressive book's 65.4 pp/yr total.

**What forces a re-classification without a trigger:** nothing. The filter is continuous and the posterior migrates on its own. There is no manual re-labelling channel, deliberately — a human "we are clearly late-cycle now" override is exactly the hindsight device §6.1 is built to prevent. Stage 2 may only nominate a *pre-registered* trigger, per L01's interface contract.

---

## 9. Interfaces

**Consumes**

| From | Object | Constraint |
|---|---|---|
| L17 data pipeline | `pit_store(series, asof)` | Release-date calendar enforced; a read whose `knowledge_date > asof` raises |
| L01 taxonomy | `orthogonalize()`, `influence_budget('india_credit_financial_cycle', book)`, `resolve()` | I am the credit-family **parent**; retained variance = 1.0 |
| L04 macro regime | `business_cycle_nowcast{state, quarters_in_state}` | **T6 only.** I never read IIP-general, GVA, GST, repo or CPI |
| L05 valuation | `profit_share_gdp_z` | **Classifier input only**, weight 0.15 in L. No separate budget |
| L06 external | `commodity_supercycle_state`, `oil_shock_flag` | Shifts the `late_expansion` L* by +0.15 when commodity state > +1σ. Capped, declared |
| L02 long wave | *(nothing that enters the arithmetic)* | Acyclicity: my frontier is fitted on a foreign panel, not on their `FINDEEP` |

**Exposes**

```python
L03_STATE = {
  'phase_posterior': {'repair':.., 'early_expansion':.., 'mid_expansion':..,
                      'late_expansion':.., 'stress':.., 'bust':..},
  'L': float, 'M': float, 'quarters_in_modal_phase': int,
  's_credit': float,              # [-1,+1], +1 = favourable to risk assets
  'indicator_z': {code: float}, 'triggers_fired': [str],
  'effective_budget_use': float,  # fraction of nominal budget reachable; ~0.60
  'asof': date, 'stale_quarters': int }

L03_ALLOCATION = {'equity_pp','gold_pp','debt_pp','cash_routing_flag',
                  'max_delta_pp_per_month_down','max_delta_pp_per_month_up'}
L03_SECTOR_TILT  = {sector: pp}          # L1 <= 8 (agg) / 6 (mod); to L09
L03_FACTOR_TILT  = {factor: active_beta} # zero budget; recommendation to L10
L03_SIZE_TILT    = {'smid_pp': float}    # subject to registry patch, §13
L03_CONSTRAINTS  = {'gross_leverage_ceiling': float, 'max_debt_weight': float}
DEBT_SLEEVE_RISK = {'e_return','vol','worst_dd','corr_equity'}   # to L14, L18
L03_TO_L02       = {'bis_credit_gap_10y_slope': float}           # their contract
```

**Stage 1 sufficiency.** With Stage 2 switched off, every field above is still produced: the filter runs on data alone and no trigger requires a human. Asserted by the L01 CI test that `resolve()` output is byte-identical with the overlay disabled.

---

## 10. MVP versus deferred

Honest total for the layer ≈ 26 engineer-days. **MVP must fit in 14.**

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Indicator adapters, Blocks A + B | 10 series with release-date calendars, splice handling, trailing-GDP denominators, committed fixtures | 3.0 | ✅ |
| 2 | Deepening frontier | 40-country BIS+World Bank panel fit, coefficients frozen with fit date, 5y embargo | 1.5 | ✅ |
| 3 | L/M composites | z-scoring on expanding windows (never full-sample), weights from §4, `pit=lag_approx` labelling | 1.0 | ✅ |
| 4 | Phase filter | Archetypes, tempered emission, declared Π, duration hazard, confidence cap, `test_no_em_fitting` | 3.0 | ✅ |
| 5 | Portfolio mapping | §7.1–7.4 tables, both books, cash-routing rule, `DEBT_SLEEVE_RISK` | 2.0 | ✅ |
| 6 | Triggers + asymmetric rate limiter | T1–T7 in versioned YAML, break-glass path, arbitration log | 1.5 | ✅ |
| 7 | Historical replay 1996–2026 | Posterior vs the §3 frozen labels; lead/lag at each of 2008, 2011, 2018, 2020; confusion report | 1.5 | ✅ |
| 8 | Registry patches + fixtures + tests | §13 PR against `cycle_registry.yaml` | 0.5 | ✅ |
| **MVP total** | | | **14.0** | |
| 9 | Block C real-side capex, full | `PROJ` scraper, `GCAP` from CGA, capex sector sub-model | 3.0 | ⬜ |
| 10 | Block D composition risk | Sectoral deployment monthly, retail delinquency, CIBIL summaries | 2.5 | ⬜ |
| 11 | `npa_provisioning_cycle` as a separate registry child | Residualised, ±83bps per L01's worked example | 2.0 | ⬜ |
| 12 | Real-estate composite | RBI HPI/NHB/BIS splice, CRE credit, city dispersion | 2.0 | ⬜ |
| 13 | MS-AR identifiability diagnostic | The published evidence for §6.1's prohibition | 1.5 | ⬜ |
| 14 | `long_capex_swing` (Kuznets) stub | Registry row, `status: deferred`, full sourcing | 1.0 | ⬜ |

**The ruthless cut:** Blocks C and D are *deferred as full sub-models* but their three highest-value series — `CU_SA`, `CAPG`, and the sectoral-deployment splits behind `T7` — ship in MVP because they are cheap single-file downloads and they carry the entire 2026 diagnosis. Everything with a scraper attached waits.

---

## 11. Validation — what can and cannot be tested

**Cannot:** a Sharpe ratio for this signal. 2.4 independent traversals. Any Sharpe computed here is a statement about 2008.

**Can, and must:**

1. **Directional replay.** For each of 2008, 2011, 2018, 2020: did `P(stress) + P(bust)` cross 0.35 *before* the equity drawdown began, and by how many months? Reported as a signed lead/lag, not a hit rate. Expected honest result: **2011 yes (~2 quarters), 2018 yes (~1 quarter, largely via T1), 2008 marginal, 2020 no — a clean miss.**
2. **The false-repair test.** Replay 2013Q4–2015 and confirm the classifier is *not* fooled into `repair`+`early` before the AQR. If it is fooled, the SMA-2/credit-cost splice (§4.4) is not doing its job. This is the single most informative backtest in the layer.
3. **Conditional forward returns.** Nifty 500 TRI 1y/3y forward return by modal phase, with block-bootstrap CIs that will be embarrassingly wide. Publish the width.
4. **Ablation.** Bank-credit-only M-axis vs total-flow M-axis over 2018–19. If `TFR` does not change the 2018 call, it has not earned its 60-day lag.
5. **Property tests.** Posterior sums to 1; `max(P) ≤ 0.55` always; monthly Δequity respects the §8 rate limits on every path; transition-matrix hash equals the frozen value; no full-sample statistic reachable from a point-in-time call.

**The 2020 miss is not a bug to be fixed here.** A five-week 39.6% fall with no preceding credit deterioration is outside anything a B2 signal can see. L01 §13.4 already says this; this layer confirms it from the inside and declines to add an epicycle that would have "caught" COVID in-sample.

---

## 12. Risks and constraint conflicts

1. **The registry's de-risking rate limit is unworkable.** `min_traverse_months: 96` symmetric means an 8-year de-risk. 2008 took three quarters. §8 requests the asymmetric replacement; without it this layer contributes nothing to the drawdown objective and should be honestly re-described as a return signal only.
2. **The registry's sign convention is internally contradictory** for this cycle (§6.4). `k = −1.50` with a "heat" z contradicts the file's stated `+1 = favourable`. Unpatched, the equity call inverts.
3. **The debt sleeve's frozen 6% worst drawdown is a mid-cycle number.** In a bust the same AA/A paper gates (Franklin Templeton, April 2020). §7.5 puts the bust figure at ~18% [verify]. If the optimizer runs the 6% number through a credit bust it will hold 70% of the book in the asset that is failing, and the "10% flat return" assumption will have caused the drawdown it was supposed to cushion.
4. **The confidence cap means this layer can never use its budget.** Effective reach is ≈ −6.0/+4.0pp against a nominal ±10/+8. This is correct, not a defect — but L01's 3σ aggregation test should use the effective figure, and someone will eventually propose rescaling. The answer is no, for the same reason L01 §6.2 refuses to renormalise residuals.
5. **The raw BIS gap is biased positive for India** and would keep this layer permanently late-cycle. §4.1 is the mitigation; if the 40-country frontier fit is dropped for time, the layer must be run on `CGAP_bis` with an explicitly widened `SIGMA_L` and a note that it will cry wolf.
6. **This cycle's stress will not look like the last one's.** Retail/NBFC/CRE-led credit growth against 20-year-low corporate leverage means `LEV_corp` and corporate GNPA will under-read. Block D is deferred to v2, which means the MVP is genuinely blind to the most likely form of the next Indian credit event. Stated so it is not discovered later.
7. **`TFR` is semi-annual with a ~60-day lag** — the single most important M-axis input is also the slowest. Between prints the layer leans on `CIMP` and `SPRD`, and `SPRD`'s long free history is the weakest data link in the whole layer [verify: FBIL/CCIL archive depth].
8. **2.4 observed cycles against ~30 declared parameters** (6 archetypes × 2 coordinates, 6 values, 30 transition entries, 15 weights). None are fitted, all are frozen in git, and the two-signature rule is the only defence. It will be tested the first time a frozen archetype looks stupid.
9. **`repair` is the phase most likely to be mis-called**, and it is the highest-`v_k` non-early phase. 2013–15 was a false repair for 18 months. A wrong `repair` call adds risk into a deteriorating balance sheet — the one direction where being wrong is expensive.
10. **Demographics and financialisation, which the brief asked for, are ceded to L02 and carry zero authority here.** If the owner wants a demographic tilt with teeth, the right conversation is with L02's `A` constant, not a second implementation in this layer.

---

## 13. Registry patch requests (PR against `config/cycle_registry.yaml`)

```yaml
india_credit_financial_cycle:
  gain: {target: equity_weight, k_pp_per_unit: [16.7, 13.3],   # [down, up]
         mapping_fn: piecewise_linear, input: s_credit_favourability}  # SIGN FIX §6.4
  rate_limit:
    max_delta_pp_per_month_up:   0.104
    max_delta_pp_per_month_down: 0.104        # 1.25 break-glass, 3.00 on T1/T2
    min_traverse_months_up: 96
    min_traverse_months_down: 8
  influence:
    agg: {..., size_tilt_pp: 5}               # NEW channel, §7.3
    mod: {..., size_tilt_pp: 3}
  turnover_pp_yr: {agg: 10.5, mod: 8.4}       # was 8.0 / 6.4; event turnover
  effective_budget_use: 0.60                  # for L01's 3-sigma test
  indicators: [ ... 10 entries per §4 ... ]

smallcap_breadth_cycle:
  parent_id: [.., india_credit_financial_cycle]   # cross-parent, beta_prior 0.40
```

---

## 14. References

- Borio, C. (2014). *The financial cycle and macroeconomics: what have we learnt?* Journal of Banking & Finance.
- Drehmann, M., Borio, C. & Tsatsaronis, K. (2012). *Characterising the financial cycle: don't lose sight of the medium term!* BIS Working Paper 380. — financial cycle ≈ 16y vs business cycle 1–8y; the ~10pp credit-gap distress threshold.
- Kiyotaki, N. & Moore, J. (1997). *Credit Cycles.* Journal of Political Economy. — collateral amplification.
- Minsky, H. (1986). *Stabilizing an Unstable Economy.* — hedge → speculative → Ponzi.
- Hamilton, J. (1989). *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle.* Econometrica. — the MS-AR whose identifiability §6.1 rejects for India.
- Daniel, K. & Moskowitz, T. (2016). *Momentum Crashes.* Journal of Financial Economics. — basis for the negative `bust` momentum tilt.
- Pandey, R., Patnaik, I. & Shah, A. (2017). Dating business cycles in India. *Indian Growth and Development Review* 10(1). — the three dated recessions used in §3.
- Government of India, *Economic Survey 2016-17*, Ch. 4 — the Twin Balance Sheet framing of 2010–20.
- BIS, *Credit-to-GDP gaps* methodology notes — including the caveat on the buffer guide's reliability in rapidly financialising EMs. [verify exact document title]
- RBI: *Financial Stability Report* (half-yearly) · *Trend and Progress of Banking in India* (annual) · *Handbook of Statistics on the Indian Economy* (annual) · OBICUS quarterly releases · *Sectoral Deployment of Bank Credit* (monthly) · *Weekly Statistical Supplement* · *Performance of Private Corporate Business Sector* (quarterly) · *Private Corporate Investment: Performance and Near-term Outlook* (RBI Bulletin).
- Data portals: `data.bis.org/topics/CREDIT_GAPS` · `data.bis.org/topics/TOTAL_CREDIT` · `dbie.rbi.org.in` · `mospi.gov.in` · `cga.nic.in` · `ibbi.gov.in` · `residex.nhbonline.org.in` · World Bank `NY.GDP.PCAP.PP.KD` · FRED `QINN628BIS`, `CRDQINAPABIS`.

**2026 data points used in §3 and §6.5** (retrieved 28 Aug 2026 via search; all require confirmation against the primary release before use): non-food bank credit +18.3% YoY, fortnight ended 30-Jun-2026 (RBI); SCB GNPA 1.8%, CRAR 17.7%, CET1 15.3% at Mar-2026 (RBI *Financial Stability Report*, Jun-2026); OBICUS CU-SA 74.8% for Q2 FY26; BIS credit to private non-financial sector 97.4% of GDP, Q3-2025; RBI House Price Index +4.2% YoY Q4 FY26; GFCF ≈ 29.6% of GDP (World Bank, 2024), private capex ≈ 12% of GDP.
