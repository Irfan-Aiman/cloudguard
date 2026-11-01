# 📊 Executive Retail & Profitability Analytics
 
`PYTHON` `SQL` `POWER BI` `DATA CLEANING` `DASHBOARD DESIGN`
 
An end-to-end analytics project on the Superstore retail dataset (9,994 order lines, 5,009 orders, 2014–2017). Raw data is cleaned in Python, explored with SQL, and presented in an interactive Power BI dashboard built for executive decision-making.
 
**Business question:** Where does the business make and lose money, and what is driving the losses?
 
---
 
## 📸 Dashboard Preview
 
<!-- Export each page from Power BI (File → Export → PDF, or a screenshot) and save it under Assets/ with these names. -->
 
### Executive Overview
![Executive Overview](Assets/executive-overview.png)
 
KPI cards (Total Sales, Total Profit, Profit Margin %, Total Orders), a monthly Sales vs Profit trend, a Sales by State map, and a Sales by Region donut.
 
### Product Details
![Product Details](Assets/product-details.png)
 
Sales and profit by sub-category, plus a Category → Sub-Category matrix of sales, profit and quantity. Custom tooltip pages show top products and category share on hover.
 
---
 
## 🔍 Key Insights
 
| Metric | Value |
|---|---|
| Total Sales | $2.30M |
| Total Profit | $286.4K |
| Overall Profit Margin | 12.5% |
 
1. **Discounting destroys margin.** Orders with no discount average a 34% margin. Orders discounted above 20% lose money in aggregate, about $135K across 1,393 order lines.
2. **Furniture barely breaks even.** It brings in $742K in sales but only $18K in profit. Tables (−$17.7K) and Bookcases (−$3.5K) are loss-making sub-categories.
3. **Technology carries the business.** Copiers, Phones and Accessories are the three most profitable sub-categories.
4. **Central is the weakest region.** It has the lowest margin (7.9%) and the highest average discount (24%). West leads on both sales and margin (14.9%).
---
 
## 🧮 SQL Analysis
 
The cleaned data was loaded into SQLite and queried in DBeaver to validate the dashboard figures.
 
**Regional sales and profit, ranked by profit**
![Region profit query](Assets/sql-region-profit.png)
 
**Regional margin vs average discount**
![Region margin and discount query](Assets/sql-region-margin-discount.png)
 
The second query confirms the discount story: margin falls as average discount rises across regions.
 
---
 
## ⚙️ Workflow
 
1. **Clean (Python / pandas)** in `portfolio1.ipynb`
   - Converted date columns to datetime.
   - Checked for nulls and duplicates.
   - Engineered `Profit Margin %`, `Order Year`, `Order Month`, `Unit Price` and `Unit Cost`.
2. **Query (SQL)** using `SQL/superstore.sql`, a SQLite database holding the cleaned table.
3. **Visualise (Power BI)** in `Dashboard/portfolio.pbix`
   - Four report pages: two main pages and two tooltip pages.
   - DAX measures and a slate theme.
## 📁 Repository Structure
 
```
├── Data/
│   ├── Raw/              # Original Superstore CSV
│   └── Cleaned/          # Superstore_cleaned.csv (Python output)
├── SQL/superstore.sql    # SQLite database
├── Dashboard/portfolio.pbix
├── portfolio1.ipynb      # Cleaning & feature engineering
└── Assets/               # Screenshots
```
 
## 🛠️ Tech Stack
- **Python:** pandas, run in Google Colab
- **SQL:** SQLite, queried in DBeaver
- **Power BI:** DAX, custom tooltip pages
