# Layer 02 — Long-Wave Layer: Currency, Reserve Order and Sovereign Debt (50–250 years)

**Abstract.** This layer supplies the slowest input in the cycle stack: a Bayesian *prior* over where the global monetary order and India's own development arc sit in multi-decade arcs, expressed as a strategic centre of gravity for gold weight, equity theme tilts, defensive ballast, a true-cash floor, the gross-leverage ceiling and standing tail-hedge policy. Fifteen slow indicators are smoothed over 4–20 quarters and discretised into five wide states by a Schmitt trigger with a minimum dwell of **30 to 84 months**, so no indicator flips more than roughly once per business cycle and a full −2→+2 traverse takes 10–28 years. A *phase clock* carries an ordinal stage (P1 sound money → P5 reset) as a posterior distribution, with a bounded **±3.0-year "trigger slide"** that pre-registered, human-signed events may apply. Portfolio impact is hard-capped at **300 bps (aggressive) / 250 bps (moderate) of allocation change per quarter and 900 bps of one-way turnover per year** — under 3% of the aggressive book's turnover budget. Two frozen decisions shape the design: the debt sleeve is a flat 10% return with **no duration overlay**, which removes the classic debasement channel and forces this layer to speak through gold, equity tilts, true cash and options; and capital is proprietary, so leverage and the full option overlay are available. The layer is **not a forecaster** — with two-and-a-bit independent observations of a reserve-currency succession and dozens of tunable thresholds, its degrees of freedom exceed its effective sample size by two orders of magnitude. It is a prior, a constraint generator and an insurance policy, engineered so that being wrong for a decade costs tens of basis points a year rather than the mandate.

---

## 1. Epistemic contract (read before anything else)

| Claim | Status |
|---|---|
| Multi-decade arcs of debt build-up → monetisation → reset exist | Well-evidenced *narratively*, weakly *statistically*. n ≈ 2–3 independent successions (Dutch→British c.1780–1815; British→US c.1914–1945; a possible incomplete third). |
| Those arcs have an estimable period | **False, or unestimable.** Do not model a period. Model an ordinal stage plus elapsed time. |
| Financial repression liquidates government debt | Strongly evidenced, mechanism-level (Reinhart & Sbrancia). The single most reliable plank here. |
| Systemic banking crises are followed by large, persistent asset drawdowns | Strongly evidenced (Reinhart & Rogoff 2009; Jordà-Schularick-Taylor). Usable as a *conditional loss distribution*, never as a timing signal. |
| Reserve status collapses suddenly, winner-take-all | **Contradicted** by Eichengreen, Chiţu & Mehl: sterling and the dollar coexisted for decades; inertia is weaker *and* transitions slower than the popular narrative. Used to **damp** this layer. |
| Kondratiev 50–60y waves exist in output | Largely rejected in the literature. **Not implemented.** |

**The layer produces exactly three things.**

1. **A prior** — a centre of gravity for the strategic mix, which the Stage-3 optimizer treats as the centre of a quadratic penalty, never as a target.
2. **A constraint set** — never zero gold; a true-cash floor in late states; a cut gross-leverage ceiling in the reset tail.
3. **A hedge policy** — standing option and INR expressions sized against a *rare-disaster prior* (Barro–Ursúa: ~3.5%/yr, ~22% mean loss), not a point forecast.

It produces no expected return, no Sharpe estimate and no timing signal; any consumer treating `LW_*` as alpha is misusing it. **Asymmetry rule:** this layer may *lower* portfolio risk unilaterally, and may never override the drawdown/cash engine to *raise* it.

---

## 2. Evidence actually used

| Source | What is taken from it |
|---|---|
| **Reinhart & Rogoff (2009), _This Time Is Different_** | The crisis-aftermath regularity: after systemic banking crises, real equity −55% over ~3.4y, real house prices −35% over ~6y, real public debt +86% over 3y. The 90%-debt/GDP growth threshold was materially weakened by **Herndon, Ash & Pollin (2013)**; **no debt/GDP growth threshold is used here.** Debt levels enter only as a state variable for fiscal flexibility. |
| **Reinhart & Sbrancia (2011/2015), "The Liquidation of Government Debt"** | Negative real rates in 1945–1980 liquidated government debt at ~1–5% of GDP/yr (US/UK ~3–4%). **The mechanism behind `RPR`**, and the strongest empirical plank in the layer. |
| **Jordà, Knoll, Kuvshinov, Schularick & Taylor (2019), _QJE_; Macrohistory DB (17 countries, 1870–)** | Long-run real returns — equity ~7%, housing ~7%, safe assets ~1–3% — with multi-decade stretches of negative real safe-asset returns. Sets the priors the anchor centres on and supplies the long z-score windows. |
| **Eichengreen, Chiţu & Mehl (2016, 2018)** | Reserve status is contestable, multipolar and slow-moving; inertia is weaker *and* transitions slower than the popular narrative. Justifies the **lowest weight (0.15) on `RSVDIV`**. |
| **Barro (2006); Barro & Ursúa (2008)** | Rare-disaster frequency (~3.5%/yr) and size (~22% mean loss). **This, not the phase estimate, sizes the tail hedge.** |
| **Dalio (2018, 2021)** | The *structure* of the stage ordering and the mechanisms (debt service crowding out → monetisation → debasement → reserve-status loss). **Not the scores** — the Great Power Index has hand-set weights fitted in-sample to known outcomes and is not an estimated model. |
| **Kondratiev** | Garvy (1943) is the classic demolition [verify journal]; Solomou (1987) finds weak, unstable evidence in output [verify subtitle]. Spectral tests on long price series generally fail to reject no-50-60y-periodicity once trend and war shocks are removed. **No Kondratiev clock is implemented.** Long lead times in commodity capex belong to the commodity/external layer. |
| **Bloom & Williamson (1998)** | Demographic transition explains roughly a third of the East Asian growth miracle. Basis for `DEMO`. |
| **Sivasubramonian (2000); Broadberry, Custodis & Gupta (2015)** | India annual output from 1900, extended to 1600. Enough to *describe* India's arc, nowhere near enough to *estimate* an India long wave — there is no such literature with usable market data before 1950. This layer therefore **imports the global wave and estimates only India's position on a development S-curve.** |

