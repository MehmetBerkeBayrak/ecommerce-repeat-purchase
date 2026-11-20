from pathlib import Path

import joblib
import pandas as pd

klasor = Path(__file__).parent
paket = joblib.load(klasor / "models/tekrar_alisveris.joblib")

kasim = pd.read_csv(
    klasor / "data/processed/musteriler_2011-11-01.csv"
)

skorlar = paket["pipeline"].predict_proba(
    kasim[paket["ozellikler"]]
)[:, 1]

tahminler = (skorlar >= paket["esik"]).astype(int)

print("Musteri sayisi:", len(kasim))
print("Alir tahmini:", tahminler.sum())