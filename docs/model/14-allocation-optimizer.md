# Layer 14 — Stage 3: The Allocation and Optimisation Engine

**Abstract.** This layer turns seventeen active cycle signals, five capital-market assumptions and roughly seven hundred name scores into two portfolios. Its central decision is architectural rather than mathematical: **the asset-class mix is not optimised, it is composed**, and only the cross-section inside the equity sleeve is solved by a quadratic program. That split is forced by arithmetic, not taste. Fed L05's frozen capital-market assumptions, a naive mean-variance optimiser puts **70.0% in debt at every risk aversion from λ=2 to λ=40, and 0.0% in gold**; inverse-volatility risk parity independently lands on **67.3% debt**; and — the fact that settles it — the corner portfolio *also* beats the 60/12/28 policy portfolio on modelled drawdown (−15.6% vs −24.2% in a March-2020 replay). No risk measure, no correlation regime and no constraint short of a hard weight bound rejects it. The 60/12/28 policy point is therefore not a risk decision; it is a declaration that the frozen 10% debt return is not believed, and reverse-optimisation prices the disbelief exactly: **the policy portfolio embeds a −396 bps/yr haircut to debt and a +315 bps/yr uplift to gold**. That number is stated, not hidden. Everything else follows: registry influence caps are consumed literally as pp deviations from the policy point; slow buckets move a smoothed centre and fast buckets a bounded deviation, with per-bucket EWMA half-lives set at `tau_half/12` so Stage 3 adds at most 12% of `tau_half` in phase lag; rate limits are enforced by a *smooth → clip → slew* ordering that is provably non-violating; and the two books differ in eleven named parameters, of which the turnover penalty turns out to be the least important — at the registry's current budgets the aggressive book runs at **39% of its 500%/yr turnover ceiling** and the moderate book at **41% of 100%/yr**, so both are influence-constrained, not turnover-constrained. Four defects in the frozen contract are flagged with fixes: an inverted sign convention on `leverage_x`, a book-independent `rate_limit` that is 2–4× too loose for the moderate book, a sector-cap formula that does not solve the problem it names, and a no-trade band expressed in pp when the two books' score→weight gains differ by 5.7×.

---

## 0. Scope, and a numbering note

I own: signal aggregation into weights, the constraint set and its projection, covariance, turnover control, the Stage-2 entry point, and the two-book parameterisation. I do **not** own: the cash-call / de-gearing ladder and the fast vol and funding triggers (L17), the execution scheduler and tranching (L15), the options overlay and hedge-ratio sweep (L16), the factor library (L09), or any signal.

*Numbering.* This spec uses the **ROADMAP §2 / registry numbering**, which the machine-readable registry follows (`owner_layer: L17` for `volatility_regime_cycle`). `01-cycle-taxonomy.md` §8.6 uses an older scheme in which "L14" means the options overlay and "L18" the risk engine. Where L01 says "the options overlay (L14)" it means **L16** here. Flagged rather than silently reconciled.

---

## 1. Signal aggregation: evaluating and choosing

### 1.1 The five candidates, scored against this problem

| Scheme | What it would do | Why it fails or survives here |
|---|---|---|
| **Mean–variance with shrunk Σ and L05 μ** | Solve for equity/gold/debt from the CMA | **Fails at the asset level.** Corners into the 70% debt cap at every λ (§3.1). It also cannot consume a pp influence cap — the registry's primary currency. **Survives inside the equity sleeve**, where n is large and evidence is tier A |
| **Black–Litterman, cycles as views, confidence as Ω** | Blend an equilibrium prior with cycle views | **Fails at the asset level for three reasons.** (i) The prior is reverse-optimised from the market or from a "neutral" portfolio; reverse-optimising anything that contains the frozen debt sleeve reintroduces the free lunch through the back door. (ii) BL has no way to express a *hard* pp cap — the registry's caps are bounds, and BL produces unbounded posteriors. (iii) Calibrating τ and Ω honestly requires a sample; at `n_eff < 8` for every B0–B2 cycle the calibration is unfalsifiable. **Survives as the Stage-2 view channel** (§8), where views are few, explicit, and bounded by an L1 cap |
| **Risk-parity core plus cycle tilts** | Equal risk contribution, then tilt | **Fails.** Inverse-vol on σ = (17%, 16%, 4%) gives 15.8 / 16.8 / **67.3%**; true ERC gives 16.7 / 15.6 / **67.7%**. It is the same corner in different clothing — vol-based rather than Sharpe-based — and it is *worse*, because it corners without even consulting expected returns |
| **Hierarchical scorecard with bucket budgets** | Additive pp deviations from a policy point, bounded per cycle and per bucket | **Survives, and is recommended for the asset level.** It consumes `influence.*_pp` literally, is exactly what L01 §9 (A1–A7) already specifies, is auditable line by line, and cannot corner because its reachable set is bounded by construction |
| **Ensemble of the above** | Average two or more | **Rejected.** Averaging a degenerate allocator with a sound one produces a less-degenerate wrong answer and destroys attribution. When the book loses 8% you must be able to say which line caused it; an ensemble weight is not a line |

### 1.2 Recommendation — a two-block engine

> **Block A — the allocation ladder.** Asset-class weights (equity, gold, debt, cash) and the gross envelope. A deterministic, bounded, additive scorecard over the policy portfolio. **No objective function. Nothing maximises anything.**
>
> **Block B — the cross-sectional program.** Name weights inside the equity sleeve, whose total is *given* by Block A. A convex QP with expected active return, a factor-model covariance, an explicit cost term and the full constraint set.

The boundary between the blocks is the debt-free-lunch firewall. Block B never sees the debt sleeve, the gold sleeve, or a Sharpe ratio for anything but equities relative to equities. Block A never sees a covariance matrix except for reporting.

This is not a compromise; it is the only formulation consistent with the evidence tiers. Block A's inputs have `n_eff` between 2 and 7, and mean-variance sensitivity to μ scales with Σ⁻¹ (Best & Grauer 1991) — exactly what a three-asset, two-observation problem cannot estimate. Block B's inputs are tier A with thousands of stock-months, where optimisation earns its keep and where constraints themselves act as shrinkage (Jagannathan & Ma 2003).

### 1.3 Block A formulation

Contract with the registry, stated precisely because it is the most likely place to introduce a silent bug:

```
NEUTRAL   n = {equity: 60.0, gold: 12.0, debt: 28.0, cash: 0.0}      # pp of NAV
For each active cycle i and target T in {equity, gold, debt}:

  u_i   = clip( (R_i,t / R_i,0) · sqrt(rv_i,t / rv_i,0) · psi_i(z_i) , −1, +1 )
  x_iT  = S[i][T] · u_i
  c_iT  = cap_iT[up] · x_iT           if x_iT > 0
        = −cap_iT[dn] · |x_iT|        if x_iT < 0
```

- `psi_i` is the registry's `gain.mapping_fn` (linear / cos / logistic / table), normalised to [−1, +1].
- **The tier multiplier is NOT applied here.** `config/cycle_registry.yaml` states that budgets are already "AFTER tier multipliers and phase attenuation", and R4 confirms it: the single active tier-C cycle, `monetary_order_debasement`, has an allocation L1 of exactly 1.50pp = the 150bps aggregate cap. Re-applying ×0.30 in Stage 3 would double-count. **CI assertion: the Stage-3 config contains no tier multiplier table.**
- Attenuation *ratios* are applied, because `R` is time-varying (a trigger slide inflates σ_c per L01 §7.3) while the cap is static. `R_i,0` is the inception attenuation stored in the registry; `state` cycles carry `R = 1` in both slots.
- `S[i][T]` is a **sign matrix** that Stage 3 publishes, because the registry does not contain a consistent one (§12.2). With `z` defined as risk-favourability (L01 `SIGN_CONVENTION`):

  | Target | Sign | Exceptions |
  |---|---|---|
  | equity | **+1** | none |
  | gold | **−1** | none — risk-off always raises gold, whether the source is debasement, inflation or stress |
  | debt | **−1** | **+1** for `monetary_order_debasement` and `inflation_cycle` — these are the two states in which risk-off is *bad* for a nominal credit sleeve. This is the correlation flip encoded as structure rather than as a covariance entry |

Aggregation then follows L01 §9 verbatim: bucket sums → the A2 slow gate → the A3 disagreement haircut → the §6.4 cluster cap → A6 no-trade band → budget closure (§2.4) → projection (§4).

**A3, implemented.** L01 specifies the haircut for contributions "two or more rungs apart" without saying how to aggregate. Stage 3 uses the two-block reduction: `C` = Σ(B0,B1,B2), `Dv` = Σ(B3,B4,B5),

```
D          = 1 − |C + Dv| / (|C| + |Dv|)
net_final  = (C + Dv) · (1 − 0.35·D)
```

which reproduces L01's own worked example exactly: `c = (−5, +8)` → `D = 0.769`, `net = 2.19 pp`.

### 1.4 Block B formulation

Over name weights `w` inside an equity sleeve of size `E` (from Block A), against benchmark `w_b` renormalised to `E`:

