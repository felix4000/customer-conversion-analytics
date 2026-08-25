# Methodology

## Data

| Table | Grain | Rows |
|---|---|---|
| `data/website_sessions_by_segment.csv` | month x device x acquisition channel | 216 |
| `data/customers.csv` | 1 row per customer | 320 |

Funnel rates by device and channel are built with realistic, deliberately
different completion rates per device (mobile checkout completion lower
than desktop) so the segment-level analysis has a real pattern to find,
not noise.

> This project uses synthetic/anonymised data inspired by real-world
> customer behaviour and conversion analytics scenarios. No confidential
> company data or real customer data is included.

## Approach

1. Funnel by device: sessions through purchase, conversion rate and
   checkout completion, to locate where device-level drop-off actually
   happens.
2. Funnel by acquisition channel: conversion rate per channel.
3. Device x channel cross-tab: the specific combinations converting worst,
   which a device-only or channel-only view would miss.
4. Repeat purchase rate by country and customer type.
5. Acquisition-month cohorts, with an explicit right-censoring caveat (see
   below).

## Tools

SQL (SQLite/PostgreSQL-compatible), Python (pandas), Jupyter.

## A note on the cohort analysis

`acquisition_month_cohorts()` in `python/cohort_and_segmentation.py`
measures repeat rate "as of today" for each acquisition cohort. Cohorts
acquired more recently have had less time to generate a second purchase
than older cohorts, so their repeat rate is mechanically understated. This
is flagged directly in the notebook rather than left for the reader to
catch — a proper fix is to measure repeat rate within a fixed window (e.g.
90 days post-acquisition) per cohort, which needs more history than this
one-year dataset provides.

## Limitations

- Segment data is monthly, not daily — enough to see device/channel
  patterns, not enough for day-of-week effects within a segment.
- Cohort analysis has the right-censoring caveat above; treat the most
  recent 2-3 months of cohort data as provisional.
- Figures are illustrative of method, not a claim about any real
  business's customers.
