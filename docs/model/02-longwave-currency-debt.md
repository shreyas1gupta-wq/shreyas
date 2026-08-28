# Layer 02 — Long-Wave Layer: Currency, Reserve Order and Sovereign Debt (50–250 years)

**Abstract.** This layer supplies the slowest-moving input to the cycle stack: a Bayesian *prior* over where the global monetary order and India's own development arc sit within multi-decade arcs, expressed as a strategic anchor for gold weight, bond duration, equity theme tilts, leverage ceiling and standing tail-hedge policy. It is built from 14 slow indicators, each smoothed over 8–20 quarters, discretised into five wide states through a Schmitt-trigger with an explicit minimum dwell of 2.5–6 years, so that no indicator can flip more than roughly once per presidential cycle. A separate *phase clock* carries an ordinal stage (P1 sound money → P5 reset) with a posterior distribution rather than a point estimate, and a bounded ±3.0-year "trigger slide" that named, pre-registered, human-signed-off events may advance or retard. Portfolio impact is hard-capped at **300 bps of absolute allocation change per quarter and ~900 bps (moderate) / 1,400 bps (aggressive) of one-way turnover per year**, i.e. under 3% of the aggressive book's turnover budget. The layer is explicitly *not* a forecaster: with two-and-a-bit independent observations of a reserve-currency succession and fourteen indicators carrying dozens of tunable thresholds, its degrees of freedom exceed its effective sample size by two orders of magnitude. It is designed as a prior, a constraint generator and an insurance policy, and it is engineered so that being wrong for a decade costs the fund a few tens of basis points a year rather than a mandate.

---

## 1. Epistemic contract (read this before anything else)

Everything downstream depends on being honest about what can be known here.

| Claim | Status |
|---|---|
| "The global monetary order goes through multi-decade arcs of debt build-up, monetisation and reset" | Well-evidenced *narratively*, weakly evidenced *statistically*. n ≈ 2–3 independent successions (Dutch→British c.1780–1815; British→US c.1914–1945; a possible incomplete third). |
| "Those arcs have a stable period we can date" | **False, or at least unestimable.** Do not model a period. Model an *ordinal stage* plus elapsed time. |
| "Financial repression liquidates government debt" | Strongly evidenced, mechanism-level, ~35 country-years of clean data (Reinhart & Sbrancia). This is the single most reliable mechanism in the layer. |
| "Banking crises are followed by large, persistent asset drawdowns" | Strongly evidenced (Reinhart & Rogoff 2009, Jordà-Schularick-Taylor). Usable as a *conditional loss distribution*, not as a timing signal. |
| "Reserve-currency status collapses suddenly and is winner-take-all" | **Contradicted** by Eichengreen, Chiţu & Mehl: sterling and the dollar coexisted for decades; network effects are weaker and more reversible than the popular narrative assumes. This finding is used to *damp* the layer. |
| "Kondratiev 50–60y waves exist in output" | Largely rejected by the academic literature. Not used. |

**Design consequence.** The layer produces three things and nothing else:

1. **A prior**: a centre-of-gravity for the strategic asset mix, which the allocation engine (L11) treats as a penalty centre, not a target.
2. **A constraint set**: floors and ceilings (never zero gold; never maximum duration when debasement pressure is high; leverage ceiling cut in the reset tail).
3. **A hedge policy**: standing option and currency expressions sized against a rare-disaster prior, not against a point forecast.

It does **not** produce an expected return, a Sharpe estimate, or a timing signal. Any downstream layer that treats `LW_*` outputs as alpha is misusing them.

---

## 2. Evidence base actually used

- **Reinhart, C. & Rogoff, K. (2009), _This Time Is Different: Eight Centuries of Financial Folly_.** The durable content is the crisis aftermath regularity — after systemic banking crises, real equity prices fall ~55% over ~3.4 years, real house prices ~35% over ~6 years, real public debt rises ~86% over 3 years, unemployment +7pp over ~4 years. The much-cited 90% debt/GDP growth threshold was materially weakened by the Herndon, Ash & Pollin (2013) replication (spreadsheet error plus contested country weighting); **we do not use any debt/GDP threshold as a growth predictor.** We use debt levels only as a *state variable for fiscal flexibility*.
- **Reinhart, C. & Sbrancia, M.B. (2011/2015), "The Liquidation of Government Debt" (NBER WP 16893; later _Economic Policy_).** Finds that negative real interest rates in the 1945–1980 repression era liquidated government debt at roughly 1–5% of GDP per year for advanced economies (~3–4%/yr for the US and UK). **This is the mechanism our real-policy-rate indicator (RPR) is built on**, and it is the single strongest empirical plank in the layer.
- **Jordà, Ò., Schularick, M. & Taylor, A. (Macrohistory Database, 17 countries, 1870–present), and Jordà, Knoll, Kuvshinov, Schularick & Taylor (2019), "The Rate of Return on Everything, 1870–2015", _QJE_.** Long-run real returns: equity ~7%, housing ~7%, safe assets ~1–3%, with multi-decade swings and long periods of negative real safe-asset returns. Used to set the long-run return priors that the anchor is centred on.
- **Eichengreen, B., Chiţu, L. & Mehl, A. (2016), "Stability or Upheaval? The Currency Composition of International Reserves in the Long Run", _IMF Economic Review_; and _How Global Currencies Work_ (2018).** Reserve status is contestable and multipolar, transitions are slow, and inertia is weaker than assumed. **Directly damps the reserve-diversification indicator's weight** (0.15, the smallest in the global block).
- **Barro, R. (2006), "Rare Disasters and Asset Markets in the Twentieth Century", _QJE_; Barro & Ursúa (2008), Brookings.** Roughly 3.5%/yr unconditional probability of a macroeconomic disaster (consumption/GDP contraction >10%), mean disaster size ~22%. **This, not the long-wave phase estimate, is what sizes the tail hedge.**
- **Dalio, R. (2018), _Principles for Navigating Big Debt Crises_; (2021), _Principles for Dealing with the Changing World Order_.** Used for the *structure* of the stage ordering and the mechanisms (debt service crowding out, monetisation, currency debasement, reserve status loss). **Not used for its scores**: the "Great Power Index" has hand-set weights fitted in-sample to known outcomes and cannot be treated as an estimated model.
- **Kondratiev long waves.** Garvy (1943), "Kondratieff's Theory of Long Cycles" (_Review of Economic Statistics_) is the classic demolition [verify exact journal name]; Solomou (1987), _Phases of Economic Growth 1850–1973_ finds at best weak and unstable evidence in output series [verify title]. Spectral tests on long price series generally fail to reject the null of no 50–60y periodicity once trend and war shocks are removed. **We do not implement a Kondratiev clock.** The one salvageable element — that technology diffusion and commodity capex have long lead times — is handled in the commodity layer (L06), not here.
- **Bloom, D. & Williamson, J. (1998), "Demographic Transitions and Economic Miracles in Emerging Asia", _World Bank Economic Review_.** Demographic transition accounts for a large share (roughly a third) of East Asia's growth miracle. Basis for the DEMO indicator.
- **India long-run data.** Sivasubramonian, S. (2000), _The National Income of India in the Twentieth Century_ (OUP) gives annual output from 1900; Broadberry, Custodis & Gupta (2015), "India and the great divergence: An Anglo-Indian comparison of GDP per capita, 1600–1871", _Explorations in Economic History_, extends coverage earlier. **These are enough to describe India's arc but nowhere near enough to estimate an India-specific long wave.** Say so plainly: there is no India long-wave literature with usable market data before 1950. This layer therefore imports the *global* wave and estimates only India's *position on a development S-curve*.

