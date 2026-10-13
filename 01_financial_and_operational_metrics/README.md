# SCOR Operational Reliability & Financial Performance Model
This project shows how to connect supply chain operations with corporate finance using data and SQL. Based on the ASCM/SCOR framework, this PostgreSQL model quantifies how everyday logistics problems (like shipping delays and paperwork errors) directly impact working capital, liquidity, and financial performance.

## Problem Statement: The SCM & Finance Gap
In many companies, logistics and finance teams work separately and have different goals:
*   **The Finance Goal**: Cut inventory and reduce holding costs to improve Return on Working Capital (**ROWC**).
*   **The Logistics Reality**: Fast inventory cuts without a clear plan create **stockout risks** and drop service levels (**Perfect Order Fulfillment - POF**). Also, small mistakes in documents delay customer payments and trap cash.

This project uses a synthetic FMCG dataset to run a data-driven root-cause analysis. It shows exactly how operational failures damage cash flow.

---

##  Stack & SQL Pipeline
Built on **PostgreSQL** with a synthetic data pipeline created via **Python**. The analytics focus on three main areas:
1.  **Operational Focus**: Running binary slicing on 4 SCOR criteria to calculate the exact **Perfect Order Fulfillment (POF)** metric.
2.  **Financial Focus**: Calculating quarterly **capital turnover days**, **ROWC**, and **ROFA** using monthly asset values.
3.  **Inventory Optimization**: Extracting lead time volatility via SQL and building a What-If simulation model in Excel.

---

### Phase 1: Operational Reliability (SCOR POF)
This phase isolates whether service level drops in the Key Account segment are caused by internal warehouse inefficiencies or 3PL carrier bottlenecks.

#### 1. Isolating 3PL Logistics Bottlenecks
This query finds orders that the warehouse prepared perfectly (`is_in_full = 1`), but the carrier delivered late (`is_on_time = 0`) at border crossings:

```sql
SELECT *
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_on_time = 0
  AND is_in_full = 1;
```

#### 2. Perfect Order Fulfillment (POF) Absolute Metric
This query calculates the number of 100% flawless deliveries where all 4 SCOR criteria are met at the same time:

```sql
SELECT COUNT(*)
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_in_full = 1 
  AND is_on_time = 1 
  AND is_doc_accurate = 1 
  AND is_perfect_condition = 1;
```

### Phase 2: Financial Supply Chain Analytics (Capital Velocity)
This phase maps operational delays to financial cycles, tracking capital turnaround times and overall returns on supply chain assets.

#### 1. Supply Chain Capital Velocity (Days Supply of Inventory + DSO)
This query joins quarterly financial performance with monthly asset valuations to track capital turnaround time:

```sql
WITH assets_per_month AS (
    SELECT period, SUM(value) AS total_assets
    FROM sc_current_assets
    WHERE period LIKE '%2025%'
    GROUP BY period
)
SELECT 
    CASE 
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (1, 2, 3) THEN 'Q1'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (4, 5, 6) THEN 'Q2'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (7, 8, 9) THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    (AVG(assets_per_month.total_assets) / SUM(cogs)) * 90 AS capital_turnover_days
FROM sc_finance_performance AS sc_finance
JOIN assets_per_month ON sc_finance.period = assets_per_month.period
GROUP BY 1
ORDER BY quarter;
```
#### 2. Strategic Executive S&OP Dashboard (ROWC & ROFA)
This query calculates return on working capital and fixed supply chain assets with automated performance flags:

```sql
WITH assets_per_month AS (
    SELECT period, SUM(value) AS total_assets
    FROM sc_current_assets
    GROUP BY period
),
fixed_per_month AS (
    SELECT period, SUM(warehouse_value + fleet_value + it_systems_value) AS total_fixed_assets
    FROM sc_fixed_assets 
    GROUP BY period
)
SELECT sc_finance.period,
    ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) AS ROFA,
    ((sc_finance.revenue - sc_finance.cogs) / assets_per_month.total_assets::numeric) AS ROWC,
    CASE
        WHEN ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) > 0.40 THEN 'High'
        WHEN ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) BETWEEN 0.20 AND 0.40 THEN 'Medium'
        ELSE 'Low'
    END AS rowc_status
FROM sc_finance_performance AS sc_finance
LEFT JOIN assets_per_month ON sc_finance.period = assets_per_month.period
LEFT JOIN fixed_per_month ON sc_finance.period = fixed_per_month.period;
```
## Phase 3: Inventory Optimization & Lead Time Variability (FMCG Case Study)

### Business Problem
We need to balance customer service levels (POF) and working capital speed at a Global FMCG Enterprise. Raw materials (like cocoa beans and packaging film) often have unstable delivery times at borders. Cutting stock without a plan reduces costs but can stop factory production.

### Data & Analytical Solutions
1. **SQL Data Extraction (`inventory_optimization_queries.sql`):** I analyzed 1,000 transaction logs to find average demand and lead time stability using the `STDDEV_SAMP` function:
```sql
SELECT sku_name, 
       vendor_name, 
       COUNT(po_id) AS total_orders,
       ROUND(AVG(actual_lead_time), 2) AS avg_lead_time,
       ROUND(AVG(average_daily_demand), 2) AS avg_daily_demand,
       ROUND(STDDEV_SAMP(actual_lead_time), 2) AS std_dev
FROM raw_materials_orders
GROUP BY sku_name, vendor_name;
```
2. **Excel Financial Modeling & What-If Simulation:**
I built a dynamic inventory model using absolute cell references for the Service Factor (Z-score) to calculate risk:
*   **Safety Stock Formula**: `=StdDev_LT * Avg_Demand * Z`
*   **Reorder Point (ROP) Formula**: `=(Avg_LT * Avg_Demand) + Safety_Stock`

#### Simulation Results
*   **Scenario A (98% Service Level | Z = 2.05)**: Total Safety Stock = **8,263.95 units**. This gives maximum protection against delivery delays.
*   **Scenario B (95% Service Level | Z = 1.65)**: Total Safety Stock = **6,651.47 units**.
*   **Financial Impact**: Moving from Scenario A to Scenario B frees **1,612.48 units of raw materials** from Working Capital. This improves cash flow, but increases stockout risks for long-distance items (like raw materials from overseas).

---

## Key Takeaways
*   **Operational Failures = Frozen Cash**: Small mistakes in shipping documents delay customer billing. This directly increases **Days Sales Outstanding (DSO)** and locks up company liquidity.
*   **Smart Buffering**: Instead of **blanket inventory cuts**, the data backs a tiered **safety stock** strategy (98% POF for core SKUs vs. 85% via cross-docking for tail items).

## 
