-- Run once in a fresh warehouse schema.
CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE dw.dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stock_code TEXT NOT NULL UNIQUE,
    product_description TEXT
);

CREATE TABLE dw.dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_customer_id TEXT UNIQUE,
    customer_status TEXT NOT NULL
        CHECK (customer_status IN ('Known', 'Unknown'))
);

CREATE TABLE dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    calendar_year SMALLINT NOT NULL,
    month_number SMALLINT NOT NULL
        CHECK (month_number BETWEEN 1 AND 12),
    day_of_month SMALLINT NOT NULL
        CHECK (day_of_month BETWEEN 1 AND 31),
    iso_day_of_week SMALLINT NOT NULL
        CHECK (iso_day_of_week BETWEEN 1 AND 7),
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE dw.stg_sales (
    source_row_number INTEGER PRIMARY KEY,
    invoice_no TEXT NOT NULL,
    invoice_timestamp TIMESTAMP NOT NULL,
    stock_code TEXT NOT NULL,
    source_customer_id TEXT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC NOT NULL CHECK (unit_price > 0)
);

CREATE TABLE dw.fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_row_number INTEGER NOT NULL UNIQUE,
    invoice_no TEXT NOT NULL,
    invoice_timestamp TIMESTAMP NOT NULL,
    product_key BIGINT NOT NULL
        REFERENCES dw.dim_product(product_key),
    customer_key BIGINT NOT NULL
        REFERENCES dw.dim_customer(customer_key),
    date_key INTEGER NOT NULL
        REFERENCES dw.dim_date(date_key),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC NOT NULL CHECK (unit_price > 0),
    line_amount NUMERIC
        GENERATED ALWAYS AS (quantity * unit_price) STORED
);