---

## 3. Dated snapshot — 28 August 2026

State variables as observed today. All figures should be re-pulled from the point-in-time store, not from this document.

| Variable | Value | Source / date |
|---|---|---|
| US federal debt held by public | 101% of GDP, projected 120% by 2036 | CBO Budget & Economic Outlook, Feb 2026 |
| US net interest | 3.3% of GDP (~$1.0tn), → 4.6% by 2036 | CBO Feb 2026 |
| USD share of allocated FX reserves | 57.13% (2026Q1, up from 56.42% in 2025Q4 on valuation) | IMF COFER |
| Central-bank gold | Gold now a larger share of global reserves than US Treasuries, first time since 1996; record 45% of CBs plan to add | WGC Central Bank Gold Reserves Survey 2026 |
| Gold | ~$4,600–4,710/oz | Aug 2026 |
| USD/INR | ~95.4–95.9 | Aug 2026 |
| India external debt | $762.8bn, 20.8% of GDP (from 19.8% Mar-25) | RBI, Mar-2026 |
| India FX reserves | ~$691bn; ~11 months import cover; 90.3% of external debt | RBI, Mar-2026 |
| India short-term debt / reserves | 21.6% (from 20.1%) | RBI, Mar-2026 |
| India debt service / current receipts | 5.8% (from 6.6%) | RBI, Mar-2026 |
| India credit to private non-financial sector | 97.4% of GDP; BIS credit-to-GDP gap ≈ −3.2pp | BIS, Q3-2025 |
| India nominal GDP / per-capita | ~$4.15tn / ~$2,813 | IMF, 2026 |
| India household savings | 21.7% of GDP; net financial savings depressed (~5–6%), physical ~12.9% | RBI/MOSPI |
| India sovereign rating | Three upgrades in 2025 (DBRS→BBB May, S&P→BBB Aug, R&I→BBB+ Sep) | Agencies |

**The tension this snapshot creates, and which the design must resolve honestly:** every *debasement* indicator is loud (record debt, record CB gold buying, gold above US Treasuries in reserves, term premium rebuilding), while every *India external* indicator is benign (20.8% external debt, 11 months cover, negative credit gap, three rating upgrades) — and gold is at an all-time high in real USD terms. A naive "late debt cycle → buy gold" rule buys the most expensive gold in history. The valuation brake in §6 exists precisely for this.

---

## 4. The fourteen slow indicators

Blocks: **GMO** (global monetary order / debasement), **IEF** (India external fragility), **IARC** (India structural arc).

| # | Code | Block | Definition (exact) | Source | History | Freq | Smoothing | Dwell + confirm |
|---|---|---|---|---|---|---|---|---|
| A1 | `GDS` | GMO | 0.6·(G4 GDP-weighted general-govt gross debt/GDP) + 0.4·(US net interest / federal revenue) | IMF WEO `GGXWDG_NGDP`; CBO; BIS `TOTAL_CREDIT` sector G | WEO 1980–; BIS 1950s–; JST 1870– | Q/A | 8q median | 12q + 2q |
| A2 | `RPR` | GMO | GDP-weighted Σwᵢ(policy rateᵢ − core CPI YoYᵢ) over US, EA, JP, UK | BIS policy rates; OECD/FRED CPI | 1960– (US 1954–) | M→Q | 12q median | 8q + 2q |
| A3 | `CBGS` | GMO | 0.5·z(official gold at market / total official reserves incl. gold) + 0.5·z(trailing 4q net CB gold purchases, tonnes) | WGC Goldhub; IMF IFS | IFS 1948–; WGC flows 2000– | Q | 8q median | 10q + 2q |
| A4 | `RSVDIV` | GMO | −1 × (5-yr change in USD share of *allocated* reserves, pp/yr), plus 0.3 weight on HHI of reserve-currency shares | IMF COFER | COFER 1999– quarterly; annual 1965– | Q | 8q median of the 5y slope | 12q + 3q |
| A5 | `GVAL` | GMO (**brake, not a driver**) | 0.5·z₅₀ᵧ(gold / US CPI) + 0.5·z₅₀ᵧ(above-ground gold stock × price ÷ G4 broad money) | LBMA/COMEX; BLS CPI; WGC stock; FRED M2 + ECB/BoJ/BoE M3 | Free float 1968–; CPI 1913– | M→Q | 8q median | 8q + 2q |
| A6 | `TPR` | GMO | z(ACM 10y US term premium), + 0.3·z(India 10y G-sec − 1y T-bill) | NY Fed ACM (1961–); CCIL/RBI | 1961– / 1997– | D→Q | 12q median | 10q + 2q |
| B1 | `EXSOL` | IEF | Composite of 4: external debt/GDP; short-term debt (orig. maturity)/reserves; import cover months; reserves/external debt. Equal weight after individual banding. | RBI *India's External Debt* (quarterly), RBI WSS, RBI Handbook | Quarterly 1990–; annual 1970s– | Q | 4q median (already slow) | 8q + 2q |
| B2 | `REERDEV` | IEF | log(REER₄₀) − log(trend), trend = 10y rolling mean **plus** a Balassa–Samuelson allowance of +0.9%/yr for India's productivity catch-up [verify magnitude] | RBI 40-currency REER (2015-16=100); BIS REER | RBI 1993–; BIS 1994– | M→Q | 8q median | 8q + 2q |
| B3 | `INRTREND` | IEF | Residual of log(USDINR) from a 25y log-linear trend, expressed in z. Fitted drift ≈ **3.0–3.4%/yr** (45.0 in 2000 → 95.5 in 2026 ⇒ 2.93%/yr; 31.4 in 1993 → 95.5 ⇒ 3.43%/yr). Forward drift prior compressed to **2.0–2.5%/yr** given India's 4% CPI target vs US ~2%. | RBI reference rate | 1947– (with regime breaks 1966, 1991) | D→Q | 8q median | 8q + 2q |
| C1 | `PCI` | IARC | Nominal USD GDP per capita, log-scaled position on the empirical consumption/financialisation S-curve. Steepest band ≈ $2,000–$8,000. Current $2,813. | IMF WEO, MOSPI | 1950– (1900– via Sivasubramonian) | A | 3y mean | 20q + 4q |
| C2 | `FINDEEP` | IARC | 10y trailing **slope** of (private non-fin credit/GDP), + z(market cap/GDP), + z(MF AUM/GDP). **Uses only the low-frequency component — the BIS credit *gap* itself belongs to L03.** | BIS `TOTAL_CREDIT`; NSE/BSE; AMFI | BIS India 1951–; AMFI 1965– | Q/A | 12q median | 16q + 3q |
| C3 | `HHFIN` | IARC | 10y trailing mean of (household gross financial savings / total household savings), + 5y slope of net financial savings/GDP | RBI Annual Report; MOSPI National Accounts | Annual 1950-51– | A | 5y mean | 20q + 4q |
| C4 | `FORM` | IARC | z-composite: tax revenue/GDP, GST collections/GDP, UPI value/GDP, EPFO+NPS subscribers/working-age population | CBDT/GST Council, NPCI, EPFO, PFRDA | GST 2017–; tax/GDP 1950– | Q/A | 8q median | 16q + 3q |
| C5 | `DEMO` | IARC | Years to peak working-age (15–64) population share, and level of that share. India's peak ≈ 2036–2041 [verify UN WPP 2024]. | UN World Population Prospects; RGI Census | 1950–2100 projections | A (revised 2y) | none (already smooth) | 24q + 4q |

