TRUNCATE TABLE t_settle_amount_info; insert into t_settle_amount_info( period , alipay_settle , alipay_settle_p , alipay_settle_r , alipay_settle_usd , alipay_settle_p_usd , alipay_settle_r_usd , alipay_fee_usd , account_fee)
SELECT period ,
         sum(alipay_settle) ,
         sum(alipay_settle_p) ,
         sum(alipay_settle_r) ,
         sum(alipay_settle_usd) ,
         sum(alipay_settle_p_usd) ,
         sum(alipay_settle_r_usd) ,
         sum(alipay_fee_usd) ,
         sum(account_fee)
FROM 
    (SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) AS period , sum(Rmb_settlement) alipay_settle , 0 AS alipay_settle_p , 0 AS alipay_settle_r , sum(Settlement) AS alipay_settle_usd , 0 AS alipay_settle_p_usd , 0 AS alipay_settle_r_usd , sum(Fee) AS alipay_fee_usd , 0 AS account_fee
    FROM load_settledetails_info
    GROUP BY  SUBSTR(Settlement_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) , 0 , sum(Rmb_amount) , 0 , 0 , sum(Amount) , 0 , 0 , 0
    FROM load_settledetails_info
    WHERE Type = 'P'
    GROUP BY  SUBSTR(Settlement_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) , 0 , 0 , sum(Rmb_amount) , 0 , 0 , sum(Amount) , 0 , 0
    FROM load_settledetails_info
    WHERE Type = 'R'
    GROUP BY  SUBSTR(Settlement_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(Settlement_time
    FROM 1 FOR 10) , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(Fee * Rate)
    FROM load_settledetails_info
    GROUP BY  SUBSTR(Settlement_time
    FROM 1 FOR 10)) t
GROUP BY  period; 