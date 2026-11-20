from pathlib import Path

import joblib
import pandas as pd

klasor = Path(__file__).parent
paket = joblib.load(klasor / "models/tekrar_alisveris.joblib")
musteriler = pd.read_csv(
    klasor / "data/processed/musteriler_2011-11-01.csv"
)


def musteri_sorgula(musteri_id):
    kayit = musteriler.loc[musteriler["CustomerID"] == musteri_id]

    if kayit.empty:
        return {"hata": "Musteri bu tarihsel tabloda bulunamadi."}

    skor = paket["pipeline"].predict_proba(
        kayit[paket["ozellikler"]]
    )[0, 1]

    return {
        "musteri_id": musteri_id,
        "tahmin_tarihi": "2011-11-01",
        "model_skoru": float(skor),
        "esik": paket["esik"],
        "tahmin": int(skor >= paket["esik"]),
    }


if __name__ == "__main__":
    kimlik = int(input("Musteri kimligi: "))
    print(musteri_sorgula(kimlik))