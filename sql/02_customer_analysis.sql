-- Run after importing the November customer CSV.
-- Expected rows: 3,974.

-- 1. Repeat-purchase counts and percentages
SELECT
    tekrar_aldi,
    COUNT(*) AS customer_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM public.musteriler_kasim
GROUP BY tekrar_aldi
ORDER BY tekrar_aldi;

-- 2. Historical behavior by observed outcome
SELECT
    tekrar_aldi,
    COUNT(*) AS customer_count,
    ROUND(AVG(son_alisveristen_gecen_gun), 2) AS mean_recency_days,
    ROUND(AVG(siparis_sayisi), 2) AS mean_invoice_count,
    ROUND(AVG(pozitif_satis_tutari), 2) AS mean_positive_purchase_amount,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY pozitif_satis_tutari
        ))::NUMERIC,
        2
    ) AS median_positive_purchase_amount
FROM public.musteriler_kasim
GROUP BY tekrar_aldi
ORDER BY tekrar_aldi;

-- 3. Repeat-purchase rate by recency
WITH customer_groups AS (
    SELECT
        tekrar_aldi,
        CASE
            WHEN son_alisveristen_gecen_gun < 30 THEN 1
            WHEN son_alisveristen_gecen_gun < 90 THEN 2
            ELSE 3
        END AS recency_group
    FROM public.musteriler_kasim
)
SELECT
    recency_group,
    COUNT(*) AS customer_count,
    ROUND(100.0 * AVG(tekrar_aldi), 2) AS repeat_purchase_percentage
FROM customer_groups
GROUP BY recency_group
ORDER BY recency_group;