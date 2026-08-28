# Owner Decisions — Rounds 1 and 2

Answers to the 10 blocking questions and the 10 follow-ups. These are binding design constraints; anything
that contradicts them in a layer spec must be revised, not the other way round.

Status: **Rounds 1 and 2 complete.** Q19 deferred by owner; see open items.

---

## Q1. Legal / tax wrapper → **Proprietary capital**

No SEBI PMS or AIF constraints. Leverage and the full options overlay are permitted.
Taxed at the owner's own slab. Cat III AIF productisation is not in scope for now.

## Q2. AUM to design capacity for → **₹100 cr high-churn, ₹1,000 cr low-churn**

The two books have a 10x capacity difference, which means they are **not** the same
universe in practice:

- **High-churn (aggressive), ₹100 cr** — can reach into the NIFTY 750 mid/small tail.
  At a 10% ADV participation cap, names with ≥ ₹5 cr ADV are tradeable in meaningful size.
- **Low-churn (moderate), ₹1,000 cr** — effectively constrained to large and upper-mid caps.
  The bottom ~250 names of the NIFTY 750 are largely untradeable at this size. The universe,
  the position count, and the factor capacity all have to be re-derived for this book rather
  than inherited from the aggressive one.

This changes the earlier "one engine, different parameters" assumption: it is one engine with
different parameters **and different investable universes**.

## Q3. Return target basis → **Net of costs, pre-tax**

Targets are net of transaction costs and slippage, before tax at the owner's slab.

## Q4. Drawdown → **Max drawdown should be below Nifty 50's, and not more than 30–35%**

Explicitly: no hard mandate limit, but the *design objective* is that the portfolio's
maximum drawdown is **lower than the Nifty 50's** over the same window, with an absolute
ceiling around **30–35%**. Cash calls (raising cash on cycle signals) are the intended
primary mechanism for achieving this.

This is a materially tighter constraint than the earlier −35% working default, because
"below Nifty 50" is a *relative* condition that must hold in the worst historical windows —
Nifty 50 drew down roughly 38% in Mar 2020 and roughly 60% in 2008. Beating that while
running up to 1.5x gross leverage is the central tension in the whole design, and the
drawdown-control and de-gearing machinery has to be built to it from the start rather
than bolted on.

## Q5. Architecture → **Sequential pipeline, quant stage must be independently sufficient**

Owner's stated design:

```
  Cycles + Quant  (technofunda, evaluated across multiple timeframe relevances)
         |
         v
     raw outputs   <-- must already be sufficient to build a portfolio on their own
         |
         v
  AI agents + human layer  (forward-looking views, sanity and risk checks)
         |
         v
     Optimizer  (final portfolio construction)
```

The load-bearing requirement is the annotation on the second box: **the quant stage's output
must be enough to create a portfolio by itself.** The AI + human layer is an *overlay that can
be switched off*, not a dependency. This means:

- The quant stage must emit a complete, self-sufficient target portfolio, not a partial signal
  set awaiting human completion.
- The system must be runnable in a "quant-only" mode, and that mode is the backtestable
  baseline against which the AI + human layer's contribution is measured.
- The AI/human layer is therefore evaluable: quant-only vs quant-plus-overlay is a
  measurable comparison, which is exactly the accountability mechanism the forward-looking
  layer needs.

## Q6. Data budget → **Free sources only; scraping permitted**

Named: Kaggle, Hugging Face, and equivalents. No CMIE Prowess, no Refinitiv/LSEG, no Bloomberg,
no paid fundamentals or estimates feeds.

This is the single most consequential answer for the build. Consequences that must be
designed around rather than wished away:

- **Point-in-time fundamentals** are the hard problem. Free sources publish *current*
  financials, usually restated, without a knowledge date. Backtests on them leak the future.
  Mitigation: scrape and archive filings forward from today with our own knowledge dates, and
  apply a conservative fixed reporting lag to historical data while labelling every such
  backtest as lag-approximated rather than true point-in-time.
- **Survivorship-free price history** for delisted and suspended names is not freely
  available in clean form. Must be assembled from exchange archives and bhavcopy history.
- **Historical index membership** for the NIFTY 750 has to be reconstructed from NSE circulars.
- **Analyst estimates and revisions** are effectively unavailable. Any signal depending on
  estimate revision breadth has to be dropped or proxied.
- **Long-dated option history** is unavailable, so the options overlay cannot be backtested
  properly and must be justified structurally and sized conservatively.
