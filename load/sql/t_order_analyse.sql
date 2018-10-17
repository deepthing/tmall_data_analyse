TRUNCATE TABLE t_order_analyse; 
insert into t_order_analyse( fin_period , order_num , saled_num , closed_num , waiting_num , close_unpaid_num , close_return_num , order_amount , saled_amount , closed_amount , waiting_amount , close_unpaid_amount , close_return_amount)
SELECT create_date ,
         sum(order_num) ,
         sum(saled_num) ,
         sum(closed_num) ,
         sum(waiting_num) ,
         sum(close_unpaid_num) ,
         sum(close_return_num) ,
         sum(order_amount) ,
         sum(saled_amount) ,
         sum(closed_amount) ,
         sum(waiting_amount) ,
         sum(close_unpaid_amount) ,
         sum(close_return_amount)
FROM 
    (SELECT left(create_time ,
         10) AS create_date ,
         count(*) AS order_num ,
         0 AS saled_num ,
         0 AS closed_num ,
         0 AS waiting_num ,
         0 AS close_unpaid_num ,
         0 AS close_return_num ,
         sum(amount) AS order_amount ,
         0 AS saled_amount ,
         0 AS closed_amount ,
         0 AS waiting_amount ,
         0 AS close_unpaid_amount ,
         0 AS close_return_amount
    FROM load_tmallso_info
    GROUP BY  left(create_time , 10)
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0 ,
         0 ,
         0 ,
         0
    FROM load_tmallso_info
    WHERE order_status = '交易成功'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0 ,
         0 ,
         0
    FROM load_tmallso_info
    WHERE order_status = '交易关闭'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0 ,
         0
    FROM load_tmallso_info
    WHERE order_status = '卖家已发货，等待买家确认'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0 ,
         0
    FROM load_tmallso_info
    WHERE order_status = '卖家已发货，等待买家确认'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0 ,
         0
    FROM load_tmallso_info
    WHERE order_status = '卖家已发货，等待买家确认'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount) ,
         0
    FROM load_tmallso_info
    WHERE order_status = '交易关闭'
            AND close_reason = '买家未付款'
    GROUP BY  create_date
    UNION
    SELECT left(create_time ,
         10) AS create_date ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         count(*) ,
         0 ,
         0 ,
         0 ,
         0 ,
         0 ,
         sum(amount)
    FROM load_tmallso_info
    WHERE order_status = '交易关闭'
            AND close_reason = '退款'
    GROUP BY  create_date) t1
GROUP BY  create_date; 