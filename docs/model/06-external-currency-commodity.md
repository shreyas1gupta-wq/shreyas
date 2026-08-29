# Layer 06 — External Sector: the Rupee, the Dollar, Crude and Commodities (2–25 years)

**Abstract.** This layer owns everything that reaches the Indian portfolio through the balance of payments: the USDINR cycle, the global dollar cycle, crude oil as India's dominant terms-of-trade variable, the commodity supercycle, and India's external-vulnerability state. Its central analytical claim is an identity, not a forecast: rupee depreciation against the dollar decomposes exactly into an inflation differential, a real (REER) term, and the dollar's own move against the trade basket — and only the first is structural. Measured over five windows the realised drift is **3.0–4.4 %/yr**, not the folk-wisdom 3 %, and essentially **all of it is delivered in six-to-eighteen-month devaluation jumps** (1991, 1995–96, 1998, 2008, 2011–13, 2018, 2022, 2025–26) separated by long quiet stretches at 4–6 % annualised vol. That jump structure, not the drift, is what the portfolio must be positioned for, and it is why a carry-based INR view is a peso-problem trade. The layer emits five machine-readable objects — `INR_STATE` (with a dollar-orthogonalised stress index), `USD_CYCLE`, `OIL_STATE` (with a Kilian-style supply/demand shock classifier, because a demand-driven oil rise is a materially different event for India than a supply-driven one), `COMMODITY_STATE`, and `EXTERNAL_VULNERABILITY` — plus the sector-beta matrix the sector model consumes and the INR-gold decomposition the gold sleeve consumes. The most important single output is the separation of *flow* stress from *solvency* stress: on 28 Aug 2026 the rupee is at an all-time low of ≈95.5 with record FPI outflows, yet the external-vulnerability composite scores **low** — reserves cover 10+ months of imports, the FY26 current-account deficit was 0.6 % of GDP, REER is *below* 100. In 2013 the identical nominal signal came with the opposite balance sheet; conflating the two produces exactly the wrong trade in one of the two years. All indicators are free: RBI DBIE and WSS, PPAC, NSDL, FRED, EIA, World Bank Pink Sheet, IMF PCPS, BIS, LBMA.

---

## 0. Dated snapshot — 28 August 2026

Every number here is a live reading, not a design assumption. Sources in §15; items I could not confirm to a primary source are marked `[verify]`.

| Variable | Reading | Note |
|---|---|---|
| USDINR | **95.5–95.8** (all-time low) | −6.0 % CYTD; FY26 −9.9 %, worst fiscal year in 14 |
| RBI REER, 40-currency (2015-16=100) | **≈98.8** (Jul-26) `[verify]` | **Below** 100 — rupee is *not* overvalued in real terms |
| DXY | **≈99.5** | Below its 200-dma; the dollar is **not** the driver |
| FX reserves | **$716.9 bn** (14-Aug-26), gold $111.4 bn | >10 months import cover |
| CAD, FY26 | **−0.6 % of GDP** ($25.2 bn); Q4FY26 a **+0.7 % surplus** | Externally, India is in good shape |
| Brent | **$88.3** (28-Aug); 52w high **$120.9** (30-Apr-26); Aug range $87–95 | A geopolitical spike, now half-retraced |
| Gold | **$4,454/oz**; record **$5,597** (29-Jan-26) → **−20.4 %** | MCX ≈ ₹1,63,120/10g `[verify basis]` |
| Copper | Record; **>$13,900/t** LME close (11-May-26), intraday >$14,500 (Jan-26) | Structural-deficit narrative |
| FPI equity, CY2026 | **−₹2.2 lakh crore** (≈ −$24 bn), worst year since 1993 | Foreign holding 14.7 %, a 14-year low |
| RBI repo | **5.25 %** (held, Aug-26) | US differential compressed → thin forward premium |

**The configuration in one line:** a *bifurcated* commodity cycle (transition metals at records, hydrocarbons capped and falling), a *weak* dollar, and *India-idiosyncratic* currency stress driven by portfolio outflows rather than the external balance sheet. A rarer state than 2013 or 2022, and it maps to different trades — §9.

---

## 1. Scope, and what this layer must not rebuild

**Owns.** USDINR cycle and stress state · REER/NEER valuation · the global dollar cycle · crude oil (level, shock type, terms of trade, the India oil sector-beta matrix) · the commodity supercycle and the energy-transition overlay · India's external balance, reserves and vulnerability composite · the currency decomposition of INR gold returns.

**Does not own and must not rebuild.**

| Object | Owner | My boundary |
|---|---|---|
| The 25–50-year INR debasement drift, gold *anchor*, reserve-order phase | L02 | L02 states it plainly: "cyclical FX (1–3y) is theirs, the 25y drift is mine". I emit **cyclical** FX and a **measured** structural drift as evidence; I never set `w_gold_anchor` |
| CPI/WPI nowcast, monsoon, food, policy-rate cycle, the *tactical* gold tilt on global real rates | L04 | I hand L04 `oil_shock_flag` and `imported_infl_inputs`; L04 owns pass-through to CPI |
| Credit cycle, capex, bank balance sheets | L03 | I supply `commodity_supercycle_state` and `oil_shock_flag` as archetype conditioners only |
| Aggregate equity valuation | L05 | — |
| FPI/DII flow *cycle* as a positioning signal | L07 | I use FPI flows only as a **BoP financing** and **currency-pressure** input, never as a sentiment or contrarian signal. Declared to avoid double-counting; CI must assert the residualisation |
| Sector scores and final sector weights | L10 | I emit **betas and a tilt vector**; L10 blends them with sector momentum/valuation/growth and owns the result |
| Gold instrument, sizing and implementation | L13 | I emit the return decomposition, the conditional-beta estimator and the duty/basis break table |
| Cash call, de-gearing ladder | L17 | I emit `external_derisk_score`; L17 decides |

*Numbering note:* `docs/ROADMAP.md` numbers the risk engine L17 and the Stage-2 overlay L18; specs 03/04 use L17/L18 for the reverse. I follow the ROADMAP. This drift should be fixed once, centrally.

---

## 2. Data spine — free sources only

| Code | Series | Source (free) | Freq / History | PIT status |
|---|---|---|---|---|
| `USDINR` | RBI reference rate | RBI DBIE `data.rbi.org.in`; FRED `DEXINUS` (1973–) | D / 1973– | **True PIT** |
| `INRFWD1Y` | Forward premia of USD, 1m/3m/6m/12m | RBI DBIE → *Forward Premia of US Dollar* | W-M / 1997– | True PIT |
| `REER40`,`REER6`,`NEER40` | RBI effective exchange rates | RBI DBIE; monthly RBI *Bulletin* table | M / 1993– | **REVISED + REBASED** — see §2.1 |
| `REER_BIS` | BIS broad/narrow REER, 60+ economies | `data.bis.org/topics/EER`; FRED `RBINBIS` | M / 1994– | Revised, but gives the peer cross-section RBI cannot |
| `RES` | FX reserves: FCA, gold, SDR, IMF position | RBI *Weekly Statistical Supplement* | W / 1998–; M / 1950s– | Near-PIT (7d lag, rarely revised) |
| `BOP` | Current account, trade, invisibles, FDI, FPI, basic balance | RBI DBIE BoP tables; RBI quarterly press release | Q / 1990Q2– | **Revised 2–3 q**; ~90d lag |
| `EXTDEBT` | External debt, short-term by residual maturity, debt/GDP | RBI *India's External Debt* (Q); MoF status report (A) | Q / 1990– | Revised; ~90d lag |
| `TRADE` | Monthly exports/imports by commodity, country | `tradestat.commerce.gov.in`; PIB monthly release | M / 1996– | Provisional then revised |
| `OILVOL`,`OILBILL`,`BASKET` | India crude import volume, import bill, **Indian basket price (daily)**, product consumption, retail prices | **PPAC** `ppac.gov.in` | D/M / 1998– | True PIT for basket price |
| `BRENT`,`WTI` | Crude spot | FRED `DCOILBRENTEU` (1987–), EIA API | D / 1987– | True PIT |
| `OILINV` | OECD commercial stocks, US crude stocks, world supply/demand balance, STEO | EIA open data `eia.gov/opendata` (free key) | W/M | Revised (STEO is a forecast — never backtest on the current vintage) |
| `PINK` | World Bank *Commodity Markets* Pink Sheet — ~70 commodities, nominal + real | `worldbank.org/en/research/commodity-markets`, monthly XLSX | M / 1960–; A / 1960– | Revised for MUV deflator only |
| `PCPS` | IMF Primary Commodity Price System; FRED `PCOPPUSDM` (copper), `PALUMUSDM` | imf.org / FRED | M / 1980–90– | True PIT (prices) |
| `DXY`,`BROAD` | FRED `DTWEXBGS` (broad, 2006–), `DTWEXEMEGS`, `DTWEXAFEGS`; DXY via stooq CSV | FRED / stooq | D | True PIT |
| `UST` | `DGS10`, `DFII10`, `DFF`, `SOFR`, `VIXCLS` | FRED | D | True PIT |
| `FPI` | FPI net equity/debt daily + AUC by sector | **NSDL** `fpi.nsdl.co.in/web/Reports/Archive.aspx` | D / 2002– | True PIT |
| `GOLD` | LBMA AM/PM fix USD/oz | `lbma.org.uk/prices-and-data` | D / 1968– | True PIT |
| `MCX` | MCX bhavcopy — gold, silver, crude, copper INR futures | `mcxindia.com/market-data/bhavcopy` | D / ~2005– | True PIT |
| `DUTY` | Gold/silver import duty schedule | CBIC notifications — **must be hand-encoded** (§8.4) | Event | Hand-built table with effective dates |
| `CPI_IN`,`CPI_US`,`CPI_TP` | India CPI (MOSPI, 2012 base), US CPI (FRED `CPIAUCSL`), trade-partner CPI (IMF IFS / OECD) | MOSPI / FRED / IMF | M | India CPI revised 1m |

