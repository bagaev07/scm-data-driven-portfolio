--CREATE DATABASE scm_portfolio;


/* Isolate Carrier Failures

SELECT *
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_on_time = 0
  AND is_in_full = 1;

*/

/* Perfect Order Fulfillment

SELECT COUNT(*)
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)'
  AND is_in_full = 1
  AND is_on_time = 1
  AND is_doc_accurate = 1
  AND is_perfect_condition = 1;


*/

/* OTIF (On Time In Full)

SELECT COUNT(*) AS all_orders,
    COUNT(CASE WHEN is_on_time = 1 THEN 1 END) AS OTIF,
    ROUND(
        COALESCE(
            COUNT(CASE WHEN is_on_time = 1 THEN 1 END)::NUMERIC / NULLIF(COUNT(*),0) *100,
        0), 
    2) AS otif_percentage
FROM scor_orders_log
WHERE client_segment = 'Key Account (KA)';

*/



