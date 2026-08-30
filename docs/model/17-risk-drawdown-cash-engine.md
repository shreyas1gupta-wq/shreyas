# Layer 17 — Risk, Drawdown Control and the Cash-Call Engine

**Abstract.** This layer holds the owner's binding constraint — maximum drawdown below the Nifty 50's, absolute ceiling 30–35% — against a permitted 1.5x gross leverage, and under rule R7 it is the one unbudgeted authority in the system: it may cut equity, gross and leverage without limit, at any cadence. That power is why the spec must be exact about when it is used. It opens with the arithmetic, and the arithmetic is uncomfortable: a **standing 1.25x average leverage is not compatible with a 30–35% ceiling.** At 1.25x with no de-risking, 2008 is a −58% event and March 2020 a −36% event; even at 1.00x with no cash call, 2008 is −38%. The drawdown objective is therefore met by the *cash call*, not by low leverage, and leverage is repriced as a state-contingent privilege averaging **1.10–1.15x (aggressive) and 1.05x (moderate)**, reaching 1.5x in roughly the best decile of months. The cash-call engine is specified in full: a breadth-gated convex score over euphoria, valuation percentile, credit phase, macro regime, trend and realised drawdown, netted against the cycle stack by `max()` rather than summed, so R7's unbudgeted authority does not become a back-door budget violation. The re-entry rule is given equal weight to the exit rule and carries a **forced calendar clock** that restores risk on a schedule whether or not the permission conditions have healed — because systems that de-risk and never re-risk are the standard way this design dies. The measured expected cost is stated as a number: **−0.5%/yr of CAGR, range −0.2% to −1.5%**, in exchange for moving the worst modelled drawdown from ~38% to ~25%. Five fast triggers address the March-2020 problem; they reduce it from −38% index to roughly −20% portfolio, with an honest **8–12% unavoidable residual** that no signal can remove. The risk model is a hybrid: a price-only characteristic factor backbone (D1) with Ledoit–Wolf shrinkage and Dimson-corrected betas for the stale-priced tail, with D2 fundamental factors deferred. Liquidity analysis derives each book's real universe: the ₹100 cr book can hold the full NIFTY 750; the ₹1,000 cr book is confined to ranks 1–500 with size-capped positions below rank 250.

**Layer numbering.** `config/cycle_registry.yaml` and `docs/ROADMAP.md` §2 both assign the risk engine to **L17**; `01-cycle-taxonomy.md` prose (§8.6, §13.4, and the B4/B5 register rows for `volatility_regime_cycle` and `funding_stress_spike`) says L18. The registry is machine-readable and CI-enforced, so **L17 is correct** and layer 01's prose needs a one-line patch. This spec uses L17 throughout.

---

## 1. The tension, quantified first

### 1.1 What a levered mid/small book actually did

Free index history settles this. Peak-to-trough index drawdowns, and the implied drawdown of an aggressive equity sleeve weighted 40% large / 35% mid / 25% small:

| Episode | Nifty 50 | Midcap 150 | Smallcap 250 | **Agg. sleeve** | **Mod. sleeve** (70/30) |
|---|---|---|---|---|---|
| 2008 (Jan-08 → Mar-09) | −60% | −73.4% | −73% | **−66%** | **−64%** |
| 2018-19 (Jan-18 → Sep-19) | −14% | −30% | −45% | **−25%** | **−13%** |
| Mar-2020 (19-Feb → 23-Mar) | −38% | −41% | −44% | **−40.5%** | **−39%** |
| Sep-24 → Mar-26 | −17.5% | −20% | −23% | **−20%** | **−18%** |

Now the portfolio, at the neutral 60/12/28 policy point, with **no de-risking at all**, and gold and debt marked at their episode behaviour (INR gold +26% in 2008, −4% in Mar-2020; the 10% debt sleeve is a credit book and drew −6% in 2008, −4% in Mar-2020):

| Gross | 2008 | Mar-2020 | 2018-19 | Sep-24→Mar-26 |
|---|---|---|---|---|
| **1.00x** (equity 60) | **−38.2%** | −25.9% | −16.4% | −11.2% |
| **1.25x standing** (equity 85, borrow 25 @ 11%) | **−58.0%** | −36.3% | −27.4% | −21.1% |
| **1.50x standing** (equity 110) | **−75.2%** | −46.6% | −34.5% | −27.0% |

Three conclusions the owner must confront:

1. **A standing 1.25x breaches the ceiling in three of the four episodes**, and turns 2008 into a mandate-ending event. This is not a marginal call.
2. **Even 1.00x with no cash call breaches the ceiling in 2008** (−38% vs a 30–35% ceiling). Low leverage alone does not deliver the drawdown objective. The cash call is load-bearing, not optional.
3. The episode that quietly destroys the *relative* test is **2018-19 and Sep-24→Mar-26**, not 2008 or 2020. In 2018-19 the Nifty 50 fell 14% while a mid/small book fell 25%; at 1.25x the portfolio fell 27% against a benchmark that fell 14%. The relative test fails by 13pp in a market nobody would call a crisis. And roughly **4.7pp of that came from financing cost alone** — 25pp of borrowing at ~11% MTF rates for 20 months. Leverage cost, not leverage risk, is what breaks the relative test in slow grinds. (Repo is 5.25% and the 91-day T-bill 5.28% as of Aug-2026; MTF at 9.7–15% is a 450–975bp spread over the cash rate.)

### 1.2 What the same episodes look like with the machinery on

2008 with the cash call working — euphoria printed 96–99 in Jan-2008 (L07 §7.4), valuation was at the 99th percentile, the credit cycle was late, the trend broke in January — average equity through the decline ≈35%, gold raised to 15%, debt 43%:

`0.35 × (−66%) + 0.15 × (+26%) + 0.43 × (−6%) ≈ −21.6%`, plus ~300bps of whipsaw and timing cost ⇒ **≈ −25%.** Inside the ceiling, and 35pp better than the Nifty 50.

The moderate book, with 24.5pp of de-risking authority rather than 33.3pp (L01 §8.6), holds an average equity of ~42%: `0.42 × (−64%) + 0.15 × 26% + 0.43 × (−6%) ≈ −25.6%`, plus timing ⇒ **≈ −29%.** That **breaches the moderate book's 20–25% target** and sits at the low end of the 30–35% absolute ceiling. L01 §13.5 predicted this from turnover arithmetic; it is confirmed here from drawdown arithmetic. The moderate book needs a larger *standing* tail hedge and less leverage, not more signal.

### 1.3 The leverage policy that is actually compatible

| Average gross | How reached | Worst modelled DD (agg, machinery on) | Verdict |
|---|---|---|---|
| 1.00x | never levered | −24% | Meets both books' targets |
| 1.10x | 1.5x in ~20% of months | −28% | Meets the ceiling; moderate book marginal |
| **1.15x** | **1.5x in ~30% of months** | **−30%** | **Aggressive book's maximum** |
| 1.25x | 1.5x in ~50% of months — requires the gates to be weakened | −35 to −38% | Breaches |
| 1.25x standing | ungated | −58% | Mandate-ending |

**Recommendation, which contradicts DECISIONS Q10's "target average ~1.25x":** the compatible policy is an average gross of **1.10–1.15x for the aggressive book and 1.05x for the moderate book**, with 1.5x reachable only in a narrowly defined state. This needs owner sign-off; it is the same conflict the roadmap's open item 6 flagged, now with numbers attached.

