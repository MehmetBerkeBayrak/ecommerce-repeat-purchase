\# PostgreSQL Setup



1\. Create a separate database named ecommerce\_repeat\_purchase.

2\. Open Query Tool in that database and run 01\_create\_customer\_table.sql.

&#x20;  This expects a fresh database without public.musteriler\_kasim.

3\. In pgAdmin, right-click public.musteriler\_kasim and select Import/Export Data.

4\. Import data/processed/musteriler\_2011-11-01.csv with:

&#x20;  - Format: CSV

&#x20;  - Encoding: UTF8

&#x20;  - Header: enabled

&#x20;  - Delimiter: comma

&#x20;  - All seven columns selected in table order

5\. Run 02\_customer\_analysis.sql.



Expected checks:

\- Total customers: 3,974.

\- Outcome 0: 2,633; outcome 1: 1,341.

\- Recency group counts: 1,364 / 1,097 / 1,513.

\- Repeat-purchase rates: 45.60% / 39.56% / 18.84%.



The original project database was created before the seventh feature column

was added. This setup script targets the updated seven-column CSV.



The updated seven-column setup was tested in a separate empty database

on 21 November 2026. Import checks returned 3,974 customers and 1,341

repeat buyers, with the new feature populated for all customers.

The recency-group counts and repeat-purchase rates matched the original analysis.