### 2.1 The REER trap, and the fix

RBI's REER is **revised and thrice rebased** (1993-94 → 2004-05 → 2015-16), with periodic trade-weight updates. The value downloadable today for August 2013 is not what RBI published in August 2013; a backtest reading the current vintage as a real-time overvaluation signal leaks the future.

**MVP fix — build our own.** A fixed-weight REER from raw inputs is fully point-in-time and free:

```
REER_own(t) = 100 · Π_j [ (S_j(t)/S_j(0)) · (P_IN(t)/P_IN(0)) / (P_j(t)/P_j(0)) ] ^ w_j
  S_j  = INR per currency j (RBI/FRED daily, PIT)
  P_IN = India CPI (MOSPI, use the vintage available at t)
  P_j  = partner CPI (FRED/IMF, vintage at t)
  w_j  = trade weights FROZEN at the last DGCIS release available at t, re-struck each April
```
Use the top 12 partners by two-way trade (≈75 % of trade): US, China, UAE, Saudi, Iraq, Singapore, Hong Kong, Korea, Germany, Indonesia, Japan, UK. Publish `REER_own` as the signal and RBI's `REER40` as a **cross-check only**, with a CI test asserting the two track within ±3 points over any 5-year window; a persistent divergence is a bug or a weight change, and either way a human must look.

---

## 3. The USDINR cycle

### 3.1 The identity that organises everything

For a basket of partners *j* with weights *w*:

```
Δlog(USDINR)  =  [π_IN − π_partners]           (A) inflation differential
              −  Δlog(REER_INR)                 (B) real appreciation of the rupee
              +  Δlog(USD vs partner basket)    (C) the dollar's own move
```

(A) is structural and slow. (B) is a Balassa–Samuelson / productivity term, slow and small. (C) is **cyclical, mean-reverting over 7–10 years, and not about India at all**. The single most common analytical error in Indian FX commentary is to read a (C)-driven move as an India story. §3.6 makes the separation mechanical.

### 3.2 Measured drift — five windows, not an assertion

USDINR is a spliced series: official pre-1993, market-determined after the March 1993 unification. Anchor points from RBI/FRED daily reference rates.

| Window | Years | Start → End | Realised CAGR | India CPI − US CPI (approx) | Residual (real term) |
|---|---|---|---|---|---|
| 1993 unification → Aug 2026 | 33.6 | 31.37 → 95.5 | **3.31 %** | ≈4.1 % | −0.8 % (real appreciation) |
| Jan 2000 → Aug 2026 | 26.6 | 43.5 → 95.5 | **2.96 %** | ≈3.6 % | −0.6 % |
| Jan 2005 → Jan 2015 | 10.0 | 43.8 → 62.2 | **3.51 %** | ≈4.5 % | −1.0 % |
| Jan 2010 → Jan 2020 | 10.0 | 45.9 → 71.4 | **4.42 %** | ≈5.1 % | −0.7 % |
| Jan 2016 → Aug 2026 (post-IT) | 10.6 | 66.2 → 95.5 | **3.46 %** | ≈**1.3 %** | **+2.2 % (real depreciation)** |
| Jan 2020 → Aug 2026 | 6.7 | 71.4 → 95.5 | **4.45 %** | ≈1.9 % | +2.5 % |

Three findings the design must respect:

1. **"3–4 %" is a range, not a number, and the recent decade sits at the top of it (4.4 %).**
2. **The sign of the residual flipped after inflation targeting.** Pre-2015 the rupee depreciated *less* than the CPI differential — India ran a real appreciation, the classic catch-up pattern. Post-2016 India's inflation converged toward the US's, yet the rupee depreciated *faster* — a genuine real depreciation of ~2 %/yr. Part of that is term (C): the dollar's 2014–2022 up-cycle. Part is a smaller invisibles/FDI cushion and, since 2025, tariff pressure on Indian exports. **The pure-inflation-differential forecast of 2.0–2.5 %/yr that L02 uses has under-predicted the last decade by roughly 200 bps a year.**
3. This layer's structural prior is therefore **3.0 %/yr (band 2.0–4.0 %)**, the extra 50–100 bps over L02's 2.0–2.5 % attributed explicitly to the residual, not to conviction. Numbered disagreement, logged in §13.

### 3.3 The jump structure — the finding that actually changes portfolio behaviour

The drift is not earned smoothly. Devaluation episodes, peak-to-trough of the rupee:

| Episode | Trigger | Move | Duration | Vol regime |
|---|---|---|---|---|
| Jul 1991 | BoP crisis, 2 weeks' import cover | 21.1 → 25.9, **−18 %** | 3 days (two-step) | Administered |
| Oct 1995 – Feb 1996 | Post-liberalisation reserve pressure | 31.4 → 35.7, **−12 %** | 5 m | 8 % |
| Aug 1997 – Aug 1998 | Asian crisis contagion + Pokhran sanctions | 35.8 → 42.8, **−16 %** | 12 m | 9 % |
| Jan 2008 – Mar 2009 | GFC, dollar funding squeeze | 39.3 → 51.9, **−24 %** | 14 m | 14 % |
| Aug 2011 – Aug 2013 | CAD 4.8 % of GDP + taper tantrum | 44.0 → 68.9, **−36 %** | 24 m | 12–18 % |
| Apr – Oct 2018 | Oil to $86, EM contagion (TRY/ARS) | 64.9 → 74.5, **−13 %** | 6 m | 7 % |
| Feb – Oct 2022 | Fed 425 bp, dollar +19 %, oil to $128 | 74.5 → 83.3, **−11 %** | 8 m | 6 % |
| **Sep 2025 – Aug 2026** | Tariffs, record FPI exit, oil spike to $121 | ≈86 → 95.8, **−11 %** | 12 m | 7–9 % `[verify]` |

Sum of episode moves ≈ 141 log-% over 35 years ≈ **3.6 %/yr** — **the entire long-run drift is delivered inside eight episodes covering ~25 % of elapsed months.** In the other 75 % the rupee is flat to mildly appreciating at 4–6 % vol with positive carry. Three design rules follow:

- **R6-1.** No INR signal may be built as a smooth drift term. The state machine must be able to represent "quiet, carry-positive" and "jumping" as distinct states with different portfolio maps.
- **R6-2.** Backtests of any INR-conditional strategy must report the **episode-excluded** and **episode-only** results separately. A strategy that works only outside episodes is short a fat tail and must be labelled as such.
- **R6-3.** Realised USDINR vol systematically understates risk. Use `max(realised_60d, 8 %)` as the vol input to the optimizer for any INR-denominated exposure, and `18 %` conditional on `INRSI ≥ STRESS`.

### 3.4 REER over/under-valuation

Two measures, deliberately different:

```
REERDEV_trend = 100 · ( REER_own(t) / MA60m(REER_own) − 1 )        # cyclical, MVP
REERDEV_level = REER_own(t) − 100                                   # base-period anchored, informational only
REERDEV_peer  = z_xs( REER_BIS_India(t) / MA60m , across 20 EM peers )   # cross-sectional, deferred
```

`REERDEV_level` is *not* a valuation statement — it is an artefact of the base year. Only the trend and peer forms are used for signalling. RBI's **6-currency** index (USD, EUR, GBP, JPY, CNY, HKD) is the *competitiveness-relevant* one for IT and pharma exporters; the **40-currency** index is the macro-relevant one. Both are consumed; the 6-currency version drives the exporter tilt, the 40-currency version drives the vulnerability composite.