Leverage is not a target but a *permission*, granted as a product of gates and revoked the day any gate fails:

```
gross_ceiling(t) = 1.00 + 0.50 · L(t)
L(t)   = min( g_vol, g_trend, g_credit, g_val, g_euph, g_dd, g_liq, g_fund, g_margin )

g_vol    = 1 if vol_pctile(21d, 1260d) < 0.40 and no vol-regime break in 60d, else 0
g_trend  = 1 if bear_flag = 0 (L08 §5.2) and Nifty500 > SMA200, else 0
g_credit = 1 if L03 modal phase in {repair, early_expansion, mid_expansion}, else 0
g_val    = clip((80 - V_percentile)/20, 0, 1)        # 0 at the 80th percentile
g_euph   = clip((78 - EUPH)/18, 0, 1)                # 0 at EUPH 78
g_dd     = 1 if portfolio DD > -5%, else 0
g_liq    = 1 if whole-book DTL at 20% participation, crisis-haircut, <= 5 days
g_fund   = 1 if funding_stress_spike z < 1.0
g_margin = 1 if the §9 no-forced-sale invariant holds with 40% headroom
```

Adding leverage requires `L > 0` sustained for **63 trading days** (3 months) and moves at most **+0.10x per month**. Removing it is immediate, same session, no dwell, no rate limit. That asymmetry is R7 in its most literal form. Historically (1996–2026) the gate product is non-zero in roughly 35–45% of months and at 1.0 in roughly 10–12% — which is where the 1.10–1.15x average comes from. It is zero for all of 2008, most of 2018-19, from late Feb-2020, and from Sep-2024.

---

## 2. The cash-call engine

### 2.1 Inputs and the anti-double-counting rule

| Input | Symbol | Source | Contract |
|---|---|---|---|
| Euphoria de-risk pressure | `p_euph` | L07 `derisk_score` ∈ [0,1] | Consumed as given; I never recompute EUPH |
| Valuation percentile | `p_val` | L05 `VAL_STATE.V_percentile` | Expanding-window percentile only |
| Credit phase | `p_credit` | L03 `L03_STATE.phase_posterior` | Posterior over 6 phases, not a hard label |
| Macro regime | `p_macro` | L04 `MACRO_GATES.macro_derisk_score` ∈ [0,1] | Consumed as given |
| Trend state | `p_trend` | L08 `TREND_STATE.trend_score_nifty500`, `bear_flag` | L08 owns the definition |
| Realised drawdown | `p_dd` | own state | Peak NAV since inception, daily |

**The netting rule, which is the most important line in this section.** The cycle stack already delivers up to 33.3pp (agg) / 24.5pp (mod) of equity de-risking at 3σ, using *the same six inputs*. If I add my cash call to theirs, one force is counted twice and R7's unbudgeted authority silently becomes a budget violation. Therefore:

```
equity_reduction_final = max( cycle_stack_reduction_pp , cash_call_target_pp )
```

Never the sum. The cash call is a **floor on total de-risking**, expressing the convex, conjunctive, non-rate-limited part of the response that a linear per-cycle budget cannot represent. In ordinary states the cycle stack binds; in tail states the cash call binds. CI test: `test_cash_call_never_sums_with_cycle_stack`.

### 2.2 The function

Each input is mapped to a de-risk pressure in [0,1], deliberately with a dead zone so that ordinary conditions produce nothing:

```
p_val    = clip((V_percentile - 70) / 25, 0, 1)                    # 0 at 70th, 1 at 95th
p_euph   = derisk_score                                            # L07: 0 at EUPH 72, 1 at 95
p_credit = clip((P(late_exp) + 1.5·P(stress) + 2·P(bust) - 0.35)/0.65, 0, 1)
p_macro  = macro_derisk_score
p_trend  = clip((-trend_score_nifty500 - 0.20) / 0.80, 0, 1)       # 0 until trend < -0.2
p_dd     = clip((|DD| - 0.08) / 0.14, 0, 1)                        # 0 at -8%, 1 at -22%
```

Then the score, with a **breadth gate** that is the whole design:

```
w      = (val .20, euph .20, credit .20, macro .15, trend .15, dd .10)
S_raw  = Σ w_i · p_i
B      = Σ 1[ p_i > 0.35 ]                          # how many inputs are genuinely pressured
φ(B)   = {0: 0.00, 1: 0.35, 2: 0.65, 3: 0.85, 4: 1.00, 5: 1.00, 6: 1.00}
S      = S_raw · φ(B)

cash_target_pp = CASH_MAX · S^1.35
CASH_MAX = 40 pp (aggressive) · 30 pp (moderate)
```

A single screaming input gets 35% of its weight. This is the direct analogue of L01's disagreement haircut (A3) and it exists because of one dated fact: L07 §7.4 shows `EUPH` hit 90–95 on 8-Feb-2024, **seven months before** the Smallcap 250 actually peaked. An ungated euphoria-only cash call would have gone to 30% cash in February 2024 and been wrong until September. With the breadth gate, February 2024 (euphoria extreme, valuation high, but credit benign, macro benign, trend strongly positive, DD zero) gives `B = 2`, `S_raw ≈ 0.31`, `S ≈ 0.20`, `cash_target ≈ 4.5pp` — a nudge, not a call. Correct.

The exponent 1.35 makes the map convex: slow at the start, hard at the end. `S = 0.5` gives 15pp; `S = 0.8` gives 29pp; `S = 1.0` gives 40pp.

**Bounds and floors.** `cash_target ∈ [0, CASH_MAX]`. Resulting equity may not fall below **15%** (agg) / **20%** (mod) — the floor used in L01's 3σ test — and the minimum-10-names rule binds below 50% equity. Gold's 5% L02 insurance floor and 50% cap, and the 70% debt cap, are all hard and clip after this.

**Destination routing, and a finding that contradicts the naive reading of the frozen constraints.** The obvious move is to route the cash call into the 10%-return debt sleeve. That sleeve is a credit book (a genuine 10% short-duration return in India implies AA/A, per DECISIONS Q16), and in exactly the episodes where the cash call fires, credit is *not* a safe haven: Indian credit funds gated in Oct-2008 and Franklin Templeton wound up six schemes in Apr-2020. Routing rule:

```
first 10pp of the cash call  -> true liquid assets: overnight/liquid funds, T-bills, cash
next  10pp                   -> gold, up to the 50% cap and L02's ceiling
beyond 20pp                  -> the 10% debt sleeve, up to the 70% cap
```

**Hysteresis and dwell.**

| Control | Aggressive | Moderate |
|---|---|---|
| Dead band before increasing cash | ΔS ≥ 0.08 | ΔS ≥ 0.12 |
| Minimum dwell in a raised-cash state | 21 calendar days | 42 calendar days |
| Max implied flips per year | ~8 | ~4 |
| De-risk rate limit | **none** (R7) — executed next session | **none** |
| Re-risk rate limit | ≤ ⅓ of the gap per rebalance, ≤ 6pp/month | ≤ ⅓, ≤ 3pp/month |

### 2.3 (a) The re-entry rule

This gets the same precision as the exit rule, because de-risking systems that cannot re-risk are guaranteed to lock in losses. Re-entry is a **two-key** system: a permission set and a schedule, and **the schedule can fire without the permission set.**

