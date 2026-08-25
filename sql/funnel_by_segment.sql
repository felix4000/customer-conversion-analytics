-- ============================================================
-- Funnel by Segment (Device x Acquisition Channel)
-- Dataset: website_sessions_by_segment.csv (synthetic, monthly grain)
-- ============================================================

-- 1. Conversion rate and checkout completion by device
SELECT
    device,
    SUM(sessions)                                                  AS sessions,
    SUM(add_to_cart)                                                AS add_to_cart,
    SUM(checkout)                                                   AS checkout,
    SUM(purchases)                                                  AS purchases,
    ROUND(100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0), 2)     AS conversion_rate_pct,
    ROUND(100.0 * SUM(checkout) / NULLIF(SUM(add_to_cart), 0), 2)   AS checkout_completion_pct
FROM website_sessions_by_segment
GROUP BY device
ORDER BY conversion_rate_pct DESC;

-- 2. Conversion rate by acquisition channel
SELECT
    acquisition_channel,
    SUM(sessions)                                                AS sessions,
    SUM(purchases)                                               AS purchases,
    ROUND(100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0), 2)  AS conversion_rate_pct
FROM website_sessions_by_segment
GROUP BY acquisition_channel
ORDER BY conversion_rate_pct DESC;

-- 3. Device x channel cross-tab (where does the worst combination sit?)
SELECT
    device,
    acquisition_channel,
    SUM(sessions)                                                AS sessions,
    ROUND(100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0), 2)  AS conversion_rate_pct
FROM website_sessions_by_segment
GROUP BY device, acquisition_channel
ORDER BY conversion_rate_pct ASC
LIMIT 10;

-- 4. Monthly conversion rate trend by device (is the mobile gap closing or widening?)
SELECT
    month,
    device,
    ROUND(100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0), 2) AS conversion_rate_pct
FROM website_sessions_by_segment
GROUP BY month, device
ORDER BY month, device;

-- 5. Repeat purchase rate by country and customer type (customers.csv)
SELECT
    country,
    customer_type,
    COUNT(*)                                                      AS customers,
    SUM(repeat_purchase)                                          AS repeat_customers,
    ROUND(100.0 * SUM(repeat_purchase) / COUNT(*), 1)             AS repeat_rate_pct
FROM customers
GROUP BY country, customer_type
ORDER BY repeat_rate_pct DESC;