### Band tables (entry thresholds; exit thresholds carry hysteresis `h`)

Scores are integers in {−2, −1, 0, +1, +2}. **Sign convention for GMO/IEF: +2 = maximum stress/debasement/fragility. For IARC: +2 = maximally favourable structural arc. For GVAL: +2 = gold maximally expensive.**

**A1 `GDS`** (native units, G4 debt/GDP | US interest/revenue):
| State | G4 debt/GDP | US int/rev | h |
|---|---|---|---|
| −2 | < 60% | < 6% | 4pp / 1.0pp |
| −1 | 60–80% | 6–10% | 4pp / 1.0pp |
| 0 | 80–100% | 10–14% | 5pp / 1.5pp |
| +1 | 100–120% | 14–19% | 5pp / 1.5pp |
| +2 | > 120% | > 19% | 5pp / 1.5pp |
*Today: G4 ≈ 110%+, US ≈ 19% ⇒ **+2**.*

**A2 `RPR`** (GDP-weighted G4 real policy rate):
| State | Range | h |
|---|---|---|
| +2 (deep repression) | < −1.5% | 0.40pp |
| +1 | −1.5% to +0.5% | 0.40pp |
| 0 | +0.5% to +1.5% | 0.35pp |
| −1 | +1.5% to +3.0% | 0.40pp |
| −2 (creditor-friendly) | > +3.0% | 0.40pp |
*Today ≈ +0.2% [verify 2026 policy rates] ⇒ **+1**.*

**A3 `CBGS`**: bands on trailing-4q net CB purchases: >900t ⇒ +2; 550–900t ⇒ +1; 150–550t ⇒ 0; −150 to +150t ⇒ −1; net selling >150t ⇒ −2. `h` = 100t. *Today ~1,000t/yr ⇒ **+2**.*

**A4 `RSVDIV`**: 5y slope of USD share: < −1.2pp/yr ⇒ +2; −1.2 to −0.5 ⇒ +1; −0.5 to +0.3 ⇒ 0; +0.3 to +1.0 ⇒ −1; > +1.0 ⇒ −2. `h` = 0.25pp/yr. *Today ≈ −0.55pp/yr on a 10y basis, but +0.7pp in the last quarter ⇒ smoothed **+1**.*

**A5 `GVAL`**: composite z: > +1.75 ⇒ +2; +0.75 to +1.75 ⇒ +1; −0.75 to +0.75 ⇒ 0; −1.75 to −0.75 ⇒ −1; < −1.75 ⇒ −2. `h` = 0.35z.
*Worked example, today.* Real gold: Jan-1980 peak $850 × (CPI_2026 ≈ 330 / CPI_1980 ≈ 78) ≈ **$3,596 in 2026 dollars** [verify CPI level]; spot $4,600 is therefore **an all-time real high**, z ≈ +2.0. Gold/broad money: above-ground stock ~216,000t = 6.95bn oz × $4,600 ≈ $32tn; vs US M2 ~$22.5tn ⇒ ratio 1.42 — high, but *below* the 1980 peak (~90,000t × $850 = $2.46tn vs M2 $1.48tn ⇒ 1.66) and far above the 2000 trough (~0.26). z ≈ +1.2. Composite ≈ **+1.5** ⇒ state **+2** on the raw band, but the 8q median holds it at **+1** until confirmed. Use **V = +1.5** as the continuous value.

**A6 `TPR`**: ACM 10y TP z: > +1.0 ⇒ +2; +0.25 to +1.0 ⇒ +1; −0.25 to +0.25 ⇒ 0; −1.0 to −0.25 ⇒ −1; < −1.0 ⇒ −2. `h` = 0.30z. *Today, TP rebuilt from deeply negative (2016–2021) to modestly positive ⇒ **+1** [verify current ACM level].*

**B1 `EXSOL`** sub-bands (score each, then average and round):
| Sub | +2 (fragile) | +1 | 0 | −1 | −2 (strong) |
|---|---|---|---|---|---|
| Ext debt/GDP | >30% | 24–30% | 18–24% | 14–18% | <14% |
| ST debt/reserves | >60% | 40–60% | 25–40% | 15–25% | <15% |
| Import cover (m) | <6 | 6–9 | 9–12 | 12–16 | >16 |
| Reserves/ext debt | <50% | 50–70% | 70–90% | 90–120% | >120% |
`h` = 2pp / 5pp / 0.75m / 5pp. *Today: 0, −1, 0(11m, near boundary), −1 ⇒ mean −0.5 ⇒ **−1** (mildly strong). For reference, 1991: ST/reserves ~380%, cover ~3 weeks ⇒ +2 across the board.*

**B2 `REERDEV`**: > +15% ⇒ +2; +7 to +15% ⇒ +1; −5 to +7% ⇒ 0; −12 to −5% ⇒ −1; < −12% ⇒ −2. `h` = 2.5pp. *Today ⇒ ≈ **0** [verify REER₄₀ level].*

