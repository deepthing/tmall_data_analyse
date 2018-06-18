-- 数据初始化 TRUNCATE TABLE t_monthly_order_amount; -- 数据生成 insert into t_monthly_order_amount( fin_period , actual_paid , alipay_actual_recieve , refund , order_fee , account_fee , alipay_get)
SELECT order_date ,
         sum(actual_paid) ,
         sum(alipay_actual_recieve) ,
         sum(refund) ,
         sum(order_fee) ,
         sum(account_fee) ,
         sum(alipay_get)
FROM 
    (SELECT SUBSTR(create_time
    FROM 1 FOR 10) AS order_date , sum(actual_paid) AS actual_paid , 0 AS alipay_actual_recieve , 0 AS refund , 0 AS order_fee , 0 AS account_fee , 0 AS alipay_get
    FROM load_tmallso_info
    GROUP BY  SUBSTR(create_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(payment_time
    FROM 1 FOR 10) AS order_date , 0 AS actual_paid , sum(rmb_amount) AS alipay_actual_recieve , sum(refund * Rate) AS refund , 0 AS order_fee , 0 AS account_fee , 0 AS alipay_get
    FROM load_strade_info
    GROUP BY  order_date
    UNION
    SELECT SUBSTR(payment_time
    FROM 1 FOR 10) AS order_date , 0 AS actual_paid , 0 AS alipay_actual_recieve , 0 AS refund , sum(fee_amount) AS order_fee , 0 AS account_fee , 0 AS alipay_get
    FROM load_fee_info
    GROUP BY  order_date
    UNION
    SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) AS order_date , 0 AS actual_paid , 0 AS alipay_actual_recieve , 0 AS refund , 0 AS order_fee , sum(amount) AS account_fee , 0 AS alipay_get
    FROM load_myaccount_info
    GROUP BY  order_date
    UNION
    SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) AS order_date , 0 AS actual_paid , 0 AS alipay_actual_recieve , 0 AS refund , 0 AS order_fee , 0 AS account_fee , sum(Rmb_settlement) AS alipay_get
    FROM load_settledetails_info
    GROUP BY  order_date
    UNION
    SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) AS order_date , 0 AS actual_paid , 0 AS alipay_actual_recieve , ABS(sum(Rmb_amount)) AS refund , 0 AS order_fee , 0 AS account_fee , 0 AS alipay_get
    FROM load_settledetails_info
    WHERE Type = 'R'
    GROUP BY  order_date) AS t
GROUP BY  order_date; 