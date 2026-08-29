# Layer 07 — Flows, Supply, Positioning and Sentiment (1 month – 5 years)

**Abstract.** This layer owns the medium-frequency cycle that in India routinely overrides fundamentals for one to three years at a stretch: who is buying, who is selling, how much new paper the market is being asked to absorb, how levered the marginal buyer is, and how frightened or complacent the tape is. Its organising claim is that these four things are *not* one signal. **Supply** (IPO/QIP/OFS pipeline, insider selling, promoter dilution, net of buybacks) is slow, mechanical and leads price by three to six months — it is the most reliable sell-side information the Indian market gives away free. **Flows** are mostly *coincident*: FPI and lumpsum mutual-fund money chases returns, so it confirms trends and only carries contrarian information at the tails. **Positioning and leverage** are fast, mean-reverting, and — critically — their data series were *broken* by SEBI's 2024–25 derivative reforms, so anything fitted on pre-November-2024 F&O data is measuring a market that no longer exists. **Sentiment and breadth** are the fastest leg and the only one that fires inside a crash window. The layer fuses these into a single 0–100 `EUPH` score with prior-set (not fitted) weights, then applies a deliberately asymmetric transfer function: **contrarian without condition below 30, dead-band 30–62, momentum-*confirming* 62–80, and contrarian above 80 only when a deterioration trigger also fires.** That gate is the whole point — an ungated euphoria short would have gone bearish on Indian small-caps in February 2024 and been wrong for seven months. The layer emits `derisk_score` to the cash-call engine (L17), `hedge_intensity` to the options overlay (L16), and a size/risk-appetite tilt to L10/L14. It also states plainly what it cannot do: the "domestic SIP flows cushion the market" thesis on which much of India's current bull case rests has **never been tested by a drawdown larger than about 16% on the Nifty at the current SIP book size**, and this spec refuses to backtest as though it had.

---

## 0. Dated snapshot — 28 August 2026

Live readings, not design assumptions. Items I could not confirm to a primary source are marked `[verify]`.

| Variable | Reading | Read |
|---|---|---|
| FPI net equity, CY2026 to date | **−₹2.2 lakh crore** (≈ −$24 bn) — worst CY since 1993 | Sustained, not panic: a grind, not a gap |
| FPI ownership | ≈**14.7%** of NSE-listed mcap, a 14-year low; **17.1%** of Nifty-500 (Mar-26 ATL) `[verify basis]` | The marginal seller is running out of stock |
| DII net equity, CY2026 to 7-Aug | **+₹5.13 lakh crore** — 3rd straight year above ₹5 trn | Mar-2026 alone: **₹1.36 lakh crore**, into an 11% Nifty air-pocket |
| DII ownership, Nifty-500 | **≈20.9–21.0%** (Mar-26) — overtook FPI for the first time | Structural, not cyclical |
| SIP contribution | **₹31,961 cr** (Jul-26); record ₹32,087 cr (Mar-26); >₹31,000 cr for 10 straight months | SIP AUM ₹18.20 lakh cr ≈ 20.6% of industry AUM |
| SIP stoppage ratio | **81.9%** (Jul-26), from ~91% (Jun), **>100% in Mar and Apr 2026** | Gross contribution rising while net registrations went negative — a first |
| IPO mobilisation, FY26 | **₹1,78,963 cr** across 112 mainboard IPOs — record, 2nd consecutive record year | Total public equity raise ₹3.05 lakh cr, −18% YoY (QIPs collapsed) |
| MTF book | **₹1.51 lakh crore** (26-Aug-26), from ₹24,920 cr in FY23 | +65% over 12m during which Nifty returned **−4.4%** |
| Demat accounts | **23.44 crore** (Jul-26); +2.9 mn in Jul (+12.1% MoM); FY26 gross additions **−21.9% YoY** | New-entrant *intensity* well below 2021 |
| Index option volumes | **−52%** in FY26 across NSE+BSE; unique individual F&O investors 98.1 → 78.6 lakh | The retail option boom has been regulated away |
| Nifty Smallcap 250 | −23% Sep-24 → Mar-26, then +20% off the March low | A long de-rating, not a crash |

**The configuration in one line:** heavy and rising *supply*, collapsing *foreign* flows, record and price-insensitive *domestic* flows, **rising leverage into a falling market**, and a small-cap complex that has already de-rated. That is not a euphoria print and it is not a capitulation print — §7.4 shows why the composite should read in the low-to-mid 30s here, and why a model that screams "buy the panic" would be mis-reading a leveraged de-rating for a washout.

---

## 1. Scope and boundaries

**Owns.** FPI/FPI-debt and DII flow state · mutual-fund flow decomposition (SIP vs discretionary) · NFO activity · the primary-issuance and insider-supply complex and the composite **net supply ratio** · F&O positioning by participant category · margin/MTF leverage · put-call ratio · India VIX and the variance risk premium · market breadth · the small-vs-large risk-appetite cycle · retail participation intensity · the composite **euphoria/capitulation score** and its transfer function.

**Does not own.**

| Object | Owner | My boundary |
|---|---|---|
| FPI flow as a **BoP / currency-pressure** input | L06 | L06 uses the same NSDL series for external financing. I use it as *positioning*. Neither of us may claim the same allocation authority twice — see §11.6 |
| Credit conditions, bank/NBFC funding stress | L03 | I hand L03 `pledge_stress` and `mtf_stress`; L03 owns the credit read |
| Aggregate valuation percentile | L05 | I never compute a P/E. L05's `valuation_pct` is an *input* to my crossover gate, not a member of my composite |
| Trend and momentum state | L08 | **Critical.** My breadth block is *residualised* on L08's trend state (§7.2) or the cash engine gets a double-sized bet |
| Sector rotation, sector flows | L10 | I expose FPI fortnightly sector AUC deltas as raw input; L10 decides |
| Per-name special-situation and IPO scoring | L12 | I own the **aggregate** issuance calendar as a supply signal; L12 owns individual listings |
| Cash level, de-gearing ladder | L17 | I emit `derisk_score` ∈ [0,1]; L17 decides the cash number |
| Hedge ratio and strike selection | L16 | I emit `hedge_intensity` ∈ [0,1]; L16 owns the sweep (0/25/50/75/100/125%) |
| Universe membership, bhavcopy panel, PIT store | L19 | I consume `bhavcopy_panel` and `index_membership`; I build no ingestion of my own |

Numbering follows `docs/ROADMAP.md`.

---

## 2. Data spine — free sources only