**B3 `INRTREND`**: residual z vs 25y trend: INR *stronger* than trend by >1.25z ⇒ +2 (overvalued, expect catch-down); +0.5 to +1.25 ⇒ +1; ±0.5 ⇒ 0; −1.25 to −0.5 ⇒ −1; < −1.25 ⇒ −2. `h` = 0.30z. *2020→2026 realised 4.3%/yr depreciation vs 3.0–3.4% trend ⇒ INR already weaker than trend ⇒ **−1**.*

**C1 `PCI`**: per-capita USD: <$1,200 ⇒ −1 (pre-takeoff); $1,200–2,000 ⇒ 0; $2,000–5,000 ⇒ **+2** (steepest S-curve); $5,000–10,000 ⇒ +1; >$10,000 ⇒ 0 (maturity). `h` = $250. *Today $2,813 ⇒ **+2**.*

**C2 `FINDEEP`**: 10y credit/GDP slope + valuation-of-deepening composite z: > +1.0 ⇒ +2 … < −1.0 ⇒ −2, `h` = 0.30z. *Today: credit/GDP 97.4% with a modestly positive decade slope and a *negative* BIS gap (headroom, not froth) ⇒ **+1**.*

**C3 `HHFIN`**: financial share of household savings, 10y mean: >55% ⇒ +2; 45–55% ⇒ +1; 35–45% ⇒ 0; 25–35% ⇒ −1; <25% ⇒ −2. `h` = 2.5pp. *Today: gross financial ~11% vs physical ~12.9% of GDP ⇒ ~46% financial share, rising trend ⇒ **+1**.*

**C4 `FORM`**: composite z, same ±1.0/±0.30 structure. *Today: GST + UPI + formal-employment coverage all on strong multi-year uptrends ⇒ **+1**.*

**C5 `DEMO`**: years to peak working-age share: >25y ⇒ +2; 10–25y ⇒ +1; 0–10y ⇒ 0; 0 to −10y ⇒ −1; < −10y ⇒ −2. `h` = 2y. *Today ~10–15y to peak ⇒ **+1**.*

---

## 5. State machine — smoothing, hysteresis, dwell

Four brakes in series. Each is individually sufficient to prevent quarterly whipsaw; together they make a flip a multi-year event.

```python
@dataclass
class SlowIndicator:
    code: str
    bands: list[tuple[float, float]]   # 5 entry bands, native units, ascending
    h: float                           # hysteresis half-width, native units
    smooth_q: int                      # trailing-median window, quarters
    dwell_q: int                       # min quarters a state must be held
    confirm_q: int                     # consecutive quarters the new state must be signalled

def step(ind, hist_raw, state, quarters_in_state, pending_state, pending_count, asof):
    # 1) SMOOTH — median, not mean: robust to revisions and one-off shocks
    x = median(hist_raw[-ind.smooth_q:])          # point-in-time vintages only

    # 2) BAND with Schmitt trigger: to LEAVE the current state you must clear
    #    the band edge by h; to ENTER you only need to reach it.
    target = band_with_hysteresis(x, ind.bands, ind.h, current=state)

    # 3) DWELL — cannot even consider a change before dwell_q quarters
    if quarters_in_state < ind.dwell_q:
        return state, quarters_in_state + 1, None, 0

    # 4) CONFIRM — the new state must persist confirm_q quarters
    if target != state:
        if target == pending_state:
            pending_count += 1
        else:
            pending_state, pending_count = target, 1
        if pending_count >= ind.confirm_q:
            # 5) STEP LIMIT — at most one notch per flip event
            new = state + sign(target - state)
            log_transition(ind.code, state, new, asof, x)   # immutable audit
            return new, 0, None, 0
        return state, quarters_in_state + 1, pending_state, pending_count
    return state, quarters_in_state + 1, None, 0
```

**Guaranteed minimum time between flips** = `dwell_q + confirm_q` quarters. Given the table in §4 that is **2.5 years (RPR, GVAL, EXSOL, REERDEV, INRTREND) to 7 years (DEMO)**. Because of the one-notch step limit, traversing the full −2 → +2 range takes a minimum of 4 × (dwell + confirm), i.e. **10 to 28 years**. That is the intended behaviour.

**Vintage discipline.** All inputs must be read from the point-in-time store (L17) with an as-of timestamp. India's household savings and GDP series are revised late and heavily; using final-vintage data would make any backtest of this layer meaningless. Any indicator whose vintage lag exceeds 3 quarters is published with an explicit `stale_q` field and its weight is decayed by 0.9^(stale_q−3).

---

## 6. Composites, the valuation brake, and the phase posterior

**Global monetary order composite** (GVAL deliberately excluded — it is a brake on the *expression*, not evidence about the *state*):

```
G = 0.25·GDS + 0.25·RPR + 0.20·CBGS + 0.15·RSVDIV + 0.15·TPR        ∈ [−2, +2]
```
Weights follow evidence strength: RPR (Reinhart–Sbrancia mechanism) and GDS (directly measured) get the most; RSVDIV gets the least because Eichengreen–Chiţu–Mehl show reserve shares move slowly and reversibly.

**Valuation brake:**
```
G_eff = clip(G − 0.40·V, −2, +2)          where V = GVAL continuous value
```
This is the single most important line in the layer. It is what stops "the debt cycle is late" from becoming "buy gold at any price."

**India composites:**
```
E = mean(EXSOL, REERDEV, INRTREND)                                  ∈ [−2, +2]   (+ = fragile)
A = 0.25·PCI + 0.20·FINDEEP + 0.20·HHFIN + 0.20·FORM + 0.15·DEMO    ∈ [−2, +2]   (+ = favourable)
```

**Block slew limiter (second brake):** `|ΔG|, |ΔE|, |ΔA| ≤ 0.25 per quarter`, applied after aggregation. A full −2 → +2 traverse of a composite therefore takes ≥ 16 quarters even if every constituent flipped simultaneously.

**Today's values:** G = 0.25(2)+0.25(1)+0.20(2)+0.15(1)+0.15(1) = **1.45**. V = **1.5** ⇒ **G_eff = 0.85**. E = mean(−1, 0, −1) = **−0.67**. A = 0.25(2)+0.20(1)+0.20(1)+0.20(1)+0.15(1) = **1.25**.

### Phase clock

Rather than a period, we carry an ordinal stage with a **posterior distribution**, and elapsed time τ in the modal stage.

| Stage | Description | Prior duration |
|---|---|---|
| P1 | Sound money / new order: low debt, positive real rates, credibility rebuilding | 20–35y |
| P2 | Credit expansion / prosperity: debt rising from a low base, real rates positive but falling | 20–30y |
| P3 | Peak debt / bubble: debt/GDP high, real rates ≈ 0, assets rich | 10–20y |
| P4 | Deleveraging & monetisation: debt service unsustainable, financial repression, CB balance-sheet expansion, currency debasement, gold outperforms | 10–20y |
| P5 | Reset: devaluation, restructuring, revaluation of the anchor, political/military rupture | 3–10y |

