TRUNCATE TABLE t_myaccount_monthly_info; insert into t_myaccount_monthly_info( period , recharge , refund , payment , order_payment , not_order_payment)
SELECT trans_date ,
         sum(recharge) ,
         sum(refund) ,
         sum(payment) ,
         sum(order_payment) ,
         sum(not_order_payment)
FROM 
    (SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) AS trans_date , sum(Amount) AS recharge , 0 AS refund , 0 AS payment , 0 AS order_payment , 0 AS not_order_payment
    FROM load_myaccount_info
    WHERE type = 'recharge'
    GROUP BY  SUBSTR(Trans_Date
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) , 0 , sum(Amount) AS refund , 0 , 0 , 0
    FROM load_myaccount_info
    WHERE type = 'refund'
    GROUP BY  SUBSTR(Trans_Date
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) , 0 , 0 , sum(Amount) AS payment , 0 , 0
    FROM load_myaccount_info
    WHERE type = 'payments'
    GROUP BY  SUBSTR(Trans_Date
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) , 0 , 0 , 0 , sum(Amount) AS order_payment , 0
    FROM load_myaccount_info
    WHERE type = 'payments'
            AND LENGTH(Partner_Transaction_ID) > 10
    GROUP BY  SUBSTR(Trans_Date
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Trans_Date
    FROM 1 FOR 10) , 0 , 0 , 0 , 0 , sum(Amount) AS not_order_payment
    FROM load_myaccount_info
    WHERE type = 'payments'
            AND LENGTH(Partner_Transaction_ID) < 10
    GROUP BY  SUBSTR(Trans_Date
    FROM 1 FOR 10)) AS T
GROUP BY  trans_date; 