---

## 3. Dated snapshot — 28 August 2026

Re-pull everything from the point-in-time store; this table is documentation, not an input.

| Variable | Value | Source / date |
|---|---|---|
| US federal debt held by public | 101% of GDP → 120% by 2036 (prior high 106% in 1946) | CBO *Outlook 2026–2036*, Feb 2026 |
| US net interest | 3.3% of GDP → 4.6% by 2036; ≈19% of federal revenue | CBO Feb 2026 |
| USD share of allocated FX reserves | **57.13% (2026Q1)** from 56.42% (2025Q4); ~half the rise is USD valuation | IMF COFER |
| Central-bank gold demand | 2025 ≈863t; 2026Q1 244t; 2026F ≈850t. Gold now a larger share of global reserves than US Treasuries | WGC Goldhub / *CB Gold Survey 2026* |
| Gold | ~$4,600/oz; **all-time high $5,597 on 29-Jan-2026 (−18% from peak)** | LBMA, Aug 2026 |
| India external position | Reserves **$716.9bn (14-Aug-26)**, >10m import cover, 90.8% of external debt; external debt $762.8bn = 20.8% of GDP; ST/reserves 21.6% | RBI WSS / *India's External Debt* |
| India credit, income, savings | Private non-fin credit 97.4% of GDP with BIS **gap ≈ −3.2pp**; GDP ~$4.15tn, per capita ~$2,813; savings 21.7% of GDP (financial ~11%, physical ~12.9%) | BIS Q3-25; IMF WEO; RBI/MOSPI |
| USD/INR; sovereign rating | ~95, appreciating in Jul-26; three upgrades in 2025 (S&P, DBRS → BBB; R&I → BBB+) | RBI; agencies |

**The tension the snapshot creates.** Every *debasement* indicator is loud (record debt and debt service, central banks holding more gold than Treasuries, term premium rebuilding, Treasury buying back long bonds), while every *India external* indicator is benign (20.8% external debt, >10 months cover, negative credit gap, three upgrades, reserves at a record) — and **gold is at an all-time high in real USD terms even after an 18% drawdown from January**. A naive "late debt cycle → buy gold" rule buys the most expensive gold in history. The valuation brake in §6 exists precisely for that.

---

## 4. The fifteen slow indicators

Blocks: **GMO** (global monetary order / debasement), **IEF** (India external fragility), **IARC** (India structural arc). Sign convention: for GMO and IEF **+2 = maximum stress/debasement/fragility**; for IARC **+2 = maximally favourable**; for `GVAL` **+2 = gold maximally expensive**. `h` = hysteresis half-width (Schmitt trigger: entering a band needs the threshold, leaving it needs the threshold ± `h`). Min-dwell = `(dwell_q + confirm_q) × 3` months.