**Inception prior (2026-08-28), signed off by the investment committee and frozen in the audit log:**
`P(P3) = 0.35, P(P4) = 0.55, P(P5) = 0.10`, with **τ = 6 years** in P4 (dating entry to the 2020 monetisation episode).

Posterior update is deliberately crude and slow — a monotone logistic map from G and τ, updated **annually**, with a maximum probability shift of **0.10 per year per stage**. There is no likelihood function worth writing here; pretending otherwise would be false precision.

---

## 7. The trigger-slide mechanism

Named, **pre-registered** events may advance (+) or retard (−) the phase clock τ. Every slide requires (a) an event that matches a pre-registered definition, (b) sign-off by two members of the investment committee, and (c) an immutable, timestamped log entry (L19). **No event may be added to the table after the fact** — the table is versioned in git and a backtest may only use the version that existed at the simulated date.

### Global slide events (act on the P3/P4/P5 clock)

| Event (observable definition) | Δτ | Notes |
|---|---|---|
| Gold officially revalued or monetised on a G7 central-bank balance sheet, **or** a new multilateral settlement asset reaches >$100bn/yr turnover | **+3.0** | Forces P(P5) ≥ 0.40 |
| Reserve-currency issuer misses a scheduled payment (incl. debt-ceiling technical default) | +2.5 | |
| Explicit yield-curve control announced by the Fed or ECB (BoJ excluded — already priced) | +2.0 | |
| Direct armed conflict between nuclear-armed states, **or** freezing of a reserve-issuer's official assets >$100bn | +2.0 | 2022 Russia freeze already in the base case |
| Two of three major agencies downgrade a G3 sovereign below AA | +1.5 | |
| G4 central-bank balance sheet expands >10% of GDP in ≤12 months **outside** an acute banking crisis | +1.5 | |
| G20 currency crisis: >25% depreciation vs SDR in 12 months | +1.5 | |
| G4 debt/GDP falls ≥15pp over 5 years without default or >6% inflation | **−2.5** | |
| Credible US fiscal consolidation: primary balance ≥ 0 for 3 consecutive fiscal years | −2.0 | |
| G4 trend real GDP growth runs ≥1pp above its prior 10y mean for 3+ years (productivity shock) | −2.0 | The AI-productivity case belongs here |
| G4 real policy rate > +1.5% sustained 3+ years with stable debt/GDP | −1.5 | |

### India slide events (act on the E/IEF clock only)

| Event | Δτ_India |
|---|---|
| Reserves fall >20% peak-to-trough within 12 months | +2.0 |
| CAD > 3.5% of GDP for 4 consecutive quarters | +1.5 |
| Brent > $120/bbl sustained 6 months (India imports ~85% of crude) | +1.0 |
| Combined centre+state fiscal deficit > 11% of GDP for 2 years | +1.5 |
| Sovereign upgrade to A− or better by 2 of 3 majors | −1.0 |
| Net FPI debt inflows > 2% of GDP over 12 months (index inclusion effects) | −1.0 |
| Reserves > 15 months' import cover sustained 4 quarters | −1.0 |

### Slide arithmetic

1. Cumulative net slide is **bounded to ±3.0 years over any rolling 10-year window**. Excess is discarded, not carried.
2. Each event category may fire **at most once per 3 years**.
3. Slide is applied with a **2-quarter lag** and **amortised linearly over the following 4 quarters** — so even a +3.0y event moves the book at ≤ the §9 rate limits.
4. Slides **decay**: each logged slide loses 20% of its magnitude per year after 5 years, so a decade-old shock does not permanently distort the clock.

---

## 8. Mapping to the portfolio

The layer emits an **anchor**, not a trade. L11 (allocation engine) treats it as the centre of a quadratic penalty, so tactical layers can deviate at a cost.

### 8.1 Gold anchor

```
w_gold_anchor = clip( 10% + 5.5·G_eff + 1.5·max(E, 0) , 4%, 30% )
```
*Today:* 10% + 5.5(0.85) + 0 = **14.7%**.

Note the deliberate ceiling: the owner permits up to 50% gold, but **this layer's contribution is capped at 30%**. The remaining headroom belongs to the gold sleeve (L13, momentum/carry/lease-rate) and the macro-regime layer (L04). If both are also maximally bullish, total gold can reach the 50% mandate cap — but it cannot get there on the long wave alone. A hard floor of **4%** applies at all times: gold is insurance, and you do not cancel insurance because the sky is clear.

### 8.2 Debt sleeve: duration and composition

```
MD_anchor = clip( 4.2 − 0.9·G_eff + 0.6·A − 0.7·max(E, 0) , 1.0, 5.0 )   years
w_debt_anchor_range = [ 20% + 4·max(−G_eff,0) , 45% + 6·max(−G_eff,0) ]   capped at the 70% mandate limit
```
*Today:* MD = 4.2 − 0.765 + 0.75 − 0 = **4.19 years**; debt range **20–45%**.

The two blocks pull opposite ways and that is correct: the global wave says *shorten duration* (term premium rebuilding, monetisation risk, negative real safe-asset returns per Jordà et al.), while India's own arc says *own duration* (disinflation credibility, index inclusion, three rating upgrades, fiscal consolidation). Net: a mid-single-digit duration inside the owner's ≤5y cap.

Composition guidance the layer sets (L12 implements):

| G_eff | GSec share | Short corporate (AAA/AA+) | Floating / T-bill | Notes |
|---|---|---|---|---|
| ≤ −0.5 | 55–70% | 20–35% | 0–10% | Creditor-friendly regime, extend |
| −0.5 to +1.0 | 35–55% | 30–50% | 5–20% | Today |
| > +1.0 | 20–35% | 30–45% | 25–45% | Monetisation risk: shorten, float |

**India has no usable inflation-linked bond market** (the 2013–14 IIBs and the retail IINSS-C are illiquid/discontinued). State this plainly to the owner: the linker leg of a debasement hedge *cannot* be expressed in Indian fixed income. Its substitutes are gold, short duration, and the real-asset equity tilt below. This is a genuine structural gap in the toolkit, not something to paper over.

### 8.3 Equity theme tilts

Emitted as active weights vs the Nifty Total Market benchmark, in percentage points of the *equity sleeve*. L10 (bottom-up selection) chooses the names; this layer only sets the theme budget.

