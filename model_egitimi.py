from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

klasor = Path(__file__).parent

egitim = pd.read_csv(
    klasor / "data/processed/musteriler_2011-09-01.csv"
)

ozellikler = [
    "son_alisveristen_gecen_gun",
    "siparis_sayisi",
    "pozitif_satis_tutari",
    "son_30_gun_siparis_sayisi",
]
X = egitim[ozellikler]
y = egitim["tekrar_aldi"]

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000),
)

model.fit(X, y)

print("Egitim tamamlandi.")
print("Musteri sayisi:", len(X))
print("Kullanilan ozellikler:", ozellikler)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)


dogrulama = pd.read_csv(
    klasor / "data/processed/musteriler_2011-10-01.csv"
)

gercek = dogrulama["tekrar_aldi"]
tahmin = model.predict(dogrulama[ozellikler])

print("\nEkim dogrulama sonuclari:")
print(f"Dogruluk: %{accuracy_score(gercek, tahmin) * 100:.2f}")
print(
    f"Precision: %{precision_score(gercek, tahmin, zero_division=0) * 100:.2f}"
)
print(f"Recall: %{recall_score(gercek, tahmin, zero_division=0) * 100:.2f}")
print("Karisiklik matrisi:")
print(confusion_matrix(gercek, tahmin, labels=[0, 1]))

olasiliklar = model.predict_proba(dogrulama[ozellikler])[:, 1]
tahmin_030 = (olasiliklar >= 0.30).astype(int)

print("\nEkim — esik 0.30:")
print(f"Alir denilen musteri: {tahmin_030.sum()}")
print(
    f"Precision: %{precision_score(gercek, tahmin_030, zero_division=0) * 100:.2f}"
)
print(
    f"Recall: %{recall_score(gercek, tahmin_030, zero_division=0) * 100:.2f}"
)
print(confusion_matrix(gercek, tahmin_030, labels=[0, 1]))

from sklearn.ensemble import HistGradientBoostingClassifier

agac_model = HistGradientBoostingClassifier(
    max_iter=100,
    max_leaf_nodes=7,
    learning_rate=0.1,
    random_state=42,
)

agac_model.fit(X, y)
agac_tahmin = agac_model.predict(dogrulama[ozellikler])

print("\nAgac tabanli model — esik 0.50:")
print(
    f"Precision: %{precision_score(gercek, agac_tahmin, zero_division=0) * 100:.2f}"
)
print(
    f"Recall: %{recall_score(gercek, agac_tahmin, zero_division=0) * 100:.2f}"
)
print(confusion_matrix(gercek, agac_tahmin, labels=[0, 1]))

agac_olasilik = agac_model.predict_proba(dogrulama[ozellikler])[:, 1]
agac_tahmin_030 = (agac_olasilik >= 0.30).astype(int)

print("\nAgac modeli — esik 0.30:")
print("Alir denilen musteri:", agac_tahmin_030.sum())
print(
    f"Precision: %{precision_score(gercek, agac_tahmin_030, zero_division=0) * 100:.2f}"
)
print(
    f"Recall: %{recall_score(gercek, agac_tahmin_030, zero_division=0) * 100:.2f}"
)
print(confusion_matrix(gercek, agac_tahmin_030, labels=[0, 1]))

from sklearn.metrics import average_precision_score

print("\nEkim siralama karsilastirmasi:")
print(f"Tekrar alisveris orani: {gercek.mean():.3f}")
print(
    "Lojistik regresyon AP:",
    round(average_precision_score(gercek, olasiliklar), 3),
)
print(
    "Agac modeli AP:",
    round(average_precision_score(gercek, agac_olasilik), 3),
)

kasim = pd.read_csv(
    klasor / "data/processed/musteriler_2011-11-01.csv"
)

kasim_gercek = kasim["tekrar_aldi"]
kasim_skor = model.predict_proba(kasim[ozellikler])[:, 1]
kasim_tahmin = (kasim_skor >= 0.30).astype(int)

print("\nKasim — lojistik regresyon, esik 0.30:")
print("Musteri sayisi:", len(kasim))
print("Alir denilen musteri:", kasim_tahmin.sum())
print(
    f"Precision: %{precision_score(kasim_gercek, kasim_tahmin, zero_division=0) * 100:.2f}"
)
print(
    f"Recall: %{recall_score(kasim_gercek, kasim_tahmin, zero_division=0) * 100:.2f}"
)
print("AP:", round(average_precision_score(kasim_gercek, kasim_skor), 3))
print(confusion_matrix(kasim_gercek, kasim_tahmin, labels=[0, 1]))

kasim_sonuclar = kasim[["CustomerID", "tekrar_aldi"]].copy()
kasim_sonuclar["tekrar_alisveris_skoru"] = kasim_skor
kasim_sonuclar["tahmin_030"] = kasim_tahmin

cikti = klasor / "data/processed/kasim_model_sonuclari.csv"
kasim_sonuclar.to_csv(cikti, index=False, encoding="utf-8-sig")

print("\nTahminler kaydedildi:", cikti)