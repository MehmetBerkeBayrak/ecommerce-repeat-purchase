-- Initial load only.
-- First import the CSV files into:
-- dw.dim_product: stock_code, product_description
-- dw.dim_customer: source_customer_id, customer_status
-- dw.stg_sales: all seven CSV columns in header order.
-- Do not import generated identity columns.
-- Target dim_date and fact_sales must be empty.

BEGIN;

-- Build a continuous calendar covering the staging data.
INSERT INTO dw.dim_date (
    date_key,
    full_date,
    calendar_year,
    month_number,
    day_of_month,
    iso_day_of_week,
    is_weekend
)
SELECT
    TO_CHAR(g.day_value, 'YYYYMMDD')::INTEGER,
    g.day_value::DATE,
    EXTRACT(YEAR FROM g.day_value)::SMALLINT,
    EXTRACT(MONTH FROM g.day_value)::SMALLINT,
    EXTRACT(DAY FROM g.day_value)::SMALLINT,
    EXTRACT(ISODOW FROM g.day_value)::SMALLINT,
    EXTRACT(ISODOW FROM g.day_value) IN (6, 7)
FROM GENERATE_SERIES(
    (SELECT MIN(invoice_timestamp)::DATE FROM dw.stg_sales)::TIMESTAMP,
    (SELECT MAX(invoice_timestamp)::DATE FROM dw.stg_sales)::TIMESTAMP,
    INTERVAL '1 day'
) AS g(day_value);

-- Stop if dimension mappings are missing or ambiguous.
DO $$
BEGIN
    IF (
        SELECT COUNT(*)
        FROM dw.dim_customer
        WHERE customer_status = 'Unknown'
          AND source_customer_id IS NULL
    ) <> 1 THEN
        RAISE EXCEPTION 'Exactly one Unknown customer is required';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM dw.stg_sales s
        LEFT JOIN dw.dim_product p
            ON p.stock_code = s.stock_code
        LEFT JOIN dw.dim_customer c
            ON c.source_customer_id = s.source_customer_id
        WHERE p.product_key IS NULL
           OR (
               s.source_customer_id IS NOT NULL
               AND c.customer_key IS NULL
           )
    ) THEN
        RAISE EXCEPTION 'Missing product or customer mapping';
    END IF;
END $$;

-- Grain: one eligible source invoice-item row.
-- Exact duplicate source rows remain separate.
INSERT INTO dw.fact_sales (
    source_row_number,
    invoice_no,
    invoice_timestamp,
    product_key,
    customer_key,
    date_key,
    quantity,
    unit_price
)
SELECT
    s.source_row_number,
    s.invoice_no,
    s.invoice_timestamp,
    p.product_key,
    COALESCE(c.customer_key, u.customer_key),
    d.date_key,
    s.quantity,
    s.unit_price
FROM dw.stg_sales s
JOIN dw.dim_product p
    ON p.stock_code = s.stock_code
JOIN dw.dim_date d
    ON d.full_date = s.invoice_timestamp::DATE
LEFT JOIN dw.dim_customer c
    ON c.source_customer_id = s.source_customer_id
CROSS JOIN (
    SELECT customer_key
    FROM dw.dim_customer
    WHERE customer_status = 'Unknown'
      AND source_customer_id IS NULL
) u;

COMMIT;