| Theme | Driver | Tilt range (pp of equity sleeve) | Today |
|---|---|---|---|
| Real / hard assets (metals, mining, energy, cement, aggregates) | +2.5·G_eff | −5 to +5 | +2.1 |
| Gold financiers & gold-linked (NBFC gold lenders, jewellery retail, refiners) | +1.5·G_eff − 0.3·V | −3 to +3 | +0.8 |
| USD-revenue exporters (IT services, pharma/CRAMS, specialty chemicals, auto ancillaries) | +2.0·max(REERDEV,0) + 1.2·max(INRTREND,0) | −4 to +6 | 0.0 |
| Net USD-cost importers (OMCs, import-heavy capital goods) | −1.5·max(REERDEV,0) | −4 to +2 | 0.0 |
| Asset gatherers (AMCs, brokers, exchanges, depositories, wealth) | +2.0·HHFIN + 1.0·FORM | −2 to +6 | +3.0 |
| SLR-heavy PSU lenders | −1.5·TPR − 1.0·G_eff | −5 to +2 | −2.4 |
| Long-duration growth (top-quintile P/E, cash flows >10y out) | −2.0·max(TPR,0) − 1.0·max(G_eff,0) | −6 to +3 | −2.9 |
| Domestic consumption S-curve (discretionary, healthcare, financial penetration) | +2.5·A | −3 to +6 | +3.1 |

**Correlation cap.** Real assets + gold financiers + exporters + short duration + physical gold are, in risk terms, *one trade* (the INR-debasement trade). L18 must apply a factor-level cap: **combined ex-ante risk contribution from the "debasement complex" ≤ 35% of total portfolio variance.** Without this the layer manufactures concentration while presenting as diversification.

### 8.4 Leverage modifier

| Condition | Gross ceiling | Gross target |
|---|---|---|
| Base | 1.50x | 1.25x |
| G_eff ≥ +1.5 **or** P(P5) ≥ 0.25 | **1.25x** | **1.10x** |
| P(P5) ≥ 0.40 (reset confirmed) | **1.10x** | **1.00x** |

Rationale: in the historical reset episodes, correlations across risk assets go to one and financing is withdrawn precisely when the levered book most needs it. Cutting the ceiling is the cheapest of all the hedges here.

### 8.5 Standing hedge policy (L14 implements)

| Gate | Instrument | Sizing |
|---|---|---|
| G_eff ≥ +1.0 **and** V ≥ +1.0 (debasement loud, gold expensive) | Express *incremental* gold via 12–24m call spreads / call ladders on gold, part-funded by deep-OTM put sales | Net premium budget **25–60 bps of NAV p.a.**; max 40% of the incremental gold anchor expressed in options |
| G_eff ≥ +1.0 **and** L05 equity valuation in top quintile | Rolling 12m Nifty puts 10–15% OTM, financed by long-dated covered calls on the equity book | Net cost ≤ **40 bps of NAV p.a.**; notional 15–30% of equity |
| G_eff ≥ +1.5 | Standing INR-depreciation expression — exporter overweight floor **and/or** long USDINR forwards | 0–8% of NAV notional. **Regulatory check required**: FX derivative access under the applicable PMS/AIF wrapper generally requires an underlying exposure. Flag to L19. |
| P(P5) ≥ 0.25 | Add: far-OTM (25–35%) 12m index puts, sized on the Barro–Ursúa disaster prior (3.5%/yr × ~22% mean loss) rather than on the phase estimate | Additional ≤ 25 bps of NAV p.a. |

---

## 9. Hard rate limits (non-negotiable)

These are enforced in L11, not suggested here. Violation is a system error, not a discretionary override.

| Quantity | Max change per quarter |
|---|---|
| **Total absolute allocation change attributable to L02** | **300 bps** (L1 norm across asset classes) |
| Gold weight | 200 bps |
| Debt weight | 250 bps |
| Equity weight | 250 bps |
| Modified duration | 0.50 years |
| Any single equity theme tilt | 150 bps |
| L1 norm of the full equity tilt vector | 400 bps |
| Gross leverage ceiling | 0.15x |

**Annual turnover budget from this layer:** ≤ **900 bps one-way (moderate)** and ≤ **1,400 bps one-way (aggressive)**. Against the owner's 100% / 500%+ turnover budgets this is **9% and 2.8%** of total turnover respectively — the right order of magnitude for a layer whose signal changes once every few years.

**Sole override:** a confirmed P5 event with two-signature sign-off may raise the total cap to 600 bps/quarter for a maximum of **2 consecutive quarters**, after which it reverts automatically. The override is logged and cannot be re-invoked within 3 years.

---

## 10. Interfaces

**Consumes**

| From | Object | Use | Constraint |
|---|---|---|---|
| L17 Data infra | `pit_macro_store(series, asof)` | All 14 indicators | Point-in-time vintages mandatory; final-vintage reads are rejected |
| L01 Taxonomy | `horizon_registry`, `SignalObject` schema, sign convention | Output conformance | — |
| L03 Credit cycle | `bis_credit_gap_india` | **Only the 10y trailing slope**, into FINDEEP | L03 owns the gap itself; double-counting is prohibited and asserted in CI |
| L04 Macro regime | `nominal_growth_regime` | Gates *only* the exporter/importer tilt | Must not touch the gold anchor |
| L05 Valuation | `equity_longrun_valuation_z` | Gates the index-put hedge only | — |
| L15 Forward-looking human+AI | `phase_override_proposal`, `slide_event_nomination` | Phase posterior and slide events | Two-signature sign-off; immutable log |
| L19 Governance | `signoff_log`, `event_registry_version` | Slide legitimacy | Registry is git-versioned; backtests read the historical version |

**Exposes**

```python
LW_STATE      = {G, G_eff, V, E, A, phase_posterior: {P3,P4,P5}, tau, slide_years,
                 indicator_states: {code: int}, confidence: float, asof, stale_q}
LW_ANCHOR     = {w_gold_anchor, w_debt_anchor_range, MD_anchor,
                 equity_tilt_vector: {theme: pp}, max_delta_per_quarter: {...}}
LW_CONSTRAINTS= {min_gold: 4.0, max_gold_from_this_layer: 30.0, max_duration,
                 gross_leverage_ceiling, gross_leverage_target}
LW_HEDGE_POLICY = {gold_option_budget_bps, index_put_policy, fx_policy, disaster_put_budget_bps}
```
Every anchor field carries its own `max_delta_per_quarter` so L11 can enforce §9 mechanically without knowing anything about this layer's internals.

---

## 11. Validation approach (and why a continuous backtest is the wrong test)

A continuous 1995–2026 backtest of this layer would produce roughly two or three state changes and a performance number driven entirely by the 2001–2011 and 2019–2026 gold runs. That number is not evidence. Instead:

1. **Constraint tests (must pass, CI-enforced).** Simulate 200 years of synthetic indicator paths (AR(1) with regime jumps) and assert: no indicator flips more often than `dwell+confirm`; L02-attributable quarterly turnover never exceeds 300bps; annual turnover stays inside budget; leverage modifier fires only on the specified conditions.
2. **Regime-analog studies (qualitative, documented).** Replay the machinery over: US 1965–1982 (repression → inflation → Volcker), Japan 1989–2005 (post-bubble deleveraging), UK 1945–1970 (repression + reserve-currency demotion), India 1985–1995 (pre-crisis fragility → 1991 crisis → liberalisation). Ask only: *did the state variables move in the right direction, at the right decade, with the right slowness?* Not: *what was the Sharpe?*
3. **The null test (mandatory, and expected to be uncomfortable).** Replace the entire layer's output with a fixed anchor (12% gold, 4.0y duration, zero tilts). If the difference in realised outcome over 1995–2026 is within the noise band, **say so in the committee pack**. It probably will be. The layer's justification then rests entirely on the conditional loss distributions in the reset tail, which is exactly the honest claim.
4. **Vintage-integrity test.** Re-run with final-vintage data and compare. A large gap indicates the backtest was leaking revisions.
5. **Ablation.** Remove GVAL (the brake) and confirm the layer would have bought maximum gold in Aug-2026 at all-time real highs. That contrast is the argument for keeping the brake.

---

## 12. Data requirements

| Item | Source | History | Freq | Cost | Blocker | Fallback |
|---|---|---|---|---|---|---|
| G4 general govt debt/GDP | IMF WEO (`GGXWDG_NGDP`), BIS `TOTAL_CREDIT` | 1980– / 1950s– | Semi-A / Q | Free | No | Jordà-Schularick-Taylor Macrohistory (1870–, free) |
| US net interest, revenue, CBO projections | CBO, Treasury Fiscal Data | 1962– | A / M | Free | No | FRED |
| G4 policy rates & core CPI | BIS policy rate DB, OECD MEI, FRED | 1954– | M | Free | No | — |
| COFER USD share | IMF COFER | 1999– Q (1965– A) | Q, 1q lag | Free | No | ECB *International Role of the Euro* |
| CB gold holdings & flows | WGC Goldhub, IMF IFS | 1948– / 2000– | M/Q | Free (Goldhub registration) | No | IFS alone |
| Gold price, LBMA fix | LBMA / MCX / COMEX | 1968– free float | D | Free | No | — |
| US CPI, M2; EA/JP/UK broad money | BLS, FRED, ECB, BoJ, BoE | 1913– / 1959– | M | Free | No | — |
| ACM 10y term premium | NY Fed | 1961– | D | Free | No | Kim-Wright (1990–) |
| India external debt, reserves, import cover | RBI *India's External Debt* + Weekly Statistical Supplement + Handbook of Statistics | 1990– Q, 1950– A | Q / W | Free | No | IMF IFS/BOP |
| RBI REER (40-currency) | RBI Bulletin | 1993– | M | Free | No | BIS REER (1994–) |
| USD/INR reference rate | RBI / FBIL | 1947– | D | Free | No | — |
| BIS credit to private non-fin sector (India) | BIS `TOTAL_CREDIT`, `CREDIT_GAPS` | 1951– | Q, 2q lag | Free | No | RBI SCB credit / MOSPI GDP |
| India household savings (financial vs physical) | RBI Annual Report, MOSPI National Accounts | 1950-51– | A, ~15m lag | Free | **Partially** — long lag, heavy revisions | RBI quarterly financial-flows estimates; carry `stale_q` and decay weight |
| India tax/GDP, GST, UPI, EPFO/NPS | CBDT, GST Council, NPCI, EPFO, PFRDA | GST 2017–; tax 1950– | M/A | Free | No | Short history for GST/UPI ⇒ use z on the available window and flag low confidence |
| India market cap/GDP, MF AUM | NSE/BSE, AMFI | 1990– / 1965– | M | Free | No | — |
| UN population projections | UN WPP 2024 | 1950–2100 | Revised 2y | Free | No | RGI Census projections |
| Long-run historical panel (1870–) | Jordà-Schularick-Taylor Macrohistory DB | 1870– | A | Free | No | Essential for z-score windows; no substitute |
| India pre-1950 output | Sivasubramonian (2000); Broadberry-Custodis-Gupta (2015) | 1600–1947 | A | Book/journal | No | Descriptive use only |

**Nothing in this layer requires a paid data vendor.** That is a deliberate design choice — every input is from IMF, BIS, RBI, CBO, WGC, NY Fed, UN or an academic panel. Bloomberg/CMIE/Refinitiv are needed by other layers, not this one.

---

## 13. Risks and honest caveats

1. **The owner's aggressive CAGR target of 35–60% is not achievable from this architecture.** Long-run Indian equity nominal returns run ~12–14%; at 1.25x average gross leverage with genuinely good factor and selection alpha, a realistic ceiling is ~18–24% CAGR over a full cycle. 35–60% sustained requires extreme concentration, a multi-year small/mid-cap mania, or leverage far above 1.5x. This should be renegotiated to a target of ~20–24% (aggressive) and ~15–18% (moderate) before capital is deployed, or the mandate will force risk-taking the risk framework is designed to prevent.
2. **This layer will look useless for most of its life, and occasionally actively harmful.** Its expected Sharpe contribution over any given 5-year window is approximately zero. Anyone evaluating it on 5-year performance will kill it — probably in the year before it pays. Governance must pre-commit to the evaluation horizon.
3. **Gold is at an all-time high in real USD terms.** Initiating a large strategic gold position today is, on valuation grounds, poor timing. The GVAL brake cuts the anchor from ~18% to ~15%, which is a real but modest mitigation. If gold falls 30% the layer will *add*, which will feel wrong at the time and is the point.
4. **Threshold overfitting is unmeasurable here.** There are ~50 tunable numbers across 14 indicators and 2–3 independent long-wave observations. No cross-validation is possible. The only defence is that the thresholds were set from published economic reasoning (Reinhart-Sbrancia repression bounds, IMF ARA reserve-adequacy metrics, BIS 10pp credit-gap threshold) rather than fitted — and that defence is only as good as our discipline in never re-tuning them after seeing performance. **Freeze the thresholds in git at inception and require two-signature sign-off plus a written rationale for any change.**
5. **The debasement complex is one trade.** Gold, gold financiers, real-asset equities, exporters and short duration all load on the same factor. Without the 35%-of-variance cap in §8.3 this layer builds a concentrated macro bet dressed as strategic diversification.
6. **Regulatory constraints may make the design unimplementable as written.** Gold access depends on the wrapper (PMS cannot readily hold physical; SGB issuance was discontinued in 2024-25 [verify], leaving ETFs, MCX futures and international routes); FX derivatives generally require an underlying exposure; AIF Cat III leverage rules differ from PMS. **This must be resolved before build, not after.**
7. **India-specific tail risks are larger, nearer and less amenable to this machinery than the global long wave.** A regional conflict, an oil shock, a large NBFC/bank failure or a fiscal rupture would dominate the portfolio outcome and would arrive faster than a 10-quarter dwell can respond. Those belong to L18, and L18 must not assume this layer provides protection against them.
8. **Point-in-time data risk.** RBI/MOSPI savings and national-accounts revisions are large and arrive with 12–18 month lags. A naive backtest reading final vintages will look materially better than live performance.
9. **Dating the phase is the weakest link.** The inception prior P(P4)=0.55 with τ=6y is a judgement, not an estimate. If the correct reading is "late P3, with P4 still a decade away," this layer is systematically 5–10 percentage points too heavy in gold and too short in duration for a decade. The slew limits mean that error costs perhaps 50–120bps/yr — survivable, which is why the slew limits exist.
10. **Model-narrative capture.** The debasement story is emotionally compelling and currently fashionable. The GVAL brake, the low RSVDIV weight, the Eichengreen damping and the mandatory null test are all deliberate counterweights. They should be defended when they become unpopular.

