\# Retail Sales Data Warehouse



An independent portfolio extension using the UCI Online Retail dataset.

This project simulates a client reporting requirement.



\## Model



PostgreSQL star schema in the dw schema:



\- fact\_sales: one eligible source invoice-item row per record.

\- dim\_product: one record per stock code.

\- dim\_customer: known customer IDs plus one Unknown member.

\- dim\_date: one record per calendar day across the source date range.



Dimensions use surrogate keys. The date key uses YYYYMMDD.

Power BI relationships are active, one-to-many, and single-direction

from dimensions to the fact table.



\## Data rules



Eligible rows have a non-cancellation invoice number, positive quantity,

and positive unit price. Missing customer IDs map to Unknown.

Unknown represents missing identity, not one real customer.



Exact duplicate source rows are provisionally retained.

Product descriptions use the most frequent non-empty description per

stock code, with alphabetical tie-breaking. Description history is not modeled.



Amounts represent positive sales, not net revenue.

December 2011 contains data through December 9 only.



\## Initial setup



1\. Place the source workbook at data/raw/Online Retail.xlsx.

2\. Run ambar\_kontrol.py to generate warehouse CSV files.

3\. Run sql/04\_warehouse\_schema.sql in a fresh dw schema.

4\. Import the CSV files into dw.dim\_product, dw.dim\_customer,

&#x20;  and dw.stg\_sales. Match the CSV headers to the target columns.

&#x20;  Exclude generated identity columns from the imports.

5\. Run sql/05\_warehouse\_load.sql once.

6\. Run sql/03\_warehouse\_validation.sql and compare the results below.

7\. Open data/Retail\_Data\_Warehouse.pbix and configure the PostgreSQL

&#x20;  connection and credentials for your environment.



The load script is for an initial load, not incremental refresh.

The demonstrated database is ecommerce\_repeat\_purchase on localhost:5432.



\## Verified results



\- Fact and staging rows: 530,104 each.

\- Positive sales amount: GBP 10,666,684.54 in each table.

\- Products: 3,922.

\- Known customer members: 4,338; Unknown members: 1.

\- Calendar dates: 374.

\- Distinct eligible invoices: 19,960.

\- Sales without a matching product, customer, or date: 0.

\- Known-identity sales: 397,884 rows; GBP 8,911,407.90.

\- Unknown-identity sales: 132,220 rows; GBP 1,755,276.64.

\- November 2011 positive sales: GBP 1,509,496.33.



Power BI totals and the November and customer-status breakdowns

were checked against PostgreSQL query results.



\## Report



The Power BI report includes total positive sales, sales-line count,

distinct invoice count, monthly sales, customer identity status,

and the top 10 products by positive sales amount.



Products are displayed using stock code plus description to avoid

combining different stock codes with the same description.



