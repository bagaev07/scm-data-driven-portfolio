# Case 1: SCOR Reliability Metrics & Order Slicing via PostgreSQL

## 📌 Business Problem
A key customer segment, 'Key Account (KA)', reported service level degradation. As Head of Supply Chain, I tracked down the operational failures using the SCOR model (Perfect Order Fulfillment) to separate warehouse bottlenecks from 3PL carrier issues.

## 🛠️ Tech Stack & Environment
- **OS:** Windows
- **IDE:** VS Code (with SQLTools)
- **Database:** PostgreSQL
- **Data Gen:** Python (Pandas, SQLAlchemy)

## 📊 SQL Solutions & Insights

### Task 1: Isolate 3PL Carrier Failures
Identifying orders where the warehouse team picked items 100% In-Full, but the transport company failed the delivery schedule:
```sql
SELECT *
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_on_time = 0
  AND is_in_full = 1;
```
*Insight:* This slice provides a direct foundation for SLA penalties against underperforming transport providers.

### Task 2: Perfect Order Fulfillment (POF) Count
Calculating the absolute number of flawless deliveries (On-Time, In-Full, Accurate Docs, Perfect Condition):
```sql
SELECT COUNT(*)
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_in_full = 1
  AND is_on_time = 1
  AND is_doc_accurate = 1
  AND is_perfect_condition = 1;
```

### Task 3: On Time In Full (OTIF)
Calculation of the percentage of orders delivered on time and in full.
```sql
SELECT COUNT(*) AS all_orders,
    COUNT(CASE WHEN is_on_time = 1 THEN 1 END) AS OTIF,
    ROUND(
        COALESCE(
            COUNT(CASE WHEN is_on_time = 1 THEN 1 END)::NUMERIC / NULLIF(COUNT(*),0) *100,
        0), 
    2) AS otif_percentage
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)';
```