| Code · Blk | Definition (exact) | Free source · history | Bands −2 / −1 / 0 / +1 / +2 · `h` | Smooth · dwell+conf · **min months** | Today | MVP |
|---|---|---|---|---|---|---|
| `GDS` GMO | 0.6·(G4 GDP-wtd general-govt gross debt/GDP) + 0.4·(US net interest ÷ federal revenue) | IMF WEO `GGXWDG_NGDP`; CBO; FRED `A091RC1Q027SBEA`, `W006RC1Q027SBEA`; BIS `TOTAL_CREDIT` sector G · 1980– (JST 1870–) | debt/GDP `<60 / 60–80 / 80–100 / 100–120 / >120`%; int÷rev `<6 / 6–10 / 10–14 / 14–19 / >19`% · `h`=4–5pp, 1.0–1.5pp | 8q med · 12q+2q · **42** | **+2** | ✅ |
| `RPR` GMO | GDP-wtd Σwᵢ(policy rateᵢ − core CPI YoYᵢ), i ∈ {US, EA, JP, UK} | BIS policy-rate DB; OECD MEI; FRED `FEDFUNDS`, `CPILFESL` · 1954– | `>+3.0 / +1.5…+3.0 / +0.5…+1.5 / −1.5…+0.5 / <−1.5`% · `h`=0.40pp | 12q med · 8q+2q · **30** | **+1** | ✅ |
| `CBGS` GMO | 0.5·z(official gold at market ÷ total official reserves incl. gold) + 0.5·z(trailing-4q net CB purchases, t) | WGC Goldhub (free registration); IMF IFS · IFS 1948–, flows 2000– | net 4q purchases: `sell>150 / −150…+150 / 150–550 / 550–900 / >900` t · `h`=100t | 8q med · 10q+2q · **36** | **+2** | ✅ |
| `RSVDIV` GMO | −1 × (5y change in USD share of *allocated* reserves, pp/yr) + 0.3·z(HHI of reserve-currency shares) | IMF COFER · 1999– Q, 1965– A | `>+1.0 / +0.3…+1.0 / −0.5…+0.3 / −1.2…−0.5 / <−1.2` pp/yr · `h`=0.25pp/yr | 8q med of the 5y slope · 12q+3q · **45** | **+1** | ⬜ |
| `GVAL` GMO **brake** | 0.5·z₅₀y(gold ÷ US CPI) + 0.5·z₅₀y(above-ground stock × price ÷ G4 broad money) | LBMA/MCX; FRED `CPIAUCSL`, `M2SL`; WGC stock; ECB/BoJ/BoE M3 · free float 1968–, CPI 1913– | `<−1.75 / −1.75…−0.75 / ±0.75 / +0.75…+1.75 / >+1.75` z · `h`=0.35z | 8q med · 8q+2q · **30** | **+1** (V=+1.4) | ✅ |
| `TPR` GMO | z₃₀y(ACM 10y US term premium) + 0.3·z(India 10y G-sec − 1y T-bill) | NY Fed ACM (free CSV); CCIL/RBI · 1961– / 1997– | `<−1.0 / −1.0…−0.25 / ±0.25 / +0.25…+1.0 / >+1.0` z · `h`=0.30z | 12q med · 10q+2q · **36** | **+1** [verify] | ⬜ |
| `EXSOL` IEF | Equal-wt mean of four banded sub-scores (below) | RBI *India's External Debt* (Q), WSS (W), Handbook · 1990– Q | see sub-table | 4q med · 8q+2q · **30** | **−1** | ✅ |
| `REERDEV` IEF | log(REER₄₀) − log(20y rolling mean) − Balassa–Samuelson allowance +0.9%/yr [verify] | RBI 40-currency REER (2015-16=100); BIS REER · 1993– | `<−12 / −12…−5 / −5…+7 / +7…+15 / >+15` % · `h`=2.5pp | 8q med · 8q+2q · **30** | **0** [verify] | ⬜ |
| `INRTREND` IEF | Residual z of log(USDINR) vs 25y log-linear trend. Fitted drift **2.91%/yr** (45.0→95.0, 2000→2026) to **3.41%/yr** (31.4→95.0, 1993→2026); forward prior compressed to **2.0–2.5%/yr** on India's 4% CPI target vs US ~2% | RBI reference rate / FBIL · 1947– (breaks 1966, 1991) | INR *stronger* than trend: `<−1.25 / −1.25…−0.5 / ±0.5 / +0.5…+1.25 / >+1.25` z · `h`=0.30z | 8q med · 8q+2q · **30** | **−1** | ✅ |
| `PCI` IARC | Nominal USD GDP per capita, log position on the consumption/financialisation S-curve | IMF WEO; MOSPI · 1950– (1900– Sivasubramonian) | `— / <$1,200 / $1.2–2k or >$10k / $5–10k / $2–5k` (steepest = +2) · `h`=$250 | 3y mean · 20q+4q · **72** | **+2** | ◐ |
| `FINDEEP` IARC | 10y trailing **slope** of private non-fin credit/GDP + z(mcap/GDP) + z(MF AUM/GDP). **Low-frequency component only — the BIS credit *gap* belongs to the credit-cycle layer** | BIS `TOTAL_CREDIT`; NSE/BSE; AMFI · 1951– / 1965– | composite z, `±1.0` outer, `±0.35` inner · `h`=0.30z | 12q med · 16q+3q · **57** | **+1** | ◐ |
| `HHFIN` IARC | 10y mean of (household gross financial savings ÷ total household savings) + 5y slope of net financial savings/GDP | RBI Annual Report; MOSPI National Accounts · 1950-51– | `<25 / 25–35 / 35–45 / 45–55 / >55` % · `h`=2.5pp | 5y mean · 20q+4q · **72** | **+1** (≈46%) | ◐ |
| `FORM` IARC | z-composite: tax revenue/GDP, GST/GDP, UPI value/GDP, (EPFO+NPS subscribers)/working-age pop | CBDT, GST Council, NPCI, EPFO, PFRDA · GST 2017–, tax 1950– | composite z as `FINDEEP` · `h`=0.30z | 8q med · 16q+3q · **57** | **+1** | ◐ |
| `DEMO` IARC | Years to peak working-age (15–64) share, and the level of that share. India's peak ≈ **2036–2041** [verify UN WPP 2024] | UN WPP; RGI Census · 1950–2100 | `<−10 / −10…0 / 0–10 / 10–25 / >25` years to peak · `h`=2y | none · 24q+4q · **84** | **+1** | ◐ |
| `INGOLD` IARC | 0.5·z(household gold stock × price ÷ GDP) + 0.3·z(organised gold-loan AUM ÷ GDP) + 0.2·z(gold imports ÷ GDP). Stock ≈25,000t ≈ **$3.7tn ≈ 89% of GDP** at $4,600/oz [verify stock] | WGC India demand/stock; RBI sectoral credit; DGCI&S imports · 2000– / 2007– | composite z as `FINDEEP` · `h`=0.30z | 8q med · 12q+3q · **45** | **+1** | ⬜ |

✅ MVP live · ◐ MVP **frozen constant** (§11) · ⬜ deferred to v2.

**`EXSOL` sub-bands** (score each, average, round away from zero):

| Sub-metric | +2 fragile | +1 | 0 | −1 | −2 strong | `h` | Today |
|---|---|---|---|---|---|---|---|
| External debt / GDP | >30% | 24–30 | 18–24 | 14–18 | <14 | 2pp | 20.8% ⇒ 0 |
| ST debt / reserves | >60% | 40–60 | 25–40 | 15–25 | <15 | 5pp | 21.6% ⇒ −1 |
| Import cover (months) | <6 | 6–9 | 9–12 | 12–16 | >16 | 0.75m | >10 ⇒ 0 |
| Reserves / external debt | <50% | 50–70 | 70–90 | 90–120 | >120 | 5pp | 94% ⇒ −1 |

Mean −0.5 ⇒ **−1** (mildly strong). For contrast, 1991: ST/reserves ~380%, cover ~3 weeks ⇒ **+2** on every row.

**Three worked readings that show the machinery.**

- **`GVAL` = +1, V = +1.4.** Jan-1980 peak $850 × (CPI 2026 ≈330 ÷ CPI Jan-1980 ≈77.8) ≈ **$3,605 in 2026 dollars**; spot $4,600 is 1.28× that and the Jan-2026 $5,597 was 1.55× ⇒ real-price z ≈ +1.8. Stock-to-money leg: ~220,000t = 7.07bn oz × $4,600 = $32.5tn ÷ G4 broad money ≈$65tn = 0.50 — high, but below the 1980 analogue ⇒ z ≈ +1.0.
- **`RSVDIV` hysteresis in action.** 2021Q1 ≈59.5% → 2026Q1 57.13% = **−0.47pp/yr**, which is just inside the `0` band. The prior state `+1` is **retained** until the slope clears −0.25pp/yr. A valuation-driven quarterly uptick must not flip a 45-month state.
- **`CBGS` = +2, with the first evidence against it already logged.** Flows decelerated 1,045t (2024) → 863t (2025) → ~850t forecast (2026), which alone scores +1; the record reserve-share leg (gold above US Treasuries) carries the composite to +1.5 ⇒ +2. The deceleration is logged as evidence toward a downgrade that, under dwell, cannot act before 2029.