- Macro is fine — RBI DBIE, MOSPI, CCIL, World Bank, IMF, FRED, BIS and Our World in Data are
  all free and adequate.

Data acquisition is therefore a real engineering workstream in its own right, not a
procurement line item, and it moves earlier in the build order.

## Q7. Team and timeline → **Owner + AI, 3–6 months**

Scope must be cut to fit. A 19-layer build is not achievable in this window; the plan has to
identify the subset that delivers a working, evaluable system and defer the rest.

## Q8. Benchmark → **Owner's choice deferred to model designer**

Proceeding with: primary = Nifty 500 TRI; secondary = Nifty 50 TRI (required for the Q4
relative-drawdown test); tertiary = static 60/20/20 equity-gold-bond.

## Q9. Go-live and first live capital → **Deferred — focus on building the best model**

No go-live gating for now. Validation rigour still applies, since without it "best model"
is unmeasurable.

## Q10. Caps → **Confirmed as hard caps**

- Debt and debt-related: ≤ 70%
- Gold: ≤ 50%
- Gross leverage: ≤ 1.5x (target average ~1.25x)

Confirmed as *caps*, i.e. the outer envelope. The model decides the actual weight within them;
these are not targets to be run at.

## Q11. Rebalance cadence (high-churn book) → **Weekly permitted, bi-weekly to monthly preferred**

Weekly rebalancing is allowed where a signal genuinely requires it. Larger reallocations should
default to a bi-weekly or monthly cadence. Implies a tiered rebalance clock: fast signals may
trim and add weekly within bands, while structural reallocation happens on the slower cycle.

## Q12. Position sizing → **Entry cap 5–6%, drift cap 10%, staged entry for thin names**

- **Entry cap: 5–6% of portfolio** in any one stock; **ideal entry band 3–6%**.
- **Drift cap: 10%.** A winner may run to 10% without being trimmed; above that it is trimmed back.
- **Thin-volume names: staged entry.** Build in ~1% tranches, roughly three buys spread over
  several weeks, rather than taking impact to fill in one go. The exact schedule scales with
  AUM and the book's churn rate.
- **Minimum 10 stocks when equity weight is below 50%** (from the earlier partial answer).

Implication: the sizing rule is not a single number but a function of
`(target weight, name ADV, book AUM, urgency)`. The optimizer emits a *target* weight; a separate
execution scheduler decides how many tranches and over how many days it takes to reach it.
Those are two different modules and the design has to keep them separate.

## Q13. Liquidity floor → **Derived from AUM and position size, not a fixed ADV number**

Floor is computed per book rather than hardcoded: at ₹100 cr with a 5% position, a full position
is ₹5 cr; at ₹1,000 cr it is ₹50 cr. Eligibility follows from how many days of participation that
implies at the name's ADV.

**Slow-build allowance: up to 20% of the portfolio may be in "under construction" positions at
any one time** — i.e. the aggregate of names not yet at target weight is capped at 20%. This is
what makes the thin-name tail reachable at all without creating an unsellable book.

> Flagged for confirmation: read as an *aggregate* cap across all in-progress positions. The
> alternative reading — that a single high-conviction name may be built to 20% — would contradict
> the 10% drift cap in Q12, so the aggregate reading is assumed.

## Q14. Sector → **Fully sector-active, driven by a sector-level model**

Sector selection is itself a modelled decision, not a residual of stock picking. Inputs named:
sector momentum, sector PE, sector growth, and the forward-looking versions of each
(expected market momentum, expected PE, expected growth). No sector-neutrality constraint.

> Open: a sector *concentration cap* still needs a number. Fully sector-active with no cap plus
> 1.5x leverage is how a book ends up 60% financials. Proposing 25% single-sector cap for the
> aggressive book, 20% for the moderate, subject to override.

## Q15. Options → **≤50% cumulative notional; ≤75% for tail hedge; hedge ratio is a swept parameter**

- Cumulative options notional capped at **50%** of portfolio value.
- Exception for **tail hedges: 75%** cap.
- Explicitly **not** hedging 100% — partial hedging by design.
- The hedge ratio is to be **backtested as a parameter sweep**: 0%, 25%, 50%, 75%, 100%, 125%.

This is the right instinct — the hedge ratio is an empirical question, not an assumption. It also
means the options module must expose the ratio as a first-class config parameter from day one so
the sweep is a config loop rather than a code change.

