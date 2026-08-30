# Layer 09 — Cross-Sectional Factor Library for the NIFTY 750

**Abstract.** This layer converts free Indian accounting and price data into one signed score per name, and it is the largest single block of MVP signals in the stack. Its organising conclusion is uncomfortable and shapes everything below: **the fundamental half of a factor library cannot be built point-in-time from free Indian data, and a backtest of it is biased upward by an amount we can bound but not remove.** The response is not to abandon fundamentals but to ship two books — a genuinely point-in-time **price-only factor book (PO-FL)**, buildable in four engineer-days from bhavcopy alone and a real strategy in its own right, and a fundamental book (FUND-FL) whose entire measured performance gap against PO-FL is reported as the upper bound on data artefact. A second, sharper measurement — replaying the same book on our own forward-archived as-first-reported filings versus today's restated ones — becomes available two years after the archive starts, which is why the archive starts on day one and not in Phase F. Factor scores are computed **within sector**, because Indian accounting ratios are not comparable across sectors and because a raw cross-sector value score is a disguised sector bet that would double-count L10's `sector_rotation_cycle` budget; the sector tilt arrives separately and explicitly. Factors are combined by **integration into a single composite**, not as a portfolio of sleeves, but momentum is deliberately excluded and left to L08 so that its crash machinery can act on it in isolation. Factor timing is permitted in three narrow channels with a hard ±25% relative cap and a kill rule. Financials are scored in their own pool with their own factor set. The layer delivers the project's second most uncomfortable arithmetic: at ₹1,000 crore, capacity is *not* the factor sleeve's binding constraint — breadth and turnover are — and because value and quality have a `tau_half` roughly five times momentum's, **the factor book, not momentum, should be the moderate book's primary name-level engine.**

---

## 1. Scope, and what this layer must not rebuild

**Owns.** Definition, construction, normalisation, compositing and timing of cross-sectional *characteristic* factors over the NIFTY 750: value, quality, low-risk, size (and size×quality), yield, and the negative forensic factor. Owns the price-only factor book as a first-class deliverable. Owns the per-name `FACTOR_SCORE` and a complete Stage-1-sufficient `FACTOR_SLEEVE`.

| Belongs to | Do not duplicate here |
|---|---|
| **L08 momentum** | Any signal built from returns in the window `t−12m → t−1m`, `t−1m`, 52-week-high distance, or trend/breadth. **My composite contains no momentum factor.** My long-horizon reversal uses `t−60m → t−13m` only — a disjoint window, agreed as the boundary |
| **L10 sector model** | Sector weights. I emit sector-*neutral* scores plus a zero-budget `lowvol_sector_component` recommendation |
| **L11 bottom-up** | Reverse-DCF, incremental ROIC on reinvested capital, per-name narrative scoring. L11 must orthogonalise against my `qual_z`, per ROADMAP week 18 |
| **L05 valuation** | Aggregate market valuation, the CMA, `value_spread_z`. I *consume* their spread; I do not compute one |
| **L12 special situations** | Any name with < 252 sessions, or < 8 filed quarters. Routed out, not scored |
| **L17 risk engine** | The risk covariance matrix. L09 owns *return* factors; L17 owns the risk model and consumes my exposures |
| **L14 optimizer** | Target weights, netting across sleeves, the 3–6% entry band, the 10% drift cap |
| **L19 data pipeline** | Raw ingestion, the bitemporal store, corporate actions, membership reconstruction. I consume a `pit_store` interface only |

