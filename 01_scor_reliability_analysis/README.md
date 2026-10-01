# Data-Driven SCM: Integrating Operational Reliability with Corporate Finance (SCOR Model)

## 📌 Executive Summary & Business Context
Working within international logistics and freight forwarding, I witness operational disruptions daily. However, managing supply chains efficiently requires looking beyond physical transport metrics. This project establishes a direct, data-driven link between operational logistics defects (SLA breaches, document errors) and corporate financial performance (**Return on Working Capital - ROWC**, **Return on Supply Chain Fixed Assets - ROFA**, and **Capital Velocity**).

By applying the **SCOR Model Framework**, this repository demonstrates how custom data engineering and SQL analytics can solve the classic **Supply Chain Triangle Trade-off**: balancing customer service levels against operating costs and working capital efficiency.

---

## 🛠️ Tech Stack & Architecture
- **Environment:** Windows 11, VS Code
- **Database Engine:** PostgreSQL (Centralized `scm_portfolio` database)
- **Data Engineering:** Python (Pandas, SQLAlchemy) utilizing synthetic FMCG datasets to simulate real-world logistics challenges.
- **SQL Analytics:** Advanced Data Slicing (`WHERE`), Conditional Pivoting (`CASE WHEN`), Common Table Expressions (CTEs), and Explicit Data Type Casting.

---

## 📊 Phase 1: Operational Reliability (SCOR Perfect Order Fulfillment)

### Business Problem
A strategic customer segment, 'Key Account (KA)', experienced service level degradation. This phase isolates variables to determine whether the root cause stems from warehouse picking inefficiencies or 3PL carrier failures.

### SQL Implementation (`phase1_scor_reliability.sql`)
1. **Isolating 3PL Logistics Bottlenecks:** Extracting shipments that were 100% fully assembled at the warehouse (`is_in_full = 1`) but arrived late (`is_on_time = 0`) to enforce SLA penalties:
```sql
SELECT *
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_on_time = 0
  AND is_in_full = 1;
```

2. **Perfect Order Fulfillment (POF) Absolute Count:** Identifying flawless deliveries where all 4 conditions (In-Full, On-Time, Accurate Docs, Perfect Condition) were met simultaneously:
```sql
SELECT COUNT(*)
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_in_full = 1 AND is_on_time = 1 
  AND is_doc_accurate = 1 AND is_perfect_condition = 1;
```

---

## 💰 Phase 2: Financial Supply Chain Analytics (Capital Velocity & ROI)

### Business Problem
Operational delays do not exist in a vacuum—they freeze cash in buffer stocks and delay accounts receivable collection. This phase analyzes how logistics assets and working capital efficiency behave under operational stress.

### SQL Implementation (`phase2_financial_performance.sql`)

1. **Data Pivoting (Long to Wide Format):** Transforming transactional asset logs into structured financial metrics:
```sql
SELECT period,
    SUM(CASE WHEN asset_type = 'Inventory' THEN value END) AS inventory_val,
    SUM(CASE WHEN asset_type = 'Accounts Receivable' THEN value END) AS accounts_receivable_val,
    SUM(CASE WHEN asset_type = 'Cash' THEN value END) AS cash_val
FROM sc_current_assets
GROUP BY period;
```

2. **Supply Chain Capital Velocity (Days Supply of Inventory + DSO):** Joining financial performance with asset valuations to track capital turnaround time across 2025 quarters:
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

3. **Strategic Executive S&OP Dashboard (ROWC & ROFA):** A comprehensive analytical query calculating returns on working capital and fixed assets (Fleet, Warehouses, IT Systems) with an automated efficiency status:
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

---

## 🎯 Strategic Insights & Actionable SCM Takeaways

- **The Trade-off Discovery:** A high **ROWC** driven by blind inventory reduction threatens service levels. Slicing the data proved that buffer stock optimization must be dynamic and differentiated.
- **The Back-Office Trap:** A simple administrative delay or error in closing documents (a failure in the operational POF metric) automatically stalls customer payments. This inflates Days Sales Outstanding (DSO), bloats Accounts Receivable, and freezes vital working capital.
- **Strategic Alignment:** By tracking these numbers via automated SQL pipelines, SCM leaders can successfully defend fixed infrastructure investments (Fleet/IT systems) during S&OP cycles by proving their direct positive impact on **ROFA**.