## 5. State machine — smoothing, hysteresis, dwell, confirm

Four brakes in series; each alone prevents quarterly whipsaw.

```python
@dataclass
class SlowIndicator:
    code: str
    bands: list[tuple[float, float]]  # 5 entry bands, native units, ascending
    h: float          # hysteresis half-width, native units
    smooth_q: int     # trailing-MEDIAN window (median, not mean: robust to revisions)
    dwell_q: int      # min quarters a state must be held before change is even considered
    confirm_q: int    # consecutive quarters the new state must be signalled

def step(ind, hist_raw, st, q_in_state, pending, pend_n, asof):
    x = median(hist_raw[-ind.smooth_q:])                      # PIT vintages only
    tgt = band_with_hysteresis(x, ind.bands, ind.h, cur=st)   # Schmitt: leaving needs +h
    if q_in_state < ind.dwell_q:
        return st, q_in_state + 1, None, 0                    # dwell lock
    if tgt != st:
        pending, pend_n = (pending, pend_n + 1) if tgt == pending else (tgt, 1)
        if pend_n >= ind.confirm_q:
            new = st + sign(tgt - st)                         # ONE notch per event
            log_transition(ind.code, st, new, asof, x)        # immutable audit
            return new, 0, None, 0
        return st, q_in_state + 1, pending, pend_n
    return st, q_in_state + 1, None, 0
```

**Guaranteed minimum months between flips** = `(dwell_q + confirm_q) × 3` → **30 months (RPR, GVAL, EXSOL, REERDEV, INRTREND) to 84 months (DEMO)**, per the table in §4. Because of the one-notch limit, a full −2→+2 traverse takes ≥ 4×(dwell+confirm) = **10 to 28 years**. That is the intended behaviour, not a bug.

**Vintage discipline.** Inputs are read from the point-in-time store with an as-of timestamp. India's household-savings and national-accounts series are revised late and heavily; final-vintage reads make any backtest meaningless and are rejected at the API boundary. Any indicator with vintage lag beyond 3 quarters publishes `stale_q` and has its weight decayed by `0.9^(stale_q − 3)`.

---

## 6. Composites, the valuation brake, the phase clock

```
G      = 0.25·GDS + 0.25·RPR + 0.20·CBGS + 0.15·RSVDIV + 0.15·TPR      ∈ [−2,+2]
G_eff  = clip(G − 0.40·V, −2, +2)                      # V = GVAL continuous value
E      = mean(EXSOL, REERDEV, INRTREND)                ∈ [−2,+2]   (+ = fragile)
A      = 0.22·PCI + 0.18·FINDEEP + 0.18·HHFIN + 0.17·FORM + 0.15·DEMO + 0.10·INGOLD
```

Weights follow evidence strength: `RPR` (the Reinhart–Sbrancia mechanism) and `GDS` (directly measured) get most; `RSVDIV` least, because Eichengreen–Chiţu–Mehl show reserve shares move slowly and reversibly — a point the 2026Q1 COFER uptick confirms.

**The valuation brake is the single most important line in the layer.** `G_eff = G − 0.40·V` is what stops "the debt cycle is late" from becoming "buy gold at any price."

**Block slew limiter (second brake):** `|ΔG|, |ΔE|, |ΔA| ≤ 0.25 per quarter` after aggregation, so a full composite traverse takes ≥16 quarters even if every constituent flipped at once.

**Today:** G = 0.25(2)+0.25(1)+0.20(2)+0.15(1)+0.15(1) = **1.45**; V = **1.4** ⇒ **G_eff = 0.89**; E = mean(−1, 0, −1) = **−0.67**; A = **1.22**.

### Phase clock

| Stage | Description | Prior duration |
|---|---|---|
| P1 | New order: low debt, positive real rates, credibility rebuilding | 20–35y |
| P2 | Credit expansion: debt rising from a low base, real rates falling | 20–30y |
| P3 | Peak debt: debt/GDP high, real rates ≈0, assets rich | 10–20y |
| P4 | Deleveraging & monetisation: repression, CB expansion, debasement, gold outperforms | 10–20y |
| P5 | Reset: devaluation, restructuring, anchor revaluation, political/military rupture | 3–10y |

**Inception prior (2026-08-28), signed off and frozen in the audit log:** `P(P3)=0.35, P(P4)=0.55, P(P5)=0.10`, with **τ = 6 years** in P4 (dating entry to the 2020 monetisation episode). Posterior update is deliberately crude and slow — a monotone logistic map from `G` and `τ`, updated **annually**, max shift **0.10/year/stage**. There is no likelihood function worth writing; pretending otherwise would be false precision.

---

## 7. The trigger-slide mechanism

Named, **pre-registered** events may advance (+) or retard (−) the clock τ. Each requires (a) an event matching a pre-registered definition, (b) two-signature sign-off from the Stage-2 human layer, (c) an immutable timestamped log entry. **No event may be added retroactively** — `slide_events.yaml` is git-versioned and a backtest may only read the version that existed at the simulated date.

| Global event (observable definition) | Δτ (years) |
|---|---|
| Gold revalued/monetised on a G7 CB balance sheet, **or** a new multilateral settlement asset >$100bn/yr turnover | **+3.0** (forces P(P5) ≥ 0.40) |
| Reserve-currency issuer misses a scheduled payment (incl. debt-ceiling technical default) | +2.5 |
| Explicit yield-curve control announced by the Fed or ECB (BoJ excluded — priced) | +2.0 |
| Nuclear-armed states in direct armed conflict, **or** a reserve issuer's official assets >$100bn frozen (2022 Russia freeze already in the base case) | +2.0 |
| Two of three agencies downgrade a G3 sovereign below AA | +1.5 |
| G4 CB balance sheet +>10% of GDP in ≤12 months **outside** an acute banking crisis | +1.5 |
| G20 currency crisis: >25% depreciation vs SDR in 12 months | +1.5 |
| G4 debt/GDP falls ≥15pp over 5 years without default or >6% inflation | **−2.5** |
| US primary balance ≥ 0 for three consecutive fiscal years | −2.0 |
| G4 trend real growth ≥1pp above its prior 10y mean for 3+ years (the AI-productivity case) | −2.0 |
| G4 real policy rate > +1.5% sustained 3+ years with stable debt/GDP | −1.5 |

