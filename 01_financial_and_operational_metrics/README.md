# SCOR Operational Reliability & Financial Performance Model
This repository holds a PostgreSQL-backed model that maps logistical disruptions to liquidity impact. It translates everyday supply chain volatility — such as service level drops and delivery failures — into hard financial metrics like ROWC and DSO.

## Problem Statement: The SCM & Finance Gap
This model addresses the classic misalignment between inventory optimization and customer service levels. Aggressive inventory reductions often lead to a high stockout rate, tanking the POF metric. Furthermore, backend issues like invoice inaccuracies delay Accounts Receivable, trapping cash. The project uses a synthetic FMCG dataset to run data-driven root-cause analysis on how logistical failures impact cash flow.

---

##  Stack & SQL Pipeline
Built on PostgreSQL with synthetic data pipeline via Python. The analytical core focuses on two areas:
1. Operational Focus: Running binary slicing on 4 SCOR criteria to calculate exact Perfect Order Fulfillment (POF).
2. Financial Focus: Calculating quarterly capital turnover days, ROWC, and ROFA using dynamic asset valuations.
---

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

## Key Takeaways
• Operational Failures = Frozen Cash: Documentation errors delay customer billing, directly expanding DSO and locking up liquidity.
• Smart Buffering: Instead of blanket inventory cuts, the data backs a tiered safety stock strategy (98% POF for core SKUs vs. 85% via cross-docking for tail items).

## 
