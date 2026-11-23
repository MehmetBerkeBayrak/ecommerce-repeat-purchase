# Repeat Purchase Explorer


An independent portfolio project simulating an e-commerce client engagement.
It combines a data-quality review, SQL analysis, a Power BI report,
machine learning, and a local customer prediction interface.

## Business question


Which existing customers will make an eligible purchase within the next 30 days?
This predicts purchasing behavior, not the effect of sending a campaign.
The project was not commissioned by the source retailer.

## Data and preparation


Source: [UCI Online Retail](https://doi.org/10.24432/C5BW33), CC BY 4.0.
The workbook contains 541,909 invoice-item rows. Customer features use
non-cancellation rows with a customer ID, positive quantity, and positive price.
Exact duplicate rows are provisionally retained; their impact is documented.
Purchase amounts exclude cancellations and are not net revenue.
The original workbook is preserved locally and excluded from Git.
See `docs/DATA_INTAKE.md` and `docs/DATA_QUALITY.md`.

## Model development


Features are calculated strictly before each snapshot:

- Days since last purchase
- Historical distinct invoice count
- Historical positive purchase amount
- Distinct invoices in the previous 30 days

September 2011 is used for training, October for validation, and November
for a later-period check. Customer IDs and outcome labels are not model inputs.
The selected pipeline uses StandardScaler and logistic regression,
with a decision threshold of 0.30.

| Metric | October validation | November check |
| --- | ---: | ---: |
| Precision | 45.34% | 55.60% |
| Recall | 57.32% | 58.46% |
| Average precision | 0.539 | 0.635 |

November includes 3,974 customers: 784 true positives, 626 false positives,
557 false negatives, and 2,007 true negatives.
November outcomes had already been explored, so this is not a fully untouched
test set. Customers may appear in multiple snapshots. Probability calibration
has not been independently assessed. See `docs/MODEL_RESULTS.md`.

## Run the historical demo


From PowerShell in the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe musteri_api.py
```

Open http://127.0.0.1:8001/ and enter a customer ID from the November snapshot.
The JSON endpoint is `/api/musteri/17850`.
The application loads the saved model without retraining.
It runs locally on historical data, not on live customer records.
Only load trusted joblib files. Use the recorded dependency versions when
loading this project's saved model.

## Main files


- `veri_inceleme.py`: source inspection and customer feature preparation.
- `model_verisi.py`: snapshot generation; currently configured for November.

&#x20; Change both the snapshot date and output filename to generate another period.

- `model_egitimi.py`: model training, evaluation, and saving.
- `model_kontrol.py`: saved-model loading check.
- `musteri_sorgula.py`: customer lookup and prediction.
- `musteri_api.py` and `index.html`: local API and English interface.
- `Customer_Repeat_Purchase.pbix`: analysis and model evaluation report.

Processed snapshots and the saved model support the demo. Rebuilding from
source requires the UCI workbook at `data/raw/Online Retail.xlsx`.
Update local CSV source paths in Power BI before refreshing on another computer.

## Dimensional Data Warehouse

This project also includes a PostgreSQL retail sales warehouse
and a connected Power BI report.

The star schema contains fact_sales, dim_product, dim_customer,
and dim_date. The fact table grain is one eligible source
invoice-item row. Exact duplicate source rows are retained.

Verified results:
- 530,104 sales lines and 19,960 distinct invoices.
- GBP 10,666,684.54 in positive sales amounts.
- No sales with missing dimension relationships.
- Power BI totals reconciled with PostgreSQL.

Amounts exclude cancellations and do not represent net revenue.
Missing customer identities map to a shared Unknown dimension member.

See [warehouse documentation](docs/WAREHOUSE.md) for setup,
data rules, and validation results.

Power BI report: [Retail Data Warehouse](data/Retail_Data_Warehouse.pbix).