| India event | Δτ_India |
|---|---|
| Reserves fall >20% peak-to-trough within 12 months | +2.0 |
| CAD > 3.5% of GDP for four consecutive quarters | +1.5 |
| Combined centre+state fiscal deficit > 11% of GDP for two years | +1.5 |
| Brent > $120/bbl sustained six months (India imports ~85% of crude) | +1.0 |
| Sovereign upgrade to A− or better by two of three majors | −1.0 |
| Net FPI debt inflows > 2% of GDP over 12 months (index-inclusion effects) | −1.0 |
| Reserves > 15 months' import cover sustained four quarters | −1.0 |

**Slide arithmetic.** (1) Cumulative net slide is **bounded to ±3.0 years over any rolling 10-year window**; excess is discarded, not carried. (2) Each category may fire **at most once per 3 years**. (3) Slide is applied with a **2-quarter lag** and **amortised linearly over the following 4 quarters**, so even a +3.0y event moves the book at ≤ the §9 rate limits. (4) Slides **decay 20%/yr after 5 years**, so a decade-old shock does not permanently distort the clock.

---

## 8. Mapping to the portfolio

The layer emits an **anchor**, not a trade. Stage 3 treats it as the centre of a quadratic penalty; faster layers deviate at a cost.

### 8.0 The missing channel, stated plainly

The owner has frozen the debt sleeve as a flat 10% return with **no duration overlay and no IRF/OIS**. In the standard toolkit a debasement view is expressed *primarily* through duration (short nominal, long linkers). Both legs are gone: duration by decision, and **India has no usable inflation-linked market** (the 2013–14 IIBs and retail IINSS-C are illiquid or discontinued). Two consequences, neither to be papered over.

1. **The view must be carried by gold, equity theme tilts, true cash and options.** The gold coefficient is accordingly raised (5.5 → 6.0) and the floor 4% → 5% relative to a design with duration available. This is channel substitution, not extra conviction, and it *concentrates* the expression — hence the variance cap in §8.2.
2. **This layer owes the optimizer a state-dependent debt correlation.** The frozen assumption is that the sleeve's equity correlation flips from ≈−0.2 in disinflation to ≈+0.4 in an inflation shock. The long-wave state is precisely what determines which applies, so the layer publishes `LW_DEBT_CORR_STATE` and the optimizer must consume it instead of one unconditional number.

```
LW_DEBT_CORR_STATE = "inflation_shock" if G_eff >= 1.25 or (RPR == 2 and GDS == 2)
                   = "mixed"           if 0.25 <= G_eff < 1.25        # <- today (0.89)
                   = "disinflation"    otherwise
corr_equity_debt   = {+0.40, +0.15, -0.20}[state]
```

### 8.1 Anchor formulas

```
w_gold_anchor    = clip( 11% + 6.0·G_eff + 1.5·max(E, 0),           5%, 30% )
w_equity_anchor  = clip( 55% + 5.0·A − 7.0·max(G_eff, 0) − 3.0·max(E, 0), 30%, 75% )
w_truecash_floor = clip( 2.0·max(G_eff − 0.5, 0) + 8.0·P(P5),        0%, 12% )
w_debt_anchor    = 100% − w_gold_anchor − w_equity_anchor            # ≤ 70% mandate cap
```

*Today:* gold **16.3%**, equity **54.9%**, true-cash floor **1.6%**, debt sleeve **28.8%** (of which ≥1.6pp must be genuine liquidity, not the 10% credit sleeve).

| G_eff / phase | Gold anchor | Equity anchor | Debt+cash | True-cash floor | Gross-leverage ceiling |
|---|---|---|---|---|---|
| ≤ −1.0 (creditor-friendly) | 5–8% | 60–75% | 20–35% | 0% | 1.50x |
| −1.0 to −0.25 | 7–11% | 55–70% | 25–40% | 0% | 1.50x |
| −0.25 to +0.5 | 10–15% | 50–65% | 25–45% | 0–1% | 1.50x |
| **+0.5 to +1.25 (today)** | **14–20%** | **45–60%** | **25–45%** | **1–3%** | **1.40x** |
| +1.25 to +2.0 (loud debasement) | 18–30% | 35–55% | 20–40% | 3–8% | 1.25x |
| P(P5) ≥ 0.40 (reset confirmed) | 22–30% | 30–45% | 15–35% | 8–12% | 1.10x |

**Gold ceiling from this layer is 30%**, against the 50% mandate cap. The remaining headroom belongs to the gold-sleeve and macro-regime layers; total gold can reach 50% only if several layers agree, never on the long wave alone. A **5% floor applies at all times** — gold is insurance and you do not cancel insurance because the sky is clear. Implementation is ETF or MCX futures only (frozen); this layer specifies *economic exposure*, the gold sleeve chooses the instrument.

**True cash is not the debt sleeve.** The flat-10% assumption makes a cash call look free, but a genuine 10% short-duration return in India implies AA/A credit, which gaps and does not fund redemptions in a crisis. The `w_truecash_floor` therefore mandates T-bill/liquid exposure that is *distinct from* the debt sleeve, rising as the reset probability rises.

### 8.2 Equity theme tilts

Active weights versus the equity benchmark, in **percentage points of the equity sleeve**. The bottom-up and sector layers pick names; this layer sets only the theme budget.

