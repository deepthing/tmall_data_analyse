TRUNCATE table t_settle_fee_info; insert into t_settle_fee_info( fee_time , logisitic_tax , logisitic_service , alipay_service , tmall , juhuasuan , logisitic_tax_usd , logisitic_service_usd , alipay_service_usd , tmall_usd , juhuasuan_usd)
SELECT Settle_time ,
         sum(logisitic_tax) ,
         sum(logisitic_service) ,
         SUM(alipay_service) ,
         sum(tmall) ,
         sum(juhuasuan) ,
         sum(logisitic_tax_usd) ,
         sum(logisitic_service_usd) ,
         SUM(alipay_service_usd) ,
         sum(tmall_usd) ,
         sum(juhuasuan_usd)
FROM 
    (SELECT SUBSTR(a.Settle_time
    FROM 1 FOR 10) AS Settle_time , sum(a.Fee_rmb_amount) AS logisitic_tax , 0 logisitic_service , 0 AS alipay_service , 0 AS tmall , 0 AS juhuasuan , sum(a.Fee_amount) AS logisitic_tax_usd , 0 logisitic_service_usd , 0 AS alipay_service_usd , 0 AS tmall_usd , 0 AS juhuasuan_usd
    FROM load_settlefee_info a
    WHERE a.Remark LIKE '%进口关税%'
    GROUP BY  SUBSTR(a.Settle_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(a.Settle_time
    FROM 1 FOR 10) , 0 , sum(a.Fee_rmb_amount) , 0 , 0 , 0 , 0 , sum(a.Fee_amount) , 0 , 0 , 0
    FROM load_settlefee_info a
    WHERE a.Remark LIKE '%服务费用%'
    GROUP BY  SUBSTR(a.Settle_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(a.Settle_time
    FROM 1 FOR 10) , 0 , 0 , sum(a.Fee_rmb_amount) , 0 , 0 , 0 , 0 , sum(a.Fee_amount) , 0 , 0
    FROM load_settlefee_info a
    WHERE a.Remark LIKE '%Alipay service fee%'
    GROUP BY  SUBSTR(a.Settle_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(a.Settle_time
    FROM 1 FOR 10) , 0 , 0 , 0 , sum(a.Fee_rmb_amount) , 0 , 0 , 0 , 0 , sum(a.Fee_amount) , 0
    FROM load_settlefee_info a
    WHERE a.Remark LIKE '%Tmall Global Commission%'
    GROUP BY  SUBSTR(a.Settle_time
    FROM 1 FOR 10)
    UNION
    SELECT SUBSTR(a.Settle_time
    FROM 1 FOR 10) , 0 , 0 , 0 , 0 , sum(a.Fee_rmb_amount) , 0 , 0 , 0 , 0 , sum(a.Fee_amount)
    FROM load_settlefee_info a
    WHERE a.Remark LIKE '%Juhuasuan Overseas Commission%'
    GROUP BY  SUBSTR(a.Settle_time
    FROM 1 FOR 10)) AS t
GROUP BY  Settle_time; 