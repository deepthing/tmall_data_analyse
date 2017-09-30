UPDATE load_tmallso_info SET order_id = TRIM( Replace(order_id,
         '"',''));UPDATE load_tmallso_info SET order_id = TRIM(Replace(Replace(Replace(order_id,
         '\t',''),'\n',''),'\r','')); TRUNCATE TABLE tmp_tmall_monthly; insert into tmp_tmall_monthly (order_id,period,product_name,number)
SELECT a.order_id,
         SUBSTR(b.create_time
FROM 1 FOR 7),a.product_name,sum(number)
FROM load_tmallsodetail_info a, load_tmallso_info b
WHERE a.order_id = b.order_id
GROUP BY  a.order_id,a.product_name,SUBSTR(b.create_time
FROM 1 FOR 7); -- make sure you have import data
        AND change SQL statement
    ON the view -> v_fee_infoUPDATE load_fee_info SET Exchange_Rate = TRIM( Replace(Exchange_Rate,
         '"',''));UPDATE load_fee_info SET Exchange_Rate = TRIM(Replace(Replace(Replace(Exchange_Rate,
         '\t',''),'\n',''),'\r',''));UPDATE load_fee_info SET Partner_transaction_id = TRIM( Replace(Partner_transaction_id,
         '"',''));UPDATE load_fee_info SET Transaction_id = TRIM( Replace(Transaction_id,
         '"',''));UPDATE load_fee_info SET Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,
         '\t',''),'\n',''),'\r',''));UPDATE load_fee_info SET Transaction_id = TRIM(Replace(Replace(Replace(Transaction_id,
         '\t',''),'\n',''),'\r','')); TRUNCATE TABLE t_buyer_info; insert into t_buyer_info(buyer_account,buyer_name,is_mobile_order,create_time ,mobile)
SELECT buyer_account,
         buyer_name,
         is_mobile_order,
         SUBSTR(create_time
FROM 1 FOR 10) ,mobile
FROM load_tmallso_info
WHERE buyer_account is NOT NULL
GROUP BY  buyer_account;UPDATE load_settledetails_info SET Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,
         '\t',''),'\n',''),'\r',''));UPDATE load_settledetails_info SET Settle_batch_no = TRIM(Replace(Replace(Replace(Settle_batch_no,
         '\t',''),'\n',''),'\r','')); -- make sure you have import data to new table LIKE Settlefee****
        AND change SQL statement
    ON the view -> v_fee_infoUPDATE load_fee_info SET Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,
         '\t',''),'\n',''),'\r',''));UPDATE load_settlefee_info SET Transaction_id = TRIM( Replace(Transaction_id,
         '"',''));UPDATE load_settlefee_info SET Transaction_id = TRIM(Replace(Replace(Replace(Transaction_id,
         '\t',''),'\n',''),'\r',''));UPDATE load_settlefee_info SET Partner_transaction_id = TRIM( Replace(Partner_transaction_id,
         '"',''));UPDATE load_settlefee_info SET Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,
         '\t',''),'\n',''),'\r',''));UPDATE load_settlefee_info SET Fee_type = TRIM( Replace(Fee_type,
         '"',''));UPDATE load_settlefee_info SET Fee_type = TRIM(Replace(Replace(Replace(Fee_type,
         '\t',''),'\n',''),'\r',''));UPDATE load_settlefee_info SET Currency = TRIM( Replace(Currency,
         '"',''));UPDATE load_settlefee_info SET Currency = TRIM(Replace(Replace(Replace(Currency,
         '\t',''),'\n',''),'\r','')); -- make sure you have import table myaccount***
        AND change SQL statement
    ON the view -> v_myaccount_info 