---

## 14. Build plan

Build strictly largest-cycle-first, as mandated. Effort in engineer-days, assuming L17 (point-in-time store) exists in skeleton form.

| # | Step | Deliverable | Days | Depends on |
|---|---|---|---|---|
| 1 | Indicator registry & schema | `indicators.yaml` — 14 entries with bands, `h`, dwell, confirm, source URI, licence; JSON-schema validated | 2 | L01 taxonomy |
| 2 | Point-in-time ingestion adapters | Loaders for IMF WEO/COFER/IFS, BIS, CBO, WGC, NY Fed, RBI (external debt, WSS, REER, Handbook), UN WPP, AMFI, NPCI — each writing `(series, value, asof, vintage)` | 8 | L17 |
| 3 | JST Macrohistory + Sivasubramonian backfill | Long-window z-score bases (1870– global, 1900– India) | 3 | 2 |
| 4 | State machine engine | `SlowIndicator.step()` with median smoothing, Schmitt bands, dwell, confirm, one-notch step limit, immutable transition log | 4 | 1 |
| 5 | Constraint test suite | 200y synthetic-path property tests asserting flip frequency, turnover and slew bounds | 3 | 4 |
| 6 | Composites, GVAL brake, block slew limiter | `G, G_eff, V, E, A` with `\|Δ\| ≤ 0.25/q` | 2 | 4 |
| 7 | Phase posterior + slide registry | Versioned `slide_events.yaml`, two-signature sign-off hook, ±3y/10y bound, 2q lag + 4q amortisation, 20%/yr decay | 4 | 6, L19 |
| 8 | Anchor mapping | `LW_ANCHOR` — gold, debt range, duration, 8 equity theme tilts, leverage modifier | 3 | 6 |
| 9 | Hedge policy emitter | `LW_HEDGE_POLICY` with gates, budgets and regulatory-feasibility flags | 2 | 8, L14 |
| 10 | Rate limiter + L11 contract | Per-field `max_delta_per_quarter`, enforced in the allocation engine with a violation alarm | 2 | 8, L11 |
| 11 | Regime-analog replays | Documented studies: US 1965–82, JP 1989–2005, UK 1945–70, IN 1985–95 | 5 | 4, 3 |
| 12 | Null test + ablation + vintage-integrity test | Committee pack showing L02 vs fixed anchor, and with/without GVAL | 3 | 11, L16 |
| 13 | Monitoring & explainability | Quarterly one-page state report: every indicator, its state, quarters-in-state, distance to next flip, and the resulting anchor delta | 2 | 8 |
| 14 | Threshold freeze & governance | Git tag, sign-off record, change-control procedure | 1 | 13, L19 |

**Total ≈ 44 engineer-days.**

---

## 15. References

1. Reinhart, C. & Rogoff, K. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton UP.
2. Herndon, T., Ash, M. & Pollin, R. (2013). "Does High Public Debt Consistently Stifle Economic Growth? A Critique of Reinhart and Rogoff." *Cambridge Journal of Economics*.
3. Reinhart, C. & Sbrancia, M.B. (2011). "The Liquidation of Government Debt." NBER WP 16893; revised in *Economic Policy* (2015).
4. Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M. & Taylor, A. (2019). "The Rate of Return on Everything, 1870–2015." *Quarterly Journal of Economics* 134(3).
5. Jordà, Ò., Schularick, M. & Taylor, A. — Macrohistory Database (macrohistory.net), 17 countries, 1870–present.
6. Eichengreen, B., Chiţu, L. & Mehl, A. (2016). "Stability or Upheaval? The Currency Composition of International Reserves in the Long Run." *IMF Economic Review*. And *How Global Currencies Work* (2018), Princeton UP.
7. Barro, R. (2006). "Rare Disasters and Asset Markets in the Twentieth Century." *QJE* 121(3). Barro, R. & Ursúa, J. (2008). "Macroeconomic Crises since 1870." *Brookings Papers*.
8. Bloom, D. & Williamson, J. (1998). "Demographic Transitions and Economic Miracles in Emerging Asia." *World Bank Economic Review* 12(3).
9. Dalio, R. (2018). *Principles for Navigating Big Debt Crises*; (2021) *Principles for Dealing with the Changing World Order*. Bridgewater/Avid Reader. **Used for structure, not for scores.**
10. Garvy, G. (1943). "Kondratieff's Theory of Long Cycles." *Review of Economic Statistics* [verify journal/volume].
11. Solomou, S. (1987). *Phases of Economic Growth, 1850–1973: Kondratieff Waves and Kuznets Swings*. Cambridge UP [verify subtitle].
12. Sivasubramonian, S. (2000). *The National Income of India in the Twentieth Century*. OUP.
13. Broadberry, S., Custodis, J. & Gupta, B. (2015). "India and the great divergence: An Anglo-Indian comparison of GDP per capita, 1600–1871." *Explorations in Economic History* 55.
14. Adrian, T., Crump, R. & Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." *Journal of Financial Economics* — the ACM term-premium model.
15. BIS (2010 onward). "Guidance for national authorities operating the countercyclical capital buffer" — the credit-to-GDP gap methodology and the ~10pp distress threshold.
16. IMF (2016). "Assessing Reserve Adequacy — Specific Proposals" — the ARA EM metric used in `EXSOL`.
17. World Gold Council, *Central Bank Gold Reserves Survey 2026* and Goldhub reserves data.
18. Congressional Budget Office (Feb 2026). *The Budget and Economic Outlook: 2026 to 2036*.
19. Reserve Bank of India, *India's External Debt* (quarterly), *Handbook of Statistics on the Indian Economy*, *Annual Report 2025-26*.

*Citations marked [verify] in the body require confirmation against the primary source before this document is circulated externally.*