| `REERDEV_trend` | State | Interpretation |
|---|---|---|
| > +8 % | `REER_STRETCHED` | Historically the single most reliable pre-condition of a devaluation episode (2013: +4 % after a +12 % 2010 peak; 1995: +9 %) |
| +3 to +8 % | `REER_RICH` | Competitiveness eroding |
| −3 to +3 % | `REER_FAIR` | **Today (≈−1 %)** |
| < −3 % | `REER_CHEAP` | Exporter margin tailwind; import-cost headwind |

Frankel & Saravelos (2012, *JIE*) find across crisis episodes that **REER overvaluation and reserve adequacy are the two most consistently significant early-warning indicators** — which is precisely why both sit in the composite in §7 and why neither alone is allowed to fire.

### 3.5 Carry, vol and the peso problem

The onshore 1-year forward premium (RBI DBIE) is the carry. Historically 4–6 % through the 2010s; compressed to 1.7–2.5 % in 2022–23 as the Fed–RBI differential collapsed; today, with repo 5.25 % and US policy rates near 4 %+ and rising, the premium is thin.

```
carry_cushion = INRFWD1Y(t) − trailing_5y_realised_depreciation(t)
carry_to_vol  = carry_cushion / max(realised_vol_60d(USDINR), 0.05)
```

| `carry_cushion` | Meaning | Portfolio implication |
|---|---|---|
| > +1.5 pp | Long-INR carry well compensated | Reduce exporter tilt; INR-hedging cheap |
| −0.5 to +1.5 pp | Neutral | — |
| < −0.5 pp | **Crash risk under-compensated — today** | Raise exporter tilt; do not run unhedged INR-funded USD-asset shorts; treat "the rupee is stable" as a peso problem, per Brunnermeier–Nagel–Pedersen (2009), *Carry Trades and Currency Crashes* |

Carry currencies exhibit **negative skew with crash risk rising in accumulated positioning**; the low-vol regime is itself the risk factor. India's capital controls let the onshore premium deviate from CIP, and the offshore NDF leads onshore in stress — but daily NDF history is not free, so the **onshore–NDF spread is INFEASIBLE** and proxied by the onshore premium's deviation from CIP-implied (repo vs SOFR).

### 3.6 The INR stress indicator (INRSI) — definition and thresholds

Weekly. Every input free and PIT.

```python
# z-scores on 10y expanding windows, winsorised at ±4
z1 = z( Δ63d log USDINR )                       # nominal move
z2 = z( realised_vol_20d(USDINR) / median_3y )   # vol regime
z3 = z( Δ13w valuation_adjusted_FCA / FCA )      # reserve depletion  (sign: fall = stress)
z4 = z( INRFWD1Y − CIP_implied(repo, SOFR) )     # forward-premium dislocation
z5 = z( REERDEV_trend )                          # overvaluation pre-condition
z6 = z( 20d cumulative FPI net (eq+debt) / mktcap )   # BoP financing (sign: outflow = stress)
z7 = z( Δ63d log BROAD_DOLLAR )                  # the dollar's own move  (FRED DTWEXBGS)

INRSI_raw  = 0.25*z1 + 0.20*z2 + 0.20*(-z3) + 0.15*z4 + 0.10*z5 + 0.10*(-z6)
beta_usd   = OLS_3y( z1 ~ z7 ).beta              # refit monthly, shrink to 0.5, clip [0, 1.5]
INRSI_idio = INRSI_raw - beta_usd * z7
```

**Valuation-adjusted reserves matter:** much of the weekly FCA move is EUR/GBP/JPY revaluation, not intervention. Approximate composition as USD 60 / EUR 20 / GBP 6 / JPY 6 / other 8 `[verify vs RBI Annual Report reserve-composition table]` and strip revaluation before differencing. Skip this and `z3` is mostly noise.

| INRSI | State | Enter | Exit | Min dwell |
|---|---|---|---|---|
| < −0.50 | `INR_CALM` | −0.50 | −0.20 | 8 w |
| −0.50 … +0.75 | `INR_NEUTRAL` | — | — | 4 w |
| +0.75 … +1.50 | `INR_PRESSURE` | +0.75 | +0.40 | 8 w |
| +1.50 … +2.50 | `INR_STRESS` | +1.50 | +1.05 | 8 w |
| > +2.50 | `INR_CRISIS` | +2.50 | +1.90 | 12 w |

**Calibration targets** — the historical print the implementation must reproduce, asserted as unit tests against fixtures:

| Date | Target state | Target `idio` share | Because |
|---|---|---|---|
| Aug 2013 | `INR_CRISIS` | **high** (>60 %) | Dollar was mid-range; the crisis was India's CAD |
| Oct 2018 | `INR_STRESS` | mixed | Oil + EM contagion |
| Mar 2020 | `INR_STRESS` | **low** (<30 %) | Global dollar funding squeeze; India's balance sheet fine |
| Oct 2022 | `INR_PRESSURE` | **low** | Almost entirely the dollar (DXY +19 %) |
| Jun–Aug 2026 | `INR_STRESS` | **high** | DXY ≈99.5 and falling, rupee at record low — idiosyncratic by construction |

If a candidate weighting fails to reproduce this ordering, the weighting is wrong, not the history. This is the layer's one genuinely falsifiable in-sample test; run it before the weights are frozen in git.

---

## 4. The global dollar cycle

### 4.1 Dating and periodicity

Peak-to-peak on the broad real dollar: **1971 trough → 1985 peak → 1992 trough → 2002 peak → 2011 trough → 2022 peak**. That is roughly 15–17 years peak-to-peak on the *major* swings, i.e. **7–9 years per leg**, which is the "7–10y" the brief refers to. `n_eff` is therefore **3, maybe 3.5** — tier **B at best**, and only because the transmission mechanism (not the periodicity) is well evidenced. Represent as a **state**, never as a circular phase: with three observations a phase estimate is theatre.

### 4.2 Transmission — the evidence

- **Rey (2013, Jackson Hole), "Dilemma not Trilemma"** — a global financial cycle in capital flows, asset prices and leverage, co-moving with VIX and US monetary policy; floating rates do not insulate.
- **Bruno & Shin (2015, *RES*), "Cross-Border Banking and Global Liquidity"** — the risk-taking channel: dollar appreciation tightens intermediary balance-sheet capacity and contracts cross-border lending.
- **Avdjiev, Du, Koch & Shin (2019, *AER: Insights*)** — a stronger dollar co-moves with wider CIP deviations and lower cross-border dollar lending; the dollar is a *global risk factor*, not just a relative price.
- **Obstfeld & Zhou (2022, *BPEA*), "The Global Dollar Cycle"** — broad dollar appreciations are contractionary for EMs: weaker output, tighter financial conditions, capital outflows, and they are associated with a higher incidence of EM crises.
- **Hofmann, Shim & Shin (BIS)** — dollar appreciation widens EM **local-currency** sovereign spreads, the "original sin redux" channel: the FX loss and the credit loss arrive together.
- **Kalemli-Özcan (2019, Jackson Hole)** — US monetary policy spills to EM risk premia far more than to EM policy rates.

India-specific published evidence is thin; the cross-sectional EM evidence carries the tier-B rating.

**Magnitudes to be *estimated*, with priors** — re-estimated by L20 on the assembled free data and shrunk 50 % toward these priors. They are not facts and must not be quoted as such.

| Relationship (monthly, 2006–) | Prior beta | Note |
|---|---|---|
| MSCI EM (USD) → broad dollar | **−1.2** | Widely-observed order of magnitude |
| Nifty 50 (USD) → broad dollar | **−1.0** | Two channels: FX translation + equity |
| Nifty 50 (**INR**) → broad dollar | **−0.35** | Most of the USD-beta is the currency itself |
| FPI net equity flow (% mkt cap) → Δ broad dollar | **−0.40** correlation | NSDL daily, free |
| Gold (USD) → broad dollar | **−0.80** | Real rates dominate, dollar second (L04 owns the real-rate leg) |
| Gold (**INR**) → broad dollar | **−0.30** | The offset that makes INR gold a *better* dollar hedge — §8 |

The last two lines are the quantitative case for the gold sleeve being larger for a rupee investor than the global literature would suggest.

### 4.3 `USD_CYCLE` construction

```python
usd_level_z   = z_10y( log BROAD_DOLLAR )                 # FRED DTWEXBGS, 2006-; splice DTWEXM pre-2006 at growth level
usd_trend_z   = z_10y( Δ12m log BROAD_DOLLAR )
usd_real_z    = z_10y( BIS broad real USD EER )           # slow, the true cycle variable
usd_carry_z   = z_5y( US 2y − G3 2y weighted )            # the driver
USD_CYCLE_Z   = 0.35*usd_real_z + 0.30*usd_trend_z + 0.20*usd_level_z + 0.15*usd_carry_z
```
Sign convention per L01: **+1 = favourable to risk assets**, so the exposed signal is `usd_cycle_signal = −USD_CYCLE_Z`. States with Schmitt-trigger hysteresis at ±1.0 / ±0.6 and a **12-month minimum dwell** (a 7–9 year leg must not flip quarterly):