> Design note: options notional interacts with the 1.5x gross leverage cap. An explicit exposure
> accounting rule is required — whether options count at notional, delta-adjusted, or stress-value.
> Recommending delta-adjusted for directional positions plus a separate notional limit for tail
> hedges, since a far-OTM tail put has large notional but tiny delta and counting it at full
> notional would crowd out the equity book for no risk reason.

## Q16. Bond sleeve → **Assume a flat 10% annual return; owner handles instrument selection**

No credit model, no issuer selection, no rating mix in scope. Debt is a single line item returning
10% per annum.

> **This needs a risk number attached before the optimizer can use it.** A 10% return with no
> volatility and no drawdown is a free lunch — any mean-variance or risk-parity allocator will
> push straight to the 70% cap and stay there, and the equity book will be starved. Two things
> are needed: (a) an assumed volatility and drawdown for the sleeve, and (b) an assumed
> correlation to equity. Proposing 4% volatility, 6% worst drawdown, and a correlation to equity
> that flips from about −0.2 in disinflation to about +0.4 in an inflation shock, since that
> regime-dependent flip is precisely what removes the hedge when it is most needed.
> Also worth stating plainly: a genuine 10% short-duration return in India implies AA/A credit,
> not GSec — so the 10% is a credit-risk-bearing number, and the drawdown assumption should
> reflect that rather than treating it as risk-free.

## Q17. Duration management (IRF / OIS) → **Nil**

No duration overlay. Consistent with Q16 — the debt sleeve is a return assumption, not a
managed portfolio.

## Q18. Gold implementation → **Gold ETF and gold futures only**

No SGBs, no digital gold, no gold mutual funds. Futures available for capital-efficient exposure
under the leverage cap.

## Q19. Forward-looking view governance → **Deferred; freeze the rest first**

Revisit when the forward-looking layer is specified.

## Q20. Special situations → **In scope, and explicitly includes recently listed IPOs**

Owner's rationale: recently listed IPOs have lower correlation to the market, and base-formation
patterns after listing are tradeable.

> Design note: this needs its own sub-model rather than being folded into the main pipeline.
> A name listed three months ago has no 12-1 momentum, no multi-year fundamental history, and no
> factor percentile within the universe — every standard signal is undefined for it. It needs a
> dedicated scoring path (listing-relative price structure, anchor-lockup calendar, float and
> supply dynamics, promoter and PE-exit overhang) and its own position cap. Also worth noting
> honestly: part of the observed low correlation of newly listed names is a genuine idiosyncratic
> effect, and part is an artifact of short history and thin trading — the sub-model should be
> built to the first and not fooled by the second.

---

## Consolidated constraint set (as frozen)

| Constraint | Aggressive (₹100 cr) | Moderate (₹1,000 cr) |
|---|---|---|
| Single-name entry cap | 5–6% (ideal 3–6%) | 5–6% (ideal 3–6%) |
| Single-name drift cap | 10% | 10% |
| Minimum names (equity < 50%) | 10 | 10 |
| In-progress ("building") positions, aggregate | ≤ 20% | ≤ 20% |
| Sector cap | proposed 25% | proposed 20% |
| Debt and debt-related | ≤ 70% | ≤ 70% |
| Gold | ≤ 50% | ≤ 50% |
| Gross leverage | ≤ 1.5x (avg ~1.25x) | ≤ 1.5x (avg ~1.25x) |
| Options notional, directional | ≤ 50% | ≤ 50% |
| Options notional, tail hedge | ≤ 75% | ≤ 75% |
| Rebalance cadence | weekly permitted, bi-weekly/monthly preferred | monthly/quarterly |
| Max drawdown objective | below Nifty 50, ceiling 30–35% | below Nifty 50, ceiling 30–35% |

---

## Open items carried forward

1. Q19 (forward-looking view governance) — deferred by owner.
2. Sector concentration cap — number needed; 25%/20% proposed.
3. Debt sleeve risk parameters — volatility, drawdown and regime-dependent equity correlation
   must be set, otherwise the optimizer will corner-solution into debt.
4. Options exposure accounting rule against the 1.5x gross cap — delta-adjusted vs notional.
5. Confirm the Q13 reading of "20% cumulative" as an aggregate across in-progress positions.
6. Reconcile the 1.5x leverage cap against the "drawdown below Nifty 50" objective — these pull
   in opposite directions and the resolution needs to be explicit in the allocation engine.
7. Recently-listed-IPO sub-model needs its own scoring path, since standard factor and momentum
   signals are undefined for names with short history.
