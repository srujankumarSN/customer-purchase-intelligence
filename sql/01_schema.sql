-- 1. Cleanup and Re-creation (Professional Workflow)
DROP TABLE IF EXISTS events_raw CASCADE;

CREATE TABLE events_raw (
    event_time    TIMESTAMP NOT NULL,
    event_type    VARCHAR(50),
    product_id    INTEGER,
    category_id   BIGINT,
    category_code TEXT,
    brand         VARCHAR(100),
    price         DECIMAL(10, 2),
    user_id       INTEGER,
    user_session  TEXT -- Changed from UUID to TEXT for better Kaggle compatibility
);

-- Indexes for high-speed joins and aggregations
CREATE INDEX idx_session_id ON events_raw(user_session);
CREATE INDEX idx_user_id ON events_raw(user_id);
CREATE INDEX idx_event_type ON events_raw(event_type);




-- 2. Advanced Feature Engineering Table
DROP TABLE IF EXISTS customer_features;

CREATE TABLE customer_features AS
WITH session_agg AS (
    SELECT 
        user_session,
        user_id,
        MIN(event_time) as session_start,
        -- Core counts
        COUNT(*) AS total_interactions,
        COUNT(*) FILTER (WHERE event_type = 'view') AS view_count,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS cart_count,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase_count,
        -- Unique product discovery
        COUNT(DISTINCT product_id) AS unique_products_viewed,
        -- Price signals
        ROUND(AVG(price), 2) AS avg_price_interacted,
        MAX(price) AS max_price_interacted,
        -- Duration
        EXTRACT(EPOCH FROM (MAX(event_time) - MIN(event_time))) AS session_duration_sec
    FROM events_raw
    GROUP BY user_session, user_id
),
final_features AS (
    SELECT
        *,
        -- Behavioral ratios (Handle division by zero with NULLIF)
        ROUND(cart_count::numeric / NULLIF(view_count, 0), 2) AS view_to_cart_ratio,
        -- Time-based features for ML
        EXTRACT(HOUR FROM session_start) AS start_hour,
        CASE WHEN EXTRACT(DOW FROM session_start) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend,
        -- Target Variable (The Label)
        CASE WHEN purchase_count > 0 THEN 1 ELSE 0 END AS label_purchased
    FROM session_agg
)
SELECT * FROM final_features;