`USD_STRONG_RISING` · `USD_STRONG_STABLE` · `USD_NEUTRAL` · `USD_WEAK_STABLE` · `USD_WEAK_FALLING` — today: **`USD_NEUTRAL`, trend negative**.

---

## 5. Crude oil — India's dominant external variable

### 5.1 Elasticities

Use the **Indian crude basket** (PPAC, daily, free), not Brent: India's mix is ~Dubai-weighted and the Brent–Dubai spread moves materially in geopolitical episodes. Net volume is what matters — India exports refined products, and the gross bill overstates exposure by ~25 %.

| Channel | Effect of **+$10/bbl** | Source |
|---|---|---|
| **Current account** | **+$12.5 bn ≈ +0.40 % of GDP** (2019 estimate; recomputed on FY26 net volume ≈1.65–1.8 bn bbl and GDP ≈$4.2 trn gives **0.39–0.43 %** — the estimate has held) | RBI *Mint Street Memo* No. 17, Jan 2019 `[verify authors]` |
| **CPI** | **+35 to +49 bps** over 4 quarters, with pass-through; ~+30 bps direct | RBI MSM-17; RBI *Monetary Policy Report* boxes |
| **GDP growth** | **−20 to −25 bps** | RBI MSM-17 |
| **Fiscal deficit** | **+43 bps of GDP** *if* the government absorbs the shock via excise cuts (zero retail pass-through) | RBI MSM-17 |
| **Nifty 50 EPS** | **−1.0 % to −1.5 %** — *my estimate, not a sourced figure*, from a bottom-up weight decomposition; must be re-derived by L11 | see §5.2 |

Two refinements that matter more than the headline numbers:

**(i) The CPI and fiscal effects are substitutes, not additive.** Pass-through is a policy choice: if excise absorbs the shock, CPI is muted and the deficit widens; if retail prices move, the reverse. The free observable that reveals which is happening is **PPAC retail petrol/diesel prices versus the Indian basket** — the implied marketing margin. A collapsing `retail_margin_z` means the state is absorbing the shock and the CPI channel is deferred, not avoided.

**(ii) Not all oil shocks are alike.** Kilian (2009, *AER*) shows supply-driven and demand-driven oil price increases have opposite implications for equities. For India — a pure importer — a *demand-driven* rise arrives with stronger global growth and stronger exports, and is roughly neutral for equity; a *supply-driven* rise is a pure terms-of-trade tax. Free proxy:

```python
rho = corr_60d( Δlog Brent, Δlog copper )
demand_led = (rho > 0.30) and (sign(Δ3m copper) == sign(Δ3m Brent)) and (Δ3m EM_equity > 0)
oil_shock_type = "demand" if demand_led else "supply"
```
`oil_shock_flag` (consumed by L02, L03, L04) fires on **magnitude**; `oil_shock_type` modulates the **portfolio response**. Today: Brent −27 % from its April peak while copper is at records → **not demand-led**; the April spike was supply/geopolitical and is unwinding.

### 5.2 The India oil sector-beta matrix

This is the object L10 consumes. Each entry is the sensitivity of a sector's *excess* return (over Nifty) to a **+10 % move in Brent-INR** over 20 trading days.

**Estimator** (not asserted values):
```
r_sector_excess(w) = α + β_oil · Δlog(BrentINR)(w) + β_mkt · r_nifty(w) + β_usd · Δlog(BROAD)(w) + ε
  rolling 156-week window, weekly, HAC(4) errors
  shrink: β_used = 0.5·β_hat + 0.5·β_prior     (β_prior from the table below)
  data: NSE sector indices (bhavcopy / NSE indices archive) + FRED Brent + RBI USDINR — all free
```

| Sector (NSE index / proxy) | Cost/revenue mechanism | `β_prior` per +10 % oil |
|---|---|---|
| **Upstream** (ONGC, Oil India) | Direct realisation; capped by windfall cess above thresholds | **+4.0** |
| Gas utilities (GAIL, Gujarat Gas, IGL) | Competing-fuel parity; LNG spot linkage | +1.5 |
| Coal (Coal India) | Substitution demand | +1.0 |
| Oilfield services | Capex follows price with 2–3 q lag | +1.5 |
| **OMCs** (IOC, BPCL, HPCL) | **Asymmetric**: gain on falling crude with sticky retail prices; squeezed on rising crude when prices are administered | **−2.5 rising / +3.0 falling** |
| Refining+petchem (RIL) | GRM up, petchem spreads down; net ambiguous | +0.5 |
| **Aviation** (IndiGo) | ATF ≈ 30–40 % of operating cost, largely unhedged | **−4.5** |
| **Paints** (Asian, Berger) | Crude derivatives ≈ 50–55 % of RM; 1–2 q pass-through lag | **−3.5** |
| Tyres | Carbon black + synthetic rubber ≈ 30 % of RM | −3.0 |
| Adhesives / VAM (Pidilite) | Direct derivative input | −3.0 |
| Cement | Pet coke + diesel freight ≈ 25–30 % of cost | −2.0 |
| Specialty chemicals | Derivative inputs, but contractual pass-through; **sign flips with pricing power** | −1.5 (high dispersion) |
| FMCG | LAB, packaging, freight; also rural demand hit | −1.0 |
| Logistics / road transport | Diesel | −2.0 |
| **IT services** | No oil exposure, but **positive INR beta** — the oil trade and the INR trade are the same trade here | +1.0 *(via INR only — flagged so L03 and L10 do not add it twice)* |

**Critical anti-double-counting note.** L03 already emits a defensive IT tilt from its credit-phase term and explicitly states "L06 owns the INR/REER term". My IT beta is therefore emitted **only** through the INR channel (§9 tilt vector), never through the oil channel, and a CI assertion must check that the IT entry in `OIL_BETAS` is zero in the oil path.

### 5.3 Signals emitted

```python
oil_z          = z_5y( log(IndianBasket) )
oil_mom_z      = z_5y( Δ63d log(IndianBasket) )
oil_inr_z      = z_5y( Δ63d log(IndianBasket × USDINR) )        # what India actually pays
oil_shock_flag = oil_inr_z > +1.5                                # matches L04's definition exactly
oil_relief_flag= oil_inr_z < −1.5
tot_z          = z_5y( export_price_proxy / import_price_proxy ) # WPI-based terms of trade, DPIIT
crude_cycle_state ∈ {GLUT, SOFT, BALANCED, TIGHT, SPIKE}          # OECD days-of-cover (EIA) + backwardation
```
The inventory leg — OECD commercial stocks in days of forward cover, and the Brent 1st–12th month spread — is the honest short-cycle (6–18 m) variable. Both are free (EIA; ICE settlement curves are partially free via EIA/CME delayed quotes `[verify]`).

---

## 6. The commodity supercycle (15–25 years)

### 6.1 Mechanism and dating

The mechanism is **capital-cycle**, not demand-cycle: mine and field development takes 7–15 years from discovery to first production, so a demand surprise cannot be met with supply for a decade; prices overshoot, capex floods in, and that supply lands just as demand normalises — a 10–15 year bust. Erten & Ocampo (2013, *World Development*) date four non-oil supercycles since 1865 (troughs ≈1894, 1932, 1971, 1999); Jacks (2013/2019, NBER) gets similar dating from different filters. `n_obs = 4–5`, `CV ≈ 0.40` → **tier B, marginal**, as L01's register has it.

**Where 2026 sits.** The last peak was 2011; the trough was 2016–2020 (WTI printed negative in April 2020). Capex in mining and upstream oil collapsed 2013–2021 and has not recovered to prior peaks in real terms. On an Erten–Ocampo clock, an up-leg starting ≈2020 would be in **year 6 of a 10–15 year expansion** — early-middle. The 2026 evidence is consistent for metals (copper at all-time highs above $13,900/t, structural-deficit forecasts from BNEF/IEA) and **inconsistent for hydrocarbons** (Brent $88 after a geopolitical spike, ample OPEC+ spare capacity, shale elasticity, EV-driven demand-growth decay).

**Therefore the layer's call is a bifurcated supercycle, and it must be modelled as two signals, not one.**

```python
CS_metals = z_20y( log( PINK_metals_real ) )        # World Bank Pink Sheet metals index / MUV deflator
CS_energy = z_20y( log( PINK_energy_real ) )
CS_agri   = z_20y( log( PINK_agri_real ) )          # informational; India food CPI is L04's
commodity_supercycle_state = { "metals": band(CS_metals), "energy": band(CS_energy) }
```
Bands: `<−1σ TROUGH · −1..−0.3 EARLY_UP · −0.3..+0.7 MID_UP · +0.7..+1.5 LATE_UP · >+1.5 PEAK_RISK`, on a 20-year z with **36-month minimum dwell**. Today: metals ≈ `LATE_UP`, energy ≈ `MID_UP` trending down.