| Theme | Driver | Range (pp) | Today |
|---|---|---|---|
| Real / hard assets (metals, mining, energy, cement, aggregates) | `+2.5·G_eff` | −5 … +6 | +2.2 |
| Gold-linked (gold-loan NBFCs, jewellery retail, refiners) | `+1.5·G_eff − 0.3·V + 0.5·INGOLD` | −3 … +4 | +1.4 |
| USD-revenue exporters (IT, pharma/CRAMS, specialty chemicals, auto ancillaries) | `+2.0·max(REERDEV,0) + 1.2·max(INRTREND,0) + 0.8·max(G_eff,0)` | −4 … +6 | +0.7 |
| Net USD-cost importers (OMCs, import-heavy capital goods) | `−1.5·max(REERDEV,0) − 0.6·max(G_eff,0)` | −4 … +2 | −0.5 |
| Asset gatherers (AMCs, brokers, exchanges, depositories, wealth) | `+2.0·HHFIN + 1.0·FORM` | −2 … +6 | +3.0 |
| SLR-heavy PSU lenders (long G-sec book) | `−1.5·TPR − 1.0·G_eff` | −5 … +2 | −2.4 |
| Long-duration growth (top-quintile P/E, cash flows >10y out) | `−2.0·max(TPR,0) − 1.0·max(G_eff,0)` | −6 … +3 | −2.9 |
| Domestic consumption S-curve (discretionary, healthcare, financial penetration) | `+2.5·A` | −3 … +6 | +3.1 |

**Two-book adjustment.** The moderate (₹1,000cr) book applies the tilt vector at **0.6× scale** and may express it only within the top ~500 names by ADV, because thematic baskets in the NIFTY-750 tail are untradeable at that size. The aggressive (₹100cr) book uses full scale. Both apply tilts at most **once per quarter**.

**Correlation cap (mandatory).** Gold, gold-linked equities, real assets, exporters and the INR-short expression are, in risk terms, **one trade**. The risk layer must cap the **combined ex-ante risk contribution of the "debasement complex" at 35% of total portfolio variance**. Without it this layer manufactures concentration while presenting as diversification.

### 8.3 INR-sensitive exposures