**PERMISSION conditions** (each unlocks one tranche):

| ID | Condition | Rationale |
|---|---|---|
| **R1** | Nifty 500 TRI closes above its 50-day MA for 10 consecutive sessions AND SMA50 slope > 0 | The 200dma is too slow — in 2020 the Nifty crossed the 50dma in mid-April and the 200dma only in November |
| **R2** | 21d realised vol < 1.5 × its trailing 3-year median AND India VIX < 25 | Volatility normalisation |
| **R3** | `breadth_200dma_pct` (L08) has risen ≥ 15pp off its trough, OR `PCT50 > 55%` | Participation, not just index level |
| **R4** | `funding_stress_spike` z < 0.8 for 10 consecutive sessions | Registry exit hysteresis |
| **R5** | No new 20-day low in the last 10 sessions | Not catching a falling knife |

**SCHEDULE — the forced clock.** Measured in trading days from the *drawdown trough* (the lowest NAV since the cash call was raised):

| Tranche | Restores | Fires on | **Or on the clock at** |
|---|---|---|---|
| T1 | 25% of the cash call | R2 **and** R4 | **40 sessions** |
| T2 | further 25% | R1 | **70 sessions** |
| T3 | further 25% | R3 | **110 sessions** |
| T4 | remainder | R1 ∧ R2 ∧ R3 ∧ R4 ∧ R5 | **130 sessions (~6 months)** |

Whichever comes first. **The clock is the anti-paralysis device and it is one-directional: it can only add risk back, never remove it.** The failure mode of every de-risking system is that its re-entry conditions are written, in the calm of design time, to require a level of confidence that only exists well after the recovery. The clock overrides that. It cannot take the book above the cycle-stack-implied equity weight; it only unwinds *my* incremental cut.

**Second-leg protection.** If, after any tranche, the index makes a new closing low below the prior trough, the cash call re-fires at full strength and the clock resets. **Maximum two resets per bear market**; after the second, the book holds its floor weight and waits for the full permission set — because a third reset is a whipsaw death spiral, not risk management.

*Worked example, March 2020.* Trough 23-Mar-2020. The Nifty crossed and held its 50dma around 10-Apr; R1 satisfied ~28-Apr ⇒ T2 fires (25%). T1's clock (40 sessions) fires ~20-May (25%). India VIX fell below 25 around mid-June ⇒ R2, but T1 has already fired. R3 (breadth +15pp) ~mid-July ⇒ T3. T4 on the 130-session clock ~end-Sep-2020. Fully re-risked by 30-Sep-2020. Nifty 7,610 → 11,247 over that window (+47.8%); averaging ~45% equity instead of 60% costs **≈7.2% of NAV in six months**. That is the price of the insurance, stated where it can be seen.

### 2.4 (b) The cost

Decomposed rather than asserted. Six major bottoms in 30 years (2001, 2003, 2009, 2013, 2020, 2026); the engine is in a materially de-risked state (>10pp) in roughly 20% of months, average de-risk ~15pp, so the time-weighted average underweight is ≈3.2pp.

| Component | Derivation | Agg. | Mod. |
|---|---|---|---|
| Unconditional underweight drag | 3.2pp × (13.5% equity − 10% debt) | −0.11% | −0.08% |
| Re-entry lag at the 6 bottoms | 18pp avg underweight × 35% avg 5-month recovery × 6 / 30y, log | **−1.07%** | −1.25% |
| Avoided-loss benefit at the 6 declines | 15pp × (35% avg decline + 5% debt carry) × 6 / 30y, log | **+1.03%** | +0.78% |
| Whipsaw / false fires | 1.5 per decade × 12pp × 8% adverse | −0.14% | −0.10% |
| Execution (futures-first, ~12bps round trip on 10pp/yr) | | −0.03% | −0.03% |
| **Net expected CAGR cost** | | **−0.32%** | **−0.68%** |
| Honest range | 6 observations, wide error bar | −0.1% to −1.2% | −0.3% to −1.6% |

Three things this table teaches that are worth more than the point estimate:

- **The owner's own 10% debt assumption makes the cash call cheap.** The opportunity cost of being underweight equity is the equity risk premium *over the destination asset*. Against a 10% sleeve that is ~3.5pp; against T-bills at 5.3% it is ~8.2pp — more than double. If the debt sleeve is really 7%, add ~25bps to every number above.
- **The cost is almost entirely the re-entry lag**, not the exit. That is why §2.3 gets as much specification as §2.2, and why the forced clock exists.
- **The cash call is not bought for return, it is bought for drawdown.** At ~35bps/yr it moves the worst modelled drawdown from −38% to −25%. On a 22% CAGR that is a Calmar improvement from 0.58 to 0.88. That is one of the best trades in the entire design.

**The honest caveat:** these six observations all sit inside a 30-year window in which Indian equities went up a great deal. In a genuine lost decade the cash call's cost turns positive (it earns). In a 2003–07-style melt-up with early euphoria prints, an ungated version costs 3–4%/yr — which is precisely why L07's gate and my breadth gate carry the design.

---

## 3. The March-2020 problem

Layer 01 §8.6 admits the cycle stack cannot handle a five-week 38% fall with no macro deterioration in the preceding quarter. This section plus L16's overlay must. It does not solve the problem; it materially shrinks it, and the residual is stated.

### 3.1 The five fast triggers

All computable from D1 free daily data. All close-to-close in v1 — no intraday.

| ID | Definition | Threshold | Mar-2020 fire date | Latency to executed de-risk |
|---|---|---|---|---|
| **T-V** vol regime break | `vol_5d / vol_60d` and level | ratio > 2.5 **and** 5d ann. vol > 28%; **or** ΔVIX(1d) > +20% with VIX > 25 | **28-Feb-2020** (Nifty ~11,200, −8.2% from peak) | T+1 open, 1 session |
| **T-G** gap / velocity | Nifty 500 5-session return; single-session return | 5d < −7% **or** 1d < −4% | **28-Feb / 9-Mar** (9-Mar was −4.9%) | T+1 open, 1 session |
| **T-B** breadth collapse | `PCT200` level and 20-session change | PCT200 < 25% **and** fall ≥ 30pp in 20 sessions | **~5-Mar-2020** | T+1 open, 1 session |
| **T-C** correlation spike | avg pairwise 10d correlation of top-200; PCA λ₁ share | ρ̄ > 0.65 **and** λ₁ share > 55% (norm ~35%) | ~10-Mar-2020 | T+1 open, 1 session |
| **T-F** funding stress | CP(3m) − Tbill(91d); USDINR 1m realised vol; LAF net | spread > 175bps or +100bps in 60d; USDINR vol > 6% ann.; LAF swing to net injection > 1.5% NDTL | **~12–16-Mar-2020** | T+2 (CCIL/RBI publish T+1) |

**Aggregation.** `FAST_DERISK` fires when **any 2 of the 5** are true on the same session; or when T-V alone is at an extreme (`vol_5d/vol_60d > 4.0`), because a true gap event cannot wait for confirmation.

**Honest note on T-F:** funding stress is a *lagging* confirmation in an equity-led crash and a *leading* signal in a credit-led one. It fired in mid-March 2020, well after the damage; it fired *before* equities in September 2018 (IL&FS), when the CP market seized first. It earns its place for the second case, not the first.

