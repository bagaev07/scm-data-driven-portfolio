/*

WITH

assets_per_month AS (SELECT period,
    SUM(value) AS total_assets
    FROM sc_current_assets
    GROUP BY period),

fixed_per_month AS (
    SELECT period,
    SUM(warehouse_value + fleet_value + it_systems_value) AS total_fixed_assets
    FROM sc_fixed_assets 
    GROUP BY period
    )

SELECT sc_finance.period,
    ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) AS ROWC,
    ((sc_finance.revenue - sc_finance.cogs) / assets_per_month.total_assets::numeric) AS ROFA,
    CASE
        WHEN ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) > 0.40 THEN 'High'
        WHEN ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) BETWEEN 0.20 AND 0.40 THEN 'Medium'
        WHEN ((sc_finance.revenue - sc_finance.cogs) / fixed_per_month.total_fixed_assets::numeric) < 0.20 THEN 'Low'
    END AS rowc_status
FROM sc_finance_performance AS sc_finance
LEFT OUTER JOIN assets_per_month ON sc_finance.period = assets_per_month.period
LEFT OUTER JOIN fixed_per_month ON sc_finance.period = fixed_per_month.period

*/

/*
SELECT sc_finance.revenue - sc_finance.cogs
FROM sc_finance_performance AS sc_finance
*/




/* WITH

assets_per_month AS (SELECT period,
    SUM(value) AS total_assets
    FROM sc_current_assets
    WHERE period LIKE '%2025%'
    GROUP BY period)


SELECT 
    CASE 
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (1, 2, 3) THEN 'Q1'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (4, 5, 6) THEN 'Q2'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (7, 8, 9) THEN 'Q3'
    ELSE 'Q4'
    END AS quarter,
    (AVG(assets_per_month.total_assets)/SUM(cogs)) * 90
FROM sc_finance_performance AS sc_finance
JOIN assets_per_month ON sc_finance.period = assets_per_month.period
GROUP BY CASE 
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (1, 2, 3) THEN 'Q1'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (4, 5, 6) THEN 'Q2'
        WHEN CAST(RIGHT(sc_finance.period, 2) AS INT) IN (7, 8, 9) THEN 'Q3'
    ELSE 'Q4'
    END
ORDER BY quarter;
*/ 

/*SELECT *
FROM sc_current_assets AS sc_assets
INNER JOIN sc_finance ON sc_assets.period = sc_finance.period
*/

--FULL OUTER JOIN sc_current_assets.period ON sc_finance_performance = sc_current_assets

/*
SELECT 
    SUM(CASE WHEN asset_type = 'Inventory' THEN value END) AS inventory_val,
    SUM(CASE WHEN asset_type = 'Accounts Receivable' THEN value END) AS accounts_receivable_val,
    SUM(CASE WHEN asset_type = 'Cash' THEN value END) AS cash_val
FROM sc_current_assets
*/