The long-run prior is a **2.0–2.5%/yr INR depreciation drift** against USD (compressed from the 2.9–3.4% realised 25y trend, on India's 4% CPI target vs US ~2%). Three expressions in priority order: (1) the exporter/importer tilt above — always available, no derivative needed; (2) gold, which for an INR investor is simultaneously long-USD and long-real-asset and has historically earned the INR drift on top of the USD gold return; (3) a direct long-USDINR position, gated at `G_eff ≥ +1.5`, sized **0–8% of NAV notional**. Execution note: RBI's exchange-traded currency-derivative rules require valid contracted underlying exposure, with proof thresholds around USD 100mn [verify current circular] — immaterial in size at ₹100–1,000cr, but a compliance step rather than a free position.

### 8.4 Leverage and the drawdown objective

| Condition | Gross ceiling | Gross target |
|---|---|---|
| Base | 1.50x | 1.25x |
| G_eff ≥ +0.75 | 1.40x | 1.20x |
| G_eff ≥ +1.5 **or** P(P5) ≥ 0.25 | 1.25x | 1.10x |
| P(P5) ≥ 0.40 | 1.10x | 1.00x |

This is this layer's contribution to the "drawdown below Nifty 50" objective. In every historical reset episode, cross-asset correlations converged to one and financing was withdrawn exactly when the levered book most needed it. Cutting the *ceiling* years in advance is the cheapest of all the hedges available here, and it is a ceiling only — the drawdown/cash engine may always go lower.

### 8.5 Standing hedge policy

The options-overlay layer implements; hedge ratio remains its swept parameter (0/25/50/75/100/125%). This layer only sets **gates and budgets**.

| Gate | Instrument | Budget |
|---|---|---|
| `G_eff ≥ +1.0` **and** `V ≥ +1.0` (debasement loud, gold expensive — **today's configuration, just below the gate**) | Express *incremental* gold via 12–24m call spreads/ladders, part-funded by deep-OTM put sales | 25–60 bps of NAV p.a.; ≤40% of the incremental gold anchor in options |
| `G_eff ≥ +1.0` **and** equity valuation in top quintile | Rolling 12m index puts 10–15% OTM, financed by long-dated covered calls | ≤40 bps of NAV p.a.; notional 15–30% of equity |
| `P(P5) ≥ 0.25` | Far-OTM (25–35%) 12m index puts sized on the **Barro–Ursúa disaster prior** (3.5%/yr × ~22% mean loss), *not* on the phase estimate | ≤25 bps of NAV p.a. |

Long-dated option history is unavailable, so none of this is backtestable. It is justified **structurally**: a premium budget bounded at ≤125 bps of NAV/yr in the worst case is a known, capped cost, unlike the loss it insures.

---

## 9. Hard rate limits (non-negotiable)

Enforced in the optimizer, not suggested here. A violation is a system error, not a discretionary override.

| Quantity | Max change per quarter — aggressive | — moderate |
|---|---|---|
| **Total absolute allocation change attributable to this layer (L1 norm)** | **300 bps** | **250 bps** |
| Gold weight | 200 bps | 175 bps |
| Equity weight | 250 bps | 200 bps |
| Debt + cash weight | 250 bps | 200 bps |
| Any single equity theme tilt | 150 bps | 100 bps |
| L1 norm of the full equity tilt vector | 400 bps | 250 bps |
| Gross-leverage ceiling | 0.15x | 0.15x |

**Annual one-way turnover from this layer ≤ 900 bps.** Against the owner's 500%+ and <100% budgets that is **1.8%** and **9%** of total turnover respectively — the right order for a signal that changes once every few years.

**Sole override:** a confirmed P5 event with two-signature sign-off may raise the total cap to **600 bps/quarter for at most two consecutive quarters**, after which it reverts automatically and cannot be re-invoked for three years.

---

## 10. Interfaces

**Consumes**

| From | Object | Use and constraint |
|---|---|---|
| Free-data pipeline | `pit_macro_store(series, asof)` | All 15 indicators. PIT vintages mandatory; final-vintage reads rejected at the API boundary |
| Cycle taxonomy | `horizon_registry`, `SignalObject` schema | Output conformance and sign convention |
| Credit cycle | `bis_credit_gap_india` | **10y trailing slope only**, into `FINDEEP`. That layer owns the gap; double-counting is prohibited and asserted in CI |
| External / currency / commodity | `reer_cycle_state`, `oil_shock_flag` | Gates the exporter/importer tilt; oil feeds an India slide event. Must not touch the gold anchor — cyclical FX (1–3y) is theirs, the 25y drift is mine |
| Valuation & expected returns | `equity_longrun_valuation_z` | Gates the index-put hedge only |
| Stage-2 AI + human overlay | `phase_override_proposal`, `slide_event_nomination` | Phase posterior and slide events. Two-signature sign-off, immutable log, git-versioned registry |

**Exposes**

```python
LW_STATE       = {G, G_eff, V, E, A, phase_posterior:{P3,P4,P5}, tau, slide_years,
                  indicator_states:{code:int}, quarters_in_state:{code:int},
                  confidence: float, asof, stale_q}
LW_ANCHOR      = {w_gold_anchor, w_equity_anchor, w_debt_anchor, w_truecash_floor,
                  equity_tilt_vector:{theme: pp}, book_scale:{aggressive:1.0, moderate:0.6},
                  max_delta_per_quarter:{field: bps}}
LW_CONSTRAINTS = {min_gold: 5.0, max_gold_from_this_layer: 30.0,
                  gross_leverage_ceiling, gross_leverage_target,
                  debasement_complex_max_variance_share: 0.35}
LW_RISK_INPUTS = {debt_corr_state, corr_equity_debt, disaster_prob_annual: 0.035,
                  disaster_mean_loss: 0.22}
LW_HEDGE_POLICY= {gold_option_budget_bps, index_put_policy, fx_policy, disaster_put_budget_bps}
```

Every anchor field carries its own `max_delta_per_quarter`, so the optimizer enforces §9 mechanically without knowing anything about this layer's internals. **Stage 1 sufficiency:** with the Stage-2 overlay switched off, this layer still emits a complete anchor and constraint set — the phase posterior simply stays at its frozen inception prior and no slide events fire.

---

## 11. MVP versus deferred

The build is 3–6 months for one owner plus an AI across ~20 layers. This layer's honest total is ~40 engineer-days; **its MVP must fit in 12**. The ruthless cut: **the entire India structural-arc block is a signed constant in v1.** `PCI`, `FINDEEP`, `HHFIN`, `FORM`, `DEMO` and `INGOLD` have minimum dwells of 45–84 months — not one can change state inside the first two years of live running. Freeze `A = 1.22`, revisit annually. Building live ingestion for six series that cannot move is misallocated effort.

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Indicator registry | `indicators.yaml` — 15 entries with bands, `h`, dwell, confirm, source URI, licence; JSON-schema validated. Non-MVP entries marked `live: false` | 1.0 | ✅ |
| 2 | PIT adapters, MVP series | IMF WEO + COFER, BIS `TOTAL_CREDIT`, FRED (policy rate, core CPI, M2, CPI), NY Fed ACM, WGC Goldhub, RBI External Debt + WSS + reference rate — each writing `(series, value, event_date, knowledge_date)` | 4.0 | ✅ |
| 3 | State machine | `SlowIndicator.step()` with median smoothing, Schmitt bands, dwell, confirm, one-notch limit, immutable transition log | 2.0 | ✅ |
| 4 | Composites + GVAL brake + slew limiter | `G, G_eff, V, E`; `A` from a signed constants file | 1.0 | ✅ |
| 5 | Anchor mapping + rate limiter contract | `LW_ANCHOR`, `LW_CONSTRAINTS`, `LW_RISK_INPUTS`, per-field `max_delta_per_quarter`, two-book scaling | 1.5 | ✅ |
| 6 | Property tests | 200y synthetic AR(1)+jump paths asserting flip frequency ≥ dwell+confirm, quarterly L1 ≤ cap, annual turnover ≤ 900bps, leverage ladder monotone | 1.5 | ✅ |
| 7 | Null test | Fixed-anchor comparison (15% gold, zero tilts, 1.25x) over 1995–2026 in the backtest harness | 1.0 | ✅ |
| 8 | Quarterly state report | One page: each indicator, state, quarters-in-state, distance to next flip, resulting anchor delta | 0.5 | ✅ |
| **MVP subtotal** | | **6 live indicators + 6 frozen constants + 3 deferred** | **12.5** | |
| 9 | Slide registry + phase posterior | Versioned `slide_events.yaml`, sign-off hook, ±3y/10y bound, 2q lag, 4q amortisation, 20%/yr decay, annual logistic update | 4.0 | ⬜ |
| 10 | Remaining live indicators | `RSVDIV`, `TPR`, `REERDEV`, then the IARC block | 5.0 | ⬜ |
| 11 | Hedge-policy emitter | Gates and budgets wired to the options layer | 2.0 | ⬜ |
| 12 | Regime-analog replays | US 1965–82, JP 1989–2005, UK 1945–70, IN 1985–95 | 5.0 | ⬜ |
| 13 | Ablation + vintage-integrity tests | With/without `GVAL`; final-vintage vs PIT gap | 2.5 | ⬜ |
| 14 | Threshold freeze | Git tag, sign-off record, change-control procedure | 0.5 | ✅ |

In MVP, `G_eff` is driven by four live indicators (`GDS`, `RPR`, `CBGS`, `GVAL`) with `RSVDIV` and `TPR` held at signed constants (+1, +1), and `E` by `EXSOL` and `INRTREND` with `REERDEV` at 0. Because both deferred GMO indicators carry only 0.15 weight, the maximum error this introduces in `G_eff` is **±0.6**, which maps to **±3.6pp of gold** — inside the layer's own annual movement budget. That is the argument for the cut, and it is quantified rather than asserted.

---

## 12. Validation — and why a continuous backtest is the wrong test

A 1995–2026 backtest produces two or three state changes and a performance number driven entirely by the 2001–2011 and 2019–2026 gold runs. That number is not evidence. Instead:

1. **Constraint tests (CI-enforced, must pass).** Synthetic 200-year paths; assert flip frequency, per-quarter L1 cap, annual turnover budget, and that the leverage ladder fires only on its stated conditions.
2. **Regime-analog replays (qualitative, documented).** Ask only: *did the state variables move in the right direction, in the right decade, with the right slowness?* Never: *what was the Sharpe?*
3. **The null test (mandatory, expected to be uncomfortable).** Replace the layer with a fixed anchor (15% gold, zero tilts, 1.25x). If the realised difference over 1995–2026 is inside the noise band, **say so in the committee pack.** It probably will be. The justification then rests entirely on the conditional loss distribution in the reset tail — which is the honest claim.
4. **Vintage-integrity test.** Re-run on final vintages; a large gap proves the backtest was leaking revisions.
5. **Ablation.** Remove `GVAL` and confirm the layer would have bought maximum gold in Jan-2026 at $5,597, eighteen percent before the drawdown. That contrast is the argument for the brake.

---

## 13. Risks and constraint conflicts

1. **The 35–60% aggressive CAGR aspiration is not achievable from this architecture.** Long-run Indian equity nominal returns run ~12–14%; at 1.25x average gross with genuinely good selection alpha the realistic full-cycle ceiling is ~18–24%. 35–60% sustained needs extreme concentration, a multi-year small/mid mania, or leverage far beyond 1.5x — each contradicting the drawdown objective. Renegotiate to ~20–24% aggressive, ~15–18% moderate.
2. **Removing the duration overlay removes the natural debasement channel** (§8.0). The view concentrates in gold and a correlated equity complex; the 35%-variance cap and 30% gold ceiling mitigate but do not eliminate it. This follows directly from a frozen decision and the owner should see it stated.
3. **The flat-10% debt sleeve makes de-risking look free.** Any optimizer corners into it, and in a real crisis an AA/A credit sleeve is not a liquidity source. `w_truecash_floor` and `LW_DEBT_CORR_STATE` are partial mitigations; the free lunch remains until the sleeve carries a real drawdown assumption.
4. **This layer will look useless for most of its life and occasionally harmful.** Expected Sharpe contribution over any 5-year window ≈ 0. Anyone evaluating it on 5-year performance kills it, probably in the year before it pays. Governance must pre-commit to the evaluation horizon.
5. **Gold is at an all-time real high even after an 18% drawdown from January 2026.** Initiating a large strategic position now is poor valuation timing; the brake cuts the anchor from 19.7% to 16.3%. If gold falls another 30% the layer *adds* — which will feel wrong and is the point.
6. **Threshold overfitting is unmeasurable.** ~50 tunable numbers, 2–3 independent observations, no cross-validation possible. The only defence is that thresholds came from published reasoning (Reinhart–Sbrancia repression bounds, IMF ARA metrics, BIS credit-gap methodology) rather than fitting — and it holds only as long as we never re-tune after seeing performance. **Freeze thresholds in git; two signatures plus written rationale to change.**
7. **Dating the phase is the weakest link.** `P(P4)=0.55, τ=6y` is a judgement. If the truth is "late P3, P4 a decade away", the layer runs 5–10pp too heavy in gold for a decade, costing ~50–120 bps/yr. Survivable — which is why the slew limits exist.
8. **India-specific tails are nearer and faster than the global wave.** A regional conflict, oil shock, large NBFC failure or fiscal rupture would dominate outcomes and arrive faster than a 30-month dwell can respond. They belong to the risk/drawdown layer, which **must not assume this layer protects against them**.
9. **Point-in-time data risk.** RBI/MOSPI savings and national-accounts revisions are large and arrive 12–18 months late; naive final-vintage backtests will flatter live performance.
10. **Narrative capture.** The debasement story is compelling and currently fashionable. The `GVAL` brake, the low `RSVDIV` weight, the Eichengreen damping and the mandatory null test are deliberate counterweights, and should be defended when they become unpopular.

---

## 14. References

1. Reinhart & Rogoff (2009), *This Time Is Different.* Princeton UP. — Herndon, Ash & Pollin (2013), *Cambridge J. Economics*, the critique.
2. Reinhart & Sbrancia (2011), "The Liquidation of Government Debt", NBER WP 16893; rev. *Economic Policy* (2015).
3. Jordà, Knoll, Kuvshinov, Schularick & Taylor (2019), "The Rate of Return on Everything, 1870–2015", *QJE* 134(3); Macrohistory Database, macrohistory.net/database.
4. Eichengreen, Chiţu & Mehl (2016), "Stability or Upheaval?", *IMF Economic Review*; *How Global Currencies Work* (2018), Princeton UP.
5. Barro (2006), "Rare Disasters and Asset Markets in the Twentieth Century", *QJE* 121(3); Barro & Ursúa (2008), *Brookings Papers.*
6. Bloom & Williamson (1998), "Demographic Transitions and Economic Miracles in Emerging Asia", *World Bank Economic Review* 12(3).
7. Dalio (2018), *Principles for Navigating Big Debt Crises*; (2021), *Principles for Dealing with the Changing World Order.* **Structure, not scores.**
8. Garvy (1943), "Kondratieff's Theory of Long Cycles", *Review of Economic Statistics* [verify]; Solomou (1987), *Phases of Economic Growth, 1850–1973*, Cambridge UP [verify subtitle].
9. Sivasubramonian (2000), *The National Income of India in the Twentieth Century*, OUP; Broadberry, Custodis & Gupta (2015), *Explorations in Economic History* 55.
10. Adrian, Crump & Moench (2013), "Pricing the Term Structure with Linear Regressions", *JFE* — the ACM term premium, series free from the NY Fed.
11. BIS, countercyclical-capital-buffer guidance (credit-to-GDP gap methodology); IMF (2016), "Assessing Reserve Adequacy — Specific Proposals" (the ARA metric behind `EXSOL`).
12. Data: IMF WEO & COFER · BIS `TOTAL_CREDIT` · FRED · NY Fed ACM · CBO *Budget & Economic Outlook 2026–2036* (Feb 2026) · WGC Goldhub and *Central Bank Gold Reserves Survey 2026* · RBI *India's External Debt*, WSS, Handbook of Statistics, Annual Report · MOSPI · NPCI · AMFI · UN WPP · MeasuringWorth (long-run gold and price levels) · Our World in Data.

*Every item marked [verify] must be confirmed against the primary source before this document is circulated.*