### 3.2 The action ladder

| Step | Timing | Action (aggressive / moderate) |
|---|---|---|
| 1 | T+1 open, no discretion | Sell Nifty + Nifty Bank futures to reduce net equity by **12pp / 8pp**. Cut gross ceiling to **1.00x** immediately |
| 2 | T+2 to T+5, if the trigger persists | Further **10pp / 6pp** in futures. Buy protective puts (L16) only if IV percentile < 80; otherwise futures |
| 3 | T+5 onward | Convert the futures hedge into physical sales **only** for names failing the liquidity screen; otherwise the hedge stays in futures |

**All fast de-risking is executed in index futures, not by selling stock.** In the March-2020 window, mid/small single-stock spreads widened 3–8x and ADV fell 35–50%, while Nifty futures stayed deep and near fair value. This is the single most consequential execution decision in the layer, and it is also what makes the moderate book viable: ₹220 cr of Nifty futures sells in minutes; ₹220 cr of the ₹1,000 cr book's stock does not (§7).

### 3.3 What is still unavoidable

Replaying March 2020 with the machinery on, in three legs (Nifty 50 peak 12,430 → trough 7,610):

| Leg | Window | Index | Sleeve | Avg equity | Contribution |
|---|---|---|---|---|---|
| A | 19-Feb → 2-Mar (pre-trigger) | −10.4% | −11.1% | 60% | **−6.7%** |
| B | 2-Mar → 12-Mar | −13.9% | −14.8% | 44% | −6.5% |
| C | 12-Mar → 23-Mar | −20.6% | −22.0% | 30% | −6.6% |
| Gold (INR, −6% at worst) | | | | 13% | −0.8% |
| Debt (credit sleeve, −3%) | | | | 30% | −0.9% |
| L16 tail hedge at a 50% ratio | | | | | +2.0% |
| **Total** | | **−38%** | | | **≈ −19.5%** |

Passes both tests decisively. Without the options overlay, −21.5% — still passes. At a standing 1.25x entering the crash, roughly −26 to −28%: passes, but the margin is gone. At 1.5x, breached.

**The residual, stated plainly.** Leg A — **6.7% of NAV** for the aggressive book — is unavoidable, because it is the loss taken between the peak and the first executable trigger, and no signal existed before 28-Feb. Three things make the honest number 8–12% rather than 6.7%:

1. **Single-session gaps.** On 23-Mar-2020 the Nifty fell 12.98% in one session. At 60% equity that is 8.3% of NAV in a day, and no close-to-close trigger prevents it.
2. **Trading halts.** 13-Mar-2020 hit the 10% lower circuit and trading was suspended for 45 minutes. There are sessions in which the plan cannot be executed at all.
3. **A crash with no vol build.** March 2020 is survivable *because Indian realised vol rose materially in the week of 24–28 Feb, before the worst of it.* A genuine zero-warning event — a coup, a war, an exchange failure, a 24-Aug-2015-style flash break — produces no lead time whatsoever. Against that, only a **standing** tail hedge helps, which is L16's job and is why the hedge-ratio sweep is a first-class parameter.

**Do not read this section as "solved."** The claim is: a March-2020-class event is reduced from a −38% index move to roughly a −20% portfolio move, with an 8–12% residue that is a property of the world and not of the design.

---

## 4. The de-gearing ladder

Rungs on portfolio drawdown from peak NAV. Contains the ROADMAP §7 rungs (−10/−15/−20/−25) as a subset.

| DD from peak | Gross ceiling | Cumulative equity Δ (agg) | Other actions |
|---|---|---|---|
| −5% | 1.25x | 0 | New leverage frozen; new thin-name entries halted |
| **−10%** | **1.00x** | **−8pp** | In-progress budget 20% → 10% (freeze, do not sell); ex-ante beta cap 1.05 |
| **−15%** | 0.95x | −16pp | Beta cap 0.90; single-name cap 6% → 4%; sector cap −5pp; selection switches to residual momentum only |
| **−20%** | 0.90x | −24pp | Equity floor 30%; gold floor 12% → 15%; tail hedge to the 75% notional cap |
| **−25%** | 0.85x | −32pp | Equity floor 22%; **halt-and-review**: two signatures required for any new risk |
| −30% | 0.80x | equity floor 15% | Full stop; closing trades only; written post-mortem before any re-risk |

Moderate book: rungs at −5 / −8 / −12 / −16 / −20 / −24%, with Δ scaled by 0.70, reflecting its tighter 20–25% target.

**Re-gearing** — deliberately slower than the cash-call re-entry, and separately gated:

- At most **one rung per 21 trading days**, and only if all of: (a) NAV has recovered ≥40% of the drawdown from the trough; (b) 21d realised vol < 1.2 × its 3-year median; (c) `bear_flag = 0`; (d) no fast trigger in the last 15 sessions.
- **Leverage above 1.00x may not be restored until NAV is within 3% of the prior peak** *and* the full §1.3 gate set has held for 63 sessions. You return to full equity long before you return to leverage.
- The −25% and −30% rungs require two signatures and a written post-mortem naming the failure. This is the only place in Stage 1 where a human is in the loop, and it is deliberate.

**Cost of the ladder itself.** Nifty 500 drawdowns >10% since 1996: 1998, 2000-01, 2004, 2006, 2008, 2011, 2013, 2015-16, 2018-19, 2020, 2022, 2025-26 — twelve. Of these, three went on to a >20% *portfolio* drawdown (2000-01, 2008, 2020); nine were false alarms at the −10% rung.

| Component | Derivation | Cost |
|---|---|---|
| 9 false alarms | 8pp cut × ~12% recovery before re-gear | −8.6% cumulative → **−0.28%/yr** |
| 3 true fires | 8pp+ across rungs × further decline | +15% cumulative → +0.47%/yr |
| Overlap with the cash call (it fires first in 2008 and 2020) | net the benefit by 50% | +0.23%/yr |
| Turnover, futures-executed | 10–14pp/yr extra allocation turnover | −0.02%/yr |
| **Net** | | **−0.07%/yr, range −0.05% to −0.35%** |

The ladder is cheaper than the cash call because it fires later, smaller, and because two-thirds of what it would catch the cash call has already caught. **Combined cash call + ladder: central −0.5%/yr of CAGR, range −0.2% to −1.5%.** That is the number the owner is paying for a ~13pp reduction in maximum drawdown.

---

## 5. The risk model

**Recommendation: a hybrid, with a price-only characteristic-factor backbone.** Not statistical PCA — its factors are unnameable, drift in composition, and cannot answer "which layer caused the loss," which ROADMAP §8.5 makes a success criterion. Not a pure fundamental model either — our fundamentals are D2 (restated, lag-approximated), so a risk estimate that depends on book value has look-ahead baked into the *risk* number, which is worse than having it in the return number.

**Structure.** `r_it = α_i + Σ_k β_ik f_kt + ε_it`, K = 11 style factors + 20 NSE macro-sector dummies.