| Code | Series / fields | Free source | Freq / history | PIT status |
|---|---|---|---|---|
| `FPI_D` | FPI net equity, net debt, debt-VRR, hybrid — daily ₹ cr and $ mn | **NSDL** `fpi.nsdl.co.in/web/Reports/Archive.aspx` | D / 2002– (M from 1993) | **True PIT** |
| `FPI_AUC` | FPI assets under custody, by sector, fortnightly/monthly | NSDL `fpi.nsdl.co.in` → *FPI Investments* | 2W-M / 2010– | True PIT |
| `DII_D` | FII and DII cash-market gross buy / gross sell / net | **NSE** `nseindia.com/reports/fii-dii`; BSE equivalent | D / 2007– | True PIT |
| `AMFI_M` | Net inflow by scheme category; gross sales; redemptions; **SIP contribution**; SIP AUM; SIP accounts; **new SIP registrations**; **SIPs discontinued/tenure-completed**; **NFO count and amount by category** | **AMFI** `amfiindia.com/research-information/amfi-monthly` (XLS/PDF) | M / 2007– (SIP series from Apr-2016) | **NOT archived** — see §2.1 |
| `SEBI_ISS` | Public issues: IPO, FPO, rights, QIP, OFS — issue size, dates, type | **SEBI Bulletin** monthly statistical tables `sebi.gov.in/sebi-data/bulletin`; NSE/BSE new-listing circulars | M / 1993– | Revised once, then stable |
| `DRHP` | Draft offer documents filed; SEBI observations issued; proposed issue size | **SEBI** `sebi.gov.in/filings/public-issues` | Event / 2005– | True PIT (filing date is the knowledge date) |
| `SHP` | Shareholding pattern (Reg 31 LODR): promoter %, public %, **encumbered/pledged promoter shares** | NSE `nseindia.com/companies-listing/corporate-filings-shareholding-pattern`; BSE XBRL | Q, ≤21 days after quarter-end / 2001– | **Near-PIT** (filing date known) |
| `PIT7` | Insider trades (SEBI PIT Reg 7(2)): entity, category (promoter/KMP/designated), buy/sell, quantity, value, mode | NSE `companies-listing/corporate-filings-insider-trading`; BSE | D, ≤2 trading days after trade / 2015– | **True PIT** |
| `BULK` | Bulk deals (>0.5% of listed shares) and block deals: date, symbol, client name, buy/sell, qty, price | NSE `report-detail/display-bulk-and-block-deals`; BSE | D / 2004– | True PIT |
| `BUYBK` | Buyback offers: company, route (tender/open-market), max amount, price | Exchange corporate announcements; SEBI buyback filings | Event / 2000– | True PIT. **Regime break Oct-2024** — §4.4 |
| `FAO_OI` | **Participant-wise open interest**: Client / DII / FII / Pro × {index futures L/S, stock futures L/S, index call L/S, index put L/S, stock options L/S} | **NSE archives** `nsearchives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv` | D / 2011– `[verify start]` | True PIT |
| `FAO_VOL` | Participant-wise volume, same categories | `.../fao_participant_vol_DDMMYYYY.csv` | D / 2011– | True PIT |
| `FO_BHAV` | F&O bhavcopy — contract, expiry, strike, option type, settlement price, OI, change in OI | NSE `all-reports-derivatives` (udiff format post-2024, legacy before) | D / 2000– | True PIT |
| `MTF` | Margin Trading Facility disclosure — aggregate and scrip-wise funded book | NSE `all-reports` → *Margin Trading*; BSE equivalent | D / 2018– `[verify start]` | True PIT |
| `VIX` | India VIX open/high/low/close | NSE historical index data | D / Nov-2007– | True PIT |
| `IDX` | Nifty 50 / 100 / 500 / Midcap 150 / Smallcap 250 / Microcap 250 — price and TRI | NSE `niftyindices.com` historical data | D / varies, most from 2005 | True PIT |
| `BHAV` | Full cash bhavcopy incl. `DELIV_QTY`, `DELIV_PER` | via **L19** (`sec_bhavdata_full`) | D / 2011– for delivery | True PIT |
| `DEMAT` | Demat account counts, CDSL and NSDL; monthly additions | **SEBI Bulletin** monthly tables; CDSL/NSDL investor presentations | M / 2000– | True PIT |
| `NPS` | NPS AUM and subscribers by scheme (E/C/G) | `npstrust.org.in`, PFRDA monthly bulletins | M / 2013– | True PIT |
| `INSUR` | Life insurance new business premium by insurer | IRDAI `irdai.gov.in` → *Business Figures* | M / 2004– | True PIT (equity share not disclosed — proxy only) |
| `EPFO` | EPFO ETF investment; payroll additions | EPFO annual report; PIB releases; Lok Sabha answers | A, irregular / 2015– | Poor. Treat as a **level**, not a signal |
| `SEBI_FO` | SEBI's annual study on individual traders' P&L in equity F&O | `sebi.gov.in` studies | A / FY22– | The definitive free evidence on Indian retail derivative behaviour |
| `MPULSE` | NSE *Market Pulse* monthly — flows, ownership, breadth, participation | `nseindia.com` research | M / 2018– | Cross-check only, never a primary feed |

### 2.1 The AMFI vintage problem, and the fix

AMFI publishes one monthly XLS and overwrites nothing, but it maintains **no vintage archive** — a figure revised later is silently replaced, and pre-2016 monthly files are no longer downloadable in their original form. The SIP series in particular has been re-tabulated at least once when AMFI changed the SIP-AUM definition `[verify]`.

**Fix (mandatory, starts day one).** L19's forward-archiver must snapshot the AMFI monthly file on the 8th–12th of each month with our own knowledge timestamp, hash it, and store the hash. For history before our archive starts, we use the current vintage and **label every backtest that touches AMFI data as `vintage=current, pit=lag-approximated`**. Because AMFI publishes with roughly a 7–10 day lag, all AMFI-derived signals are lagged **15 calendar days** before entering any backtest. Same rule for SEBI Bulletin (lag 45 days) and shareholding patterns (lag 25 days after quarter-end).

---

## 3. Flows

### 3.1 The four flow pools, and why they must be separated

Reporting "DII bought ₹5.13 lakh crore" as one number is the single most common analytical error in Indian market commentary. That number is four different behaviours:

| Pool | Approx. run-rate, Aug-2026 | Price sensitivity | Signal content |
|---|---|---|---|
| **Equity SIP** | ≈₹23,000–24,000 cr/month (≈73% of the ₹31,961 cr SIP book is equity-oriented `[verify split — AMFI does not publish SIP by category]`) | **Near zero** (mandate-driven) | A *level*. Almost none. Never put it in the composite |
| **Discretionary MF (lumpsum + switches)** | AMFI equity net inflow **minus** equity SIP; ranged −₹8,000 to +₹25,000 cr/month over 2024–26 | **Strongly procyclical** | **High.** This is the real retail sentiment series |
| **NFO** | Reported separately by AMFI | Extremely procyclical (launched into hot themes) | High, and specifically a *late-cycle* signal |
| **Insurance / EPFO / NPS** | ≈₹8,000–12,000 cr/month combined `[verify]` | Zero to mildly countercyclical (rule-based rebalancing) | Low. Treat as a constant in MVP |

The extractable signal is therefore:

```
EQ_SIP(m)       ≈ 0.73 * SIP_contribution(m)          # calibrate the ratio annually from AMFI category AUM growth
LUMPSUM_NET(m)  = AMFI_equity_net_inflow(m) - EQ_SIP(m) - NFO_equity_amount(m)
LUMP_SIG(t)     = z_exp( sum_{3m} LUMPSUM_NET / free_float_mcap(t) )
NFO_SHARE(t)    = sum_{3m} NFO_equity_amount / sum_{3m} AMFI_equity_gross_sales
```

`NFO_SHARE` thresholds (priors, to be re-struck once 10 years of clean data exist): <6% quiet · 6–12% normal · **12–18% elevated** · **>18% extreme**. FY2021-22 and CY2024 both printed above 18% `[verify]`.

### 3.2 FPI and DII: coincident, not leading

The best-established India-specific finding is that FPI flows are largely a *consequence* of Indian returns rather than a cause — return-chasing, not information (Chakrabarti 2001, *FII Flows to India: Nature and Causes* `[verify title]`; consistent with Froot, O'Connell & Seasholes 2001 on EM portfolio flows generally). This settles a design question: **FPI net flow enters the composite with a *positive* sign** (buying raises the euphoria score). It is not a contrarian input in the middle of its range; it becomes contrarian only through the transfer function at the tails, which is exactly what §8 does.

```
FPI_SIG(t) = z_exp( sum_{63d} FPI_net_equity / free_float_mcap(t) )
DII_SIG(t) = z_exp( sum_{63d} DII_net_equity / free_float_mcap(t) )
FPI_DII_DIVERGENCE(t) = FPI_SIG - DII_SIG
```

The divergence term is the interesting one and is currently at an extreme (FPI −₹2.2 lakh cr, DII +₹5.13 lakh cr in the same year). Historically a large positive divergence (domestics absorbing foreign selling) has resolved *upward* when the foreign selling was flow-driven (2018-19, 2022-23) and *downward* when it was solvency-driven (2008). L06's `external_vulnerability` composite is the discriminator, which is why it is an input, not something I re-estimate.

### 3.3 The SIP cushion thesis — quantified, and honestly stress-tested

**The arithmetic in favour.** Equity SIP ≈ ₹23,500 cr/month = **₹2.82 lakh crore/year** of price-insensitive demand. The worst FPI equity outflow year in Indian history is CY2026 at ₹2.2 lakh crore. Add insurance/EPFO/NPS (≈₹1.2 lakh cr/yr) and the passive domestic bid alone exceeds the worst-ever foreign outflow by roughly **80%**. On a monthly basis: peak historical FPI selling is ~₹60,000–₹1,00,000 cr/month (Mar-2020: ₹62,000 cr; Oct-2021 to Jun-2022: ₹2.6 lakh cr over nine months); domestic institutional buying printed ₹1.36 lakh crore in March 2026 alone. The cushion is real at observed magnitudes.

**The arithmetic against, which matters more.** Three things:

1. **The SIP book has never been drawdown-tested at scale.** It grew from ≈₹8,000 cr/month (2020) to ≈₹32,000 cr/month (2026). The worst Nifty drawdown in that entire window is roughly 16% (2024-25 and the March-2026 air-pocket); the worst broad-market drawdown is the 23% Smallcap-250 de-rating. **Zero observations at >30%.** Any backtest that runs the current SIP level through a synthetic 2008 is extrapolating four standard deviations outside its support.
2. **What evidence exists says the cushion bends, with a lag.** In 2020 the SIP book fell from roughly ₹8,641 cr (Mar-2020) to a trough near ₹7,302 cr (Nov-2020) — about **−15%, and the trough came eight months *after* the price low** `[verify exact AMFI figures]`. The flow did not collapse; it eroded slowly and kept eroding into the recovery. That is the correct prior: **slow, lagged, partial erosion**, not a stop.
3. **The stoppage ratio leads the contribution.** In March and April 2026 the stoppage ratio exceeded 100% — more SIPs ended than started — while gross contribution simultaneously hit a record ₹32,087 cr, because the surviving book steps up and cancellations take effect with a lag. **The contribution number is the last thing to turn.** Model the ratio, not the rupees.

**Mandated design consequence (this is a constraint on L17 and L20, not a suggestion).** The backtest harness must carry an explicit `sip_stress` scenario, applied whenever a simulated Nifty drawdown exceeds 25%:

```
eq_sip_runrate(t) = eq_sip_base(t) * (1 - 0.30 * ramp(t - t_dd25, months=6))
lumpsum_net(t)    = min(lumpsum_net(t), -0.5 * eq_sip_runrate(t))   # discretionary flow goes negative
```

i.e. a 30% erosion of the equity SIP run-rate phased over six months, and discretionary flow flipping to net redemption. This is a **prior, not an estimate** — there is no data to fit it. Report every drawdown statistic twice: with and without `sip_stress`. If the strategy only meets the 30–35% drawdown ceiling in the unstressed case, it does not meet it.

The exportable summary statistic:

```
DOMESTIC_CUSHION_RATIO(t) = (12m passive domestic equity demand) / (trailing 12m peak FPI monthly outflow * 12)
```
Currently ≈ **1.5–1.8x**. Below 1.0 the cushion thesis is arithmetically dead; between 1.0 and 1.5 it holds only if the discretionary component does not turn.

---

## 4. Supply — the layer's most reliable leg

Academic backbone: Baker & Wurgler (2000), *The Equity Share in New Issues and Aggregate Stock Returns* (JF) — the share of equity in total new issues is one of the strongest known predictors of aggregate returns; Ritter (1991) and Loughran & Ritter (1995) on the new-issues puzzle; Lakonishok & Lee (2001) and Jeng, Metrick & Zeckhauser (2003) on aggregate insider trades. Issuers and insiders are the best-informed sellers in the market and they sell into strength. India offers all of this data free.

### 4.1 The net supply ratio

```
NET_SUPPLY_12m(t) = IPO_main + IPO_SME + FPO + QIP + OFS + Rights_cash
                  + INSIDER_NET_SELL + BLOCK_DEAL_VALUE * kappa
                  - BUYBACK_ACTUAL - PROMOTER_NET_BUY - DELIST_CONSIDERATION

NSR(t) = NET_SUPPLY_12m(t) / free_float_mcap(t)
```

- `kappa` = 0.35, the assumed fraction of block-deal value that is genuine concentrated-holder exit rather than institutional reshuffling. A prior, not an estimate. Sensitivity-test it at 0.2 and 0.5.
- `free_float_mcap` must be **point-in-time**: mcap from bhavcopy at t, free-float factor from the most recent shareholding pattern filed on or before t. MVP may use total mcap × 0.50 and must label the approximation.

**Thresholds** (12-month NSR on free-float mcap; the historical anchors below are reconstructions to be recomputed from primary data, and mcap estimates are `[verify]`):

| NSR (12m) | State | Block-A contribution | Historical anchor |
|---|---|---|---|
| < 0.5% | Drought | +1.0 | FY2003, FY2013, FY2020-H1 |
| 0.5 – 0.9% | Light | +0.5 | FY2015, FY2024-H1 |
| 0.9 – 1.3% | Neutral | 0.0 | long-run median |
| 1.3 – 1.7% | Elevated | −0.5 | **FY2026 ≈ 1.3%** (₹3.05 lakh cr / ≈₹230 lakh cr free float) |
| 1.7 – 2.2% | Heavy | −1.0 | FY2022 ≈ 1.6%; **FY2025 ≈ 1.6%** |
| > 2.2% | Indigestion | −1.0 and arms the euphoria overlay | **FY2008 ≈ 2.7%** (₹87,000 cr on ≈₹32 lakh cr free float) |

**Always use the ratio, never the rupee record.** FY26's ₹1.79 lakh crore IPO haul is an all-time record in rupees and merely *elevated* as a ratio, because market cap has grown faster than issuance. Reporting the record is how commentators produce false sell signals.

**Add the rate of change**, because supply is a *response* to valuation and the acceleration carries more information than the level:

```
NSR_ACCEL(t) = 2 * NSR_6m(t) - NSR_12m(t)          # annualised 6m vs the trailing year
BLOCK_A_supply = 0.6 * band_score(NSR_12m) + 0.4 * clip(-z_exp(NSR_ACCEL), -1, 1)
```

### 4.2 The pipeline — the single best leading indicator in this layer

SEBI publishes every DRHP filed and every observation letter issued, free, with dates. Issuers file when they believe the window is open, and the filing precedes the issue by three to six months.

```
PIPE(t) = sum of proposed issue size in DRHPs filed in trailing 63 trading days   (₹ cr)
APPR(t) = sum of issue size with live SEBI observations (valid 12 months) not yet issued
PIPE_SIG(t) = z_exp( (PIPE + 0.4 * APPR) / free_float_mcap(t) )
```

Book-built DRHPs before ~2022 often omit a rupee amount for the OFS portion. Where the amount is missing, fall back on a **count-based** z-score for that observation and flag the coverage ratio; if amount-coverage drops below 60% for a quarter, use counts for the whole quarter rather than mixing.

The four episodes the owner named line up on this indicator with almost embarrassing neatness. Reliance Power (₹11,563 cr, the largest Indian IPO to that date) opened on 15 January 2008 — the Nifty peaked on **8 January 2008**. Paytm (₹18,300 cr, again the largest ever) opened 8 November 2021 — the Nifty peaked on **19 October 2021**. In both cases the *record issue* came within a month of the top, and the *pipeline* had been at a z-score above +2 for a quarter before it. That is the signal.

### 4.3 Insider and promoter supply

Three instruments, three frequencies:

| Signal | Definition | Freq | Threshold |
|---|---|---|---|
| `INSIDER_NET_20d` | Σ(promoter + designated-person **sell** value) − Σ(**buy** value) over 20 trading days, from PIT Reg 7(2) filings, / 20d cash turnover | Daily | z > +1.5 → −0.5; z > +2.5 → −1.0. Symmetric on the buy side, which is the *stronger* of the two directions (insiders buy for one reason and sell for many — Lakonishok & Lee 2001) |
| `PROMOTER_STAKE_D4Q` | Float-weighted mean promoter holding %, 4-quarter change, universe-wide | Quarterly | < −0.8 pp → −0.5; < −1.5 pp → −1.0 |
| `PLEDGE_RATIO` | Σ encumbered promoter shares / Σ promoter shares, universe-wide; and its 4-quarter change | Quarterly | Level z > +1.5 **and** index 6m return < 0 → forced-selling risk; exported to L03 as `pledge_stress` |

Following Cohen, Malloy & Pomorski (2012), *Decoding Inside Information*, split PIT filings into **routine** (an entity that trades in the same calendar month in ≥3 of the prior 5 years) and **opportunistic**, and weight opportunistic trades 2:1. This is computable from free NSE filings and is DEFERRED to v2 only because it needs the entity-history table.

### 4.4 Buybacks, and a real regime break

Buybacks are the offset term. From **1 October 2024** buyback proceeds are taxed as dividend income in the shareholder's hands, which collapsed Indian buyback activity. This is not a data artefact to be smoothed — it is an economics change. Handle it explicitly:

```
BUYBACK_ADJ(t) = BUYBACK_ACTUAL(t) if t >= 2024-10-01
                 else BUYBACK_ACTUAL(t) * lambda_regime
lambda_regime = median(BUYBACK post-2024-10 / trailing mcap) / median(BUYBACK pre / trailing mcap)
```
estimated once, on ≥3 years of post-break data, and until then set `lambda_regime = 1` with buybacks capped at 15% of the gross-supply term so the pre-break series cannot dominate. Report `lambda_regime` in every backtest header.

---

## 5. Positioning and leverage — and the structural break

### 5.1 The break, stated precisely

| Date | Change | Effect on the data |
|---|---|---|
| **20-Nov-2024** | Index derivative minimum contract value raised from ₹5–10 lakh to **₹15–20 lakh**; weekly expiries cut to **one benchmark index per exchange** | **Contract counts are discontinuous.** Any OI series in contracts breaks here. Weekly-expiry OI/PCR series for the discontinued indices simply end |
| **01-Feb-2025** | Upfront collection of option premium from buyers | Retail short-option writing falls; the client category's option composition changes character |
| **10-Feb-2025** | Calendar-spread margin benefit removed on expiry day | Expiry-day OI behaviour changes |
| **01-Apr-2025** | Intraday monitoring of position limits | Intraday OI profile changes |
| **01-Jul-2025 → 05-Dec-2025** | SEBI circular of **29-May-2025**: **Future Equivalent (delta-adjusted) Open Interest**; index options net limit **₹1,500 cr FutEq**, gross **₹10,000 cr**; glide path over the window | The *definition* of open interest changes. Pre- and post- OI are not the same quantity |

Observed magnitude: index option volumes **−52%** across NSE+BSE in FY26; unique individual F&O investors **98.10 → 78.60 lakh**; unique F&O traders **−20% to 6.7 million**; NSE F&O turnover −18% in FY26.

### 5.2 The rules that follow (binding on implementation)

1. **No F&O quantity may enter this layer as a level across 20-Nov-2024.** Only scale-free ratios.
2. **PCR must be computed on the monthly-expiry series only** — the last-expiry-of-month Nifty contract chain — never on weekly series. Expiry rationalisation destroyed weekly-series continuity; the monthly series survives it intact. This single choice is what makes a continuous 2008–2026 PCR possible at all.
3. **Block B is demoted to tier C** (max influence 3 pp aggressive / 2 pp moderate, per `01-CYCLE-THEORY.md §5`) until five years of post-break data exist, i.e. not before late 2029. Its thresholds are **priors, never fitted**.
4. Any signal that needs the pre-2024 retail-option-frenzy regime — small-lot option volume share, weekly-expiry gamma proxies — is **dropped**, not proxied.

### 5.3 The surviving signals

```
FII_LSR(t)    = FII_fut_index_long / (FII_fut_index_long + FII_fut_index_short)   # from fao_participant_oi
CLIENT_LSR(t) = same for the Client category
PCR_M(t)      = OI_put / OI_call, monthly-expiry Nifty chain only
MTF_RATIO(t)  = MTF_book / free_float_mcap
MTF_DIVERG(t) = z_exp(126d growth of MTF_book) * (1 if Nifty500_126d_return < 0 else 0)
DELIV(t)      = z_exp( turnover-weighted market-wide DELIV_PER, 20d mean )     # low = speculative churn
```

| Signal | Bearish (euphoria) | Bullish (capitulation) | Note |
|---|---|---|---|
| `FII_LSR` | > 0.72 | < 0.22 | Ratio form is break-proof. Priors from pre-2024 tape behaviour, not fitted |
| `CLIENT_LSR` | > 0.75 | < 0.30 | Retail is the weak hand; sign is opposite to FII |
| `PCR_M` | < 0.80 | > 1.35 | Monthly series only |
| `MTF_RATIO` z | > +1.5 | < −1.0 | Expanding-window z |
| `MTF_DIVERG` | > +1.0 | n/a | **Asymmetric by construction** — leverage rising into a falling market is a warning; falling leverage into a rising market is not a signal |
| `DELIV` z | < −1.5 | > +1.5 | Inverted sign |

`MTF_DIVERG` is the most valuable single item here and is firing today: the MTF book is up 65% over twelve months during which the Nifty returned −4.4%. That configuration — a growing levered bid absorbing a de-rating — is what turns an orderly de-rating into a liquidation, and it is precisely why §7.4 argues the 2026 print should be in the low 30s and not below 15.

---

## 6. Sentiment and breadth

| Signal | Definition | Source | Freq |
|---|---|---|---|
| `VIX` | India VIX close | NSE | D |
| `VRP` | India VIX / (annualised 20d realised vol of Nifty 50 × 100) | Computed | D |
| `VIX_TS` | 60d ATM IV − 30d ATM IV, Nifty | **See below** | D |
| `PCT200` | Fraction of NIFTY 750 constituents above their own 200-dma | L19 panel | D |
| `NHNL` | (52w new highs − 52w new lows) / count, 10d mean | L19 panel | D |
| `ADLINE` | Cumulative (advances − declines), NSE all-equity | L19 panel | D |
| `SMLC` | Nifty Smallcap 250 TRI / Nifty 100 TRI, 252d change | niftyindices | D |
| `DEMAT_INT` | 3m mean monthly gross demat additions / total accounts, annualised | SEBI Bulletin | M |

**The VIX term-structure hole, stated honestly.** India has no liquid VIX futures curve, so there is no free, continuous, backtestable term structure. Two options: (a) reconstruct 30d and 60d ATM implied vol by inverting Black-76 on F&O bhavcopy settlement prices, near- and next-month, using MIBOR as the rate — this **is** feasible from free data back to roughly 2001 and is the right answer, but it is 6–8 person-days and belongs in v2; (b) MVP proxy: use **`VRP`** alone. VRP captures most of what a term-structure signal would, with one line of code.

`VRP` bands (priors; India's long-run mean is near **1.25** `[verify]`): < 0.85 → fear is *under*priced relative to what is actually happening, typical of the middle of a crash, score +1 (capitulation) · 0.85–1.10 → +0.5 · 1.10–1.45 → 0 · 1.45–1.75 → −0.5 · > 1.75 → complacency, −1.

`PCT200` bands: < 15% → +1 · 15–30% → +0.5 · 30–70% → 0 · 70–82% → −0.5 · > 82% → −1.

`DEMAT_INT` is deliberately an *intensity* ratio, not a count. Gross additions of 2.9 mn/month on a 23.4 crore base (≈1.24%/month) is a far lower entrant intensity than 2021's ~2.6 mn/month on a ~7 crore base (≈3.7%/month), even though the absolute numbers look similar. The ratio is the signal.

---

## 7. The composite EUPHORIA / CAPITULATION score

### 7.1 Construction

Four blocks. Weights are **priors set from the evidence hierarchy in §4 and §5, not fitted** — with roughly eight observations of the 1–3 year flow cycle in India (`ROADMAP` cycle ladder), fitting more than about four free parameters is overfitting, and Baker–Wurgler-style PCA on a sample this short is not defensible.

| Block | Weight | Members (within-block weights) |
|---|---|---|
| **A — Supply** (issuers and insiders; slow, leading) | **0.30** | `NSR_12m` band score 0.40 · `PIPE_SIG` 0.25 · `INSIDER_NET_20d` 0.20 · `PROMOTER_STAKE_D4Q` 0.15 |
| **B — Positioning and leverage** (fast, mean-reverting, break-damaged) | **0.25** | `MTF_DIVERG` 0.35 · `FII_LSR` 0.25 · `PCR_M` 0.20 · `DELIV` 0.20 |
| **C — Sentiment and breadth** (fastest; **residualised**, see §7.2) | **0.25** | `VRP` 0.25 · `PCT200` 0.25 · `SMLC` 0.25 · `NHNL` 0.15 · `DEMAT_INT` 0.10 |
| **D — Discretionary flows** (coincident) | **0.20** | `LUMP_SIG` 0.35 · `NFO_SHARE` 0.25 · `FPI_SIG` 0.25 · `SIP_STOPPAGE` (inverted) 0.15 |

**The SIP contribution level is deliberately absent.** It is a near-deterministic uptrend; including it would inject a permanent positive drift into the euphoria score and the model would read every year as more euphoric than the last. Only the *stoppage ratio* carries information.

All z-scores are **robust and expanding-window**:

```
z_exp(x, t) = clip( (x_t - median(x_{0..t})) / (1.4826 * MAD(x_{0..t})), -3, +3 )
```
with a minimum 1,250-observation (5-year) warm-up before a series may contribute; before that its weight is redistributed within its block. Median/MAD rather than mean/sd because every flow series in India is heavily right-skewed and a single 2008 or 2020 print destroys a mean-based z.

```
EUPH_raw(t) = 0.30*A + 0.25*B + 0.25*C + 0.20*D
EUPH(t)     = 100 * expanding_percentile_rank(EUPH_raw, t)
              # Gaussian-CDF fallback 100*Phi(z_exp(EUPH_raw)) while sample < 5 years
```

### 7.2 The residualisation requirement (non-negotiable)

`PCT200`, `NHNL` and `ADLINE` are breadth measures that are close cousins of L08's aggregate trend state, and `SMLC` overlaps L09's size factor. Stacking them naively means the cash-call engine receives one bet reported twice. Before block C is formed:

```
for s in [PCT200, NHNL, ADLINE, SMLC]:
    resid_s = s - beta_s * L08.trend_state_aggregate      # beta from a 3y rolling OLS, refit monthly
    use resid_s in block C
```
A CI test must assert `|corr(EUPH_raw, L08.trend_state_aggregate)| < 0.55` over any rolling 3-year window. If it breaches, the layer's influence cap is automatically halved until it is fixed. This implements `01-CYCLE-THEORY.md §6` (aliasing).

### 7.3 Hysteresis and smoothing

Zone membership uses a Schmitt trigger: a boundary must be crossed by **≥3 points**, and a minimum dwell of **15 trading days** applies before a zone change is recognised. The emitted tilt is then exponentially smoothed with a **10-trading-day half-life**. Raw `EUPH` is published unsmoothed for diagnostics.

### 7.4 Calibration against dated Indian extremes

These are **design targets with their driving evidence**, not backtest output — the model does not exist yet. The v1 acceptance test in §12 is that the built composite lands within the stated band at each date without any parameter having been tuned to make it do so.

| Episode | Date | What was actually true | A / B / C / D | Target `EUPH` |
|---|---|---|---|---|
| **Peak, 2007-08** | 8-Jan-2008 | NSR ≈2.7% (record); Reliance Power ₹11,563 cr opens 15-Jan; FPI bought a record ₹71,486 cr in CY2007 `[verify]`; retail demat and F&O frenzy; breadth extreme | ++ / ++ / ++ / ++ | **96–99** |
| **Trough, COVID** | 23-Mar-2020 | Primary market shut, pipeline zero; India VIX **83.6** all-time high; `PCT200` ≈2%; FPI sold ₹62,000 cr in March alone; SMLC at a multi-year low | −− / −− / −− / −− | **2–5** |
| **Peak, 2021** | 19-Oct-2021 | FY22 IPO record ₹1.11 lakh cr; Zomato/Nykaa/Paytm; NFO share >18%; demat intensity ≈3.7%/month (all-time); SMLC at cycle high; MTF rising | ++ / + / ++ / ++ | **88–94** |
| **Trough, 2023** | 28-Mar-2023 | Post-Adani; FPI selling; IPO market frozen (FY23 ₹52,116 cr, half of FY22 `[verify]`); SMLC at a 2y low; `PCT200` ≈25%; **VIX only ~13 — a grind, not a panic** | − / 0 / − / − | **15–25** |
| **Small-cap euphoria peak** | ~8-Feb-2024 | SME IPOs 100x+ subscribed; SMLC at an all-time high; `PCT200` >85%; thematic NFO boom; SEBI publicly flagged "froth"; AMFI mandated mid/small-cap stress tests and several AMCs restricted lumpsum inflows | ++ / + / ++ / ++ | **90–95** |
| **Small-cap de-rating trough** | ~Mar-2026 | Smallcap 250 −23% from Sep-24; `PCT200` <20%; SIP stoppage >100%; **but** FY26 IPO issuance a record and **MTF book still rising** | 0 / **+** / −− / − | **28–36** |

The last row is the one that matters. A naive breadth-only or VIX-only sentiment gauge would have printed sub-15 in March 2026 and called a washout. The composite should not, because **supply never stopped and leverage never left** — and a de-rating with leverage intact is not a capitulation. Equally, the February 2024 row is the layer's hardest lesson: `EUPH` was correctly extreme **seven months before the Smallcap 250 actually peaked in September 2024**. An ungated contrarian short at 90 would have been right eventually and ruinous in the interim. That single fact determines the design of §8.

---

## 8. The mapping: contrarian at extremes, momentum-confirming in the middle

### 8.1 The transfer function

| Zone | `EUPH` | Regime | `tilt` |
|---|---|---|---|
| Capitulation | 0 – 12 | Contrarian long, unconditional | +0.70 → **+1.00** |
| Recovering | 12 – 30 | Contrarian long, fading linearly | +0.20 → +0.70 |
| Neutral | 30 – 62 | **Dead band** | 0.00 |
| Confirmation | 62 – 80 | **Momentum-confirming** | 0.00 → +0.30 |
| Distribution | 80 – 90 | Contrarian short, ramping — **gated** | 0.00 → −0.60 |
| Euphoria | 90 – 100 | Contrarian short — **gated** | −0.60 → −1.00 |

```python
def tilt(E, gate_open, trend_up):
    if E <= 12:  t = 1.00
    elif E <= 30: t = 0.70 - 0.50*(E-12)/18
    elif E <= 62: t = 0.00
    elif E <= 80: t = 0.30*(E-62)/18
    elif E <= 90: t = -0.60*(E-80)/10
    else:         t = -0.60 - 0.40*min((E-90)/10, 1.0)
    if t > 0 and E > 62 and not trend_up:   t = 0.0     # no confirmation without a trend to confirm
    if t < 0 and not gate_open:             t = 0.0     # the gate — see 8.2
    return t
```

### 8.2 The crossover, and the gate

**The lower crossover is at `EUPH` = 30 and is unconditional.** Below 30 the layer is contrarian-long with no further test.

**The upper crossover is at `EUPH` = 80 and is conditional.** Above 80 the layer becomes contrarian-bearish **only if a deterioration trigger also fires** — at least one of:

- **(a) Sentiment momentum has rolled over.** `EUPH` is ≥8 points below its trailing 60-trading-day maximum.
- **(b) Breadth divergence.** Nifty 500 within 2% of its own 60-day high **while** `PCT200` is ≥10 pp below *its* 60-day high. This is the 2018 signature exactly — the Nifty made highs through 2018 while small-caps fell ~30%.
- **(c) Trend break.** L08's aggregate trend state for the Nifty 500 has flipped from `up` to `neutral` or `down`.

If `EUPH` ≥ 80 and **no** trigger fires, the tilt is clamped to **0.00** — neutral. The layer stands aside. It does not go long into euphoria and it does not fight it either.

**The asymmetry is deliberate and should be defended, not apologised for.** Buying panic early costs drawdown, which the portfolio can survive by construction. Selling euphoria early costs the entire back half of a bull market, which in India — where upside tails are fat and the 2003-07, 2013-17 and 2020-24 advances each ran for two-plus years past the first "expensive" reading — is the more expensive error. The February-2024 case in §7.4 is the empirical justification: gate (b) or (c) would have deferred the bearish flip from February 2024 to roughly September–October 2024, converting a seven-month early exit into a near-coincident one.

### 8.3 Output contract

```python
@dataclass(frozen=True)
class FlowsSentimentState:
    asof: date
    euph: float                    # 0-100, smoothed
    euph_raw: float                # unsmoothed, diagnostics
    zone: Literal["capitulation","recovering","neutral","confirmation","distribution","euphoria"]
    gate_open: bool
    gate_reason: list[str]         # which of (a)/(b)/(c) fired
    tilt: float                    # -1..+1
    equity_tilt_pp: float          # tilt * max_influence_pp  (10.0 aggressive / 6.0 moderate)
    blocks: dict[str, float]       # A_supply, B_positioning, C_sentiment, D_flows -> z
    net_supply_ratio_12m: float
    pipeline_z: float
    domestic_cushion_ratio: float
    fpi_dii_divergence: float
    leverage_stress: float         # 0-1, from MTF_DIVERG and MTF_RATIO
    pledge_stress: float           # 0-1, exported to L03
    smallcap_risk_appetite: float  # -1..+1, exported to L10 / L14
    derisk_score: float            # 0-1, exported to L17
    hedge_intensity: float         # 0-1, exported to L16
    staleness_days: dict[str,int]
    coverage: dict[str,float]      # weight fraction present, per block
    confidence: float              # 0-1
```

```python
# to L17 (cash-call engine)
derisk_raw   = max(0.0, (euph - 72.0) / 23.0)          # 0 at 72, 1.0 at 95
derisk_score = derisk_raw * (0.60 + 0.40*leverage_stress) * (1.0 if gate_open else 0.35)
if euph < 40: derisk_score = 0.0                        # never de-risk into a panic

# to L16 (options overlay)
if euph >= 60:
    hedge_intensity = clip(0.55*(euph/100) + 0.45*(1 - vix_pctile), 0.0, 1.0)
else:
    hedge_intensity = 0.15                              # standing baseline
```

Note the structure of `hedge_intensity`: it rises when euphoria is high **and volatility is cheap**. Buying insurance when it is cheap and feels unnecessary is the only time it is worth buying. Note also that `derisk_score` is not zeroed when the gate is shut, only heavily damped to 0.35 — a shut gate means "do not fight the trend", not "ignore the risk".

**Influence budget.** The `ROADMAP` cycle ladder grants this layer two rows — *Flows and supply* (8 pp / 5 pp) and *Small-vs-large cap cycle* (8 pp / 5 pp) — which naively sum to 16 pp. Per `01-CYCLE-THEORY.md §6` these are one family and must be consolidated. **Proposal: 10 pp aggressive / 6 pp moderate on the equity-vs-cash axis, plus a separate 5 pp / 3 pp on the size (small-vs-large) tilt**, with block B capped at 3 pp / 2 pp inside that budget until the post-reform F&O sample is adequate.

---

## 9. Decay and staleness

Flow signals rot. Each input carries `last_update` and a half-life; past `max_staleness` the contribution decays as `exp(-ln2 * (age - max_staleness) / half_life)` and `confidence` falls. If a block's live weight coverage drops below **60%**, the block's z is set to 0 and `EUPH_raw` renormalises over the surviving blocks.

| Signal | Half-life | Max staleness | Why |
|---|---|---|---|
| `FII_LSR`, `PCR_M` | 5 td | 3 td | Fastest in the layer; a stale positioning read is worse than none |
| `VRP`, `VIX` | 6 td | 3 td | |
| `FPI_SIG` (63d sum) | 45 td | 5 td | The daily print decays in ~8 td; only the quarter-sum persists |
| `NHNL` | 10 td | 5 td | |
| `PCT200`, `INSIDER_NET_20d` | 15 td | 5 td | |
| `MTF_DIVERG` | 30 td | 10 td | |
| `SMLC` (252d) | 60 td | 10 td | |
| `LUMP_SIG`, `NFO_SHARE` | 3–4 months | 45 d | Monthly AMFI cadence plus publication lag |
| `SIP_STOPPAGE` | 3 months | 45 d | |
| `PIPE_SIG` | 4 months | 60 d | Filings lead issuance 3–6 months |
| `NSR_12m` | **6 months** | 90 d | The layer's slowest and most durable leg; supply overhang genuinely persists |
| `PROMOTER_STAKE_D4Q`, `PLEDGE_RATIO` | 2 quarters | 150 d | Quarterly filings, ≤21-day lag |
| `DEMAT_INT` | 6 months | 60 d | |
| SIP contribution *level* | n/a — a level, not a signal | 60 d | Enters `domestic_cushion_ratio` only |

---

## 10. MVP vs deferred

**MVP (v1, must exist in the 3–6 month window). ≈23 person-days.**

| # | Deliverable | Days |
|---|---|---|
| 1 | NSDL FPI daily parser → `FPI_SIG`, `FPI_DII_DIVERGENCE` | 1.0 |
| 2 | NSE FII/DII cash daily → `DII_SIG` | 0.5 |
| 3 | AMFI monthly parser (XLS+PDF) → equity net, SIP contribution, stoppage ratio, NFO amount; forward-archiver | 2.0 |
| 4 | `NSR_12m` from primary issuance (IPO/FPO/QIP/OFS) + free-float mcap, with the ratio thresholds of §4.1 | 3.0 |
| 5 | SEBI DRHP/observation scrape → `PIPE_SIG` | 2.0 |
| 6 | NSE PIT Reg 7(2) insider filings → `INSIDER_NET_20d` (unfiltered; no routine/opportunistic split) | 2.5 |
| 7 | NSE MTF daily report → `MTF_RATIO`, `MTF_DIVERG`, `leverage_stress` | 1.5 |
| 8 | `fao_participant_oi` parser → `FII_LSR`, `CLIENT_LSR`; monthly-series `PCR_M` from F&O bhavcopy | 1.5 |
| 9 | India VIX + `VRP` | 0.5 |
| 10 | Breadth from L19 panel: `PCT200`, `NHNL`, `ADLINE`, `SMLC`; residualisation against L08 | 2.0 |
| 11 | Composite, zone machine, hysteresis, transfer function, full output contract, property tests | 4.0 |
| 12 | Episode replay and calibration report against the six dates in §7.4 | 3.0 |

**Deferred (v2+).**

| Item | Days | Why deferred |
|---|---|---|
| ATM IV term structure via Black-76 inversion on F&O bhavcopy | 6–8 | Real work, and `VRP` covers most of it |
| Promoter stake and pledge aggregation across 750 names (quarterly XBRL) | 5 | Blocked on L19's XBRL ingestion |
| Routine vs opportunistic insider split (Cohen–Malloy–Pomorski) | 3 | Needs a 5-year entity-history table |
| Block/bulk-deal PE-exit classification | 4 | Needs a maintained counterparty entity list |
| Buyback series with the Oct-2024 regime adjustment | 2 | `lambda_regime` not estimable before ~2028 |
| EPFO / NPS / IRDAI flows modelled rather than constant | 4 | Low signal-to-effort |
| FPI fortnightly **sector** AUC deltas → L10 | 3 | Useful but L10 has its own momentum |
| Market-wide delivery-percentage series | 1.5 | Nice-to-have |
| Client-category option positioning re-fit post-reform | — | **Blocked by time, not effort.** Needs ~5 years of post-Nov-2024 data |

---

## 11. Risks and honest limitations

1. **The SIP cushion is an untested extrapolation.** Stated in full in §3.3. The entire modern SIP book has never seen a Nifty drawdown beyond ~16%. The `sip_stress` override is a prior with no data behind it, and every drawdown statistic must be reported with and without it. If the 30–35% ceiling is only met unstressed, it is not met.
2. **The F&O series break is not fully repairable and block B is weak until 2029.** As of August 2026 there are ~1.8 years of post-break data. Ratio-form signals with prior thresholds are the honest maximum; anything fitted is fitted to noise. Block B is demoted to tier C accordingly.
3. **This layer cannot deliver the drawdown objective on its own, and claiming otherwise would be dishonest.** In a March-2020-shaped event — 38% in about 30 trading days — flow and supply signals lead by days at best. Realistically this layer contributes **2–4 pp** of pre-emptive de-risking into a fast crash; the rest must come from L17's trend and volatility machinery and L16's standing hedge. Where it genuinely earns its keep is the *slow* de-rating — 2018, 2022, the Sep-2024→Mar-2026 small-cap grind — where the supply leg leads by three to six months. Design the cash engine's expectations accordingly.
4. **Prior-set weights are a confession, not a shortcut.** With ~8 observations of the 1–3 year flow cycle, the §7.1 weights are defensible priors and nothing more. They must not be optimised on the same six calibration episodes they are validated against; doing so converts the calibration table from a test into a tautology.
5. **AMFI has no vintage archive.** Everything AMFI-derived before our forward-archive begins is `lag-approximated`, not point-in-time, and must be labelled as such in every backtest header.
6. **Aliasing with L06 and L08 is real.** L06 uses the same NSDL FPI series for BoP financing; L08 owns trend and its breadth cousins. §7.2's residualisation and the `|corr| < 0.55` CI assertion are the mitigation, and the automatic influence-halving on breach is the enforcement. Without them the cash engine receives a bet roughly twice its intended size — which is exactly how a levered book breaches a drawdown limit.
7. **No free India VIX term structure with history exists.** Genuine hole; §6 states the workaround and its cost.
8. **Free-source fragility.** SEBI reorganises its filings pages periodically and links break silently. NSE requires session priming and rate limiting. Every scraper needs an integrity check that fails loudly on a schema change rather than returning an empty frame that a z-score will happily treat as zero.

**Constraint conflicts to escalate.** (i) The ladder grants this layer 16 pp across two rows that are one family — §8.3 proposes 10/6 plus 5/3 and needs owner ratification. (ii) The relative-drawdown objective implicitly assumes a layer like this can pre-empt a fast crash; risk 3 says it cannot, and the resolution belongs in L17's design, not here.

---

## 12. Falsification protocol

The layer ships only if all four pass, with parameters frozen before the tests are run:

1. **Episode replay.** `EUPH` lands inside the §7.4 bands at all six dates, with no parameter tuned to make it do so. Any band missed by more than 10 points is a design failure, not a calibration adjustment.
2. **The gate earns its keep.** Backtest `tilt` with and without the §8.2 gate. The gated version must have a materially better return over the Feb-2024→Sep-2024 and Jan-2007→Jan-2008 windows, and must not be worse over 2020 or 2008. If the gate does not help, delete it — an unused complication is worse than none.
3. **Supply-leg standalone.** `NSR_12m` alone, as a univariate predictor of forward 12-month Nifty 500 TRI return, must show a monotonic decline in mean forward return across its six bands over 2001–2026. This is the one leg with real academic backing (Baker–Wurgler 2000); if it does not replicate in India, say so in the results rather than burying it in a composite.
4. **Ablation.** Drop each block in turn. If dropping block B or D improves out-of-sample Sharpe of the quant-only portfolio, drop it permanently.

---

## 13. References

Marked `[verify]` where I am confident of the finding but not of the exact citation.

- **Baker, M. & Wurgler, J. (2000)**, *The Equity Share in New Issues and Aggregate Stock Returns*, Journal of Finance — the equity share of new issues predicts aggregate returns. The academic basis for §4.1.
- **Baker, M. & Wurgler, J. (2006, 2007)**, investor-sentiment index construction — the methodological template. This spec uses theory-weighted blocks rather than PCA because the Indian sample is too short for PCA.
- **Baker, M., Wurgler, J. & Yuan, Y. (2012)**, *Global, Local, and Contagious Investor Sentiment*, JFE — cross-market sentiment indices.
- **Ritter, J. (1991)**, *The Long-Run Performance of Initial Public Offerings*, JF; **Loughran, T. & Ritter, J. (1995)**, *The New Issues Puzzle*, JF — heavy IPO volume predicts poor subsequent returns.
- **Lakonishok, J. & Lee, I. (2001)**, *Are Insider Trades Informative?*, RFS; **Jeng, L., Metrick, A. & Zeckhauser, R. (2003)**, *Estimating the Returns to Insider Trading*, REStat — aggregate insider activity has predictive content, asymmetric toward buys.
- **Cohen, L., Malloy, C. & Pomorski, L. (2012)**, *Decoding Inside Information*, JF — routine vs opportunistic insider trades.
- **Frazzini, A. & Lamont, O. (2008)**, *Dumb Money: Mutual Fund Flows and the Cross-Section of Stock Returns*, JFE; **Warther, V. (1995)**, *Aggregate Mutual Fund Flows and Security Returns*, JFE — retail fund flows are return-chasing and negatively predictive.
- **Froot, K., O'Connell, P. & Seasholes, M. (2001)**, *The Portfolio Flows of International Investors*, JFE — EM portfolio flows exhibit positive feedback and price impact.
- **Chakrabarti, R. (2001)**, *FII Flows to India: Nature and Causes*, Money & Finance `[verify title/venue]` — FII flows into India are largely a consequence of Indian returns rather than a cause. Directly motivates the positive sign on `FPI_SIG` in §3.2.
- **Barber, B. & Odean (2000, 2008)** — retail attention and trading behaviour.
- **SEBI**, annual studies on individual traders' profit and loss in the equity F&O segment (FY22 onward), `sebi.gov.in` — the definitive free evidence on Indian retail derivative behaviour and on the effect of the 2024-25 reforms.
- **SEBI circulars**: index derivative measures dated 1-Oct-2024 (effective 20-Nov-2024, 1-Feb-2025, 1-Apr-2025) and 29-May-2025 (FutEq OI, effective 1-Jul-2025 → 5-Dec-2025). Primary sources for §5.1 — **fetch and pin the exact circular numbers before implementation**.
- **Data portals**: NSDL FPI `fpi.nsdl.co.in` · AMFI `amfiindia.com/research-information/amfi-monthly` · SEBI Bulletin and public-issue filings `sebi.gov.in` · NSE archives `nsearchives.nseindia.com`, all-reports and corporate-filings sections · niftyindices.com · IRDAI `irdai.gov.in` · NPS Trust `npstrust.org.in` · Prime Database press releases `primedatabasegroup.com/newsroom` (free PR tables; the database itself is paid and is used only as a cross-check).
