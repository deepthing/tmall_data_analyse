TRUNCATE TABLE t_buyer_info; INSERT INTO t_buyer_info( buyer_name , buyer_account , is_mobile_order , create_time , mobile)
SELECT buyer_name ,
         buyer_account ,
         is_mobile_order ,
         create_time ,
         mobile
FROM load_tmallso_info
GROUP BY  buyer_account;