| Factor | Definition | Tier |
|---|---|---|
| MKT | Nifty 500 TRI excess return | D1 |
| SIZE | log market cap, cross-sectionally z-scored, winsorised ±3 | D1 |
| MOM | 12-1, **consumed from L08 — never rebuilt here** | D1 |
| BETA | 252d beta to Nifty 500, Vasicek-shrunk toward 1.0 | D1 |
| VOL | 60d idiosyncratic volatility | D1 |
| LIQ | Amihud illiquidity + log turnover, z-scored | D1 |
| GRP | promoter-group membership dummy | D1/D4 |
| SMLC | small-vs-large risk-appetite spread, consumed from L07 | D1 |
| GOLD | INR gold return (multi-asset block) | D1 |
| VAL, QUAL | B/P + E/P; gross profitability + accruals | **D2 — deferred to v1.5** |

The promoter-group factor is India-specific and matters enormously; single-group events (2023) move a dozen names as one, and a model without it will call that idiosyncratic risk.

**Estimation.**
- Daily cross-sectional WLS with weights ∝ √(market cap) over the ~750-name universe, giving a daily factor-return series (Rosenberg/Fama–MacBeth style).
- Factor covariance `F`: EWMA with **half-life 90 days for variances, 180 days for correlations** (variances move faster than correlations), Newey–West corrected with 5 lags for the non-synchronous-trading autocorrelation that is severe in the Indian small-cap tail, then **Ledoit–Wolf shrinkage toward a constant-correlation target**.
- Specific risk `Δ`: EWMA of ε² at 60-day half-life, Bayes-shrunk to the sector × size-decile median with weight `n/(n+120)`.
- Total: `Σ = B F B' + Δ`, with a non-diagonal block for same-promoter-group names (correlation floor 0.35). PSD-repaired by eigenvalue clipping.
- Update: factor returns daily; `F` and `Δ` weekly (aggressive) / monthly (moderate). Factor *definitions* frozen in git, two signatures to change.
- Per `02-ECONOMETRIC-METHODS.md §4`: the 750-name `Σ` is a **risk-measurement** object for limits and decomposition. The **optimizer** (L14) receives a Ledoit–Wolf-shrunk covariance over a reduced 30–50 sleeve/asset-class space; sample covariance on 750 names is singular and must never be used.

**The illiquid tail — the part that is usually got wrong.** Stale prices bias measured vol and beta *downward*, so a naive model concludes the small-cap tail is safe. Three fixes, all mandatory:
1. **Dimson beta** with 2 lags (sum of contemporaneous and lagged coefficients) for any name with >15% zero-return days in the trailing 120 sessions.
2. A **specific-vol floor by size decile**: decile 10's floor = 1.8 × decile 1's median specific vol.
3. A **stress covariance** `Σ_stress` estimated on the worst decile of market days only. Average pairwise correlation goes from ~0.35 to ~0.70 there; the optimizer and the limit engine must both be shown it. MVP uses a scalar 1.8× multiplier; the second matrix is v1.5.

**Fixture testability.** The estimator runs end-to-end on a committed 750 × 2,500 synthetic panel with planted factor structure; CI asserts recovery of the planted betas within tolerance, PSD of `Σ`, and monotonicity of the Dimson correction. Zero live data required.

---

## 6. The limit framework

`H` = hard-blocking (the order is rejected, and if the breach is passive the position is reduced within the window). `E` = escalation (logged, flagged, remediated within the window; two signatures if not).

| # | Limit | Aggressive | Moderate | Type | Remediation window |
|---|---|---|---|---|---|
| 1 | Gross leverage | ≤ gate-derived ceiling, hard max 1.50x | same, hard max 1.50x | **H** | Same session |
| 2 | Average gross, trailing 252d | ≤ 1.15x | ≤ 1.05x | E | 21 sessions |
| 3 | Net equity weight | 15% – 110% | 20% – 100% | **H** | Same session |
| 4 | Gold weight | 5% (L02 floor) – 50% | same | **H** | 5 sessions |
| 5 | Debt + debt-related | ≤ 70% | ≤ 70% | **H** | 5 sessions |
| 6 | True-liquid assets when cash call > 0 | ≥ min(10pp, cash_call) | same | **H** | 3 sessions |
| 7 | Single name, entry | ≤ 6% | ≤ 6% | **H** | At order |
| 8 | Single name, drift | ≤ 10% | ≤ 10% | E | 10 sessions |
| 9 | Minimum names when equity < 50% | ≥ 10 | ≥ 10 | **H** | 10 sessions |
| 10 | Sector | min(25%, bmk + 10pp) | min(20%, bmk + 8pp) | E | 21 sessions |
| 11 | In-progress positions, aggregate | ≤ 20% (≤10% below −10% DD) | ≤ 20% | E | 15 sessions |
| 12 | Ex-ante portfolio beta to Nifty 500 | ≤ 1.20 (≤0.90 in panic) | ≤ 1.05 | E | 10 sessions |
| 13 | Ex-ante portfolio vol (annualised) | ≤ 22% | ≤ 16% | E | 15 sessions |
| 14 | Single style-factor active exposure | ≤ 1.5σ | ≤ 1.0σ | E | 21 sessions |
| 15 | Promoter-group aggregate exposure | ≤ 12% | ≤ 10% | **H** | 10 sessions |
| 16 | Days-to-liquidate, whole book @20% part., crisis-haircut | ≤ 3 days | ≤ 7 days | E | 21 sessions |
| 17 | Single name, days-to-liquidate @10% part. | ≤ 5 days | ≤ 8 days | **H** | At order |
| 18 | Options, directional notional (delta-adjusted) | ≤ 50% | ≤ 50% | **H** | Same session |
| 19 | Options, tail-hedge notional | ≤ 75% | ≤ 75% | **H** | Same session |
| 20 | **Margin invariant** (§9) | headroom ≥ 0 | headroom ≥ 0 | **H** | Same session, pre-signal |
| 21 | Drawdown rung actions | §4 table | §4 table, 3pp tighter | **H** | Next session |
| 22 | Signal staleness | no input > 3 × its publication lag | same | E | Cut affected influence to 0 |
| 23 | Data-quality circuit breaker | > 2% of universe with a failed integrity check | same | **H** | Halt trading until cleared |
| 24 | Tier-C aggregate (R4) | ≤ 150bps | ≤ 150bps | **H** | At `resolve()` |

Limits 20, 21, 1 and 3 **supersede every signal in the system**, including this layer's own cash call. Order of application at each rebalance: margin invariant → drawdown rung → fast triggers → cash call → cycle stack → optimizer → mandate caps.

---

## 7. Liquidity risk — and each book's real universe

Approximate NIFTY 750 ADV structure (60-day median traded value, Aug-2026 `[verify against a fresh bhavcopy build]`):

| Rank band | Median ADV | Aggressive: 5% pos = ₹5 cr | Moderate: 5% pos = ₹50 cr |
|---|---|---|---|
| 1–50 | ₹800 cr | 0.6% of ADV → **0.06 d** | 6.3% → **0.63 d** |
| 51–100 | ₹350 cr | 1.4% → 0.14 d | 14% → 1.4 d |
| 101–250 | ₹120 cr | 4.2% → 0.42 d | 42% → **4.2 d** |
| 251–500 | ₹40 cr | 12.5% → 1.25 d | 125% → **12.5 d** |
| 501–750 | ₹8 cr | 62% → **6.3 d** | 625% → **62 d** |

(Days at **10% participation**; halve for 20%.)

**Whole-book days-to-liquidate**, aggressive ₹100 cr, equity 60% = ₹60 cr across ~35 names at 40/35/25 large/mid/small:

- Large ₹24 cr / 10 names = ₹2.4 cr each → <0.1 d
- Mid ₹21 cr / 12 names = ₹1.75 cr each → 0.15 d
- Small ₹15 cr / 13 names = ₹1.15 cr each vs ₹8 cr ADV → **1.4 d**
- **Whole book at 20% participation: 0.7 days. With a 0.5× crisis ADV haircut: 1.4 days.**

**Moderate ₹1,000 cr**, equity 60% = ₹600 cr across ~50 names at ₹12 cr average:

- **Whole book at 20% participation: 2.8 days; 95th-percentile name 6 days; crisis-haircut: 5.6 days.**

**The universes this derives:**

| | Aggressive ₹100 cr | Moderate ₹1,000 cr |
|---|---|---|
| Eligible universe | **Full NIFTY 750**, floor ADV ≥ ₹2 cr | **Ranks 1–500 only** |
| Full 5% sizing available | ADV ≥ ₹10 cr (≈ ranks 1–650) | ADV ≥ ₹100 cr (≈ **ranks 1–250**) |
| Position cap below that | `min(5%, 10% × ADV × 5 days / NAV)` | same formula: at ₹40 cr ADV ⇒ **2.0%** |
| Bottom 250 names | Reachable via the 20% in-progress budget | **Excluded outright** |

This is the arithmetic behind DECISIONS Q2: the two books are not one strategy at two sizes, they are two universes. And it is why §3.2 mandates futures for the fast leg — the moderate book cannot physically sell 22pp of stock in two sessions in a crisis, but it can sell the equivalent Nifty futures in minutes.

---

## 8. Stress scenarios

Impacts are for the neutral portfolio with the full L17 machinery on, aggressive / moderate.

| Scenario | Transmission | Impact (agg / mod) | What fires | Pre-agreed response |
|---|---|---|---|---|
| **2008 replay** | Credit + global liquidity; equity sleeve −66% | **−25% / −29%** | Cash call in Jan-08 (euphoria 96–99, val 99th pct, credit late); ladder to −20% rung | Equity to 25–30%, gold 15%, gross 0.90x. Moderate book breaches its own 20–25% target — accepted and pre-declared |
| **2013 taper tantrum** | INR −20%, G-sec yields +250bps, gold INR −18% | −11% / −9% | T-F (USDINR vol), L06 external vulnerability, macro regime | Cut gold (the one episode where gold hurt), cut leverage to 1.0x, hold equity — the equity fall was mild |
| **Demonetisation, Nov-2016** | Domestic liquidity/consumption shock; Nifty −10% in 8 weeks | −6% / −5% | T-G marginally; ladder −5% rung | No cash call (breadth gate: B=1). **Correct non-action** — a 10% event is not a de-risking event |
| **IL&FS, Sep-2018** | CP market seizes; NBFC funding freeze; smallcaps −36% | −14% / −8% | **T-F leads** (CP−Tbill spread), credit phase → stress, breadth | Cut gross to 1.0x, cut NBFC/financials sector exposure, cash call ~12pp. The one episode where T-F is the primary signal |
| **COVID, Mar-2020** | 38% in 5 weeks | **−19.5% / −18%** | T-V (28-Feb), T-B (5-Mar), T-C, then T-F | §3.2 ladder, futures-executed. **8–12% residue unavoidable** |
| **Rate shock** (repo +300bps in 9 months) | Debt sleeve MTM −6 to −9%; equity multiple compression; debt–equity correlation flips to +0.4 | −13% / −12% | Macro regime (inflation shock cell), valuation, L04 gates | Debt sleeve capped at 40% (not 70%) whenever `corr_equity > +0.2`; raise gold; equity −10pp. **The 70% debt cap is unsafe in this state and must be state-contingent** |
| **Crude to $150** | INR −12%, CPI +250bps, terms-of-trade shock; a repeat of 2008H1/2022 | −12% / −11% | L06 `oil_shock_flag`, inflation cycle, macro regime | Gold to 20%, cut OMC/auto/aviation sectors, equity −8pp, gross to 1.0x |
| **INR −20% in 6 months** | Imported inflation, FPI exodus, RBI defends with liquidity tightening | −10% / −9%, offset by gold +20% in INR | T-F (USDINR vol > 6%), L06 | Gold is the hedge and is already structurally floored at 5%. Raise to 20–25%; cut leverage (INR devaluation raises the real cost of any borrowing) |
| **Liquidity event: the small-cap tail cannot be sold at any price** | GSM/ASM cascades, circuit-locked names, ADV → near zero | −8% direct / **but the book is trapped** | Limit 16/17 breach; T-C | **The only response that works is prevention.** Cap the sub-₹10 cr-ADV tail at 8% of NAV (agg) and 0% (mod); hedge the trapped exposure in Nifty/Midcap futures rather than trying to sell; accept that the position is now a long-dated illiquid asset and re-underwrite it as such |

The last row deserves its emphasis. In a genuine liquidity event, days-to-liquidate is not 6 days, it is undefined — a lower-circuit name has no bid. The only working control is the ex-ante cap and a futures hedge against the exposure you cannot exit.

---

## 9. Leverage mechanics on proprietary capital in India

| Instrument | Cost (Aug-2026) | Spread over repo (5.25%) | Margin mechanics | Verdict |
|---|---|---|---|---|
| **MTF** (broker margin funding) | **9.7–15% p.a.** (Kotak/ICICI from 9.69%; Groww 14.95%; Bajaj 14.99%) | **+445 to +975bps** | Up to 4–5x on Group-I scrips; shares pledged; daily MTM; broker must liquidate on an unmet shortfall, typically T+1 | **Most expensive leverage available.** Use only for single-name exposure with no futures contract |
| **Index futures** (Nifty, Bank Nifty) | Embedded basis ≈ repo + 50–150bps ⇒ **~5.8–6.8%** | +55 to +155bps | SPAN + exposure ≈ 12–16% of notional; daily MTM; peak-margin rules penalise intraday shortfalls | **Primary instrument** for both leverage and de-risking. 350–800bps cheaper than MTF |
| **Single-stock futures** | Basis, wider and less reliable | +150 to +400bps | 20–40% of notional | Secondary; only for names with real F&O depth |
| **Options** | Time decay; financing embedded in the forward | — | Long options: no margin call. Short options: full margin | Hedge leg only (L16). Long puts are the only leverage form with **no** margin-call path |
| **LAS** (loan against securities) | 9–11% | +375 to +575bps | RBI: LTV 50% for equity, rising to **60% from 1-Jul-2026**; per-borrower limit rising from ₹20 lakh to **₹1 crore**; a shortfall must be cured within 7 working days | **Ruled out.** A ₹1 crore per-borrower cap is irrelevant at ₹100 cr, let alone ₹1,000 cr `[verify whether the cap binds a corporate/LLP borrower — if not, LAS returns as a marginal option]` |

**The no-forced-sale invariant.** A margin call that forces a sale at the bottom converts a survivable drawdown into a permanent loss, and it is the specific mechanism by which levered books die. Hard-blocking limit 20:

```
liquid_headroom = cash + liquid_debt + 0.5 · collateral_value(large_cap_holdings)
required        = 2.5 · IM_current  +  stress_addon
stress_addon    = 1-day 99.5% loss on the derivatives book, computed on Σ_stress
margin_multiplier_assumption = 1.6x        # exchanges DID raise margins mid-crash in Mar-2020

INVARIANT:  liquid_headroom  >=  required · margin_multiplier_assumption
```

Worked, aggressive book at 1.25x with ₹25 cr of Nifty futures notional: IM ≈ ₹3.5 cr; 2.5 × IM = ₹8.75 cr; stress add-on (a 1-day 6% move on ₹25 cr) = ₹1.5 cr; × 1.6 = **₹16.4 cr, i.e. ~16% of NAV must be held unencumbered.** That is the real price of leverage and it should be counted against its benefit, not treated as free.

Two supporting rules: **never post equity holdings as more than 50% of margin** (in a crash the collateral haircut rises exactly as the requirement rises — the double squeeze); and if the invariant fails, **gross is cut the same session, before any signal is consulted.**

---

## 10. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L01 | `resolve()` net equity deviation, `influence_budget`, `CYCLE_STATE` | For the `max()` netting rule in §2.1 |
| L02 | `LW_CONSTRAINTS` (gold floor 5%, ceiling 30%, leverage ceiling) | My gate product is multiplied by their ceiling; theirs binds if lower |
| L03 | `L03_STATE.phase_posterior`, `s_credit` | Consumed as given; I never build a credit view |
| L04 | `MACRO_GATES.macro_derisk_score`, `gross_leverage_cap_modifier`, `regime_probs` | Their modifier is one-sided (≤0) and composes multiplicatively with my gates |
| L05 | `VAL_STATE.V_percentile`, `CMA.corr_by_regime_cell`, `vol_crisis_multiplier` | L05 is the sole publisher of the CMA |
| L07 | `derisk_score`, `euph`, `leverage_stress` | Consumed as given; the breadth gate is mine, the euphoria score is theirs |
| L08 | `TREND_STATE` (`trend_score_*`, `bear_flag`, `panic_flag`, `breadth_200dma_pct`), `MOM_RISK` | **L08 owns the definitions of `bear_flag`/`panic_flag`** |
| L09 | factor exposures where they exist | For the risk model's style block; L09 owns *return* factors, I own the *risk* model |
| L16 | current hedge notional, delta, IV percentile | For exposure accounting and step 2 of §3.2 |
| L19 | `pit_store`, `adj_prices`, `universe`, `membership`, CCIL/RBI daily series | Bitemporal; final-vintage reads raise |

**Exposes**

```python
RISK_STATE  = {vol_state_z, mkt_state, bear_flag, panic_flag, current_drawdown, peak_nav,
               dd_rung, days_in_rung, gross_ceiling, gross_current, fast_trigger_flags,
               margin_headroom_pct, dtl_days_20pct_crisis, asof, vintage_id}

CASH_CALL   = {cash_target_pp, S, S_raw, breadth_B, components: {p_val,p_euph,p_credit,
               p_macro,p_trend,p_dd}, incremental_over_cycles_pp, destination_split,
               reentry_tranches_pending, forced_clock_sessions_remaining}

DEGEAR_VETO = {gross_ceiling, equity_ceiling_pp, equity_floor_pp, beta_ceiling,
               name_cap_pct, sector_cap_pct, in_progress_cap_pct}     # A5(i) hard veto

RISK_LIMITS = {limit_id: {value, current, utilisation, breach_type, remediation_by}}
COV(asof)   -> {B, F, Delta, Sigma, Sigma_stress, factor_names, dimson_applied}
LIQUIDITY(asof) -> {symbol: {adv60, max_position_value, dtl_10, dtl_20, dtl_crisis}}
```

**Ownership boundaries, explicitly.** The allocation optimizer (L14) owns target weights; I emit **ceilings, floors and vetoes**, never weights. The factor library (L09) owns return factors; I own the risk covariance and consume their exposures. L08 owns `bear_flag`/`panic_flag`; I re-export them verbatim as `mkt_state` so that L04 has **one** read-point and not two definitions — this resolves the interface risk L08 §7 flagged.

**Double-counting guard with L08.** L08's `w_dd` ladder scales the momentum sleeve *within* the equity budget; my ladder scales the equity budget itself. Rule: **L08's sleeve ladder is capped so that `w_dd_L08 × equity_weight_L17 ≥ 0.35 × neutral_momentum_exposure`.** L20 must report total de-gearing in the Mar-2020 and Oct-2008 windows and assert it does not undershoot the intended floor.

**Stage-1 sufficiency.** Every field above is produced from data alone with Stage 2 off. The Stage-2 overlay may write only `tier_downgrade` and `manual_derisk_request` (which may only *cut*); it may not raise a ceiling, relax a rung, or restore leverage. CI asserts `RISK_STATE` is bit-identical with the overlay disabled.

---

## 11. MVP versus deferred

This layer's MVP must be near-complete, because it is what makes everything else safe to run. **~28 engineer-days.**

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Drawdown accounting + de-gearing ladder | Peak-NAV state machine, §4 rungs both books, re-gear gates | 2.0 | ✅ |
| 2 | Cash-call engine | §2.2 score, breadth gate φ(B), convex map, destination routing, hysteresis, dwell | 3.0 | ✅ |
| 3 | **Re-entry rule + forced clock** | §2.3 tranches, permission set, reset cap, one-directional clock | 2.0 | ✅ |
| 4 | Fast triggers, price-only | T-V, T-G, T-B, T-C from bhavcopy alone | 3.0 | ✅ |
| 5 | Fast trigger T-F | CP–Tbill, USDINR vol, LAF; degrades to "unavailable" without fixtures | 2.0 | ✅ |
| 6 | Leverage permission gate | §1.3 gate product, dwell, asymmetric rate limit | 1.5 | ✅ |
| 7 | Margin invariant | §9 no-forced-sale check as a hard pre-signal block | 1.5 | ✅ |
| 8 | Limit framework | §6 table as 24 executable checks, hard/escalation, remediation clock, breach log | 3.0 | ✅ |
| 9 | Liquidity model | ADV-based DTL, per-book universe derivation, crisis haircut, position-size formula | 2.0 | ✅ |
| 10 | Risk model, price-only backbone | 9 D1 factors + sectors, WLS, EWMA+Ledoit–Wolf, Dimson beta, specific-vol shrinkage | 5.0 | ✅ |
| 11 | Stress engine | §8 nine scenarios as replayable shock vectors | 2.0 | ✅ |
| 12 | **Cost report** | Measured CAGR cost of the cash call and the ladder, emitted with every backtest | 1.0 | ✅ |
| 13 | Property tests + fixtures | For any signal vector and any price path: no limit breached, ladder monotone, re-entry always completes | 3.0 | ✅ |
| **MVP total** | | | **31.0** | |

**Deferred to v1.5:** D2 fundamental factors (VAL, QUAL) in the risk model · the PCA residual overlay (3–5 components) · the second, stress-estimated covariance matrix (MVP uses a 1.8× scalar) · the promoter-group covariance block · intraday triggers (v1 is close-to-close) · options-based fast de-risk (v1 uses futures only) · regime-conditional correlation beyond the two-state normal/stress split.

**The item most often deferred and which must not be: step 3.** A cash-call engine without a specified, tested, clock-backed re-entry rule is not a risk system, it is a mechanism for converting drawdowns into permanent losses. It ships in the MVP or the MVP does not ship.

