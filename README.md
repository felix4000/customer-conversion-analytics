# Customer Conversion Analytics

Conversion funnel and retention broken down by segment (device, acquisition
channel, country, customer type) instead of one blended number — because
the blended number usually hides where the actual problem is.

> This project uses synthetic/anonymised data inspired by real-world
> customer behaviour and conversion analytics scenarios. No confidential
> company data is included. See [docs/methodology.md](docs/methodology.md).

## Business Problem

A single site-wide conversion rate tells you almost nothing about what to
fix. Mobile and desktop behave differently, channels bring different intent,
and "repeat purchase rate" changes a lot by segment. This project answers:
which specific segments are underperforming, and by how much.

## Objectives

- Break the funnel down by device and acquisition channel.
- Find the worst-converting device x channel combinations specifically.
- Measure repeat purchase rate by country and customer type.
- Build a lightweight acquisition-cohort view, with its limitations stated
  plainly rather than glossed over.

## Dataset

| Table | Rows | Grain |
|---|---|---|
| `data/website_sessions_by_segment.csv` | 216 | month x device x channel |
| `data/customers.csv` | 320 | 1 row per customer |

## Methodology

1. Funnel by device (conversion rate, checkout completion).
2. Funnel by acquisition channel.
3. Device x channel cross-tab — worst combinations.
4. Repeat purchase rate by country x customer type.
5. Acquisition-month cohorts, with a stated right-censoring caveat.

Full detail: [docs/methodology.md](docs/methodology.md).

## Data Architecture

```text
Sessions (by device, channel, month)
        │
        ▼
  Funnel by segment  ──────────►  Worst device x channel combos
        │
        ▼
   Customers (country, type, repeat flag)
        │
        ▼
  Repeat rate by segment  ──────►  Acquisition-month cohorts (caveated)
```

## Tools

SQL (SQLite/PostgreSQL-compatible), Python (pandas), Jupyter.

## Analysis

| Area | File |
|---|---|
| Funnel-by-segment SQL | [`sql/funnel_by_segment.sql`](sql/funnel_by_segment.sql) |
| Cohort/segmentation Python | [`python/cohort_and_segmentation.py`](python/cohort_and_segmentation.py) |
| Full walkthrough notebook | [`notebooks/conversion_analysis.ipynb`](notebooks/conversion_analysis.ipynb) |

Example — conversion rate and checkout completion by device
(`sql/funnel_by_segment.sql`):

```sql
SELECT
    device,
    ROUND(100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0), 2)   AS conversion_rate_pct,
    ROUND(100.0 * SUM(checkout) / NULLIF(SUM(add_to_cart), 0), 2) AS checkout_completion_pct
FROM website_sessions_by_segment
GROUP BY device
ORDER BY conversion_rate_pct DESC;
```

## Key Findings

1. **Desktop converts at 6.60% vs. 3.13% on mobile**, and the gap is
   concentrated in checkout completion (69.1% vs. 51.7%) — a checkout
   problem, not an add-to-cart problem.
2. **Referral converts best per session (4.82%)**, ahead of organic
   (4.72%) and paid search (4.56%), despite the smallest volume.
3. **Mobile + paid search is the worst-converting combination (3.04%)** —
   the least efficient place acquisition budget is currently landing.
4. **Repeat purchase rate ranges from ~12% to ~52% by country/segment** —
   too wide a spread to treat "repeat rate" as one company-wide number.

## Recommendations

| Finding | Recommendation |
|---|---|
| Mobile checkout completion far below desktop | Audit and fix mobile checkout specifically before any other mobile work |
| Referral converts best, smallest volume | Identify and scale the specific referral sources driving that rate |
| Mobile + paid search converts worst | Review or pause underperforming mobile paid placements, reallocate to what's working |
| Repeat rate varies widely by segment | Investigate the highest-repeat segment's experience and see what transfers |

## Project Structure

```text
customer-conversion-analytics/
├── README.md
├── data/
│   ├── website_sessions_by_segment.csv
│   └── customers.csv
├── sql/
│   └── funnel_by_segment.sql
├── python/
│   └── cohort_and_segmentation.py
├── notebooks/
│   └── conversion_analysis.ipynb
└── docs/
    └── methodology.md
```

## How to Run

```bash
pip install pandas
python python/cohort_and_segmentation.py
jupyter notebook notebooks/conversion_analysis.ipynb
```

## Limitations

Monthly (not daily) segment grain, and a right-censoring caveat on the
cohort analysis — see [docs/methodology.md](docs/methodology.md).

## About the Author

**Felix Ibeh** — Data Analyst, conversion and customer-journey analytics
across e-commerce. Currently at Groupe Cipanguo, previously Euro4x4parts.

[LinkedIn](https://www.linkedin.com/in/felix-ibeh-data-analyst/) ·
[CV](https://felix4000.github.io/felix-ibeh-cv/) ·
[GitHub](https://github.com/felix4000)
# customer-conversion-analytics
Conversion funnel and retention broken down by device, channel and segment (synthetic data)