### 6.2 The energy-transition overlay

The transition is a **demand-side shift that is simultaneously bullish transition metals and bearish long-dated hydrocarbon demand** — the two legs decouple, which is why §6.1 splits them. Copper is the cleanest expression: EVs use ~3–4× the copper of an ICE vehicle, with grid build-out and data-centre electrification on top; BNEF's *Transition Metals Outlook* projects transition copper demand tripling by 2045 with a structural deficit potentially opening from 2026.

**For an India book this is mostly a cost, not an opportunity.** There is no large listed Indian copper or lithium miner; Hindustan Zinc, Hindalco, Vedanta and NALCO are the real producer exposures, and aluminium is an *energy-price* play as much as a metal play. The larger India-specific effect is on **consumers** — Polycab, Havells, KEI, R R Kabel, transformer and motor makers, EV supply chain, auto — for whom a copper up-leg is direct gross-margin compression with a 1–2 quarter pass-through lag. The overlay therefore enters as a **sector-relative tilt with an explicit consumer leg**, not a "buy commodities" call the portfolio cannot express.

Lithium: no meaningful listed Indian exposure; **INFEASIBLE as a portfolio expression** and dropped, kept only as a `COMMODITY_STATE` diagnostic (IMF PCPS / Pink Sheet lithium series).

### 6.3 The sign trap

Historically "commodity supercycle up" was *good* for Indian equity in 2003–08 (global growth dominated) and *bad* in 2011–13 (terms-of-trade tax without the growth). The distinguishing variable is the same one as §5.1(ii): **is the commodity move demand-led or supply-led?** The supercycle signal's portfolio sign is therefore conditional on `oil_shock_type` and on `USD_CYCLE` — a commodity boom with a *weak* dollar has historically been the best EM configuration (2003–07, 2009–11), and a commodity boom with a *strong* dollar the worst (2021–22). This interaction is coded explicitly in §9, not left to the optimizer to discover from 3 observations.

---

## 7. India's external balance cycle and the vulnerability composite

### 7.1 Indicators, danger thresholds, and 2013 vs 2026

| Metric | Definition | Danger (3) | Warning (2) | Watch (1) | Safe (0) | **Aug 2013** | **Aug 2026** |
|---|---|---|---|---|---|---|---|
| CAD/GDP | 4q trailing, RBI BoP | > 3.5 % | 2.5–3.5 | 1.5–2.5 | < 1.5 % | **4.8 %** → 3 | **0.6 %** → 0 |
| Basic balance | (CA + net FDI)/GDP | < −2.0 % | −2.0…−1.0 | −1.0…0 | > 0 | ≈ **−3.2 %** → 3 | ≈ **+0.5 %** → 0 `[verify]` |
| Import cover | Reserves / monthly merch. imports | < 7 m | 7–9 | 9–10 | > 10 m | **≈7.0** → 3 | **>10** → 0 |
| ST debt / reserves | Residual maturity, RBI Ext. Debt | > 45 % | 30–45 | 25–30 | < 25 % | **≈59 %** → 3 | **21.6 %** → 0 |
| External debt / GDP | RBI | > 25 % | 20–25 | 18–20 | < 18 % | **22.4 %** → 2 | **20.8 %** → 2 |
| Reserve adequacy | Reserves / (CAD + ST debt) | < 1.0 | 1.0–1.5 | 1.5–2.0 | > 2.0 | **≈1.1** → 3 | **≈3.0** → 0 |
| REER dev. | `REERDEV_trend`, 40-ccy | > +8 % | +3…+8 | 0…+3 | < 0 | ≈ +4 % → 2 | **≈ −1 %** → 0 |
| FPI dependency | FPI equity AUC / total mktcap (NSDL) | > 22 % | 18–22 | 16–18 | < 16 % | ≈21 % → 2 | **14.7 %** → 0 |

```
EVC_raw = Σ scores  (0–24)
EVC_z   = (EVC_raw − 6) / 4          # centred so 2026 ≈ 0, 2013 ≈ +3.5
```
**Aug 2013 = 21/24 → EVC_z ≈ +3.75 → `CRITICAL`. Aug 2026 = 2/24 → EVC_z ≈ −1.0 → `LOW`.**

| EVC_raw | State | Meaning |
|---|---|---|
| ≤ 4 | `EXT_STRONG` | **Today** |
| 5–8 | `EXT_ADEQUATE` | |
| 9–13 | `EXT_WATCH` | Pre-2013 (2011–12) territory |
| 14–18 | `EXT_FRAGILE` | |
| ≥ 19 | `EXT_CRITICAL` | 1991, Aug 2013 |

Quarterly update (BoP and external-debt releases), with the weekly reserve and REER legs refreshed in between. **Minimum dwell 2 quarters; escalation may be immediate, de-escalation requires 2 consecutive quarters.** De-risking is allowed to be fast and re-risking slow — the asymmetry L01 R7 mandates.

### 7.2 Why this matters more than any other output of the layer

The nominal rupee signal in Aug-2013 and Aug-2026 looks the same: record lows, heavy foreign selling, currency-crisis headlines. The balance sheets score **21/24 versus 2/24**. In 2013 the correct response was a genuine de-risk — equity down, gold up, leverage cut — and the market validated it: the RBI's July-2013 liquidity defence pushed the MSF to 10.25 % and broke banks and bonds. In 2026 the same nominal signal has a *flow* cause behind a sound balance sheet, and the correct response is a **sector rotation into exporters plus a modest gold add**, not a cash call. A layer that cannot tell these apart is worse than no layer, because it will produce a large, confident, wrong de-risk. This separation is why the layer exists.

---

## 8. Gold in INR versus gold in USD

### 8.1 Decomposition by decade

`INR gold return = (1 + USD gold return) × (1 + INR depreciation) − 1`. LBMA fixes and RBI reference rates, both free, both PIT.

| Period | USD gold CAGR | INR depreciation CAGR | **INR gold CAGR** | Currency contribution |
|---|---|---|---|---|
| 1990s (end-89 → end-99) | **−3.2 %** | **+9.9 %** | **+6.4 %** | +9.6 pp |
| 2000s (end-99 → end-09) | **+14.1 %** | **+0.7 %** | **+14.9 %** | +0.8 pp |
| 2010s (end-09 → end-19) | **+3.4 %** | **+4.4 %** | **+8.0 %** | +4.6 pp |
| 2020s (end-19 → Aug-26) | **+17.5 %** | **+4.5 %** | **+22.7 %** | +5.2 pp |
| **1990–2026 (36.7 y)** | **+6.8 %** | **+4.8 %** | **+11.9 %** | **+5.1 pp/yr** |

*(Anchors: gold $401 → $290 → $1,087 → $1,523 → $4,454; USDINR ≈16.9 → 43.6 → 46.5 → 71.4 → 95.5. All spliced from LBMA and RBI/FRED. Recompute in code from the actual series — these are the arithmetic the fixtures must reproduce.)*

**A rupee investor has earned roughly 500 bps a year more on the identical asset than a dollar investor, for 36 years, from the currency alone.** The 1990s line is the most instructive: USD gold *lost* 3.2 %/yr through the decade that made gold's dead-money reputation, while INR gold returned **+6.4 %/yr**. The asset that failed in dollars did not fail in rupees.

### 8.2 Why it is smoother, and the drawdown evidence

The variance arithmetic:
```
σ(INR gold)² = σ_g² + σ_fx² + 2·ρ·σ_g·σ_fx
             = 0.160² + 0.055² + 2(−0.30)(0.160)(0.055) = 0.0233  →  σ ≈ 15.3 %
```
versus σ(USD gold) ≈ 16.0 %. The vol reduction is small — **the vol is not the point.** The point is the **drawdown**, because the negative ρ between the USD-gold leg and the INR leg bites hardest exactly when the USD-gold leg is losing:

| Gold bear market | USD gold | USDINR | **INR gold** | Rupee absorbed |
|---|---|---|---|---|
| Sep 2011 → Dec 2015 | **−44.7 %** ($1,900 → $1,051) | 47.6 → 66.3 (+39 %) | **≈ −22 %** | **≈ half the drawdown** |
| Jan 2026 → Aug 2026 | **−20.4 %** ($5,597 → $4,454) | ≈90.5 → 95.5 (+5.5 %) | **≈ −16 %** | ≈ 4.4 pp |

The mechanism is structural: USD gold falls when the dollar is strong and real rates rising; the rupee falls in the same states. **The two legs are negatively correlated by construction of the global monetary cycle**, so the rupee hedge inside gold is reliable rather than lucky. This is the strongest quantitative argument for a rupee investor holding *more* gold than the global literature recommends, and it belongs in L13's sizing case.

