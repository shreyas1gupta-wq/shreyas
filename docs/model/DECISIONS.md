# Owner Decisions — Round 1

Answers to the 10 blocking questions. These are binding design constraints; anything
that contradicts them in a layer spec must be revised, not the other way round.

Status: **Q12 answer incomplete — owner was cut off mid-sentence and will finish it.**

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

## Q12. Position count → **INCOMPLETE**

Owner stated: *"minimum 10 stocks (if equity weight <50% ..."* — cut off mid-sentence.

Partial reading: the minimum name count is conditional on the equity weight, with a floor of
10 names when equity is below 50% of the book. Awaiting the rest before setting position-count
and concentration rules.

---

## Open items carried forward

1. Finish Q12 (position count / concentration as a function of equity weight).
2. Set B questions 13–20 remain at their recommended defaults unless overridden.
3. Re-derive the low-churn book's investable universe for ₹1,000 cr capacity.
4. Reconcile the 1.5x leverage cap against the "drawdown below Nifty 50" objective — these
   pull in opposite directions and the resolution needs to be explicit.
