\# Repeat-Purchase Model Results



\## Prediction task

Predict whether an existing customer makes an eligible purchase within

30 days of the snapshot date. Eligible purchases require a customer ID,

positive quantity and price, and a non-cancellation invoice.



\## Features

Calculated strictly before each snapshot:

\- Days since last purchase

\- Distinct invoice count

\- Positive purchase amount (not net revenue)

\- Distinct invoices in the previous 30 days



CustomerID and the outcome label are not model inputs.

Exact duplicate source rows are provisionally retained.



\## Development design

\- Training snapshot: 2011-09-01; 3,317 customers.

\- Validation snapshot: 2011-10-01; 3,616 customers.

\- Later-period check: 2011-11-01; 3,974 customers.



Labels cover the next 30 days, including the snapshot date and excluding

the endpoint. Scaling is fitted only on September training data.



Logistic regression and histogram gradient boosting were compared on

October. The selected model is four-feature logistic regression with a

0.30 decision threshold. It remains fitted on September.



\## Results



| Metric | October validation | November check |
| --- | ---: | ---: |
| Precision | 45.34% | 55.60% |
| Recall | 57.32% | 58.46% |
| Average precision (AP) | 0.539 | 0.635 |



November: 784 true positives, 626 false positives,

557 false negatives and 2,007 true negatives.



\## Interpretation and limitations

\- November outcomes had already been explored, so this is not a fully

&#x20; untouched test set.

\- Customers can appear in multiple snapshots. This evaluates future

&#x20; behavior of existing customers, not generalization to unseen customers.

\- Repeat-purchase prevalence differs between months.

\- Scores have not been independently assessed for probability calibration.

\- Predicting repeat purchases does not establish campaign effectiveness

&#x20; or incremental sales.

\- The 0.30 threshold is a prototype choice, not a validated business optimum.

\- Source data is historical; deployment on current customers would require

&#x20; further validation.