### 8.3 The conditional correlation — the number that actually justifies the weight

The unconditional monthly correlation of INR gold to the Nifty is small and slightly **positive** (prior ≈ **+0.05 to +0.10**) — both are risk assets denominated in rupees. Sizing gold off that number understates its value. The correct statistic is the **downside beta**:

```python
# Estimator — this is a specification, not a result. L20 computes it; L13 consumes it.
r_g   = monthly INR gold return (LBMA × RBI ref rate, or MCX continuous with a duty-break adjustment)
r_e   = monthly Nifty 500 TRI return
down  = r_e < -0.05
beta_down = OLS( r_g[down] ~ r_e[down] ).beta
beta_up   = OLS( r_g[~down] ~ r_e[~down] ).beta
asym      = beta_up - beta_down                 # the quantity that justifies the weight
# Report Newey-West(3) errors, a stationary block bootstrap CI (block=6m, 2000 draws),
# and n_down. With ~1996-2026 monthly data n_down ≈ 45-55: report the CI, never a point estimate alone.
```

**Prior, from episode arithmetic** (to be confirmed or refuted, not assumed):

| Indian equity drawdown | Nifty | INR gold |
|---|---|---|
| Jan 2008 – Mar 2009 | **−60 %** | **+33 %** |
| Nov 2010 – Dec 2011 | −25 % | **+35 %** |
| Aug – Oct 2018 | −14 % | +5 % |
| **19 Feb – 23 Mar 2020** | **−38 %** | **−3.5 %** |
| Oct 2021 – Jun 2022 | −18 % | +6 % |
| Sep 2024 – Mar 2025 | −16 % | **+25 %** |
| Jan 2026 – ongoing | negative | **INR gold also negative (−16 %)** |

Prior: `beta_down ≈ −0.15` (band −0.35 … +0.05), `beta_up ≈ +0.05`, `asym ≈ +0.20`.

**Two honesty flags that must travel with this number.**

1. **March 2020 is the counterexample and it is the exact scenario the drawdown mandate cares about.** In the first three weeks of a liquidity crisis gold is sold for margin like everything else; the rupee cushion turned −9.5 % into −3.5 %, which is protection but not a hedge. Gold's crisis alpha in that episode arrived in the *following four months*, not during the crash. Any claim that gold delivers the sub-Nifty-50 drawdown objective on its own is false, and L13/L16/L17 must be told so.
2. **2026 is a second counterexample and it is live.** Gold and Indian equity are falling together because a global gold unwind and an India-specific outflow coincided. `n_down` is small enough that two counterexamples in seven episodes matter. The correct posture is a **wide prior and a hard cap on how much gold weight this evidence may justify** — the layer's gold authority is ±3 pp, not ±10 pp.

### 8.4 The implementation break nobody models: import duty and the MCX basis

INR gold measured from LBMA × USDINR is **not** what an Indian investor earns. Domestic gold carries import duty plus a local basis. India's gold import duty has been a step function — 2 % (2011) ratcheting to 10 % (2013, imposed as a CAD-control measure during exactly the episode in §3.3), to 12.5 %, to 7.5 %, to 15 % (2022), and **cut from 15 % to 6 % in the July 2024 Budget, producing a roughly 5 % one-day fall in domestic gold prices with no move in international gold.**

Mandatory consequences:
- A backtest of INR gold on MCX or domestic spot **contains fake returns and fake drawdowns** at every duty change. A −5 % day in July 2024 that never happened in dollars corrupts every drawdown, vol and conditional-beta statistic spanning it.
- Hand-encode a `DUTY` table (effective date, rate) from CBIC notifications and publish **both** `INRGOLD_synthetic` (LBMA × USDINR × (1+duty) — economically clean) and `INRGOLD_traded` (MCX/domestic — what an ETF tracks). Signals use the synthetic; execution and cost modelling use the traded series. Duty-change dates are excluded from return-statistic estimation, flagged in the fixture, asserted in CI.
- **A data-integrity task for L19 and a blocker for L13** — roughly one engineer-day, and it invalidates a lot of work if skipped.

---

## 9. The external regime map

Five archetypes, resolved in priority order, plus a one-sided EVC override. Values are **percentage points of NAV** for the aggressive book; the moderate book applies **0.65×** and may express sector tilts only within the top ~500 names by ADV.

| # | State | Definition | Gold | Equity | Debt | Exporters (IT, pharma, chem, auto anc.) | Importers (OMC, aviation, paints, cap-gds) | Metals producers | Metals consumers | Leverage | Hedging posture |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **E1** | `BENIGN` | USD ≤ 0, `INR_CALM/NEUTRAL`, oil `SOFT/BALANCED`, EVC ≤ 8 | **0** | **+2** | −2 | −1.5 | **+2.0** | +0.5 | +0.5 | +0.05x | Minimum standing hedge |
| **E2** | `DOLLAR_SQUEEZE` | `USD_STRONG_RISING` and `INRSI_idio` share < 40 % | **+2.5** | **−3** | +2 | **+3.0** | −2.0 | −2.0 | +1.0 | **−0.15x** | Index puts on; the dollar leg of gold is doing the work |
| **E3** | `TOT_SHOCK` | `oil_shock_flag` and `oil_shock_type == supply` | +1.5 | **−3** | +2 | **+2.0** | **−4.0** | 0 | 0 | −0.10x | Long upstream/gas as the natural hedge; do not buy puts against oil |
| **E4** | `INDIA_IDIO` | `INRSI ≥ STRESS` and idio share > 60 % — **today** | **+1.5** | **−1** | 0 | **+3.5** | −2.5 | 0 | −1.0 | −0.05x | **Sector rotation, not a cash call** — unless EVC also fires |
| **E5** | `COMMOD_BOOM_WEAK_USD` | `CS_metals ≥ LATE_UP` and USD_CYCLE ≤ −0.5 and `oil_shock_type == demand` | +1.0 | **+2.5** | −2 | −1.0 | −1.0 | **+3.0** | **−2.5** | +0.05x | Historically the best EM configuration; re-risk allowed |
| **OV** | `EVC ≥ FRAGILE` | External balance sheet deteriorating | **+3.0** | **−6** | +4 | +3.0 | −3.0 | −1.0 | 0 | **−0.30x** | **One-sided.** Overrides E1/E5. Routed to L17's cash-call ladder, not applied here |

**Today (28 Aug 2026): E4 dominant, E5 partly active on the metals leg, EVC `EXT_STRONG` so no override.** Net: gold +1.5, equity −1.0, exporters +3.5, importers −2.5, metals consumers −1.0, leverage ceiling −0.05x. A naive reading of "record-low rupee, record FPI outflows" would have produced the E2/OV response — a 3–6 pp equity cut — and would have been wrong on the balance-sheet evidence.

**Resolution rules.** (1) States are not mutually exclusive; compute membership for each and take the **weighted** tilt, weights = softmax of state scores at temperature 0.5, then clip to the budget in §10. (2) The EVC override is **additive and one-sided**: it may only reduce risk, and it is routed through `external_derisk_score` to L17 rather than consuming this layer's own budget — which is what L01's rule R7 requires. (3) `oil_shock_type` gates E3 versus E5; if the classifier is ambiguous (`0.2 < ρ < 0.4`) apply half weight to both.

---

## 10. Exposed signals, budgets and rate limits

L01's budgets are stated per **bucket**, but several layers own cycles in one bucket — L03 claims the full B2 equity allowance for `india_credit_financial_cycle` and I own two more B2 objects. **Unresolved interface conflict; I take the conservative reading** that budgets are per bucket and must be *split*. I claim the shares below and ask L01 to ratify.

| Signal | Bucket | `tau_half` | Tier | Equity dn/up | Gold dn/up | Debt dn/up | Sector L1 | Leverage | `max_Δ pp/month` | One-sided |
|---|---|---|---|---|---|---|---|---|---|---|
| `commodity_supercycle` (metals + energy) | B1 | 84 m | B | 1.5 / 1.5 | 1.0 / 2.0 | 1.5 / 1.5 | **3.0** | 0 | 0.036 | no |
| `global_dollar_cycle` | B2 | 48 m | B | 3.0 / 2.5 | 1.0 / 2.5 | 3.0 / 2.5 | **2.5** | −0.10 / +0.05 | 0.063 | no |
| `india_external_vulnerability` (EVC) | B2 | 48 m | B | **6.0 / 0** | 0 / 3.0 | 0 / 4.0 | 3.0 | **−0.30 / 0** | 0.125 | **yes** |
| `inr_stress_state` (INRSI) | B3 | 12 m | B | 4.0 / 0 | 0 / 2.0 | 0 / 2.0 | **5.0** | −0.15 / 0 | 0.333 | **yes** |
| `crude_cycle_short` | B4 | 6 m | B | 2.0 / 1.0 | 0 / 1.0 | 1.0 / 1.0 | **6.0** | −0.05 / 0 | 0.333 | no |
| **Σ (worst case, aggressive)** | | | | **16.5 / 5.0** | **2.0 / 10.5** | **5.5 / 11.0** | **19.5** | **−0.60 / +0.05** | | |