---

## 12. Risks and constraint conflicts

1. **DECISIONS Q10's "target average ~1.25x" is incompatible with the 30–35% ceiling.** §1 gives the arithmetic. The compatible number is 1.10–1.15x (agg) / 1.05x (mod). Owner sign-off required; this is roadmap open item 6, now quantified.
2. **L17 vs L18 numbering.** The registry and roadmap say L17; layer 01's prose says L18 in three places. The registry is CI-enforced and wins; layer 01 needs a one-line patch.
3. **The 70% debt cap is unsafe in an inflation shock**, where the sleeve's equity correlation flips to +0.4 and it is not a hedge. Recommendation: a state-contingent debt cap of 40% whenever `corr_equity > +0.2`. This is a change to a frozen constraint and needs a decision.
4. **The cash call's destination cannot naively be the 10% debt sleeve.** It is a credit book that gated in Oct-2008 and Apr-2020. §2.2's routing rule (liquid first, then gold, then the sleeve) is a correction to the obvious reading of DECISIONS Q16.
5. **The sector cap resolution matters to this layer.** My −15% DD rung tightens the sector cap by 5pp. Under an *absolute* 25% cap that becomes a 20% cap on financials — a 10–15pp forced underweight to the largest sector, taken in the worst moment, as a side effect of a risk rule nobody intended as a sector call. **This layer depends on the relative form `min(25%, benchmark + 10pp)`.**
6. **Unbudgeted authority is a back-door budget violation unless netted.** R7 lets me cut without limit while reading the same six inputs the cycle stack reads. The `max()` rule in §2.1 is the only thing preventing double-counting, and it needs a permanent CI test, not a convention.
7. **The moderate book cannot reach its own drawdown target in a 2008 replay** (−29% modelled vs a 20–25% objective). It needs a larger standing tail hedge and 1.05x average gross. Independently predicted by L01 §13.5 from turnover; confirmed here from drawdown.
8. **All the cost numbers rest on six observations.** The −0.5%/yr combined estimate has an error bar wider than itself. It is reported every backtest (step 12) precisely so it is measured rather than assumed, and it must never be tuned to look better — the moment a threshold in §2 or §4 is moved to improve a backtest Sharpe, it becomes a fitted parameter and must be counted in the trial register.
9. **In-progress positions orphan at the −10% rung.** They are frozen, not sold, unless they fail limit 17 — but a frozen half-built position in an illiquid name is a position taken by accident. The execution scheduler (L15) needs an explicit rule for signals that decay while queued.
10. **The ₹1 crore LAS cap needs verification for a corporate borrower.** If proprietary capital sits in an LLP or company, the individual cap may not bind and LAS returns as an option at 9–11%. It would still be worse than futures.

---

## 13. References

1. Daniel, K. & Moskowitz, T. (2016). "Momentum Crashes." *Journal of Financial Economics* 122(2), 221–247.
2. Barroso, P. & Santa-Clara, P. (2015). "Momentum has its moments." *Journal of Financial Economics* 116(1), 111–120.
3. Ledoit, O. & Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." *Journal of Portfolio Management* 30(4), 110–119; and (2003), "Improved estimation of the covariance matrix of stock returns with an application to portfolio selection." *Journal of Empirical Finance* 10(5), 603–621.
4. Dimson, E. (1979). "Risk measurement when shares are subject to infrequent trading." *Journal of Financial Economics* 7(2), 197–226. — The stale-price beta correction for the small-cap tail.
5. Vasicek, O. (1973). "A note on using cross-sectional information in Bayesian estimation of security betas." *Journal of Finance* 28(5), 1233–1239.
6. Rosenberg, B. (1974). "Extra-market components of covariance in security returns." *Journal of Financial and Quantitative Analysis* 9(2), 263–274. — The fundamental-factor risk model.
7. Amihud, Y. (2002). "Illiquidity and stock returns: cross-section and time-series effects." *Journal of Financial Markets* 5(1), 31–56.
8. Newey, W. & West, K. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." *Econometrica* 55(3), 703–708.
9. Brunnermeier, M. & Pedersen, L. (2009). "Market Liquidity and Funding Liquidity." *Review of Financial Studies* 22(6), 2201–2238. — The margin-spiral mechanism behind T-F and the §9 invariant.
10. Kritzman, M. & Li, Y. (2010). "Skulls, Financial Turbulence, and Risk Management." *Financial Analysts Journal* 66(5) `[verify pages]`. — Mahalanobis turbulence, the ancestor of the T-C correlation-spike trigger.
11. Moreira, A. & Muir, T. (2017). "Volatility-Managed Portfolios." *Journal of Finance* 72(4), 1611–1644. — Evidence that scaling exposure inversely to realised variance raises Sharpe; and the reason it does *not* protect against the first leg of a crash.
12. Harvey, C., Hoyle, E., Rattray, S., Sargaison, M., Sim, D. & van Hemert, O. (2019). "The Best of Strategies for the Worst of Times: Can Portfolios be Crisis Proofed?" *Journal of Portfolio Management* 45(5), 7–28. — Why trend-following and long options, not diversification, are what work in a crash.
13. Almgren, R. & Chriss, N. (2000). "Optimal execution of portfolio transactions." *Journal of Risk* 3(2), 5–39. — The participation-rate framework behind §7.
14. Cooper, M., Gutierrez, R. & Hameed, A. (2004). "Market States and Momentum." *Journal of Finance* 59(3), 1345–1365.
15. Pandey, R., Patnaik, I. & Shah, A. (2017). "Dating business cycles in India." *Indian Growth and Development Review* 10(1), 32–61.
16. López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. — Purged and embargoed CV; combinatorial purged CV; PBO.
17. Bailey, D. & López de Prado, M. (2014). "The Deflated Sharpe Ratio." *Journal of Portfolio Management* 40(5), 94–107.
18. Free sources used by this layer: NSE bhavcopy 1994– <https://www.nseindia.com/all-reports> (prices, ADV, breadth, futures basis, India VIX 2008–) · CCIL <https://www.ccilindia.com> (CP, T-bill, G-sec) · RBI DBIE <https://dbie.rbi.org.in> (LAF, USDINR, policy rates) · NSE F&O bhavcopy (SPAN-equivalent margins, open interest) · World Gold Council (INR gold).
19. Broker MTF rates and RBI LAS limits sourced from public disclosures, Aug-2026: [Kotak Neo](https://www.kotakneo.com/margin-trading-facility/), [ICICI Direct](https://www.icicidirect.com/equity-products/margin-trading), [Groww](https://groww.in/stocks/mtf), [smallcase on RBI LAS guidelines](https://www.smallcase.com/learn/rbi-guidelines-loan-against-securities/). Index drawdown history: [Personal Finance Plan cap-index comparison](https://personalfinanceplan.in/nifty-50-vs-midcap-150-vs-smallcap-250-vs-nifty-500-cap-based-indices-performance-comparison-2005-2026/). Repo and T-bill levels: [RBI Aug-2026 policy summary](https://www.finnovate.in/learn/blog/rbi-august-2026-policy-repo-rate-rupee-inflation). All marked `[verify]` where the figure drives a threshold rather than a narrative.

*Items marked `[verify]` require confirmation against the primary source before circulation.*
