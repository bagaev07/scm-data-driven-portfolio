# Data-Driven SCM Analytics: Bridging SCOR Operational Reliability & Financial Performance

This project demonstrates how data engineering and advanced SQL analytics are applied to bridge the gap between supply chain operations and corporate finance. Using the **ASCM/SCOR (Supply Chain Operations Reference) framework**, this repository contains an end-to-end data analytics model that quantifies how logistical disruptions and service level degradation directly impact working capital, liquidity, and financial performance.

## 🏢 Business Context & Problem Statement
In supply chain management, operations and corporate finance often operate in isolated silos:
* **The CFO Goal:** Maximize capital velocity and minimize inventory holding costs to boost **Return on Working Capital (ROWC)**.
* **The Logistics Reality:** Aggressive inventory reductions without tracking supply chain volatility create severe **Out-of-Stock (OOS)** risks, degrade service levels (**Perfect Order Fulfillment - POF**), and freeze cash flow when documentation errors delay accounts receivable.

This project simulates real-world FMCG supply chain transactions to isolate variables behind Key Account (KA) service degradation and maps operational failures to their financial root causes.

---

## 🛠️ Tech Stack & Architecture
* **Database Engine:** PostgreSQL
* **Data Engineering:** Python (Pandas, SQLAlchemy) for generating synthetic transactional and asset distribution datasets.
* **SQL Techniques:** Common Table Expressions (CTEs), Conditional Pivoting (`CASE WHEN`), Data Type Casting, and Advanced Aggregations.

---

## 📊 Analytical Pipeline & SQL Implementations

### Phase 1: Operational Reliability (SCOR Perfect Order Fulfillment)
This phase isolates whether service level drops in the Key Account segment are caused by internal warehouse picking inefficiencies or 3PL carrier bottlenecks.

```sql
-- 1. Isolating 3PL Logistics Bottlenecks
-- Identifies orders that were 100% fully assembled at the warehouse (is_in_full = 1) but arrived late (is_on_time = 0)
SELECT *
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_on_time = 0
  AND is_in_full = 1;

-- 2. Perfect Order Fulfillment (POF) Absolute Metric
-- Calculates the exact number of flawless deliveries across all 4 SCOR criteria simultaneously
SELECT COUNT(*)
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_in_full = 1 
  AND is_on_time = 1 
  AND is_doc_accurate = 1 
  AND is_perfect_condition = 1;
```

### Phase 2: Financial Supply Chain Analytics (Capital Velocity & S&OP Dashboard)
Tracks capital turnaround times across quarters and establishes an automated Executive Dashboard evaluating returns on supply chain assets.

```sql
-- 1. Supply Chain Capital Velocity (Days Supply of Inventory + DSO)
-- Joins quarterly financial performance with monthly asset valuations to track capital turnaround time
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

-- 2. Strategic Executive S&OP Dashboard (ROWC & ROFA)
-- Calculates return on working capital and fixed supply chain assets with automated performance flags
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

---

## 💡 Strategic SCM Insights & Strategic Decisions
1. **The Hidden Synergy (POF vs. ROWC):** The queries prove that a breakdown in operational components—specifically documentation accuracy (`is_doc_accurate = 0`)—directly causes financial delays. Missing or incorrect shipping papers prevent customers from clearing invoices on time, expanding **Days Sales Outstanding (DSO)**, inflating **Accounts Receivable**, and locking up cash flow.
2. **Mitigating "Blind" Optimization:** Blindly slashing safety stocks to maximize financial metrics destroys supply chain **Agility**. To balance this trade-off, a dynamic stock differentiation strategy must be deployed: establishing a 98% POF target with a robust **Safety Stock** buffer for high-margin SKU groups, while shifting low-margin items to **Cross-Docking** (85% POF target) to unlock **Working Capital**.

---
## 🚀 How to Run the Project
1. Clone the repository: `git clone https://github.com`
2. Set up a PostgreSQL instance named `scm_portfolio`.
3. Run the data generation script: `python generate_data.py` (populates data into `scor_orders_log`, `sc_current_assets`, and `sc_finance_performance`).
4. Execute queries inside the `queries/` folder to view S&OP metrics.