```
max_w   alpha' w
        − (lambda_A / 2) · (w − w_b)' Sigma (w − w_b)      # active risk
        − sum_j [ c_j · |w_j − w_j^0| ]                     # linear cost -> no-trade band
        − (gamma / 2) · sum_j (w_j − w_j^0)^2               # quadratic penalty -> partial adjustment
s.t.    the constraint set of §4
```

`alpha` is the composite name score expressed in **expected annualised active return**, supplied by L08/L09/L10/L11/L12 and rescaled by Stage 3 so that its L1 weight footprint equals the registry's `name_l1_pp` budget at full signal. `lambda_A` is active risk aversion, calibrated so ex-ante tracking error lands at 8% (aggressive) / 5% (moderate). Both cost terms are needed and they do different jobs: the **linear** term creates the no-trade region (a KKT inequality, not a heuristic); the **quadratic** term makes the adjustment partial rather than bang-bang, which is the Gârleanu–Pedersen (2013) result in one-period form.

### 1.5 When Block B misbehaves, and the fallback

Convex QPs on 750 names fail in specific, detectable ways. The trigger conditions and the response:

| Trigger | Threshold | Action |
|---|---|---|
| Solver non-convergence or infeasibility | any | Relax constraints in reverse priority order (§4.4) until feasible; log every relaxation |
| Covariance conditioning | κ(Σ) > 500 after shrinkage | Raise shrinkage intensity by 0.10 and re-solve; if still failing, fall back |
| Ex-ante vs realised vol bias | 60-day bias ratio outside [0.85, 1.20] for 3 consecutive months | Fall back and open a data-quality ticket |
| Solution instability | ‖w_t − w_t(Σ perturbed by 1%)‖₁ > 5pp | Fall back |
| Effective breadth collapse | Σw² implies < 12 effective names | Fall back |

**The fallback is score-tilted inverse-volatility weighting**, closed-form, no matrix inversion:

```
w_j  ∝  (1 + kappa · s_j) / sigma_j        # kappa = 0.5, s_j the standardised score
then iterate the cap projection of §4 to convergence (max 20 passes)
```

This is deliberately the scheme L08 already uses for its own sleeve, so the fallback is a *tested* code path rather than a dead branch — and with estimation error this large it is not embarrassing (DeMiguel, Garlappi & Uppal 2009): the naive scheme is competitive and its worst case is bounded.

---

## 2. Horizon-aware blending

### 2.1 Centre and deviation

```
CENTRE     c_t   = neutral + EWMA_slow( contributions from B0, B1, B2 )
DEVIATION  d_t   =            EWMA_fast( contributions from B3, B4, B5 )
w_t              = Project( c_t + d_t )
```

