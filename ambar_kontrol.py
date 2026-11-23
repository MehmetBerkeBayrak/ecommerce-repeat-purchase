from pathlib import Path

import pandas as pd

klasor = Path(__file__).parent
veri = pd.read_excel(
    klasor / "data/raw/Online Retail.xlsx",
    engine="openpyxl",
    dtype={"InvoiceNo": "string", "StockCode": "string"},
)

iptal = veri["InvoiceNo"].str.strip().str.upper().str.startswith("C")

satislar = veri.loc[
    ~iptal
    & veri["Quantity"].gt(0)
    & veri["UnitPrice"].gt(0)
].copy()

satislar["StockCode"] = satislar["StockCode"].str.strip()
satislar["temiz_aciklama"] = (
    satislar["Description"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

aciklama_sayilari = (
    satislar.groupby("StockCode")["temiz_aciklama"].nunique()
)

cok_aciklamali = aciklama_sayilari[aciklama_sayilari > 1]

print("Uygun satis satiri:", len(satislar))
print("Birden fazla aciklamasi olan stok kodu:", len(cok_aciklamali))
print("\nOrnek stok kodlari:")
print(cok_aciklamali.head().to_string())

print("\n17107D icin aciklamalar ve kullanim sayilari:")
print(
    satislar.loc[
        satislar["StockCode"] == "17107D",
        "temiz_aciklama"
    ].value_counts().to_string()
)

aciklama_adaylari = (
    satislar.dropna(subset=["temiz_aciklama"])
    .groupby(["StockCode", "temiz_aciklama"])
    .size()
    .reset_index(name="kullanim_sayisi")
    .sort_values(
        ["StockCode", "kullanim_sayisi", "temiz_aciklama"],
        ascending=[True, False, True],
    )
    .drop_duplicates(subset=["StockCode"])
)

urunler = (
    satislar[["StockCode"]]
    .drop_duplicates()
    .merge(
        aciklama_adaylari[["StockCode", "temiz_aciklama"]],
        on="StockCode",
        how="left",
        validate="one_to_one",
    )
)

print("\nUrun boyutu adaylari:")
print("Urun sayisi:", len(urunler))
print("Bos stok kodu:", urunler["StockCode"].isna().sum())
print("Bos secilmis aciklama:", urunler["temiz_aciklama"].isna().sum())
print(
    urunler.loc[urunler["StockCode"] == "17107D"].to_string(index=False)
)
ambar_klasoru = klasor / "data/processed/warehouse"
ambar_klasoru.mkdir(parents=True, exist_ok=True)

urun_ciktisi = urunler.rename(columns={
    "StockCode": "stock_code",
    "temiz_aciklama": "product_description",
}).sort_values("stock_code")

urun_ciktisi.to_csv(
    ambar_klasoru / "dim_product.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nUrun CSV kaydedildi:", ambar_klasoru / "dim_product.csv")

bilinen_musteriler = (
    satislar.loc[satislar["CustomerID"].notna(), "CustomerID"]
    .astype("Int64")
    .astype("string")
    .drop_duplicates()
    .sort_values()
)

musteri_ciktisi = pd.DataFrame({
    "source_customer_id": bilinen_musteriler.to_numpy(),
    "customer_status": "Known",
})

musteri_ciktisi.loc[len(musteri_ciktisi)] = [pd.NA, "Unknown"]

musteri_ciktisi.to_csv(
    ambar_klasoru / "dim_customer.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nBilinen musteri:", len(bilinen_musteriler))
print("Unknown kaydi dahil:", len(musteri_ciktisi))
print("Musteri CSV kaydedildi:", ambar_klasoru / "dim_customer.csv")

staging = satislar.copy()

# Excel'de 1. satir basliktir; ilk veri satiri 2'dir.
staging["source_row_number"] = staging.index + 2

staging["CustomerID"] = (
    staging["CustomerID"].astype("Int64").astype("string")
)
staging["InvoiceNo"] = staging["InvoiceNo"].str.strip()

staging = staging.rename(columns={
    "InvoiceNo": "invoice_no",
    "InvoiceDate": "invoice_timestamp",
    "StockCode": "stock_code",
    "CustomerID": "source_customer_id",
    "Quantity": "quantity",
    "UnitPrice": "unit_price",
})

staging = staging[[
    "source_row_number",
    "invoice_no",
    "invoice_timestamp",
    "stock_code",
    "source_customer_id",
    "quantity",
    "unit_price",
]]

staging.to_csv(
    ambar_klasoru / "stg_sales.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nStaging satiri:", len(staging))
print("Tekrarli kaynak satiri:", staging["source_row_number"].duplicated().sum())
print(staging.head(2).to_string(index=False))