`max_Δ pp/month = 2·b / max(2·τ½, min_traverse_by_tier)` per L01 §8.5, with `b` the larger of the dn/up equity legs and `min_traverse_B = 12 m`.

**3σ check** (L01 Test 1, `3·√(0.33·Σb²)`): equity down `Σb² = 2.25+9+36+16+4 = 67.25` → **3σ = 14.1 pp**. Against a 60 % neutral equity weight that is a move to ≈46 %, comfortably inside the 15 % floor and leaving room for the rest of the stack. Gold up `Σb² = 4+6.25+9+4+1 = 24.25` → 3σ = **8.5 pp**, inside L02's 30 % ceiling. Sector L1 19.5 pp against a B1+B2+B3+B4 aggregate allowance of 5+8+12+10 = 35 pp — I claim 56 % of the sector budget, which is too much and must be negotiated down with L10 and L03; my proposed concession is **cutting `crude_cycle_short` sector L1 from 6.0 to 4.0** and `inr_stress_state` from 5.0 to 4.0, giving 16.5 pp (47 %). Flagged, not silently resolved.

**Turnover** (L01 Test 2, `1.6·b·√(12/h)`): 1.6(1.5√0.143) + 1.6(3√0.25) + 1.6(6√0.25) + 1.6(4√1) + 1.6(2√2) = 0.9 + 2.4 + 4.8 + 6.4 + 4.5 = **19.0 pp/yr** of allocation turnover, plus sector turnover. Within the aggressive book's budget; for the moderate book, **`crude_cycle_short` is dropped entirely** (B4/B5 at 1,000 cr is uneconomic) and the remainder scaled 0.65×, giving ≈9.5 pp/yr.

---

## 11. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L19 free-data pipeline | `pit_store(series, asof)` | All of §2. Final-vintage reads must raise. REER must resolve to `REER_own`, not RBI's revised series |
| L01 taxonomy | registry entries, `influence_budget()`, `resolve()`, rate limiter, sign convention | My five ids must exist in `cycle_registry.yaml` before I may emit |
| L02 long wave | `LW_CONSTRAINTS` (gold floor 5 %, ceiling 30 %, leverage ceiling), `G_eff` | My gold tilt is **additive on their anchor** and clipped by their floor/ceiling. I never set the anchor |
| L04 macro regime | `MACRO_RATES.real_rate_z_global`, `policy_phase` | Used only to residualise `oil_z` against the global real-rate cycle so I do not re-emit L04's gold view |
| L07 flows | `fpi_flow_z` | I use FPI as **BoP financing** only. CI must assert my `z6` is orthogonalised against L07's positioning signal |
| L20 validation | `oos_r2(signal_id)`, `n_eff(signal_id)`, `beta_down_gold` | Sets my authority; `beta_down_gold` is computed there, not here |

**Exposes**

```python
INR_STATE = {usdinr, INRSI, INRSI_idio, idio_share, state,           # CALM..CRISIS
             realised_vol_60d, vol_for_optimizer,                    # max(realised, 8%) / 18% in stress
             REERDEV_trend_40, REERDEV_trend_6, reer_state,
             fwd_premium_1y, carry_cushion, carry_to_vol,
             structural_drift_prior: 0.030, drift_band: [0.020, 0.040],
             weeks_in_state, asof, vintage_id}

USD_CYCLE = {USD_CYCLE_Z, usd_cycle_signal, state, months_in_state,
             beta_priors: {em_equity, nifty_usd, nifty_inr, fpi_flow, gold_usd, gold_inr}}

OIL_STATE = {basket_usd, basket_inr, oil_z, oil_inr_z,
             oil_shock_flag, oil_relief_flag, oil_shock_type,        # "demand" | "supply" | "ambiguous"
             crude_cycle_state, retail_margin_z, tot_z,
             elasticities: {cad_pct_gdp_per_10usd: 0.40,
                            cpi_bps_per_10usd: 42, gdp_bps_per_10usd: -22,
                            fiscal_bps_per_10usd_if_absorbed: 43,
                            nifty_eps_pct_per_10usd: -1.25},         # last one is an estimate, flagged
             OIL_BETAS: {sector: beta_used}}                          # the §5.2 matrix, shrunk

COMMODITY_STATE = {CS_metals, CS_energy, CS_agri, state_metals, state_energy,
                   transition_tilt: {producers_pp, consumers_pp},
                   commodity_supercycle_state}                        # the object L03 consumes

EXTERNAL_VULNERABILITY = {EVC_raw, EVC_z, state, component_scores: {metric: 0..3},
                          quarters_in_state, external_derisk_score}   # 0..1, ONE-SIDED, for L17

EXT_TILT = {equity_pp, gold_pp, debt_pp, leverage_x,
            sector_tilt_vector: {sector: pp},                          # for L10, never applied directly
            book_scale: {aggressive: 1.00, moderate: 0.65},
            max_delta_pp_per_month: {field: value}, regime_weights: {E1..E5: w}}

GOLD_FX_INPUTS = {inr_gold_synthetic, inr_gold_traded, duty_schedule,
                  duty_break_dates, decomposition_by_period,
                  beta_down_prior: -0.15, beta_down_band: [-0.35, +0.05],
                  fx_leg_corr_to_usd_gold: -0.30}                      # for L13
```

**Stage-1 sufficiency.** With Stage 2 off, every object above is computed from data alone. Stage 2 may write only into `oil_shock_type_override` (with a written falsification condition, two signatures, logged) and `tier_downgrade`. It may not alter a threshold, a beta, a budget or the EVC. A CI test asserts `EXT_TILT` is bit-identical with the overlay disabled.

---

## 12. MVP versus deferred

**MVP (v1, must exist in 3–6 months).** `INR_STATE` including INRSI and the dollar-orthogonalisation · `REER_own` (the PIT-clean build) · `USD_CYCLE` · `OIL_STATE` with `oil_shock_flag`, `oil_shock_type` and the shrunk `OIL_BETAS` matrix · `EXTERNAL_VULNERABILITY` · `GOLD_FX_INPUTS` including the duty table · the E1–E5 regime map · `commodity_supercycle` as a **static state read once a quarter**, not a fitted cycle.

**Deferred (v2+).** The peer cross-sectional REER z (`REERDEV_peer`, 20 EM panel via BIS) · `crude_cycle_short` as a traded signal with inventory and curve structure · the agricultural leg of the supercycle · an NDF-based offshore stress proxy · a formal Kilian SVAR replacing the correlation heuristic · the energy-transition consumer-margin model at name level · endogenous re-estimation of `beta_usd` at weekly frequency.

**Cut / INFEASIBLE.** Lithium as a portfolio expression (no listed Indian exposure). Daily LME data (paid; monthly Pink Sheet/IMF used instead). Daily NDF quotes (paid). Long-dated FX option surfaces for INR (paid; the FX hedging posture is therefore **structural, not backtested** — same honesty condition as the equity options overlay). Analyst-estimate-based oil EPS sensitivities (paid).

| # | Step | Deliverable | Days | MVP | Phase |
|---|---|---|---|---|---|
| 1 | FX + commodity PIT adapters | RBI DBIE, WSS, FRED, EIA, Pink Sheet, IMF PCPS, PPAC, NSDL, LBMA → `(series, value, event_date, knowledge_date)` | 4.0 | ✅ | data |
| 2 | Fixtures for every §2 series | One committed sample per indicator so the layer runs offline (L01 hard requirement) | 1.5 | ✅ | data |
| 3 | `REER_own` builder | Fixed-weight PIT REER, 12 partners, annual weight re-strike, ±3 cross-check vs RBI | 2.5 | ✅ | data |
| 4 | Gold duty table + dual series | CBIC notification table; `INRGOLD_synthetic` / `_traded`; break flags in CI | 1.0 | ✅ | data |
| 5 | INRSI + dollar orthogonalisation | z-pipeline, valuation-adjusted reserves, Schmitt trigger, dwell | 3.0 | ✅ | mid-cycles |
| 6 | INRSI historical calibration test | Reproduce the §3.6 state/idio ordering for 2013/2018/2020/2022/2026 or the weights do not freeze | 1.5 | ✅ | validation |
| 7 | `USD_CYCLE` | Broad-dollar splice, real EER, state machine, 12m dwell | 1.5 | ✅ | long-cycles |
| 8 | `OIL_STATE` + shock-type classifier | Indian basket, oil-INR z, retail-margin proxy, demand/supply heuristic | 2.0 | ✅ | mid-cycles |
| 9 | `OIL_BETAS` estimator | Rolling 156w multivariate regression, HAC, 50 % shrinkage to priors, IT-channel assertion | 2.5 | ✅ | sector |
| 10 | `EXTERNAL_VULNERABILITY` | 8 metrics, banded scoring, asymmetric dwell, 1991/2013/2018/2026 back-scoring test | 2.5 | ✅ | mid-cycles |
| 11 | `COMMODITY_STATE` (static-state form) | Pink Sheet real indices, 20y z, metals/energy split, 36m dwell | 1.5 | ✅ | long-cycles |
| 12 | Regime map E1–E5 + softmax resolver | Tilt vector, budget clipping, one-sided EVC routing to L17 | 2.0 | ✅ | overlay |
| 13 | `GOLD_FX_INPUTS` + conditional-beta harness | Decomposition, block-bootstrap CI, hand-off to L13/L20 | 2.0 | ✅ | validation |
| 14 | Explainability page | Per-rebalance: state, each z, idio share, every tilt, every clip and why | 1.0 | ✅ | production |
| 15 | Deferred items 1–7 above | Registry rows with `status: deferred` and full sourcing | 3.0 | ⬜ | — |
| | **MVP total** | | **28.5 days** | | |

