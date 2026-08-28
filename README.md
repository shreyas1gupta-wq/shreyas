# Multi-Cycle Basket Model

A multi-horizon "cycle stack" portfolio construction model for Indian markets.

**Universe:** NIFTY 750 (Nifty Total Market) equities, Gold, and Indian fixed income.

**Core idea:** dozens of cycles operating on horizons from ~250 years down to ~1 month are
estimated simultaneously, each with an evidence tier, a phase estimate carried as a *band*
rather than a point, and a hard cap on how much allocation it may move. Slow cycles set the
portfolio's strategic centre of gravity; fast cycles move a bounded tactical deviation
around it.

Two portfolios are produced from one engine, differing only in parameters:

| | Aggressive | Moderate |
|---|---|---|
| Target avg. annual turnover | 500%+ | < 100% |
| Rebalance cadence | high frequency | low frequency |
| Leverage | up to 1.5x gross (1.25x typical) | up to 1.25x gross |

## Status

🚧 **Design phase.** The repository currently holds specifications only — no implementation yet.

## Layout

| Path | Contents |
|---|---|
| `docs/model/` | Layer-by-layer design specifications |
| `config/` | Machine-readable configuration — the cycle registry lives here |

Start with `docs/model/00-MASTER-PLAN.md`.

## Design principles

1. **Evidence tiering is mandatory.** Every cycle is classified as statistically estimable (A),
   reasoned from limited history plus theory (B), or narrative only (C). Tier C gets a hard,
   small influence cap. A 200-year cycle has roughly one observation and is therefore a
   Bayesian prior and a tail-risk policy, not a forecast.
2. **Long cycles move slowly.** Wide bands, hysteresis, minimum dwell times, and a cap on
   allocation change per quarter. They must never whipsaw the book.
3. **Influence is budgeted.** The sum of every signal screaming at once must still land inside
   the mandate's constraints. The arithmetic is checked, not assumed.
4. **Point-in-time or it didn't happen.** A bitemporal store with both event date and knowledge
   date, and a test suite that deliberately tries to leak the future and must fail.
5. **The forward-looking layer is falsifiable or it is rejected.** Every non-backtestable view
   states what would prove it wrong, is logged before it is acted on, is capped in aggregate
   influence, and is scored against outcomes so persistently overconfident sources get
   down-weighted automatically.
6. **Costs and taxes are modelled before returns are believed.** At 500% turnover in Indian
   markets both are large enough to decide whether a strategy is viable at all.
