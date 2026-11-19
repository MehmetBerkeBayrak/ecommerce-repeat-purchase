\# Data Quality Review



\## Source inspection

\- Raw rows: 541,909.

\- Missing CustomerID: 135,080 rows (24.93% of rows).

\- Missing Description: 1,454 rows.

\- Cancellation-prefixed rows: 9,288.

\- Negative-quantity rows: 10,624.

\- Zero-price rows: 2,515.

\- Negative-price rows: 2, both described as "Adjust bad debt".



\## Decisions

\- Preserve the raw workbook unchanged.

\- Exclude missing customer IDs from customer-level analysis.

&#x20; Do not combine them into one artificial customer.

\- Define candidate purchases as non-cancellation rows with positive

&#x20; quantity and positive price. Customer features also require CustomerID.

\- Retain cancellation and adjustment records in the raw data.

&#x20; Do not interpret all negative quantities as customer returns.

\- Retain exact duplicate rows provisionally because their cause is unknown.



\## Duplicate sensitivity check

Removing exact duplicates from candidate purchase rows reduced the amount

from GBP 10,666,684.54 to GBP 10,642,110.80.

The number of distinct invoices remained 19,960.

These amounts exclude cancellations and are not net revenue.



\## November snapshot

\- Prediction time: 2011-11-01 00:00.

\- Features use purchases strictly before prediction time.

\- Label window: 2011-11-01 inclusive to 2011-12-01 exclusive.

\- Customers: 3,974; one row per customer.

\- Repeat purchase observed: 1,341; not observed: 2,633.

\- Features: recency in days, distinct invoice count, positive purchase amount.

\- No missing values in these features or the label.

\- Model training and evaluation have not yet been performed.

