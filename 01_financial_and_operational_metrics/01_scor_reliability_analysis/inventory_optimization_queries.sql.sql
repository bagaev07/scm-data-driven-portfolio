SELECT sku_name,
    vendor_name,
    COUNT(po_id) AS total_orders,
    ROUND(AVG(actual_lead_time),2) AS avg_lead_time,
    ROUND(AVG(average_daily_demand),2) AS avg_daily_demand,
    ROUND(STDDEV_SAMP(actual_lead_time), 2) AS std_dev
FROM mars_raw_materials_orders
GROUP BY sku_name, vendor_name



/*

SELECT vendor_name,
    COUNT(po_id),
    MAX(actual_lead_time),
    ROUND(AVG(actual_lead_time),2)
FROM mars_raw_materials_orders
GROUP BY vendor_name
ORDER BY AVG(actual_lead_time) DESC;

*/

/* 
SELECT *
FROM mars_raw_materials_orders
WHERE sku_name = 'PM-003-Film' AND vendor_name = 'China Pack Ltd'
AND actual_lead_time > 30
*/