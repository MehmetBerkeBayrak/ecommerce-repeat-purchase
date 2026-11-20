from pathlib import Path

import pandas as pd

dosya = Path(__file__).parent / "data" / "raw" / "Online Retail.xlsx"

with pd.ExcelFile(dosya, engine="openpyxl") as excel:
    print("Sayfalar:", excel.sheet_names)

    ornek = pd.read_excel(excel, sheet_name=0, nrows=5)
    print("\nSutunlar:", ornek.columns.tolist())
    print("\nIlk 5 satir:")
    print(ornek.to_string(index=False))

veri = pd.read_excel(dosya, engine="openpyxl")

print("\nSatir ve sutun sayisi:", veri.shape)
print("\nHer sutundaki bos hucre sayisi:")
print(veri.isna().sum())

print("\nToplam satir:", len(veri))
print("Musteri kimligi dolu satir:", veri["CustomerID"].notna().sum())
print(
    "Musteri kimligi bos satir orani: %",
    round(veri["CustomerID"].isna().mean() * 100, 2),
)
iptal = (
    veri["InvoiceNo"]
    .astype(str)
    .str.strip()
    .str.upper()
    .str.startswith("C")
)

print("\nC ile baslayan iptal satiri:", iptal.sum())
print("Negatif miktarli satir:", (veri["Quantity"] < 0).sum())
print(
    "C ile baslamayan negatif miktarli satir:",
    ((veri["Quantity"] < 0) & ~iptal).sum(),
)
kontrol = veri.loc[
    (veri["Quantity"] < 0) & ~iptal,
    ["InvoiceNo", "StockCode", "Description",
     "Quantity", "UnitPrice", "CustomerID"]
]

print("\nC ile baslamayan negatif kayitlardan ilk 10:")
print(kontrol.head(10).to_string(index=False))

print("\nC olmadan negatif miktarli kayitlar:")
print("Toplam:", len(kontrol))
print("Fiyati sifir:", kontrol["UnitPrice"].eq(0).sum())
print("Musteri kimligi bos:", kontrol["CustomerID"].isna().sum())
print("Aciklamasi dolu:", kontrol["Description"].notna().sum())

print("\nDolu aciklamalardan ornekler:")
print(kontrol["Description"].dropna().value_counts().head(10))

print("\nFiyat kontrolleri:")
print("Sifir fiyatli satir:", veri["UnitPrice"].eq(0).sum())
print("Negatif fiyatli satir:", veri["UnitPrice"].lt(0).sum())
print(
    "Pozitif miktarli ama fiyati sifir satir:",
    (veri["Quantity"].gt(0) & veri["UnitPrice"].eq(0)).sum(),
)
print("\nNegatif fiyatli kayitlar:")
print(
    veri.loc[
        veri["UnitPrice"] < 0,
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID"]
    ].to_string(index=False)
)
print("\nTam satir tekrar kontrolu:")
print("Ilk kayit haric tekrar sayisi:", veri.duplicated().sum())
print(
    "Tekrarlanan gruplardaki toplam satir:",
    veri.duplicated(keep=False).sum(),
)

print("\nTamamen ayni satirlardan ornekler:")
ornek_tekrarlar = veri.loc[veri.duplicated(keep=False)]
print(ornek_tekrarlar.head(10).to_string(index=False))

satis_kosulu = (
    ~iptal
    & veri["Quantity"].gt(0)
    & veri["UnitPrice"].gt(0)
)

satislar = veri.loc[satis_kosulu].copy()
tekrarsiz = satislar.drop_duplicates()

for ad, tablo in [
    ("Tekrarlar korunuyor", satislar),
    ("Tam satir tekrarlari cikariliyor", tekrarsiz),
]:
    tutar = (tablo["Quantity"] * tablo["UnitPrice"]).sum()
    print(f"\n{ad}")
    print("Satir:", len(tablo))
    print("Benzersiz fatura:", tablo["InvoiceNo"].nunique())
    print(f"Pozitif satis satirlari tutari: {tutar:.2f} GBP")
musterili_satislar = satislar.loc[satislar["CustomerID"].notna()].copy()

print("\nMusteri analizi icin ilk aday tablo:")
print("Satir:", len(musterili_satislar))
print("Benzersiz musteri:", musterili_satislar["CustomerID"].nunique())
print("Benzersiz fatura:", musterili_satislar["InvoiceNo"].nunique())

