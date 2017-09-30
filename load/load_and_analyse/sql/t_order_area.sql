SELECT SUBSTR( recieve_address ,
         1 ,
         POSITION(' ' IN recieve_address) - 1)
FROM load_tmallso_info; TRUNCATE TABLE t_order_area; INSERT INTO t_order_area( area_info , province , fin_period , order_number , order_amount)
SELECT IFNULL( CONCAT(t2.area_code ,
         '-' , t2.area_name) , '9-其他') , SUBSTR( t1.recieve_address , 1 , POSITION(' ' IN t1.recieve_address) - 1) AS province , substr(t1.create_time , 1 , 10) AS create_date , count(*) , IFNULL(sum(t1.amount) , 0)
FROM load_tmallso_info t1
LEFT JOIN t_bas_area_info t2
    ON SUBSTR( t1.recieve_address , 1 , POSITION(' ' IN t1.recieve_address) - 1) = t2.province
WHERE t1.order_status = '交易成功'
GROUP BY  create_date , province