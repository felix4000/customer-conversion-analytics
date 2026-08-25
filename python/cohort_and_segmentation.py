"""
cohort_and_segmentation.py

Two things: (1) conversion funnel broken down by device and acquisition
channel, to find where the funnel actually leaks for specific segments
rather than on average, and (2) a simple customer segmentation (repeat vs.
one-time, by country and customer type) to see who actually comes back.

Usage:
    python python/cohort_and_segmentation.py
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load():
    segments = pd.read_csv(os.path.join(DATA_DIR, "website_sessions_by_segment.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"), parse_dates=["first_purchase"])
    return segments, customers


def funnel_by_device(segments: pd.DataFrame) -> pd.DataFrame:
    out = segments.groupby("device").agg(
        sessions=("sessions", "sum"), add_to_cart=("add_to_cart", "sum"),
        checkout=("checkout", "sum"), purchases=("purchases", "sum"),
    )
    out["conversion_rate_pct"] = round(100 * out["purchases"] / out["sessions"], 2)
    out["checkout_completion_pct"] = round(100 * out["checkout"] / out["add_to_cart"], 2)
    return out.sort_values("conversion_rate_pct", ascending=False)


def worst_device_channel_combos(segments: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    out = segments.groupby(["device", "acquisition_channel"]).agg(
        sessions=("sessions", "sum"), purchases=("purchases", "sum")
    )
    out["conversion_rate_pct"] = round(100 * out["purchases"] / out["sessions"], 2)
    return out.sort_values("conversion_rate_pct").head(n)


def repeat_rate_by_segment(customers: pd.DataFrame) -> pd.DataFrame:
    out = customers.groupby(["country", "customer_type"]).agg(
        customers=("customer_id", "count"), repeat_customers=("repeat_purchase", "sum")
    )
    out["repeat_rate_pct"] = round(100 * out["repeat_customers"] / out["customers"], 1)
    return out.sort_values("repeat_rate_pct", ascending=False)


def acquisition_month_cohorts(customers: pd.DataFrame) -> pd.DataFrame:
    """Simple acquisition cohort: repeat rate of customers first acquired
    in each month. A lightweight stand-in for a full cohort retention
    matrix, useful when you just need 'are recent cohorts stickier'."""
    c = customers.copy()
    c["cohort_month"] = c["first_purchase"].dt.to_period("M").astype(str)
    out = c.groupby("cohort_month").agg(
        customers=("customer_id", "count"), repeat_customers=("repeat_purchase", "sum")
    )
    out["repeat_rate_pct"] = round(100 * out["repeat_customers"] / out["customers"], 1)
    return out


def main():
    segments, customers = load()

    print("=== Funnel by device ===")
    print(funnel_by_device(segments))

    print("\n=== 5 worst device x channel combinations by conversion rate ===")
    print(worst_device_channel_combos(segments))

    print("\n=== Repeat purchase rate by country x customer type (top 5) ===")
    print(repeat_rate_by_segment(customers).head())

    print("\n=== Acquisition month cohorts ===")
    print(acquisition_month_cohorts(customers))


if __name__ == "__main__":
    main()