---

## 13. Risks and constraint conflicts

1. **Every long signal here has `n_eff` between 3 and 5** — three dollar cycles, four supercycles, eight INR episodes, two external crises. The thresholds in §3.6, §6.1 and §7.1 carry far more degrees of freedom than the data can identify. The only defence is L01's: freeze them in git at inception, two signatures to change one, never tune them to improve a backtest. Expect this to be tested the first time a frozen threshold looks stupid.
2. **I disagree with L02's INR drift by ~50–100 bps/yr.** L02 uses 2.0–2.5 %/yr from the inflation differential; realised is 3.0–4.4 % across every window I measured, and the post-2016 residual is *positive*, not negative. L02's number is the correct *equilibrium* answer and the wrong *empirical* one. Since L02's gold and exporter tilts are calibrated off it, the difference is material and needs adjudication, not averaging.
3. **The REER PIT problem is real and expensive.** RBI's published REER is revised and thrice-rebased. If §2.1's own-build is skipped for time, every REER-conditioned backtest result in this layer is contaminated and must be labelled `pit=contaminated`, not `pit=lag_approx`.
4. **The gold-duty break will silently corrupt L13 if not fixed.** A −5 % phantom day in July 2024 and a +duty step in 2013 sit inside exactly the windows used to estimate gold's crisis beta. One engineer-day; skipping it invalidates the sizing case.
5. **INR gold is not a March-2020 hedge, and 2026 is a second counterexample.** Two of seven Indian equity drawdowns since 2008 saw INR gold fall too. With `n_down ≈ 50` months the conditional beta's confidence interval will span zero. The drawdown mandate must not be assumed to rest on gold; §10's per-signal gold cap (max +3.0 pp from any one signal, 8.5 pp at 3σ for the whole layer) reflects that and should not be loosened.
6. **The options overlay for currency is not backtestable at all.** No free long-dated INR option history exists. Any USDINR hedge is justified structurally or not at all — and RBI's exchange-traded currency-derivative rules require contracted underlying exposure above documented thresholds `[verify current circular]`, which is a compliance step even for proprietary capital.
7. **My sector-L1 claim of 19.5 pp is too large** relative to the 35 pp bucket allowance shared with L03 and L10. I have proposed a cut to 16.5 pp in §10, but this needs an explicit three-way negotiation, and the honest position is that the oil sector-beta matrix is the highest-conviction, best-evidenced thing this layer produces and should win most of that argument.
8. **The FPI flow series is used by both me and L07** for different purposes. Without the CI-asserted orthogonalisation, a flow shock will be counted twice — once as sentiment, once as BoP pressure — and the equity de-risk will be double-sized.
9. **The commodity supercycle cannot be backtested in any meaningful sense.** Four observations, 160 years, and India's investable expression of it did not exist for three of them. It is a tier-B prior with ±1.5 pp of equity authority, and its main honest use is as a *conditioner* on L03's late-expansion threshold and L10's metals tilt, not as a standalone allocator.
10. **35–60 % CAGR is not reachable from here.** External-regime timing plausibly adds 50–150 bps/yr net of costs, concentrated in a handful of episodes. Its value is drawdown-shaped — correctly calling 2013 a solvency event and 2026 a flow event is worth far more than the return contribution suggests, and shows up as a *lower left tail*, not a higher mean. I concur with L01 §13.8 and L02: 18–24 % (aggressive) full-cycle is the defensible range.

---

## 14. Registry patch requests (PR against `config/cycle_registry.yaml`)

- **`commodity_supercycle`**: `status: deferred → active`, `mvp: true`, but **as a static quarterly state, not a fitted circular phase** — L01's `phase_repr: circular (marginal)` should become `state`. Split into `metals` and `energy` sub-states.
- **`global_liquidity_cycle`**: L01 assigns `owner_layer: L04/L06`. Resolve to **L06 owns the dollar leg** (`global_dollar_cycle`, new id) and L07 owns the central-bank-balance-sheet leg. Ambiguous joint ownership is how double-counting gets built.
- **`em_capital_flow_cycle`**: `status: cut`, `cut_reason: "subsumed by india_external_vulnerability; tier-C L1 budget (R4, 150 bps total) is better spent elsewhere"`. Replace with new entry **`india_external_vulnerability`**, bucket B2, `tau_half: 48`, tier **B** (cross-sectional evidence, Frankel–Saravelos), `one_sided: true`, `data_tier: D1`.
- **New: `inr_stress_state`**, bucket B3, `tau_half: 12`, tier B, `phase_repr: state`, `one_sided: true`, `data_tier: D1`.
- **`crude_cycle_short`**: `status: deferred → active` for the aggressive book only; `mvp: true` for the sector channel, `mvp: false` for the allocation channel; `moderate: null`.

---

## 15. References

1. Rey, H. (2013). *Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence.* Jackson Hole.
2. Bruno, V. & Shin, H.S. (2015). *Cross-Border Banking and Global Liquidity.* Review of Economic Studies 82(2).
3. Avdjiev, S., Du, W., Koch, C. & Shin, H.S. (2019). *The Dollar, Bank Leverage, and Deviations from Covered Interest Parity.* AER: Insights 1(2).
4. Obstfeld, M. & Zhou, H. (2022). *The Global Dollar Cycle.* Brookings Papers on Economic Activity, Fall 2022.
5. Hofmann, B., Shim, I. & Shin, H.S. — BIS work on the dollar, EM local-currency bond spreads and "original sin redux" `[verify exact paper title/year]`.
6. Kalemli-Özcan, Ş. (2019). *U.S. Monetary Policy and International Risk Spillovers.* Jackson Hole.
7. Kilian, L. (2009). *Not All Oil Price Shocks Are Alike: Disentangling Demand and Supply Shocks in the Crude Oil Market.* American Economic Review 99(3).
8. Erten, B. & Ocampo, J.A. (2013). *Super Cycles of Commodity Prices Since the Mid-Nineteenth Century.* World Development 44.
9. Jacks, D. (2013/2019). *From Boom to Bust: A Typology of Real Commodity Prices in the Long Run.* NBER WP 18874.
10. Frankel, J. & Saravelos, G. (2012). *Can Leading Indicators Assess Country Vulnerability? Evidence from the 2008–09 Global Financial Crisis.* Journal of International Economics 87(2).
11. Brunnermeier, M., Nagel, S. & Pedersen, L. (2009). *Carry Trades and Currency Crashes.* NBER Macroeconomics Annual 23.
12. Reserve Bank of India (2019). *Mint Street Memo No. 17* — oil price shocks and the Indian economy `[verify authors and exact title]`.
13. Reserve Bank of India — *Monetary Policy Report*, *Weekly Statistical Supplement*, *India's External Debt* (quarterly), *Handbook of Statistics on the Indian Economy*, Database on Indian Economy (`data.rbi.org.in`).
14. Petroleum Planning & Analysis Cell (`ppac.gov.in`) — Indian crude basket, import volumes and bill, consumption, retail prices.
15. World Bank *Commodity Markets Outlook* / Pink Sheet; IMF *Primary Commodity Price System*; EIA *Short-Term Energy Outlook* and open data API; BIS effective exchange rate statistics; FRED; NSDL FPI statistics; LBMA precious-metal prices.
16. BloombergNEF *Transition Metals Outlook* (Dec 2025) and IEA commentary on copper markets (2026) — cited for the transition-demand and structural-deficit claims; both are secondary reporting, marked `[verify primary]`.

*Dated readings in §0 are as of 28 August 2026 and were taken from public reporting; each should be re-pulled from the primary free source listed in §2 before any number is used in code.*