The split is not decoration: the A2 gate acts across the boundary (a strong risk-off centre scales the deviation's *upside* by `(1 − 0.5|s|)`, floored at 0.50, and never its downside), and only the deviation carries a hard bound.

**Deviation bounds**, derived from the fast buckets' own registry caps as `min(Σb, 3·√(0.33·Σb²))` — the `min` matters, because with only two or three contributing buckets the 3σ expression exceeds the hard linear bound (§12 risk 6):

| Book | Equity dev | Gold dev | Debt dev | (3σ expression, for comparison) |
|---|---|---|---|---|
| Aggressive | **±18.0 pp** | **−2.5 / +8.0 pp** | **±13.0 pp** | 23.1 / 3.6–10.9 / 18.0 |
| Moderate | **±11.0 pp** | **−2.0 / +5.0 pp** | **±7.0 pp** | 15.9 / 3.4–8.6 / 12.1 |

The centre absorbs whatever is left: at the aggressive book's 3σ equity de-risking of 30.4pp, at most 18.0pp can come from the fast buckets and the remaining 12.4pp must come from B0–B2, which by construction cannot arrive in a single quarter.

### 2.2 The smoothing constants, tied to `tau_half`

The signal layers already smooth at `w = tau_half/3` (L01 §7.4). Stage 3 must not re-smooth at the same scale or the effective lag compounds. It therefore applies **one** first-order low-pass per bucket with half-life `tau_half/12` — one quarter of the signal-layer window, so the added lag is a declared minority of the total:

```
alpha_b = 1 − 2^(−12 / tau_half_b)
```

| Bucket | `tau_half` (rep.) | Stage-3 half-life | `alpha_b` | EWMA mean lag | Lag as % of `tau_half` |
|---|---|---|---|---|---|
| B0 | 120 m | 10.00 m | 0.0670 | 13.93 m | 11.6% |
| B1 | 84 m | 7.00 m | 0.0943 | 9.61 m | 11.4% |
| B2 | 42 m | 3.50 m | 0.1797 | 4.57 m | 10.9% |
| B3 | 15 m | 1.25 m | 0.4257 | 1.35 m | 9.0% |
| B4 | 6 m | 0.50 m | 0.7500 | 0.33 m | 5.6% |
| B5 | 1.5 m | 0.125 m | 0.9961 | 0.004 m | 0.3% |

The lag fraction is ~11% for the slow buckets and falls monotonically toward zero for the fast ones — the correct direction, and it falls out of the formula rather than being tuned in. Nothing here is a free parameter: the only choice is the divisor 12, and it is justified by the requirement that Stage-3 lag be ≤ ⅓ of signal-layer lag.

### 2.3 Rate-limit composition — order matters, and it is provable

A naive EWMA does **not** respect a rate limit. For `india_credit_financial_cycle` (`b` = 6pp, `α_B2` = 0.18), a single month can move the contribution by 0.18 × 12 = 2.16 pp against a `max_delta_pp_per_month` of 0.125 — a 17× violation. The fix is ordering:

```
1.  target_i,t   = cap-mapped contribution (§1.3)                    # raw
2.  smooth_i,t   = (1 − alpha_b)·smooth_i,t−1 + alpha_b·target_i,t   # SMOOTH
3.  clip_i,t     = clip(smooth_i,t, −cap_dn, +cap_up)                # CLIP
4.  c_i,t        = c_i,t−1 + clip( clip_i,t − c_i,t−1, ±rho_i )      # SLEW  <-- last
```

Because the slew limiter is applied **last and per cycle**, `|Δc_i,t| ≤ ρ_i` holds by construction for every cycle at every rebalance, and by summation `Σ_i |Δc_i,t| ≤ Σ_i ρ_i`. That is the proof; there is nothing to test empirically. Smoothing before clipping (rather than after) means the smoother reduces the amount of slew the limiter has to absorb, so the limiter rarely binds and the signal is not systematically lagged by it.

**Exemptions, stated once.** Rate limits govern *signal-driven* moves only. Constraint repair (a cap breach must be fixed now, not over six months), L17 de-gearing, and L16 hedge adjustments are exempt. This is rule R7 in operational form.

### 2.4 The book-specific slew fix — a defect in the frozen contract

`rate_limit.max_delta_pp_per_month` is stored **once per cycle**, not per book, while `influence` is stored per book with the moderate caps 25–75% smaller. The limiter is therefore 2–4× looser relative to budget for the moderate book. `intermediate_momentum_12_1` carries `max_delta = 2.5 pp/month` against a moderate `equity_pp` cap of 1.0pp — it can traverse its entire moderate range twice in a single month, which is exactly the behaviour the ₹1,000cr book's turnover cap exists to prevent.

**Fix (Stage 3 owns it, no registry change required):**

```
rho_net_i(book) = min( registry.rate_limit.max_delta_pp_per_month ,
                       2 · b_max_i(book) / max(2·tau_half_i , min_traverse_by_tier_i) )
rho_L1_i(book)  = 4 · rho_net_i(book)          # L01 §8.5's own 4x offsetting allowance
```

re-deriving L01 §8.5 with the book's own budget. `rho_net` bounds the move of any single target; `rho_L1` bounds the total across targets. Worked: `intermediate_momentum_12_1` aggressive has `b_max` = 3.0pp and `min_traverse` = 12m, so `rho_net` = min(2.500, 0.500) = **0.500 pp/month** — the registry value is 5× too loose even for the aggressive book. Summed over the budgeted cycles:

| Book | Σρ_net | Σρ_L1 | Hard one-way turnover ceiling (6·Σρ_L1) | OU-expected turnover | Binding? |
|---|---|---|---|---|---|
| Aggressive | 2.11 pp/mo | 8.43 pp/mo | **50.6 pp/yr** | 49.3 pp/yr | No — 3% headroom |
| Moderate | 1.18 pp/mo | 4.70 pp/mo | **28.2 pp/yr** | 32.1 pp/yr | **Yes — binds 12% tight** |

Two independently derived quantities — L01's OU turnover formula and L01's rate-limiter formula, which share no algebra — agree to within **3%** for the aggressive book. That is a genuine internal-consistency result for the frozen contract and worth recording. The moderate book's realised allocation turnover will be **28.2 pp/yr, not 32.1**, because the limiter binds before the budget does; its name-selection residual is therefore **71.8 pp/yr**.

### 2.5 Budget closure

Asset-class deviations must sum to zero. Gross exposure is a **separate, explicitly budgeted decision** and is never an accidental by-product of three independent tilts.

```
Rule C1.  If sum(delta) != 0, scale the same-signed deviations that create the residual
          by kappa = |sum of opposite-signed| / |sum of same-signed|, so sum(delta) = 0.
Rule C2.  gross_ceiling = clip(1.50 + sum_i lev_i , 0.50 , 1.50)
Rule C3.  gross_target  = 1.00 + clip(kappa_G · s_riskon , 0 , gross_ceiling − 1.00)
          kappa_G = 0.35 (aggressive) / 0.20 (moderate)
          GATED on ALL of: valuation percentile <= 65, vol_state_z <= +1.0,
          mkt_state in {bull, neutral}, current_drawdown <= 10%, gross_ceiling >= 1.10
Rule C4.  Leverage is applied to the EQUITY sleeve only. Borrowing to fund the debt or
          gold sleeve is PROHIBITED. (Financing at ~7.5% into a 10%/4%-vol sleeve is a
          250 bps carry at Sharpe 0.63 on borrowed money, scalable without limit. It is
          the debt free lunch re-entering as a balance-sheet trade.)
```

---

## 3. The debt free-lunch problem

Inputs, from L05 §6.6, frozen: equity_large 10.8% / 17%; equity_smid 7.5% / 24%; gold 4.0% / 16%; debt 10.0% / 4%; cash 6.0% / 1%. Mandate caps: debt ≤ 70%, gold ≤ 50%, long-only, fully invested.

### 3.1 The corner, demonstrated

| λ | Equity L | Equity S | Gold | **Debt** | Cash | E[R] | Vol | Sharpe |
|---|---|---|---|---|---|---|---|---|
| 1 | 32.3% | 0.0% | 0.0% | 67.7% | 0.0% | 10.26% | 5.87% | 0.73 |
| 2 | 30.0% | 0.0% | 0.0% | **70.0%** | 0.0% | 10.24% | 5.57% | 0.76 |
| 5 | 30.0% | 0.0% | 0.0% | **70.0%** | 0.0% | 10.24% | 5.57% | 0.76 |
| 12 | 15.7% | 0.0% | 0.0% | **70.0%** | 14.3% | 9.56% | 3.70% | 0.96 |
| 40 | 6.0% | 0.0% | 0.0% | 68.8% | 25.1% | 9.04% | 2.90% | 1.05 |

Debt is at or within 2pp of its cap at **every** risk aversion over a 40× range. Gold is **zero everywhere**, which additionally violates L02's 5% structural insurance floor and the 12% policy weight. Mid/small-cap is zero everywhere, which deletes the entire NIFTY 750 tail the aggressive book exists to reach.

### 3.2 Risk parity corners too, and so does the stressed variant

Inverse-volatility on (17%, 16%, 4%): **15.8 / 16.8 / 67.3**. True equal-risk-contribution: **16.7 / 15.6 / 67.7**. With L05's `debt_stressed` (8.6% at 6.5% vol, grounded in IL&FS, DHFL and the April-2020 Franklin Templeton wind-up), MVO at λ=5 still returns **30.0 / 0.0 / 70.0**. Softening the assumption does not fix it; it only moves the λ at which the cap starts to bind.

### 3.3 No risk measure fixes it — the point that settles the architecture

The natural rescue is "optimise drawdown, not variance, since drawdown is the binding mandate constraint." Replay a March-2020-style shock (equity −38%, INR gold +2%, debt at its frozen −6% worst drawdown):

| Portfolio | Frozen debt (−6% DD) | Stressed debt (−14% DD, gold −8%) |
|---|---|---|
| Policy 60 / 12 / 28 | **−24.2%** | **−27.7%** |
| MVO corner 30 / 0 / 70 | **−15.6%** | **−21.2%** |

**The corner wins on drawdown as well as on return, volatility and Sharpe simultaneously.** Under the frozen inputs it dominates the policy portfolio on every metric a risk model can compute. There is therefore no objective function, no risk measure and no coherent risk constraint that will reject it. Only a hard weight bound will, and a hard weight bound is a *policy*, not a model.

### 3.4 The fix, and its price

**The fix is that Block A has no objective function.** The reachable set is `neutral ± registry caps`, and the caps are set by evidence, not by Sharpe. From the registry's own numbers (budgeted cycles, 3σ aggregation):

| Book | Max debt reachable | Cap | Min equity | Max gold | Min gold | L02 floor |
|---|---|---|---|---|---|---|
| Aggressive | 28 + 26.75 = **54.8%** | 70% | 60 − 30.40 = **29.6%** | 12 + 16.72 = **28.7%** | 12 − 5.70 = **6.3%** | 5% ✓ |
| Moderate | 28 + 20.75 = **48.8%** | 70% | 60 − 22.55 = **37.5%** | 12 + 15.33 = **27.3%** | 12 − 5.63 = **6.4%** | 5% ✓ |

At three standard deviations of simultaneous signal agreement, the engine cannot reach the debt cap: it stops 15.2pp short (aggressive) and 21.2pp short (moderate). **The corner is unreachable, not forbidden.** The 70% cap is never the operative constraint, which is exactly the property L01 §8.1 was protecting and which registry.py's `_check_three_sigma` already enforces in CI.

*(These are ~9% tighter than the bucket-budget figures quoted in the brief — 30.4pp vs 33.3pp of equity de-risking — because the 17 registry entries do not fully consume their bucket budgets. Both numbers are correct at their own level of aggregation; Stage 3 uses the registry's.)*

**The price, priced.** Reverse-optimising the policy portfolio (Grinold's implied-returns identity `π = λΣw`) at the λ that makes the implied large-cap equity return equal L05's 10.8% CMA gives λ* = 2.773 and:

| Asset | Frozen CMA | Implied by 60/12/28 | **Difference** |
|---|---|---|---|
| Equity large | 10.80% | 10.80% | 0.00 |
| Equity smid | 7.50% | 11.88% | **+4.38 pp** |
| Gold | 4.00% | 7.15% | **+3.15 pp** |
| **Debt** | **10.00%** | **6.04%** | **−3.96 pp** |
| Cash | 6.00% | 6.01% | +0.01 |

**Holding the policy portfolio is exactly equivalent to marking the debt sleeve down by 396 bps/yr and marking gold up by 315 bps/yr.** That is a large, unhedged, deliberate override of a frozen owner input, and it must appear in the monthly report as a line item rather than being buried in a constraint. It is defensible — 6.04% is close to a realistic government-plus-spread short-duration return, and 7.15% for gold is close to a no-real-return assumption plus INR drift — but it is an assumption, and the model should say so out loud every month.

**CI assertion.** `assert implied_returns(policy, Sigma, lambda_star)['debt'] < CMA['debt']['mu']` — if a future covariance update ever makes the policy portfolio *consistent* with the frozen debt return, the firewall has silently dissolved and the test fails.

### 3.5 What the correlation flip actually does

Running MVO in each of L05's regime cells:

| Cell | ρ(Eq,Debt) | MVO equity | MVO gold | **MVO debt** | Vol of fixed 60/12/28 |
|---|---|---|---|---|---|
| Disinflation + growth up | −0.20 | 30.0% | 0.0% | **70.0%** | 10.07% |
| Disinflation + growth down | −0.35 | 30.0% | 0.0% | **70.0%** | 10.02% |
| Inflation shock + growth up | +0.25 | 30.0% | 0.0% | **70.0%** | 10.99% |
| Stagflation | **+0.40** | 30.0% | 0.0% | **70.0%** | 11.39% |
| Crisis overlay (vol ×1.8) | +0.35 | 16.9% | 1.7% | **70.0%** | 20.34% |

**The −0.20 → +0.40 flip changes the optimal debt weight by exactly zero pp**, because the cap binds in every cell. The entire regime-conditional correlation apparatus L05 built is informationally inert at the asset-class level under a mean-variance formulation: the constraint, not the model, is choosing the portfolio. This is the strongest available argument that the free-lunch problem is not a nuisance to be constrained away but a formulation error.

Where the flip **does** bite, and where Stage 3 therefore routes it:

1. **Portfolio volatility of the fixed policy point** rises from 10.02% (disinflation, growth down) to 11.39% (stagflation) — **+13.7%** — and to 20.34% in the crisis overlay, **+103%**. That is a risk-report and risk-engine input (L17's vol targeting and de-gear ladder), not an allocation input.
2. **The debt sign flip in the S matrix** (§1.3): `inflation_cycle` and `monetary_order_debasement` alone carry `S_debt = +1`. So in a stagflation reading, the cycle stack cuts *both* equity and debt and routes to gold and cash — structurally, without consulting a covariance matrix, and therefore without the corner. In the worked example (§9) this is visible: `inflation_cycle` at u = −0.50 contributes **−1.50pp to debt** while every other risk-off cycle adds to it.
3. **Block B's covariance** uses the regime-mixed correlation for the equity block only.

---

## 4. The frozen constraint set, implemented

### 4.1 Entry cap and drift cap are different constraints at different times

They are not two numbers in one box; they are a **ratchet**. Per rebalance, for name *j* with post-market-move weight `w_j^drift`:

```
U_j =  min( 10.0% , max( 6.0% , w_j^drift ) )        # upper bound this period
L_j =  0

MANDATORY TRIM   if w_j^drift > 10.0%:  w_j must be <= 10.0%.  Rate-limit exempt,
                 executed at the next liquidity window, overrides the signal even if
                 the score is at its maximum.
NO-ADD ZONE      if 6.0% <= w_j^drift <= 10.0%:  w_j <= w_j^drift.  Hold, never buy.
NORMAL           if w_j^drift < 6.0%:  w_j <= 6.0%.
MIN POSITION     0 < w_j < m_book  is infeasible: round to 0 or up to m_book.
                 m_book = 0.40% (aggressive) / 0.60% (moderate).
```

**Flagged conflict.** DECISIONS.md Q12 states an "ideal entry band 3–6%", which implies a 10–20 name book. The systematic sleeve carries 45–55 names at ~1.2% average. The 3% minimum **cannot** apply to systematic positions without deleting the factor sleeve. Stage 3 assumes the 3–6% band scopes to **conviction positions only** (L11 bottom-up, L12 special situations), with a separate systematic minimum `m_book`. This needs owner confirmation; if the 3% minimum is global, the name count collapses to ~20 and the factor library's capacity assumptions must be rebuilt.

### 4.2 The sector cap — the open issue, resolved with arithmetic

L01 risk #6 recommends `min(25%, benchmark + 10pp)`. **That formula does not solve the problem it names.** Financials are ~32% of the Nifty 500 [verify current]; `min(25, 42) = 25`, which is still a forced 7pp underweight. The intended semantics require `max`, not `min`.

The deeper ambiguity Stage 3 must settle: **25% of NAV, or 25% of the equity sleeve?** They behave completely differently:

| Equity, % of NAV | 25%-of-NAV cap, as % of sleeve | Max financials active vs 32% bench |
|---|---|---|
| 40% | 62.5% | +30.5 pp |
| 60% | 41.7% | **+9.7 pp** |
| 75% | 33.3% | **+1.3 pp** |
| 100% (levered) | 25.0% | **−7.0 pp** |

A NAV-denominated cap binds *only when equity is high*, which is precisely when concentration risk is greatest — the right behaviour for a risk limit, but it also means that at 1.25× gross with equity at 75% of NAV the cap allows only **+1.3pp** of active financials and the sector model becomes decorative.

**Recommendation — two caps, both live, whichever binds:**

```
RISK CAP      sector_weight_NAV   <=  25%  (aggressive)  /  20%  (moderate)
ACTIVE CAP    |sector_w_sleeve − benchmark_w|  <=  10pp  (aggressive)  /  8pp  (moderate)
```

This eliminates the permanent forced underweight (the active cap is relative, so a 32%-weight sector may be held at benchmark at any equity level) while preserving a genuine concentration limit that tightens as the book gears up. **This layer depends on the resolution**; if the owner insists on a flat 25%-of-sleeve absolute cap, the sector model's authority must be re-derived and L10's budget cut.

### 4.3 Projection versus penalty — the rule

| Constraint | Mechanism | Why |
|---|---|---|
| Debt ≤70%, gold ≤50%, gold ≥5% (L02), gross ≤1.5×, options notional ≤50%/75% | **Projection.** Hard box, enforced after the solve | Mandate limits. A penalty admits violation for a price; there is no price |
| Name entry 6% / drift 10%, min position | **Projection** (box with the §4.1 ratchet), inside the QP as bounds | Convex; free to enforce exactly |
| Sector caps | **QP linear constraints** | Convex; exact |
| Min 10 names when equity < 50% | **Post-solve repair**, cardinality | Non-convex. Repair: if `n < 10`, admit the highest-scoring excluded names at `m_book` until `n = 10`, funded pro-rata. Binds only in a deep de-risk |
| In-progress ≤ 20% aggregate | **Trade-budget linear constraint**: `Σ_j max(0, w*_j − w_j^0) over incomplete names ≤ 20 − in_progress_current` | Shared state with L15; must be a constraint here or L15's queue overflows |
| Turnover | **Objective penalty** (§7) | It is a preference with a price — the price is the cost model. This is the one thing that genuinely belongs in the objective |
| Cycle-signal targets | **Objective**, softest term | They are the first thing to yield |

Rule: **anything with a mandate number behind it is a projection; anything with a rupee cost behind it is a penalty.**

### 4.4 Priority order when constraints conflict

Relax the **lowest** priority first. The order is pre-committed and logged on every relaxation.

| P | Constraint | Notes |
|---|---|---|
| **P0** | Financing feasibility; no negative cash beyond the financed amount | Physically inviolable |
| **P1** | L17 risk-engine de-gearing; gross ≤ 1.5× | R7 asymmetry: L17 cuts without limit |
| **P2** | Mandate caps: debt ≤70%, gold ≤50%, options 50%/75% | Owner-frozen |
| **P3** | L02 structural floors: gold ≥5%, true-cash floor | Mandate backstop, not cycle influence |
| **P4** | Name drift cap 10%; sector risk cap | Concentration |
| **P5** | Name entry cap 6%; min position; min 10 names | Sizing discipline |
| **P6** | In-progress ≤20%; liquidity / days-to-liquidate (L15) | Tradability |
| **P7** | Sector active cap; turnover budget; no-trade bands | Preferences with prices |
| **P8** | **Cycle-signal targets themselves** | Sacrificed first, always |

The last row is the point of the table. When the book cannot express the signal and satisfy the mandate, **the signal loses**. Every such event is written to the arbitration log with the binding constraint named, and the monthly report carries a "signal realisation ratio" = ‖achieved deviation‖₁ / ‖requested deviation‖₁. If that ratio sits below 0.70 for two quarters, the budgets are miscalibrated against the constraints and the registry — not the constraints — should be revisited.

---

## 5. Two books from one engine

Exactly eleven parameters differ. Everything else is shared code.

| # | Parameter | Aggressive ₹100 cr | Moderate ₹1,000 cr | Source |
|---|---|---|---|---|
| 1 | Investable universe | NIFTY 750, ADV ≥ ₹5 cr | ~top 350, ADV ≥ ₹50 cr | L15 days-to-build; DECISIONS Q2/Q13 |
| 2 | Registry influence column | `influence.agg` | `influence.mod` | Registry |
| 3 | B5 authority | active | **zero** | Registry |
| 4 | Book scale from upstream tilts | 1.00 | 0.60–0.75 | L02/L04/L05/L06 publish these |
| 5 | Effective slew `ρ_L1,i(book)` | Σ 8.43 pp/mo | Σ 4.70 pp/mo | §2.4 |
| 6 | Active risk aversion `λ_A` | 8 (TE ≈ 8%) | 14 (TE ≈ 5%) | Calibration |
| 7 | Turnover penalty `γ` | 0.25 | 0.50 | §7.2 |
| 8 | No-trade band (score σ) | 0.50σ | 0.35σ | §7.3 |
| 9 | Asset-class no-trade band | 1.0 pp | 1.5 pp | L01 A6 |
| 10 | Rebalance clock | weekly (fast), monthly (alloc) | monthly (fast), quarterly (alloc) | DECISIONS Q11 |
| 11 | Target name count | 45–60 | 40–55 | Capacity |

### 5.1 The turnover arithmetic, completed

The brief supplies the allocation half. Stage 3 computes the name half, which nobody has computed yet:

| | Aggressive | Moderate |
|---|---|---|
| Allocation turnover (OU) | 49.3 pp/yr | 32.1 pp/yr → **28.2** rate-limited (§2.4) |
| **Name turnover from registry `name_l1_pp`** | **145.1 pp/yr** | **13.0 pp/yr** |
| Total | **194.4 pp/yr** | **41.2 pp/yr** |
| Ceiling | 500 pp/yr | 100 pp/yr |
| **Utilisation** | **39%** | **41%** |
| Residual name budget (ceiling − allocation) | 450.7 pp/yr | 71.8 pp/yr |
| Equity-sleeve turns/yr at the residual | 7.51 | 1.20 |
| Implied mean holding period at the residual | 1.6 months | 10.0 months |
| **Implied mean holding period at actual budgets** | **5.0 months** | **55 months** |

**This overturns the working assumption.** The moderate book is at its allocation-turnover limit, as stated — but its *name*-selection budget uses only 13.0 of 71.8 pp/yr, a 5.5× headroom. Neither book is turnover-constrained; both are **influence**-constrained. The moderate book's binding constraint is the size of its `name_l1_pp` budget (11pp L1 versus the aggressive book's 70pp), which is a liquidity-and-capacity judgement, not a turnover necessity. The owner should know that: the moderate book's cross-sectional authority could be roughly tripled without breaching the <100%/yr cap, and the reason not to is capacity at ₹1,000 cr — which is an L15 question, answerable from ADV data.

**Concentration warning.** `short_reversal_1m` alone generates **110.9 pp/yr — 76% of all aggressive name turnover** — from a 40pp `name_l1_pp` cap at `tau_half` = 1 month. At a blended 34 bps one-way cost that is **37.7 bps/yr of NAV** spent on one tier-A but famously cost-fragile signal (Novy-Marx & Velikov 2016 find short reversal among the most cost-destroyed anomalies). Stage 3 requires a **pre-committed cost hurdle**: reversal must show ≥ 60 bps/yr of net contribution over a 24-month walk-forward or its `name_l1_pp` is cut to zero by config change. This is the cost-aware objective doing its job — the term is in the objective precisely so that this decision is made by arithmetic and not by affection.

### 5.2 Cost model, and what turnover actually costs

One-way, in bps, per DECISIONS Q3 (net of costs, pre-tax):

| Component | Large cap | Mid/small |
|---|---|---|
| STT (delivery, both sides) | 10.0 | 10.0 |
| Stamp duty (buy), exchange, SEBI, GST | 2.0 | 2.0 |
| Brokerage (prop) | 2.0 | 3.0 |
| **Impact** (calibrated per book from participation) | 4–8 (agg) / 15–20 (mod) | 20–60 (agg) / 60–90 (mod) |
| **Blended one-way** | **20 (agg) / 32 (mod)** | **45 (agg) / 90 (mod)** |

| Book | Blended (smid share) | At current budgets | At the ceiling |
|---|---|---|---|
| Aggressive | 34 bps (55% smid) | **66 bps/yr** | 170 bps/yr at 500% |
| Moderate | 41 bps (15% smid) | **18 bps/yr** | 41 bps/yr at 100% |

Impact is the only calibrated term and it belongs to L15; Stage 3 consumes `EXEC_COST.c_j(name, size, urgency)` and never estimates it. Almgren–Chriss square-root impact is the assumed functional form pending L15's own calibration.

---

## 6. Turnover control

### 6.1 The band, derived from alpha decay rather than asserted

The KKT condition of §1.4's objective with a linear cost gives a no-trade region in *score* space directly: trade name *j* only if the expected alpha earned over the position's expected life exceeds the round-trip cost.

```
s_j · (h_j / 12)  >  2 · c_j        =>       s_j  >  24 · c_j / h_j
```

| Book | `c_j` one-way | `h_j` | **Alpha hurdle** |
|---|---|---|---|
| Aggressive, large | 20 bps | 6 m | **80 bps/yr** |
| Aggressive, smid | 45 bps | 6 m | **180 bps/yr** |
| Moderate, large | 32 bps | 11 m | **70 bps/yr** |
| Moderate, smid | 90 bps | 11 m | **196 bps/yr** |

It converts directly into a weight band through the score→weight gain below.

### 6.2 The score→weight gain, and a second defect in the frozen contract

With `name_l1_pp` spread over *n* names and standard-normal scores (`E|z| = 0.798`):

| Book | `name_l1` cap | Names | **Gain `k`** | 0.35σ band | 0.50σ band |
|---|---|---|---|---|---|
| Aggressive | 70 pp | 50 | **1.755 pp/σ** | 0.61 pp | 0.88 pp |
| Moderate | 11 pp | 45 | **0.306 pp/σ** | 0.11 pp | 0.15 pp |

The gains differ by **5.7×**. L01 A6 specifies a flat **0.5 pp** name band for both books. For the aggressive book that is 0.29σ — reasonable. For the moderate book it is **1.63σ**, which by §6.3's simulation costs ~20% of the signal's alpha for a turnover reduction the book does not need. **Fix: A6's name band must be expressed in score-σ, not pp.** Stage 3 publishes `no_trade_band_sigma` per book and computes the pp equivalent each rebalance.

### 6.3 Expected turnover reduction — simulated, not guessed

OU signals, 400 names, 60 years, band in units of the score's standard deviation:

| Signal `tau_half` | Band | Turnover vs unbanded | Alpha capture vs unbanded |
|---|---|---|---|
| **6 m** (momentum) | 0.25σ | 0.89 | 1.000 |
| | **0.50σ** | **0.68** | **0.995** |
| | 0.75σ | 0.52 | 0.933 |
| | 1.00σ | 0.40 | 0.896 |
| **12 m** (slower factors) | 0.50σ | 0.56 | 0.981 |
| | 0.75σ | 0.41 | 0.948 |
| **1 m** (short reversal) | 0.50σ | 0.89 | 0.985 |
| | 1.00σ | 0.67 | 0.905 |

Three readings. First, the efficient frontier of banding has a clear knee at **0.50σ**: a 32% turnover reduction for a 0.5% alpha loss, after which the alpha cost accelerates roughly sixfold. Second, **bands barely work on fast signals** — at `tau_half` = 1 month a 0.50σ band removes only 11% of turnover, because the signal crosses any reasonable band almost every period. The only turnover controls that work on short reversal are its influence cap and the §5.1 cost hurdle. Third, the aggressive book should band at 0.50σ (it has turnover headroom and should not pay alpha for nothing) and the moderate book at 0.35σ, not the wider band intuition suggests — because its turnover is already 43% of ceiling and alpha is its scarce resource.

### 6.4 The quadratic penalty, calibrated by bisection

With `Σ ≈ σ_idio² I`, the partial-adjustment fraction is `θ = λ_A σ_idio² / (λ_A σ_idio² + γ)`. At `σ_idio` = 30%:

| Book | `λ_A` | `γ` | **θ** | Name turnover after γ and band |
|---|---|---|---|---|
| Aggressive | 8 | 0.25 | 0.74 | 145.1 × 0.74 × 0.68 = **73 pp/yr** |
| Moderate | 14 | 0.50 | 0.72 | 13.0 × 0.72 × 0.80 = **7.5 pp/yr** |

`γ` is **calibrated by bisection against a turnover target**, never set by taste: `bisect(γ) until realised_turnover(γ) = target`. Targets: 250 pp/yr (aggressive, half the ceiling) and 71.8 pp/yr (moderate, the residual). Today both targets are unreachable *from above* — the registry's budgets simply do not generate that much trading — so `γ` sits at a token value and the mechanism is dormant. It is built anyway: the moment L09's factor library adds value, quality and low-volatility sleeves with their own name budgets, `γ` becomes the single knob separating the two books, and it must already be wired, tested and in the config.

---

## 7. Covariance for 750 names on short Indian history

`N` = 750, usable `T` ≈ 750–1,250 daily observations for a stable universe: `T/N` ≈ 1–1.7, so the sample covariance is singular or so ill-conditioned that its inverse is noise — 281,625 free parameters against observations that are serially and cross-sectionally dependent. **Recommendation: a hybrid factor + shrinkage estimator.**

```
1.  FACTOR BLOCK.  k = 12 factors: market, size, value, momentum, quality, low-vol,
    plus 6 principal components of the 11-sector return matrix (sectors are too
    collinear in India to enter as 11 dummies).  Parameters: 750x12 + 78 + 750
    = 9,828, a 29x reduction versus the full matrix.
    Sigma = B F B' + D
2.  FACTOR COVARIANCE F.  Two half-lives, Barra-style, because volatility mean-reverts
    faster than correlation:
        volatilities   EWMA half-life  63 trading days
        correlations   EWMA half-life 252 trading days
    Newey-West with 2 lags on F to absorb non-synchronous trading.
3.  IDIOSYNCRATIC D.  EWMA half-life 126 days, floored at the 10th percentile of the
    peer group (sector x size decile) to stop a quiet illiquid name claiming zero risk.
4.  SHRINKAGE.  Ledoit-Wolf (2004) analytic shrinkage of the RESIDUAL correlation
    toward the constant-correlation target.  Prior intensity ~0.35 for N=750,
    T=1000; the realised intensity is REPORTED every rebalance and CI-asserted
    to stay in [0.05, 0.90].  An intensity pinned at either end means the estimator
    has stopped being adaptive.
5.  ILLIQUID TAIL.  A name with < 200 traded sessions in the trailing 252, or with
    a Roll-implied spread above the 90th percentile:
        - beta estimated Dimson-style (lags 0,1,2 summed), then Vasicek-shrunk to 1.0
        - idiosyncratic vol multiplied by 1.25 (non-trading understates realised vol)
        - if < 120 sessions: no own estimate at all.  Assign the peer-group row.
6.  CONDITIONING.  Higham nearest-correlation projection; eigenvalue floor 1e-6;
    condition number capped at 500 by raising shrinkage until it holds.
7.  ASSET-CLASS BLOCK.  Comes from L05's regime-mixed CMA correlation, NOT estimated
    here, and is used for RISK REPORTING ONLY.  It never enters a weight decision.
```

**Validation, pre-committed.** The bias ratio (realised portfolio vol ÷ ex-ante forecast, 60-day rolling) must sit in [0.85, 1.20]; three consecutive months outside triggers the §1.5 fallback and a data ticket. Estimation windows are purged and embargoed per `02-ECONOMETRIC-METHODS.md` §5.1.

**Deferred:** Ledoit–Wolf (2017) nonlinear shrinkage, which is the correct estimator here but requires careful numerics and is worth ~10–20 bps of realised-risk accuracy — real, but not v1.

---

## 8. Stage-1 sufficiency and the Stage-2 overlay

**Mode Q (quant-only) is the default and the backtestable baseline.** Block A runs from `resolve()` output plus L02 anchors and L17 gates; Block B runs from L08–L12 scores. Every input has a computed default; no field waits for a human. If a signal layer is stale beyond its `staleness_days`, its contribution decays linearly to zero over `min(3 months, tau_half/4)` — it does not hold its last value and it does not block the solve.

**Mode Q+V** admits Stage-2 (L18) views as a Black–Litterman overlay on **Block B only**. Stage 2 has no asset-class authority whatsoever; L01 §11 already limits the overlay to trigger nomination, phase-override proposals and tier downgrades, and Stage 3 adds nothing.

```
pi        = lambda_A · Sigma · (w_Q − w_b)                    # implied alpha of Mode Q
Omega_k   = (1/c_k − 1) · p_k'(tau·Sigma)p_k                  # Idzorek confidence mapping
alpha_BL  = [(tau Sigma)^-1 + P' Omega^-1 P]^-1
            [(tau Sigma)^-1 pi + P' Omega^-1 q]
tau = 0.05
```

Hard limits on the overlay: **at most 8 views** per rebalance; each a *relative* statement with a written falsification condition and a review date; `‖w_{Q+V} − w_Q‖₁ ≤ 8 pp` (aggressive) / 5 pp (moderate) per rebalance and ≤ 20 pp / 12 pp standing.

**Measurement.** Both modes are solved and stored every rebalance, always, even when Stage 2 is off. The reported metric is

```
overlay_IR = mean(r_QV − r_Q) / stdev(r_QV − r_Q),  annualised,
             with per-view attribution and hit rate
```

with a **pre-committed kill rule**: if `overlay_IR < 0` over 24 months of combined live and walk-forward history, Stage 2 defaults to off and re-enabling requires two signatures. **CI assertion:** with Stage 2 disabled, `w_Q` is bit-identical to the Mode-Q solve — the same test L02, L04, L05, L06 and L08 each already assert for their own outputs.

---

## 9. Worked example — 2026 signal vector, both books, by hand

**Scenario.** Credit cycle mid-expansion; macro regime rising growth / rising inflation; valuation 70th percentile (`V_z` = +0.52); euphoria 65; momentum positive; real rates positive; INR stable; no funding stress. Signals mapped to `u` = risk-favourability after attenuation and √(retained variance).

### 9.1 Per-cycle contributions, aggressive book (pp of NAV)

| Cycle | Bkt | `u` | `u_eff` | Equity | Gold | Debt |
|---|---|---|---|---|---|---|
| `monetary_order_debasement` | B0 | −0.55 | −0.550 | −0.28 | +0.39 | −0.17 |
| `india_development_arc` | B0 | +0.30 | +0.300 | +0.90 | −0.30 | −0.90 |
| `equity_valuation_reversion` | B1 | −0.52 | −0.520 | −2.60 | +2.08 | +2.08 |
| `india_credit_financial_cycle` | B2 | +0.45 | +0.450 | +1.80 | −0.45 | −2.25 |
| `global_liquidity_cycle` | B2 | +0.20 | +0.200 | +0.40 | −0.10 | −0.40 |
| `corporate_profit_share_cycle` | B2 | −0.40 | −0.335 | −0.67 | +0.33 | +0.67 |
| `india_business_cycle` | B3 | +0.60 | +0.600 | +2.40 | −0.30 | −1.80 |
| `inflation_cycle` | B3 | −0.50 | −0.500 | −1.00 | +1.50 | **−1.50** |
| `rbi_policy_rate_cycle` | B3 | −0.35 | −0.313 | −0.63 | +0.63 | +0.63 |
| `kitchin_inventory` | B3 | +0.25 | +0.216 | +0.43 | 0.00 | −0.22 |
| `smallcap_breadth_cycle` | B3 | −0.30 | −0.300 | −0.60 | 0.00 | +0.30 |
| `intermediate_momentum_12_1` | B4 | +0.80 | +0.800 | +2.40 | 0.00 | −0.80 |
| `flows_positioning_cycle` | B4 | −0.30 | −0.300 | −0.90 | +0.60 | +0.60 |
| `volatility_regime_cycle` | B4 | +0.35 | +0.350 | +0.70 | −0.35 | −1.05 |
| **CENTRE (B0–B2)** | | | | **−0.44** | **+1.95** | **−0.97** |
| **DEVIATION (B3–B5)** | | | | **+2.81** | **+2.08** | **−3.84** |

Note the bold `inflation_cycle` row: the only entry that cuts equity **and** debt together. That is the correlation flip acting structurally.

### 9.2 Arbitration and closure

| Step | Equity | Gold | Debt |
|---|---|---|---|
| Σ (centre + deviation) | +2.363 | +4.026 | −4.806 |
| L1 | 3.252 | 4.026 | 4.806 |
| Disagreement `D` | 0.273 | 0.000 | 0.000 |
| A3 haircut (0.35·D) | 0.096 | — | — |
| Net after A3 | **+2.136** | **+4.026** | **−4.806** |
| C1 closure (κ₊ = 0.780) | **+1.666** | **+3.140** | −4.806 |

Bucket caps: none binds (B3 equity **L1** claim 5.06pp vs a 12pp budget; B1 gold 2.08pp vs a 4pp budget). Cluster cap: `equity_valuation_reversion` and `corporate_profit_share_cycle` are one family (parent–child, `rv` = 0.70 already applied); their combined equity L1 of 3.27pp is under the 1.4 × 5.0 = 7.0pp cluster cap. No scaling. A6 asset-class band (1.0pp): all three moves exceed it, all execute. Rate limits (§2.3–2.4): the largest single-cycle move is `intermediate_momentum` at +2.40pp of equity against `ρ_net` = 0.500 pp/month, so **the slew limiter binds** and momentum's equity contribution arrives over 4.8 months rather than at once — this is the limiter working as designed, and it is logged.

### 9.3 Result — aggressive book

| | Neutral | Δ | **Target** | Binding constraint |
|---|---|---|---|---|
| Equity | 60.00 | +1.67 | **61.67%** | — |
| Gold | 12.00 | +3.14 | **15.14%** | ≤50% ✓, ≥5% ✓ |
| Debt | 28.00 | −4.81 | **23.19%** | ≤70% ✓ |
| Cash | 0.00 | 0.00 | **0.00%** | — |
| Gross | 1.000× | | **1.000×** | ceiling 1.415× (leverage contributions net −0.085×); **gearing gate FAILS** — valuation percentile 70 > 65 |

**No asset-class constraint binds.** That is the honest answer and it is the right one: a mid-cycle, moderately-expensive, mildly-euphoric market should produce a portfolio close to policy. The gearing gate is the only thing that fires, and it fires on valuation — at the 60th percentile instead of the 70th, `κ_G · s_riskon` would take the aggressive book to 1.06× gross.

### 9.4 Result — moderate book

| | Neutral | Δ | **Target** |
|---|---|---|---|
| Equity | 60.00 | +0.90 | **60.90%** |
| Gold | 12.00 | +2.19 | **14.19%** |
| Debt | 28.00 | −3.09 | **24.91%** |
| Gross | 1.000× | | **1.000×** (ceiling 1.357×, gate fails) |

The moderate book moves 3.09pp of L1 versus the aggressive book's 4.81pp — a 36% smaller response from identical signals, entirely from the `influence.mod` column. C1's closure factor is more aggressive here (κ₊ = 0.666) because the moderate book's gold budget is not proportionally cut.

### 9.5 Sector layer, aggressive (equity sleeve = 61.67% of NAV)

Scenario sector tilt, L1 = 18.0 pp against a 28.6 pp 3σ budget:

| Sector | Bench | Tilt | Sleeve | % of NAV | vs 25% NAV cap | vs ±10pp active |
|---|---|---|---|---|---|---|
| Financials | 32.0 | +3.0 | 35.0 | **21.6%** | ✓ (headroom 3.4pp) | ✓ |
| Capital goods | 6.0 | +2.5 | 8.5 | 5.2% | ✓ | ✓ |
| Metals | 4.0 | +1.5 | 5.5 | 3.4% | ✓ | ✓ |
| Energy | 8.0 | +0.5 | 8.5 | 5.2% | ✓ | ✓ |
| Auto | 7.5 | +0.5 | 8.0 | 4.9% | ✓ | ✓ |
| Construction / realty | 4.5 | +1.0 | 5.5 | 3.4% | ✓ | ✓ |
| Power | 4.0 | 0.0 | 4.0 | 2.5% | ✓ | ✓ |
| IT | 10.0 | −2.0 | 8.0 | 4.9% | ✓ | ✓ |
| Healthcare | 7.0 | −1.5 | 5.5 | 3.4% | ✓ | ✓ |
| FMCG | 6.5 | −2.5 | 4.0 | 2.5% | ✓ | ✓ |
| Other | 10.5 | −3.0 | 7.5 | 4.6% | ✓ | ✓ |

Nothing binds at equity = 61.67%. The counterfactual matters more than the base case: **at equity = 75% of NAV the same +3.0pp financials tilt would produce 26.3% of NAV and the risk cap would force the active back to +1.3pp** — the sector model would be overruled by a cap it never sees. This is the §4.2 issue in numbers.

### 9.6 Name layer, aggressive — the constraints doing work

Illustrative names, sleeve 61.67%, `k` = 1.755 pp/σ, band 0.50σ = 0.88 pp, `m_book` = 0.40%:

| Name | Current | Score | Raw target | Binding constraint | **Final** |
|---|---|---|---|---|---|
| N1 large financial | 10.6% | +1.9σ | 11.2% | **Drift cap** — mandatory trim, overrides a maximum score | **10.0%** |
| N2 large industrial | 5.2% | +1.6σ | 8.0% | **Entry cap** — may hold above 6%, may not buy above it | **6.0%** |
| N3 mid-cap metal | 0.0% | +1.4σ | 3.5% | **L15 staging** — thin name, 1% tranches; counts 3.5pp against the 20% in-progress budget | **1.0%** (target 3.5%, queued) |
| N4 large IT | 3.10% | −0.2σ | 2.75% | **No-trade band** — \|Δ\| = 0.35pp < 0.88pp | **3.10%** (no trade) |
| N5 small cap | 1.8% | −1.7σ | 0.0% | none — exits are never banded | **0.0%** |
| N6 new mid cap | 0.0% | +0.2σ | 0.3% | **Min position** 0.40% — round to zero | **0.0%** |

In-progress aggregate after this rebalance: 3.5 (N3) + 0.8 (N2 residual demand) + queue carry 7.1 = 11.4pp, inside the 20pp cap; N3's next tranche is admitted.

### 9.7 Stress variant — L17 fires

Same signals, but the funding-stress trigger fires and L17 issues `equity_scaler = 0.65` (its own ladder, unbudgeted under R7):

| | Aggressive |
|---|---|
| Equity | 61.67 × 0.65 = **40.1%** |
| Gold | **15.1%** |
| Debt | **23.2%** |
| Cash | **21.6%** |
| Newly binding | **Min 10 names** activates (equity < 50%): the repair step admits the top-scoring excluded names at `m_book` until `n` = 10. Gross ceiling collapses to 1.0× under the vol/funding leverage modifiers |

The cycle stack contributed nothing to this cut and could not have: this is the L01 §8.6 admission, honoured rather than papered over. Stage 3's only job in a five-week crash is to execute L17's cut without argument and to keep the book feasible while doing it.

---

## 10. MVP versus deferred

| # | Step | Deliverable | Days | MVP |
|---|---|---|---|---|
| 1 | Block A allocation ladder | Cap-mapped contributions, sign matrix `S`, A1–A7 arbitration, C1–C4 closure, arbitration log | 3.0 | ✅ |
| 2 | Horizon blending + rate limiter | Per-bucket EWMA, smooth→clip→slew, book-specific `ρ_i(book)` | 2.0 | ✅ |
| 3 | Constraint projection engine | Entry/drift ratchet, sector two-cap, gold/debt/gross, min-position, in-progress budget, priority-ordered relaxation | 3.5 | ✅ |
| 4 | **Property test suite** | For any `u ∈ [−1,1]^17` and any score vector, output satisfies every frozen constraint. Includes the debt-corner test and the 5-copies aliasing test | 3.0 | ✅ |
| 5 | Covariance engine | 12-factor model, two-half-life EWMA, Ledoit–Wolf, Higham projection, illiquid-tail rules, bias-ratio monitor | 4.0 | ✅ |
| 6 | Block B QP | Convex solve, linear + quadratic cost, cardinality repair, transfer-coefficient report | 3.0 | ✅ |
| 7 | Fallback path | Score-tilted inverse-vol + cap iteration, with all five trip-wires | 1.0 | ✅ |
| 8 | Turnover control | Score-σ bands, `γ` bisection calibration, per-signal turnover and cost attribution | 2.0 | ✅ |
| 9 | Mode Q / Mode Q+V | BL overlay, Idzorek Ω, L1 caps, `overlay_IR` and kill rule, bit-identical CI test | 2.0 | ✅ |
| 10 | Implied-returns diagnostic | Monthly reverse-optimisation report incl. the −396 bps debt line, with the CI assertion | 0.5 | ✅ |
| 11 | Explainability report | One page per rebalance: every contribution, every haircut, every binding constraint, signal realisation ratio | 1.5 | ✅ |
| 12 | Fixtures | Synthetic 750-name panel + committed signal vectors so the whole layer runs with zero live data | 1.5 | ✅ |
| | **MVP total** | | **27.0** | |
| 13 | Multi-period / Gârleanu–Pedersen dynamic trading | Boyd et al. multi-period convex formulation | 4 | ⬜ |
| 14 | Ledoit–Wolf nonlinear shrinkage | 2017 analytical estimator | 2 | ⬜ |
| 15 | CVaR / drawdown-aware Block B objective | Only worth it once Block A is proven stable | 3 | ⬜ |
| 16 | Robust / resampled optimisation | Michaud resampling or ellipsoidal uncertainty sets | 3 | ⬜ |
| 17 | Integer cardinality (true min-position MIQP) | Replaces the §4.3 repair heuristic | 2 | ⬜ |

**Everything in the MVP runs against committed fixtures.** No module in this layer touches a network. The synthetic 750-name panel is generated from a seeded 12-factor process with a deliberately fat idiosyncratic tail and 8% of names marked illiquid, so the illiquid-tail path and the fallback path are both exercised on every CI run.

---

## 11. Interfaces

**Consumes**

| From | Object | Contract |
|---|---|---|
| L01 | `resolve(contributions, asof)`, `CYCLE_STATE`, `influence_budget(cycle_id, book)`, `HORIZON_LADDER` | Stage 3 reads **only** these; never a raw layer signal. Unregistered `cycle_id` is rejected |
| L02 | `LW_ANCHOR`, `LW_CONSTRAINTS` (gold floor 5%, `gross_leverage_ceiling`), `LW_HEDGE_POLICY` | Anchors are floors and ceilings, applied at P3; they are not cycle influence |
| L03 | `L03_CONSTRAINTS`, `L03_SECTOR_TILT` | `DEBT_SLEEVE_RISK` is **not** consumed from here — see the ownership conflict below |
| L04 | `MACRO_GATES` (`gross_leverage_cap_modifier` ≤ 0 always, `no_trade_band_multiplier`, `momentum_rebalance_interval_weeks`), `regime_probs` | Gates multiply my bands and ceilings; regime probs select the correlation mix |
| L05 | `CMA` (μ, σ, `corr_by_regime_cell`, `corr_crisis_overlay`, **both** `debt_variant` legs) | **Sole publisher of the CMA.** Both debt variants are solved every rebalance and the weight difference reported |
| L06 | `EXT_TILT`, `INR_STATE.vol_for_optimizer`, `EXTERNAL_VULNERABILITY` | One-sided de-risk input |
| L07 | `FLOW_*` name and sleeve inputs | Via `resolve()` for allocation; directly for name scores |
| L08–L12 | `MOM_SCORES`, factor exposures, sector tilts, bottom-up and special-situation scores | Name-level **scores**, not sleeve weights. `MOM_SLEEVE` is consumed only as the §1.5 fallback and as an attribution benchmark |
| L15 | `EXEC_COST.c_j(name, size, urgency)`, `in_progress_pct`, `queue`, `days_to_build`, `investable_universe(book, asof)` | The universes are *derived by L15*, not assumed here |
| L16 | `hedge_ratio`, `options_delta_adjusted`, `options_notional` | Delta-adjusted into gross; notional into the 50%/75% caps |
| L17 | `equity_scaler`, `cash_call_level`, `gross_leverage_cap`, `vol_state_z`, `mkt_state`, `current_drawdown` | **Unbudgeted and unarguable** (R7). Applied at P1, exempt from rate limits |
| L18 | `views` (P, q, confidence, falsification condition) | Block B only, ≤8 views, L1-capped |
| L20 | `turnover_measured`, `bias_ratio`, `overlay_IR`, `transfer_coefficient` | Drives the §1.5 trip-wires, the §5.1 reversal hurdle and the §8 kill rule |

**Exposes**

```python
TARGET_PORTFOLIO = {book: {asset_class: pct_nav},                  # equity, gold, debt, cash
                    names: {symbol: pct_nav},
                    sectors: {sector: pct_nav},
                    gross_x, gross_ceiling_x, net_equity_beta,
                    asof, vintage_id, mode}                        # mode in {Q, Q+V}

CONSTRAINT_LOG   = [{constraint, priority, requested, granted, binding_reason, cycle_ids}]
SIGNAL_REALISATION = {asset_class: achieved_L1 / requested_L1, overall}
IMPLIED_RETURNS  = {asset: pct}                                    # the section-3.4 diagnostic
RISK_REPORT      = {ex_ante_vol, tracking_error, factor_exposures, sector_exposures,
                    marginal_contribution_to_risk, bias_ratio_60d,
                    vol_by_regime_cell, crisis_overlay_vol}
TURNOVER_REPORT  = {allocation_pp_yr, name_pp_yr, by_cycle, cost_bps_yr, utilisation}
OVERLAY_DELTA    = {l1_pp, by_name, overlay_IR_trailing_24m}
SIGN_MATRIX      = {cycle_id: {target: +1|0|-1}}                   # section 1.3, published here
NO_TRADE_BANDS   = {book: {asset_class_pp, name_sigma, name_pp_equivalent}}
```

**Ownership conflicts to resolve.** (i) L03 and L05 both publish `DEBT_SLEEVE_RISK`; Stage 3 consumes **L05's** per L05's own recommendation, and L03's copy should be deleted. (ii) L08 publishes `MOM_SLEEVE` (target weights) while Stage 3 needs `MOM_SCORES` (alphas); publishing both is fine, but if the optimizer consumed the sleeve it would be optimising an optimised portfolio. Stage 3 consumes scores. (iii) L01 §8.5 warns that `effective_limit = min(L01_rate_limit, layer_self_limit)`; Stage 3 adds a third term, the book-derived limit of §2.4, and takes the min of all three.

---

## 12. Risks and constraint conflicts

1. **The debt override is the single largest unhedged judgement in the model.** The policy portfolio marks debt down by 396 bps/yr against a frozen owner input. If the 10% is real and achievable, the model is knowingly giving up roughly 100–150 bps/yr of portfolio return (28pp × 3.96pp × the fraction of the gap that is real) in exchange for equity exposure whose expected excess over debt is, on the frozen numbers, **negative**. This should be argued with the owner directly, not resolved in a spec.
2. **`influence.leverage_x` has an inverted sign convention relative to every other influence field.** `equity_pp: [6, 4]` means "down 6, up 4" with the down bound stored as a positive magnitude; `leverage_x: [-0.20, 0.05]` stores the down bound as a signed negative. A uniform reader applying `−cap[0]·|u|` to both gets the leverage sign **backwards**, turning every de-risking cycle into a gearing-up instruction. Found while building §9. Fix: normalise in the registry loader and add a CI assertion that all `leverage_x[0] ≤ 0` and all `*_pp[0] ≥ 0`.
3. **`rate_limit` is stored per cycle, not per book**, making the limiter 2–4× too loose for the moderate book (§2.4). Stage 3 patches it, but the registry should carry the per-book value so the CI turnover test sees the same number the optimizer does.
4. **L01's sector-cap recommendation `min(25%, bench + 10pp)` does not relieve the constraint it was written to relieve** — for any sector above 15% benchmark weight it returns 25%, the same forced underweight. The semantics require `max`, and the NAV-vs-sleeve denominator must be settled (§4.2). **This layer depends on the resolution.**
5. **A6's 0.5pp name band is 0.29σ for the aggressive book and 1.63σ for the moderate book** — a 5.7× difference in effective aggressiveness from one number. It must be expressed in score-σ (§6.2).
6. **The registry's 3σ formula `3·√(0.33·Σb²)` returns 1.72×b when a single bucket dominates**, exceeding the hard linear bound. Latent today (no asset class is single-bucket) but it would misfire on `name_l1_pp`, where B5 carries 40 of 65pp. Fix: `min(Σb, 3·√(0.33·Σb²))`.
7. **Neither book is turnover-constrained.** Both run at ~40% of ceiling (§5.1). The elaborate turnover machinery in §6 is insurance, not a current binding mechanism, and the moderate book's real constraint is its `name_l1_pp` budget of 11pp — a capacity judgement that should be re-derived from L15's ADV analysis rather than inherited.
8. **`short_reversal_1m` is 76% of aggressive name turnover from one 40pp budget.** It must clear a pre-committed 60 bps/yr net hurdle or be zeroed. Expect resistance; the answer should be the arithmetic, not the priors.
9. **The 3–6% entry band and a 45-name systematic sleeve are incompatible** (§4.1). Assumed scoping to conviction positions; requires owner confirmation.
10. **Block B's covariance cannot be validated on the illiquid tail.** Names with <120 sessions get a peer-group row, which is a structural assumption, not an estimate. At ₹100 cr reaching into the NIFTY 750 tail, this covers a meaningful slice of the aggressive book's names, and every risk number for that slice is a prior.
11. **The optimizer cannot help with March 2020 and should not be asked to.** L01 §8.6's admission is inherited verbatim. Stage 3's contribution to the drawdown objective is (a) executing L17's cut without argument or delay, (b) keeping the book feasible and liquid during the cut, and (c) not having geared into it — which is what the §2.5 C3 gate is for. The 30–35% drawdown ceiling rests on L16 and L17.
12. **Free-data note.** Every input to this layer arrives from a sibling layer, so this layer names no new data source. The two it *implicitly* requires — benchmark sector weights and index constituent weights (NSE indices, free) and daily adjusted prices for the covariance (NSE/BSE bhavcopy 1994–, own D4 reconstruction) — are already owned by L19 and must be fixture-backed here.

---

## 13. References

1. Black, F. & Litterman, R. (1992). "Global Portfolio Optimization." *Financial Analysts Journal* 48(5), 28–43.
2. Idzorek, T. (2005). "A Step-by-Step Guide to the Black–Litterman Model." Ibbotson Associates working paper; later a chapter in Satchell (ed.), *Forecasting Expected Returns in the Financial Markets* (2007). **[verify exact venue]** — source of the Ω-from-confidence mapping used in §8.
3. Michaud, R. (1989). "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?" *Financial Analysts Journal* 45(1), 31–42.
4. Best, M. J. & Grauer, R. R. (1991). "On the Sensitivity of Mean-Variance-Efficient Portfolios to Changes in Asset Means." *Review of Financial Studies* 4(2), 315–342. — the formal reason §1.2 refuses to optimise Block A.
5. Jagannathan, R. & Ma, T. (2003). "Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps." *Journal of Finance* 58(4), 1651–1683.
6. DeMiguel, V., Garlappi, L. & Uppal, R. (2009). "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?" *Review of Financial Studies* 22(5), 1915–1953. — the fallback's defence.
7. Kritzman, M., Page, S. & Turkington, D. (2010). "In Defense of Optimization: The Fallacy of 1/N." *Financial Analysts Journal* 66(2), 31–39. — the counter-case, and why Block B still optimises.
8. Ledoit, O. & Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." *Journal of Portfolio Management* 30(4), 110–119.
9. Ledoit, O. & Wolf, M. (2003). "Improved Estimation of the Covariance Matrix of Stock Returns with an Application to Portfolio Selection." *Journal of Empirical Finance* 10(5), 603–621. — the single-index shrinkage target.
10. Ledoit, O. & Wolf, M. (2017). "Nonlinear Shrinkage of the Covariance Matrix for Portfolio Selection: Markowitz Meets Goldilocks." *Review of Financial Studies* 30(12), 4349–4388. — the deferred upgrade.
11. Rosenberg, B. (1974). "Extra-Market Components of Covariance in Security Returns." *Journal of Financial and Quantitative Analysis* 9(2), 263–274. — the factor-covariance structure of §7.
12. Higham, N. J. (2002). "Computing the Nearest Correlation Matrix — a Problem from Finance." *IMA Journal of Numerical Analysis* 22(3), 329–343.
13. Dimson, E. (1979). "Risk Measurement When Shares Are Subject to Infrequent Trading." *Journal of Financial Economics* 7(2), 197–226. Scholes, M. & Williams, J. (1977). *JFE* 5(3), 309–327. — the illiquid-tail beta corrections.
14. Vasicek, O. (1973). "A Note on Using Cross-Sectional Information in Bayesian Estimation of Security Betas." *Journal of Finance* 28(5), 1233–1239.
15. Gârleanu, N. & Pedersen, L. H. (2013). "Dynamic Trading with Predictable Returns and Transaction Costs." *Journal of Finance* 68(6), 2309–2340. — the partial-adjustment result behind §6.4.
16. Constantinides, G. M. (1986). "Capital Market Equilibrium with Transaction Costs." *Journal of Political Economy* 94(4), 842–862. Davis, M. H. A. & Norman, A. R. (1990). "Portfolio Selection with Transaction Costs." *Mathematics of Operations Research* 15(4), 676–713. — the no-trade-region literature.
17. Novy-Marx, R. & Velikov, M. (2016). "A Taxonomy of Anomalies and Their Trading Costs." *Review of Financial Studies* 29(1), 104–147. — the empirical basis for the §5.1 short-reversal hurdle.
18. Almgren, R. & Chriss, N. (2001). "Optimal Execution of Portfolio Transactions." *Journal of Risk* 3(2), 5–39. — impact functional form, pending L15 calibration.
19. Boyd, S., Busseti, E., Diamond, S., Kahn, R., Koh, K., Nystrup, P. & Speth, J. (2017). "Multi-Period Trading via Convex Optimization." *Foundations and Trends in Optimization* 3(1), 1–76. — the deferred multi-period formulation.
20. Grinold, R. C. & Kahn, R. N. (2000). *Active Portfolio Management*, 2nd ed. McGraw-Hill. — implied returns, the fundamental law, and the transfer coefficient.
21. Clarke, R., de Silva, H. & Thorley, S. (2002). "Portfolio Constraints and the Fundamental Law of Active Management." *Financial Analysts Journal* 58(5), 48–66. — the transfer-coefficient reporting in §11.
22. Maillard, S., Roncalli, T. & Teïletche, J. (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *Journal of Portfolio Management* 36(4), 60–70. — the ERC computation in §3.2.
23. López de Prado, M. (2018). *Advances in Financial Machine Learning.* Wiley. — purged/embargoed CV for the covariance and band calibration.
24. Harvey, C. R., Liu, Y. & Zhu, H. (2016). "…and the Cross-Section of Expected Returns." *Review of Financial Studies* 29(1), 5–68.
25. Free sources implicitly required: NSE index constituent and sector weights <https://www.nseindia.com/all-reports>; NSE/BSE bhavcopy archives (1994–) for the covariance panel; CCIL <https://www.ccilindia.com> and RBI DBIE <https://dbie.rbi.org.in> for the financing-rate assumption in C4. All routed through L19 and fixture-backed here.

*Items marked [verify] require confirmation against the primary source before circulation. All numeric results in §2, §3, §5, §6 and §9 are reproducible from `config/cycle_registry.yaml` and L05 §6.6 alone.*