**Registry position.** This layer owns **no cycle entry**. It is a consumer of four: `equity_valuation_reversion` (via L05's `value_spread_z`), `smallcap_breadth_cycle` (L07), `sector_rotation_cycle` (L10) and `india_business_cycle` (L04). All factor-timing authority is charged against the `name_l1_pp` budgets of those cycles — no new registry entry, no new budget. This is the design choice that keeps §9 inside L01 §8 without a patch.

**Sign convention (L01).** `+1` = characteristic historically associated with higher forward risk-adjusted return. So low beta scores `+1`, high accruals scores `−1`.

---

## 2. Data spine — every route, what it really gives

| # | Object | Free route | History | Coverage | PIT | Tier |
|---|---|---|---|---|---|---|
| 1 | Daily OHLC, volume, series, ISIN | NSE bhavcopy (legacy `cm*bhav`; udiff from 2024) | 1994– | full, incl. delisted | true (reconstructed tape) | **D1/D4** |
| 2 | Free-float market cap | Shareholding pattern (LODR Reg 31) × price | 2001– | ~full | 21-day filing deadline | **D2** |
| 3 | Quarterly results — P&L, segment, standalone + consolidated | NSE/BSE **XBRL** results filings (mandatory for results since ~2017; PDF before) | XBRL ~2017–; PDF 2001– | ~full for XBRL era; parse-dependent before | **restated, no knowledge date** | **D2 → D4** |
| 4 | Balance sheet + cash-flow statement | Half-yearly under Reg 33 + annual audited | 2001– (H1 BS/CFS from 2019 amendments **[verify exact year]**) | ~full annual, weaker half-yearly | restated | **D2** |
| 5 | Bulk historical fundamentals | Kaggle / HuggingFace scrapes (e.g. "Detailed Financials of 4,4xx NSE & BSE companies") | varies, typically 10–15y | 4,000–4,500 names | **restated, survivorship-contaminated** | **D2, degraded** |
| 6 | Shareholding pattern incl. **promoter pledge** | Reg 31 quarterly filings, NSE/BSE | 2009– (pledge disclosure from 2009) | full | 21-day deadline | **D2** |
| 7 | Auditor resignation / change, audit qualification | Reg 30 announcements; Statement of Impact of Audit Qualifications (Reg 33) | 2016– | full | **true PIT** (24h disclosure) | **D1** |
| 8 | ASM / GSM surveillance stages, circuits, price bands | NSE & BSE daily surveillance files | ~2017– **[verify]** | full | true PIT | **D1** |
| 9 | Related-party transactions, contingent liabilities, subsidiary list | Annual report PDF notes; Reg 23 material-RPT disclosures | 2001– | parse-dependent, poor | restated | **D4** |
| 10 | R&D spend, SG&A decomposition (for intangibles adjustment) | Directors' Report (Cos Act Rule 8(3)); not in results filings | patchy | poor | — | **D5** |
| 11 | Sector classification (NSE 4-tier macro/sector/industry) | niftyindices factsheets, NSE industry files | current free; history D4 | full | current-as-of-today | **D2/D4** |
| 12 | IIM-A Fama-French + momentum factor returns (SMB/HML/WML/MRP) | `faculty.iima.ac.in/iffm/` | 1993– daily & monthly | index-level | true PIT | **D1 — validation only** |

**Three consequences that are not negotiable.**

1. **Row 3 is the whole game and it is D2.** Quarterly XBRL gives us P&L and little else. Everything requiring a balance sheet or cash-flow statement — ROIC, asset growth, accruals, leverage, cash conversion, FCF yield — is **half-yearly at best**, not quarterly. Any spec that assumes quarterly accruals in India is wrong.
2. **Row 10 is D5.** The intangibles-adjusted book value (Peters–Taylor; Arnott et al. 2021) cannot be built for India from free data. We do not fake it; we route around it (§4.1).
3. **Row 12 may never enter the signal path.** The IIM-A library is built from CMIE Prowess, which we do not license. It is committed as a fixture and used *only* as a validation benchmark (§6), enforced by a CI test that no module in `src/cyclestack/factors/` imports it.

---

## 3. The point-in-time bias, quantified — and the price-only book

### 3.1 Direction and magnitude

Free Indian fundamentals are **as-restated**, published without a knowledge date. Restatements are not symmetric noise: they systematically move bad news — an impairment, a related-party write-off, a revenue-recognition reversal — into a different period or out of the record entirely. A backtest reading restated data therefore *declines to buy* names that, on the data actually visible at the time, looked cheap and clean and then blew up. The bias is **upward, and concentrated in exactly the value-and-quality composite this layer sells.**

Three separable components, each with an explicit derivation and each an estimate, not a measurement:

| Component | Derivation | Estimate (bps/yr on a fundamental long-only tilt) | Removable? |
|---|---|---|---|
| **Survivorship / delisting** | ~1–2% of Indian listed names exit involuntarily per year (suspension, compulsory delisting, insolvency); a value-and-small tilt is roughly 2× overweight them; average terminal loss ~70% | **150–300** | **Yes** — L19's union-of-bhavcopy universe reconstruction |
| **Restatement look-ahead** | Assume ~3% of the long book's name-years are cases where real-time data would have shown a disqualifying figure that restatement later removed; those names lose ~50% in the following year ⇒ `0.03 × 50% = 150 bps` of drag the backtest never takes | **100–300** | **No** — irreducible until the forward archive matures |
| **Reporting-lag error** | Imposing a 45-day lag when ~30% of names file at 45–90 days confers ~15 days of unearned foresight on a third of the book; worth ~1.5% relative on a name near a results date ⇒ `0.33 × 1.5% ≈ 50 bps` | **50–150** | **Mostly** — by the conservative lag table in §7.3 |
| **Total, uncontrolled** | | **300–750** | |
| **Total, after our D4 engineering** | | **150–450** | |

Banz & Breen (1986) is the canonical demonstration that this is not a rounding error: an E/P effect that was significant in ex-post Compustat data was **absent** in point-in-time data. That result is the reason this section exists rather than a footnote.

### 3.2 The price-only variant (PO-FL) — a required deliverable

PO-FL is a complete, tradeable factor book that touches **no accounting data whatsoever** and is therefore genuinely point-in-time. It is built in week one and it is the honest baseline for everything that follows.

| Component | Definition | Sign | Source |
|---|---|---|---|
| `lowbeta` | 24m weekly beta vs Nifty 500 TRI, Dimson-corrected (1 lead, 2 lags), Vasicek-shrunk: `β* = 0.60·β̂ + 0.40·1.0` | − | bhavcopy |
| `idiovol` | Annualised residual σ from a market+size regression on 250 daily obs | − | bhavcopy |
| `maxret` | Mean of the 5 largest daily returns over the past 21 sessions (Bali–Cakici–Whitelaw lottery effect) | − | bhavcopy |
| `size` | `log(free_float_mcap)` | − (weak alone) | bhavcopy × Reg 31 |
| `size_x_lowrisk` | `z(−size) × z(lowbeta + idiovol composite)`, the price-only stand-in for Asness et al.'s "size, if you control your junk" | + | derived |
| `lt_rev` | `−` cumulative return `t−60m → t−13m` (De Bondt–Thaler); **disjoint from L08's window** | + | bhavcopy |
| `illiq` | Amihud `mean(|r_d| / turnover_d)`, 250d, capacity-gated | + | bhavcopy |
| `forensic_px` | ASM/GSM stage, circuit-day count, parabolic filter | one-sided − | NSE surveillance |

**PO-FL is a real strategy, not a placeholder.** Low-risk plus lottery-avoidance plus long-horizon reversal plus a surveillance screen is a defensible defensive-value book, and it is the only part of this layer whose backtest carries no PIT caveat at all.

### 3.3 The two measurements

- **`pit_gap` (available immediately).** `IR(FUND-FL) − IR(PO-FL)` over the same window, same universe, same construction, same cost model. Reported with every backtest, on the cover page, not in an appendix. It is an **upper bound** on the artefact, not an estimate, because the two books also differ in genuine content.
- **`restatement_delta` (available ~2028, and the reason the archive starts now).** From the day the forward archive begins, we hold both the *as-first-reported* and the *current-restated* value of every line item. Replaying FUND-FL on both over the same window isolates the artefact **exactly**. Cost of starting the archive today: zero, beyond the ingestion code L19 is writing anyway. Cost of not starting it: the number is never knowable.

---

## 4. The factor set

Scores are within-sector normal scores (§7.2). `MVP` = v1. `DEF` = deferred to v1.5/v2.

### 4.1 Value (strategic family weight `W_val`: 0.25 both books)

| Factor | Definition | Tier (E/D) | Status | Note |
|---|---|---|---|---|
| `ey` | Trailing-4q PAT (consolidated, before exceptionals) / market cap | B / D2 | **MVP** | Missing, not bottom-ranked, when PAT ≤ 0 (§7.5) |
| `sp` | Trailing-4q net sales / market cap | B / D2 | **MVP** | Always defined; the anchor for loss-makers |
| `ebit_ev` | Trailing-4q EBIT / (mcap + total debt − cash) | B / D2 | **MVP** | Preferred over EV/EBITDA: EBITDA flatters capital-intensive Indian names |
| `bp` | Book value / market cap | B / D2 | **MVP, gated** | **Excluded from the composite in low-tangibility sectors** (§4.1 note) |
| `fcfy` | (CFO − capex), trailing 4 half-years / EV | B / D2 | **MVP (half-yearly)** | Cash-flow statement is half-yearly in India; refreshes twice a year, lag 75/105d |
| `ibp` | Intangibles-adjusted book/price (R&D + 30% SG&A capitalised) | B / **D5** | **CUT** | R&D and SG&A decomposition not free for India. R6 disposition: replaced by the tangibility gate below, tier B→C, no separate budget |

**The book-to-price problem, and the India-specific fix.** B/P misprices asset-light businesses because the balance sheet omits their real capital. In India this is not a fringe case — IT services, pharma formulations, exchanges, asset managers and platform names are a large and growing share of the Nifty 500, and B/P systematically ranks them "expensive" for structural reasons. The literature's answer (Peters & Taylor 2017; Eisfeldt & Papanikolaou 2013; Arnott, Harvey, Kalesnik & Linnainmaa 2021) is to capitalise intangible investment; that requires an SG&A decomposition India does not disclose. **Our fix: a tangibility gate.** For each sector pool, compute the median `net fixed assets / total assets` over the trailing 3 years. Where that median is **< 0.20**, `bp` is dropped from the value composite for every name in the pool and the remaining legs are re-weighted by the §7.6 coverage rule. This is crude, cheap, frozen at inception, and it removes the largest single known defect in a free-data value factor for India.

### 4.2 Quality (`W_qual`: 0.30 aggressive / 0.35 moderate)

| Factor | Definition | Tier | Status |
|---|---|---|---|
| `gpoa` | Gross profit (sales − COGS) / total assets — Novy-Marx | A / D2 | **MVP** |
| `roe` | Trailing-4q PAT / average net worth | B / D2 | **MVP** |
| `roic` | NOPAT / (net worth + total debt − cash), half-yearly | B / D2 | **MVP** |
| `accruals` | (ΔCA − ΔCash) − (ΔCL − ΔSTD) − Dep, / average total assets — Sloan; or `(PAT − CFO)/avg assets` where CFO exists | A / D2 | **MVP (half-yearly)** |
| `asset_growth` | −YoY growth in total assets — Cooper–Gulen–Schill | A / D2 | **MVP** |
| `earn_stab` | −σ(YoY growth in trailing-4q PAT) over 5y / \|mean\| | B / D2 | **MVP** |
| `leverage` | −(total debt / EBITDA), winsorised; and −(net debt / net worth) | B / D2 | **MVP** |
| `cash_conv` | 3y cumulative CFO / 3y cumulative PAT | B / D2 | **MVP** — India's single most informative quality leg (§10) |
| `piotroski_f` | 9-point F-score, half-yearly | B / D2 | **DEF** — largely spanned by the legs above |
| `qmj_full` | AQR profitability + growth + safety + payout | A / D2 | **DEF** |

Weights within family: equal (`w_k = 1`), per methods §4 (DeMiguel–Garlappi–Uppal), except `gpoa` and `cash_conv` at `w = 1.5` — the two with the strongest India-specific and cross-market evidence respectively. Frozen at inception.

### 4.3 Low-risk (`W_lowrisk`: 0.20 aggressive / 0.25 moderate)

`lowbeta`, `idiovol`, `maxret` exactly as in §3.2 — all D1, all in PO-FL, all in FUND-FL unchanged. Frazzini–Pedersen's BAB mechanism (leverage-constrained investors bid up high-beta) applies with extra force in India, where the retail tail is leverage-constrained but lottery-seeking, and the F&O segment concentrates the leverage that does exist into a few hundred names.

**The sector-neutralisation carve-out.** A meaningful share of the low-risk premium is cross-sector (FMCG and pharma are structurally low-beta). Sector-neutralising destroys it. We compute both, use the **within-sector** version in the composite, and export the residual cross-sector component to L10 as `lowvol_sector_component` — a recommendation with **zero own budget**, exactly as L05 exports `value_spread_z`. The sector bet is L10's to take or refuse.

### 4.4 Size and size×quality (`W_size`: 0.15 aggressive / 0.05 moderate)

Raw size is weak in India — the IIM-A library's SMB averaged approximately **0%/yr over Jan-1994 to Dec-2014**, against HML 15.3% and WML 21.9%. Raw `size` therefore enters with weight 0.25 within its family; the family is dominated by the **interaction** `size_x_qual = z(−size) × z(qual_composite)`, weight 0.75, following Asness, Frazzini, Israel, Moskowitz & Pedersen (2018): small caps earn a premium once junk is controlled for, and the Indian micro tail is where junk concentrates. The moderate book's `W_size = 0.05` is not squeamishness, it is that its universe (§11) contains almost no small caps for the tilt to express in.

### 4.5 Yield (`W_yield`: 0.10 both books)

`net_payout = (dividends + buybacks − equity issuance) / market cap`, trailing 12 months, from corporate-action and Reg 30 filings (D1/D2). Issuance is the load-bearing leg in India, where dilution through preferential allotments and QIPs is common and is the cleanest free proxy for the "asset growth financed externally" effect. Dividend yield alone is **not** used standalone: it is a tax-regime artefact post-2020 and a value proxy, not a factor.

### 4.6 Growth — deliberately absent

There is no standalone growth factor in v1. Sustainable growth enters through `roic` and `asset_growth` (with the *negative* sign the evidence supports), through L11's bottom-up scorecard, and through L04's `duration_tilt` style prior. A long-growth factor with a positive sign has no robust cross-market premium and would double-count momentum. **DEF, with prejudice.**

---

## 5. India-specific evidence, and where India differs

The IIM-A library's own numbers, Jan-1994 → Dec-2014, are the reference point (Agarwalla, Jacob & Varma; free, survivorship-corrected, illiquid names excluded):

| Factor | Mean annual return | Implication for us |
|---|---|---|
| Market (MRP) | 11.5% | The beta we are trying to beat |
| **WML (momentum)** | **21.9%** | Strongest India factor — and it is **L08's, not mine** |
| **HML (value)** | **15.3%** | Strong on this window, but with long dead patches (see below) |
| SMB (size) | ≈ 0% | Raw size is not a factor in India; §4.4 |

Four places India genuinely differs, each with a design consequence:

1. **Quality is stronger and value is lumpier.** The quality premium in India is well supported and has become more so post-2015 as the retail-driven micro tail grew (IIMB Management Review, "Beyond junk…", 2026 **[verify journal/volume]**). Value, meanwhile, had a long drought in 2013–2020 mirroring the global one, and a violent 2021–2023 recovery. Consequence: `W_qual > W_val` in both books, and value's timing tilt (§9) is where the value-spread evidence gets its only channel.
2. **Promoter holding and governance have no developed-market analogue.** Indian promoters hold ~50% of their firms on average; pledge, dilution and related-party extraction are the dominant idiosyncratic risks, and they are not in any accounting ratio. Consequence: §10 is not an add-on screen, it is a **factor family with its own weight and its own asymmetry**.
3. **The small-cap tail is very wide and partly synthetic.** Cross-sectional dispersion of 12-month returns is roughly 1.6–1.9× as large in the Nifty Smallcap 250 as in the Nifty 100 **[verify — this is the first diagnostic we compute from our own bhavcopy build, §12 step 1]**. That is where factor alpha lives, and also where operator-driven ramps live. Consequence: the aggressive book gets the tail and the forensic screens; the moderate book gets neither, and §11 prices that.
4. **Accounting comparability across sectors is worse than in the US**, because the listed universe spans a modern IT exporter and a family-controlled sugar mill in the same index. Consequence: within-sector scoring is not a refinement, it is a correctness requirement (§7.2).

---

## 6. The IIM-A library as our validation benchmark

**The rule: if our value factor does not broadly reconcile with theirs, our construction is wrong — not theirs.** They have Prowess, a published methodology, survivorship correction and thirty years of use. We have a scraper.

Reconciliation is a CI test, run against a committed fixture of their monthly SMB/HML/WML/MRP series (attributed, small, redistributable as research data — licence checked at ingestion, `fixtures/iima_iffm_monthly.csv`).

```
For F in {HML, SMB, WML_ref}:                    # WML_ref built only for this test, never traded
    ours   = monthly return of our own long-short decile factor, same period
    theirs = IIM-A series, same period
    ASSERT corr(ours, theirs)                        >= 0.75      # monthly, >= 120 overlapping months
    ASSERT |mean_ann(ours) - mean_ann(theirs)|        <= 4.0 pp
    ASSERT beta(ours ~ theirs)                       in [0.65, 1.40]
    ASSERT max rolling-12m |cum(ours) - cum(theirs)| <= 20 pp
    ASSERT sign agreement in calendar years          >= 70%
```

A failure is a **build-blocking bug report**, and the diagnostic ladder is fixed in advance: (i) universe — are we including illiquid names they exclude? (ii) size breakpoint — they use a distribution-aware cut, not the NYSE-style median; (iii) rebalance date and lag; (iv) survivorship — are our delisted names present? (v) the value definition itself. In practice (i) and (iv) explain most divergence, and both are L19 defects, not factor defects.

**Two hard boundaries.** Their series is *never* an input to a score, a weight, or a fitted parameter — CI asserts no import from the factor package. And a reconciliation pass is **not** validation of our alpha; it validates our *plumbing*. Passing it tells us our HML is an HML. It says nothing about whether HML works next year.

---

## 7. Construction mechanics

### 7.1 Universe

Consume `L08.eligible(i, t)` verbatim — the ADV floor, the 252-session history requirement, the EQ-series and GSM/ASM screens, the parabolic filter. Do not redefine it. Add three fundamental-specific conditions:

```
factor_eligible(i,t) = eligible(i,t)
  and filed_quarters(i, t) >= 8                    # else -> L12 IPO sub-model
  and newest_statement_age(i, t) <= 400 days       # stale filers are excluded, not neutral-scored
  and sector_pool(i, t) is not None
```

### 7.2 Sector pools, and the neutralisation decision

**Decision: all factor scores are computed within sector. Score-level sector-neutrality is mandatory; the sector tilt is L10's separate, explicit, budgeted decision.**

Three reasons, in order of force:

1. **Comparability.** A 4% net margin is excellent for a distributor and catastrophic for a software exporter. A cross-sector rank on any margin- or asset-based ratio is not a factor score, it is a sector score with noise.
2. **Double-counting (L01 §6).** A raw cross-sector value score is ~40–60% a sector bet. Stacking it with L10's `sector_rotation_cycle` (`sector_l1_pp` = 4 aggressive) and L03's `L03_SECTOR_TILT` (L1 ≤ 8) puts three claims on one force — precisely the failure L01 §6.3 collapses from −1,000bps to −350bps. Within-sector scoring removes the overlap by construction rather than by residualisation after the fact.
3. **Accountability.** The book is deliberately sector-*active*. If sector exposure arrives as a side effect of stock scores, no one owns it and no one can be wrong about it. Making it explicit is what makes it reviewable.

**Pools.** NSE's tier-2 sector classification (~22 sectors) collapsed to **12 scoring pools** by merging any sector with `N < 20` eligible names into its nearest macro-sector sibling; merges are frozen in `config/factor_pools.yaml`, not recomputed per date. **Financials are always their own pool** (§7.4), and are further split into Banks / NBFC-and-HFC / Insurance-and-AMC when each has ≥ 20 names.

Sector classification history is D4; v1 applies today's classification backward. Reclassification in India is rare (single-digit names per year), and the induced look-ahead is estimated at **< 20 bps/yr**. Logged as a known bias, scheduled for D4 reconstruction from archived index factsheets in v2.

**Size neutralisation: no.** We do *not* size-neutralise scores. Size is a factor we want exposure to (via `size_x_qual`), and neutralising it would delete §4.4. Instead the *size exposure of the finished sleeve* is measured and reported every rebalance, and it is capped: sleeve `z(size)` must lie within ±0.75 of the benchmark's, so the book cannot become a covert micro-cap fund. The intentional size tilt arrives through L07's `smallcap_breadth_cycle` budget.

### 7.3 The exact point-in-time lag

Two regimes. **Forward (from archive start):** the usable date is the *observed* filing timestamp from our own archive — true PIT. **Historical (reconstruction):** we impose the table below. The effective date is always `max(imposed_date, first_observed_in_archive)`.

| Object | LODR deadline | **Imposed historical lag** | Rationale |
|---|---|---|---|
| Q1/Q2/Q3 results (standalone + consolidated) | 45 days | **period_end + 60 calendar days** | A deadline is not a distribution; the marginal filer files on day 45 and stragglers later. 60d covers ~95% |
| Q4 / annual audited results | 60 days | **period_end + 90 days** | Audit adds dispersion; Q4 is the most-restated period |
| Half-yearly balance sheet + cash-flow statement | with H1 / annual | **period_end + 75 / +105 days** | Drives `accruals`, `cash_conv`, `fcfy`, `roic` — all half-yearly, not quarterly |
| Shareholding pattern, incl. pledge (Reg 31) | 21 days | **quarter_end + 30 days** | |
| Annual report (RPT, contingent liabilities, subsidiaries) | AGM, ≤ 6 months from FY end | **FY_end + 210 days** | The reason §10's D4 screens are deferred |
| Auditor resignation, audit qualification (Reg 30/33) | 24 hours | **announcement_date + 1 day** | True PIT — the forensic screens are the *cleanest* data in the layer |
| ASM/GSM, circuits | daily | **file date** | True PIT |

Consequence worth stating plainly: **the freshest fundamental input to a January score is the September quarter, and the freshest balance-sheet input is the March or September half-year.** The fundamental book is slow by construction. That is a cost in §11 and an advantage in turnover.

### 7.4 Financials

Financials are ~30–35% of the Nifty 500 and their accounting differs in kind, not degree: there is no COGS, no EV, no working capital in the ordinary sense, and debt is raw material rather than leverage. Scoring them in the general pool would be a bug that looks like a factor.

| General pool | Financials pool replacement |
|---|---|
| `gpoa` (gross profit / assets) | `ppop_a` = pre-provision operating profit / average assets |
| `ebit_ev`, `fcfy` | **dropped** — undefined |
| `bp` | **kept, and up-weighted** — P/B is the primary bank valuation metric |
| `asset_growth` | `loan_growth` — same Cooper–Gulen–Schill mechanism; rapid loan growth predicts credit cost |
| `leverage` | `car_tier1` (capital adequacy) and `−(gnpa − pcr_coverage)` |
| `accruals` | `credit_cost_smoothing` = σ(quarterly provisions)/mean, low = suspicious in a rising-NPA cycle |
| `cash_conv` | **dropped** — meaningless |
| `earn_stab` | kept |

Insurance and AMCs get their own sub-pool when populous enough; until then they are scored on `bp`, `roe`, `earn_stab` and `net_payout` only, with a coverage haircut (§7.6). **Embedded value and VNB margin are D4/D5 and deferred.**

### 7.5 Loss-making companies

Three wrong answers are common: rank negative E/P at the bottom (mixes distressed with expensive), rank it at the top (absurd), or set it to zero (fabricates a median). Our rule:

```
if trailing_4q_PAT <= 0:
      ey       = MISSING                       # not 0, not bottom rank
      roe      = MISSING
      distress_flag = True
      value score falls back to {sp, ebit_ev, bp} via the coverage rule
if trailing_4q_EBIT <= 0 as well:
      ebit_ev  = MISSING
      forensic penalty P_i += 0.35 sigma        # persistent operating loss is a red flag, not a value signal
if PAT <= 0 in 3 of the last 4 quarters and net_debt/equity > 1.0:
      HARD EXCLUDE                              # the India "zombie" filter
```

### 7.6 Normalisation and compositing

Rank-based, not raw z-score: Indian small-cap ratios have tails that make a z-score a single-name bet.

```
within pool s, for factor k:
  x_ik    = winsorise(raw_ik, 1st, 99th percentile of pool s)        # methods §6
  r_ik    = average rank of x_ik in pool s
  n_ik    = clip( Phi^-1( (r_ik - 0.5) / N_s ), -2.5, +2.5 )         # van der Waerden normal score
  n_ik    = MISSING if raw is MISSING                                 # never mean-imputed

family score f:
  F_if    = sum_{k in f, observed} w_k * n_ik  /  sum_{k in f, observed} w_k
  c_if    = sum_{k in f, observed} w_k / sum_{k in f} w_k             # coverage in [0,1]
  F_if    = MISSING if c_if < 0.50
  Ftil_if = re-rank F_if within pool s -> normal score                # families made comparable

composite:
  S_i  =  sum_f W_f * sqrt(c_if) * Ftil_if  /  sum_f W_f * sqrt(c_if)     over observed families
  if sum_f W_f (observed) < 0.60:  name is UNSCORED and excluded from the sleeve
  S_i  =  S_i - P_i                                # forensic penalty, one-sided, P_i >= 0  (§10)
  S_i  =  clip(S_i, -3.0, +3.0)
```

`sqrt(c)` rather than `c` is deliberate and mirrors L01 §6.2's `sqrt(retained_variance)`: information scales with the square root of coverage, so a name with half its legs missing keeps ~71% of its score magnitude rather than 50%. A missingness flag travels with every score and is reported per rebalance; a systematic rise in missingness is a data-pipeline alarm, not a factor result.

**Strategic family weights `W_f` — frozen in git at inception, two signatures to change:**

| Family | Aggressive | Moderate | Justification for deviating from equal weight (methods §4) |
|---|---|---|---|
| Value | 0.25 | 0.25 | Strong India evidence but lumpy; the only family with a timing channel |
| Quality | 0.30 | 0.35 | Best-evidenced, lowest turnover, best India support; moderate gets more because it survives in large caps |
| Low-risk | 0.20 | 0.25 | D1, no PIT problem; the moderate book's most reliable large-cap factor |
| Size×Quality | 0.15 | 0.05 | Moderate's universe has no small tail to express it in (§11) |
| Yield | 0.10 | 0.10 | Thin, mostly an issuance-avoidance signal |

---

## 8. Factor combination: integrate, don't mix

**Decision: a single integrated composite `S_i` inside L09; separate sleeves across layers.**

For the reasons, in order:

1. **Integration dominates mixing at equal tracking error** for long-only books (Fitzgibbons, Friedman, Pomorski & Serban 2017 **[verify volume]**). A portfolio-of-sleeves happily holds a cheap fraud that the value sleeve loves and the quality sleeve hates; an integrated score never buys it. In India, where the forensic tail is the dominant loss source, that difference is worth more than in the US.
2. **Turnover.** Sleeves trade against each other — one sleeve buying what another sells is 100% turnover with zero net position change. The moderate book's total name-level turnover budget is ~68 pp/yr (§11); it cannot afford internal churn.
3. **Capacity and position count.** At ₹100 cr a five-sleeve book of 20 names each is 100 positions averaging 0.3% of NAV — below the entry band, below any sensible minimum, and unmanageable.

**And the carve-out, which is the interesting part: momentum stays out.** L08 owns a crash-control apparatus — Barroso–Santa-Clara volatility scaling, a Daniel–Moskowitz panic gate, an asymmetric drawdown ladder — that must act on the *momentum exposure in isolation*. Integrating momentum into `S_i` would dissolve that exposure into a composite and hide it from its own risk machinery, at exactly the moment (a rebound off a bottom) when it is most needed. So the architecture is **integrated within L09, mixed across L08/L09/L11/L12**, and L14 does the netting. The cost is some efficiency loss at the seam; the benefit is that the single most dangerous exposure in the book stays individually addressable. That trade is accepted explicitly.

**What Stage 1 emits per name** (before any Stage-2 overlay):

```python
FACTOR_SCORE[symbol] = {
  'S': float,                  # composite, clipped [-3,+3], within-sector, forensic-penalised
  'S_pofl': float,             # the price-only score, always computed, always reported
  'families': {'value','quality','lowrisk','sizequal','yield': Ftil},
  'coverage': {family: c_if}, 'n_missing_legs': int,
  'pool': str, 'pool_n': int,
  'P_forensic': float,         # >= 0, the penalty applied
  'flags': {'distress','neg_earnings','stale_filer','pledge_high','asm_gsm','bp_gated'},
  'pit_status': 'lag_approx' | 'true',      # 'true' only for S_pofl
  'confidence': float,         # sqrt(mean coverage) * (1 - stale_fraction)
  'asof': date, 'vintage_id': str }
```

`S` is a *score*, not an expected return. Converting it to an expected return is L14's job, using L05's CMA for the level; L09 asserts ordering only. Saying so prevents the standard error of treating a z-score as an alpha in basis points.

---

## 9. Factor timing: disciplined, limited, and killable

**Both sides are real.** Asness (2016), "The Siren Song of Factor Timing", and Asness, Chandra, Ilmanen & Israel (2017) show that value-spread-based factor timing is weak, is largely a disguised long-value position, and has historically *hurt* when levered onto an already value-tilted book. Arnott, Beck & Kalesnik (2016) show the opposite: factor valuations do predict factor returns, and ignoring a 95th-percentile value spread is its own error. Both are right about different magnitudes: timing exists, and it is much smaller than its advocates size it.

**Our scheme: three channels, hard caps, frozen parameters, no fitting, an explicit kill rule.**

| # | Channel | Source | Target | Max relative deviation | Dead band | Min evidence |
|---|---|---|---|---|---|---|
| T1 | Value spread | L05 `VAL_XS.value_spread_z` | `W_val` | **±25%** | \|z\| < 0.5 | Tier B; ≥ 8 non-overlapping obs; L05 already owns the estimate |
| T2 | Macro style prior | L04 `MACRO_TILT.style.duration_tilt`, `cyclicality_tilt` | `W_qual` vs `W_val`; cyclical-vs-defensive within quality | **±20%** | \|tilt\| < 0.25 | Tier B; L04 §7.3 frozen mapping |
| T3 | Credit phase & small-cap breadth | L03 `s_credit`, L07 `smallcap_breadth` phase | `W_size` and the `leverage` leg's weight inside quality | **±20%** | \|z\| < 0.5 | Tier B; charged to those cycles' `name_l1_pp` |

```
W_f(t) = W_f_strategic * (1 + delta_f(t)),   delta_f from T1..T3, linear in z, saturating at the cap
HARD CAPS, all CI-asserted:
  (a) sum_f |W_f(t) - W_f_strategic|  <=  0.35 * sum_f W_f_strategic       # total L1 deviation
  (b) resulting name-weight L1 change <=  sum over driving cycles of unused name_l1_pp
                                          (aggressive: <= 10 pp; moderate: <= 4.5 pp)
  (c) |W_f(t) - W_f(t-1)| <= 0.03 (aggressive) / 0.015 (moderate) per month   # L01 §8.5 rate limit
  (d) no W_f may fall below 0.5 * W_f_strategic or exceed 1.5 * W_f_strategic
```

**No parameter in this section is fitted.** The caps come from L05's own recommendation (±25%) and L01's budgets; the mappings are linear with frozen slopes. Any change requires two signatures and a trial-register entry (methods §5.3).

**Kill rule, pre-registered.** L20 reports `timing_contribution = return(timed weights) − return(strategic weights)`, gross and net, every quarter on a rolling 36-month basis. **If it is negative for three consecutive quarterly evaluations, factor timing is disabled and `W_f` reverts to strategic, permanently, until a written case with a fresh out-of-sample window and two signatures reinstates it.** Expected contribution, stated honestly in advance: **0 to 100 bps/yr, and plausibly zero.** It is in the MVP because it costs 1.5 days and because the value spread will eventually reach an extreme where doing nothing is the active decision — not because we expect it to earn its keep.

---

## 10. Forensic and exclusion screens — the negative factor

In India this is not a hygiene layer, it is where the largest single-name losses are avoided. Governance failures here are slow-then-sudden: years of accumulating flags, then one announcement and a 40–70% fall over days. Every screen below is one-sided — it can only reduce a score or exclude a name, never raise a score. That mirrors L01 R3's asymmetry and is enforced by `P_i >= 0`.

| Screen | Free source | Threshold | Action |
|---|---|---|---|
| **Auditor resignation mid-term** | Reg 30 announcement (D1) | any | **HARD EXCLUDE 24 months** |
| **Auditor change ≥ 2 in 5y, net of mandated rotation** | Reg 30 + Cos Act s.139 rotation calendar | 2+ unexplained | −1.00σ |
| **Audit qualification with quantified impact** | Statement of Impact of Audit Qualifications, Reg 33 (D1) | > 5% of PAT | **EXCLUDE** until two clean periods |
| **Promoter pledge** | Reg 31 shareholding pattern (D2) | pledged/promoter holding > 25% | −0.75σ |
| | | > 50% | **HARD EXCLUDE** |
| | | +10 pp QoQ increase | −0.50σ |
| **Promoter holding decline** | Reg 31 | > 5 pp in 12m, ex-offer/QIP | −0.50σ |
| **CFO-to-PAT divergence** | half-yearly CFS (D2) | 3y cum CFO / 3y cum PAT < 0.50 | −1.00σ |
| | | < 0.25 | **EXCLUDE** |
| **Receivable-days deterioration** | half-yearly BS (D2) | DSO > 1.5× own 3y median **and** > pool 75th pct | −0.75σ |
| | | two consecutive periods | **EXCLUDE** |
| **Contingent liabilities** (ex-financials) | annual report note (D4) | > 50% of net worth | −0.50σ |
| | | > 100% | **EXCLUDE** |
| **Related-party intensity** | Reg 23 material RPT + annual report (D4) | RPT revenue or loans > 15% of the base | −0.50σ |
| | | > 30% | **EXCLUDE** |
| **Subsidiary complexity** | annual report (D4) | > 25 subsidiaries **and** consol−standalone PAT gap > 40% | −0.50σ |
| **Independent-director exits** | Reg 30 resignation letters (D1, post-2021) | ≥ 2 in 12 months | −0.50σ |
| **ASM long-term stage ≥ 2 / any GSM stage** | NSE/BSE daily surveillance (D1) | any | **HARD EXCLUDE** while listed + 60 days |
| **Zombie filter** | §7.5 | PAT ≤ 0 in 3 of 4q and net debt/equity > 1.0 | **HARD EXCLUDE** |

```
P_i = min( sum of applicable penalties , 2.50 )        # sigma units, subtracted from S_i
```

**Cap the penalty, don't cap the exclusions.** A −2.5σ ceiling stops the screen becoming a de-facto short book while leaving hard exclusions absolute. Every exclusion is logged with the triggering datum and a review date; re-entry is never automatic on a hard exclusion.

**MVP split.** D1/D2 screens — auditor events, audit qualification, pledge, promoter decline, ASM/GSM, zombie, CFO/PAT, DSO — are **MVP**. The D4 screens — contingent liabilities, RPT intensity, subsidiary complexity — require parsing annual-report PDFs and are **DEFERRED to v1.5**, with the gap stated in every backtest rather than quietly ignored. Note that the MVP set is also the *cleanest PIT data in the entire layer*: Reg 30 announcements and surveillance files carry true knowledge dates.

**Interaction with the sector-cap open issue.** Financials carry pledge and RPT flags differently (inter-group lending is their business). The financials pool uses the pledge and auditor screens unchanged, drops the RPT screen, and substitutes a `related_party_advances / net worth > 10%` test. If the sector cap is resolved in the *absolute* 25% form, the financials pool is capacity-constrained before these screens bind, and the screens become decorative for the largest sector in the index. **This layer therefore joins L17 in depending on the relative form `min(25%, benchmark_weight + 10pp)`.**

---

## 11. Capacity, both books — the arithmetic

Neutral policy portfolio: equity 60%. Recommended equity-sleeve split (a recommendation to L14, which owns the blend): aggressive — factor 40%, momentum 35%, bottom-up 15%, special situations 10%; moderate — factor 55%, momentum 25%, bottom-up 20%.

| | Aggressive ₹100 cr | Moderate ₹1,000 cr |
|---|---|---|
| Equity at neutral | ₹60 cr | ₹600 cr |
| Factor sleeve | 40% ⇒ **₹24 cr** | 55% ⇒ **₹330 cr** |
| ADV floor (from L08 §11) | ₹5 cr | ₹33 cr |
| Eligible names at that floor | **~500 of 750** (~350 in stress) **[verify from our own build]** | **~275 of 750** (~180 in stress) **[verify]** |
| Sleeve holdings | 40 names, avg ₹0.60 cr (0.6% NAV) | 30 names, avg ₹11 cr (1.1% NAV) |
| Smallest eligible name's max position (10% ADV × 20 days) | ₹5cr × 0.10 × 20 = **₹10 cr** | ₹33cr × 0.10 × 20 = **₹66 cr** |
| Implied **sleeve capacity** (min holding = 1/N of sleeve) | ₹10 cr ÷ (1/40) = **₹400 cr** | ₹66 cr ÷ (1/30) = **₹1,980 cr** |
| Headroom vs requirement | **16×** | **6×** |

**Finding 1 — capacity is not the binding constraint for either factor sleeve.** Both have multiples of headroom. This differs from L08's momentum finding precisely because factor turnover is low: capacity is a function of *trading rate*, and a book that turns over 30% a year needs a sixth of the liquidity of one that turns over 200%.

**Finding 2 — breadth and dispersion bind instead, and they cost the moderate book about 45% of its factor alpha.** Grinold's law gives `IR ∝ IC · sqrt(breadth)`. Aggressive breadth ≈ 500 names, moderate ≈ 275 ⇒ `sqrt(500/275) = 1.35×` in favour of the aggressive book. Cross-sectional return dispersion in the moderate universe is ~1.3–1.6× narrower (§5, item 3), which scales the achievable spread per unit of IC. Combined: moderate factor alpha ≈ `1 / (1.35 × 1.35) ≈ 0.55` of aggressive.

| | Aggressive | Moderate |
|---|---|---|
| Sleeve gross alpha vs Nifty 500 TRI (design estimate) | **4.5–7.0%/yr** | **2.5–4.0%/yr** |
| × sleeve share of equity × equity weight | × 0.40 × 0.60 | × 0.55 × 0.60 |
| **Contribution to book CAGR, gross** | **1.1–1.7 pp** | **0.8–1.3 pp** |
| Less costs at the turnover below (~0.55% all-in per round trip) | −0.15 pp | −0.10 pp |
| **Contribution to book CAGR, net** | **~1.0–1.5 pp** | **~0.7–1.2 pp** |

**Finding 3 — the factor book, not momentum, should be the moderate book's primary name engine.** Using L01's turnover identity `annual_one_way ≈ 1.6 · (L1/2) · sqrt(12/tau_half)` at an identical name-level active L1 of 60 pp:

| Sleeve | `tau_half` | Turnover at 60pp active L1 |
|---|---|---|
| Momentum (L08) | 6 m | `1.6 × 30 × sqrt(12/6)` = **67.9 pp/yr** |
| Factor (L09) | ~30 m | `1.6 × 30 × sqrt(12/30)` = **30.3 pp/yr** |

The moderate book has ~68 pp/yr of name-level turnover budget (100% cap less L01's measured 32.1 pp/yr of allocation turnover). It can afford *one* full-size momentum sleeve **or** a full-size factor sleeve plus a half-size momentum sleeve. The recommended split — factor 55% / momentum 25% of equity — costs `0.55 × 30.3 + 0.25 × 67.9 ≈ 33.6 pp/yr`, leaving headroom for L11 and L12. The mirror-image aggressive book, with a 500%/yr budget, has no such constraint and can carry both at full size.

**Rebalance cadence follows.** Aggressive: scores refreshed monthly, sleeve rebalanced monthly with a 1.5× rank buffer. Moderate: scores refreshed monthly, sleeve rebalanced **quarterly** with a 2.0× rank buffer and a 0.4%-of-sleeve no-trade band. The buffer, not the cadence, does most of the turnover work.
