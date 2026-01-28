
-- 1. Delete the empty table
DROP TABLE IF EXISTS customer_features;

-- 2. Re-run the logic to pull data from the now-full events_raw table
CREATE TABLE customer_features AS
WITH session_agg AS (
    SELECT 
        user_session,
        user_id,
        MIN(event_time) as session_start,
        COUNT(*) AS total_interactions,
        COUNT(*) FILTER (WHERE event_type = 'view') AS view_count,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS cart_count,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase_count,
        COUNT(DISTINCT product_id) AS unique_products_viewed,
        ROUND(AVG(price), 2) AS avg_price_interacted,
        EXTRACT(EPOCH FROM (MAX(event_time) - MIN(event_time))) AS session_duration_sec
    FROM events_raw
    GROUP BY user_session, user_id
)
SELECT
    *,
    ROUND(cart_count::numeric / NULLIF(view_count, 0), 2) AS view_to_cart_ratio,
    EXTRACT(HOUR FROM session_start) AS start_hour,
    CASE WHEN EXTRACT(DOW FROM session_start) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend,
    CASE WHEN purchase_count > 0 THEN 1 ELSE 0 END AS label_purchased
FROM session_agg;

-- 3. Verify the results
SELECT * FROM customer_features LIMIT 10;


-- 4. The "Sanity Check"

SELECT 
    label_purchased, 
    COUNT(*) as session_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM customer_features
GROUP BY label_purchased;