print("\nMusterili satislarin tarih araligi:")
print("Ilk islem:", musterili_satislar["InvoiceDate"].min())
print("Son islem:", musterili_satislar["InvoiceDate"].max())

tahmin_ani = pd.Timestamp("2011-11-01")

gecmis_satislar = musterili_satislar.loc[
    musterili_satislar["InvoiceDate"] < tahmin_ani
].copy()

print("\n1 Kasim itibariyla gozlenen musteriler:")
print("Benzersiz musteri:", gecmis_satislar["CustomerID"].nunique())
print("Benzersiz fatura:", gecmis_satislar["InvoiceNo"].nunique())

donem_sonu = tahmin_ani + pd.Timedelta(days=30)

gelecek_satislar = musterili_satislar.loc[
    (musterili_satislar["InvoiceDate"] >= tahmin_ani)
    & (musterili_satislar["InvoiceDate"] < donem_sonu)
]

etiketler = pd.DataFrame({
    "CustomerID": gecmis_satislar["CustomerID"].unique()
})

etiketler["tekrar_aldi"] = (
    etiketler["CustomerID"]
    .isin(gelecek_satislar["CustomerID"])
    .astype(int)
)

print("\n30 gun icinde tekrar alisveris:")
print(etiketler["tekrar_aldi"].value_counts().sort_index())

son_alisveris = (
    gecmis_satislar.groupby("CustomerID")["InvoiceDate"]
    .max()
    .rename("son_alisveris")
    .reset_index()
)

musteri_ozellikleri = etiketler.merge(
    son_alisveris, on="CustomerID", validate="one_to_one"
)

musteri_ozellikleri["son_alisveristen_gecen_gun"] = (
    (tahmin_ani - musteri_ozellikleri["son_alisveris"])
    .dt.total_seconds() / 86400
).round(2)

print("\nIlk 5 musteri:")
print(musteri_ozellikleri.head().to_string(index=False))
siparis_sayilari = (
    gecmis_satislar.groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .rename("siparis_sayisi")
    .reset_index()
)

musteri_ozellikleri = musteri_ozellikleri.merge(
    siparis_sayilari, on="CustomerID", validate="one_to_one"
)

print("\nSiparis sayisi eklenmis ilk 5 musteri:")
print(musteri_ozellikleri.head().to_string(index=False))

gecmis_satislar["satir_tutari"] = (
    gecmis_satislar["Quantity"] * gecmis_satislar["UnitPrice"]
)

tutarlar = (
    gecmis_satislar.groupby("CustomerID")["satir_tutari"]
    .sum()
    .rename("pozitif_satis_tutari")
    .reset_index()
)

musteri_ozellikleri = musteri_ozellikleri.merge(
    tutarlar, on="CustomerID", validate="one_to_one"
)

print("\nTutar eklenmis ilk 5 musteri:")
print(musteri_ozellikleri.head().to_string(index=False))
ozellikler = [
    "son_alisveristen_gecen_gun",
    "siparis_sayisi",
    "pozitif_satis_tutari",
]

print("\nModel tablosu kontrolleri:")
print("Musteri satiri:", len(musteri_ozellikleri))
print(
    "Tekrarli musteri:",
    musteri_ozellikleri["CustomerID"].duplicated().sum(),
)
print("Bos degerler:")
print(musteri_ozellikleri[ozellikler + ["tekrar_aldi"]].isna().sum())
cikti_klasoru = dosya.parent.parent / "processed"
cikti_klasoru.mkdir(parents=True, exist_ok=True)

cikti_dosyasi = cikti_klasoru / "musteriler_2011-11-01.csv"

son_30_gun = gecmis_satislar.loc[
    gecmis_satislar["InvoiceDate"] >= tahmin_ani - pd.Timedelta(days=30)
]

son_30_siparis = (
    son_30_gun.groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

musteri_ozellikleri["son_30_gun_siparis_sayisi"] = (
    musteri_ozellikleri["CustomerID"]
    .map(son_30_siparis)
    .fillna(0)
    .astype(int)
)

print("\nSon 30 gun siparis kontrolu:")
print("Tahmin ani:", tahmin_ani)
print(
    musteri_ozellikleri[
        ["CustomerID", "siparis_sayisi", "son_30_gun_siparis_sayisi"]
    ].head().to_string(index=False)
)
musteri_ozellikleri.to_csv(
    cikti_dosyasi,
    index=False,
    encoding="utf-8-sig",
)

print("\nMusteri tablosu kaydedildi:", cikti_dosyasi)


