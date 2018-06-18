TRUNCATE table t_fee_monthly_info; insert into t_fee_monthly_info( fee_time , logisitic_tax , logisitic_service , alipay_service , tmall , juhuasuan , order_fee , account_fee)
SELECT fee_date ,
         sum(logisitic_tax) ,
         sum(logisitic_service) ,
         SUM(alipay_service) ,
         sum(tmall) ,
         sum(juhuasuan) ,
         sum(order_fee) ,
         sum(account_fee)
FROM 
    (SELECT a.fee_date ,
         sum(a.Fee_amount) AS logisitic_tax ,
         0 logisitic_service ,
         0 AS alipay_service ,
         0 AS tmall ,
         0 AS juhuasuan ,
         0 AS order_fee ,
         0 AS account_fee
    FROM load_fee_info a
    WHERE a.fee_desc LIKE '%进口关税%'
    GROUP BY  a.Fee_DATE
    UNION
    SELECT a.fee_date ,
         0 ,
         sum(a.Fee_amount) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0
    FROM load_fee_info a
    WHERE a.fee_desc LIKE '%服务费用%'
    GROUP BY  a.Fee_DATE
    UNION
    SELECT a.fee_date ,
         0 ,
         0 ,
         sum(a.Fee_amount) ,
         0 ,
         0 ,
         0 ,
         0
    FROM load_fee_info a
    WHERE a.fee_desc LIKE '%Alipay service fee%'
    GROUP BY  a.Fee_DATE
    UNION
    SELECT a.fee_date ,
         0 ,
         0 ,
         0 ,
         sum(a.Fee_amount) ,
         0 ,
         0 ,
         0
    FROM load_fee_info a
    WHERE a.fee_desc LIKE '%Tmall Global Commission%'
    GROUP BY  a.Fee_DATE
    UNION
    SELECT a.fee_date ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(a.Fee_amount) ,
         0 ,
         0
    FROM load_fee_info a
    WHERE a.fee_desc LIKE '%Juhuasuan Overseas Commission%'
    GROUP BY  a.Fee_DATE) AS t
GROUP BY  fee_date; 