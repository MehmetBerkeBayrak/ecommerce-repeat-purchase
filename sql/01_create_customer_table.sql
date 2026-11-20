-- Run in the ecommerce_repeat_purchase database.
-- Column order matches the processed November customer CSV.
-- This creates the table only; it does not import data.

CREATE TABLE public.musteriler_kasim (
    customer_id NUMERIC PRIMARY KEY,
    tekrar_aldi INTEGER NOT NULL CHECK (tekrar_aldi IN (0, 1)),
    son_alisveris TIMESTAMP NOT NULL,
    son_alisveristen_gecen_gun NUMERIC NOT NULL,
    siparis_sayisi INTEGER NOT NULL,
    pozitif_satis_tutari NUMERIC NOT NULL,
    son_30_gun_siparis_sayisi INTEGER NOT NULL
);