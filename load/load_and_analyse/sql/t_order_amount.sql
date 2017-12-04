TRUNCATE TABLE t_order_amount; 

INSERT INTO t_order_amount( order_id , fin_period , actual_paid , tmall_refund)
SELECT order_id ,
         SUBSTR(create_time
FROM 1 FOR 10) , IFNULL(sum(actual_paid) , 0) , IFNULL(sum(refund) , 0)
FROM load_tmallso_info
GROUP BY  order_id , SUBSTR(create_time
FROM 1 FOR 10); 

TRUNCATE TABLE t_group_fee_info; 

INSERT INTO t_group_fee_info( order_id , fee_amount , fee_amount_usd)
SELECT trim('\t' FROM Partner_transaction_id) , sum(Fee_amount) , sum(Foreign_fee_amount)
FROM load_fee_info
GROUP BY  Partner_transaction_id;

UPDATE load_myaccount_info a
INNER JOIN load_transaction_info b
    ON a.Partner_Transaction_ID = b.order_id SET a.partner_transaction_id = b.outter_order_id
WHERE a.partner_transaction_id LIKE 'LBX%'; 

TRUNCATE t_group_myaccount_info; 

INSERT INTO t_group_myaccount_info(order_id , amount)
SELECT trim('\t'
FROM Partner_transaction_id) , sum(amount)
FROM load_myaccount_info
WHERE Partner_transaction_id IS NOT NULL
GROUP BY  Partner_transaction_id; 

TRUNCATE TABLE t_group_settledetails_info; 

INSERT INTO t_group_settledetails_info(order_id , amount , amount_usd)
SELECT trim('\t' FROM Partner_transaction_id) , sum(Rmb_settlement) , sum(Settlement)
FROM load_settledetails_info
GROUP BY  Partner_transaction_id; -- 更新合并数据 到 t_order_amount 表

UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.alipay_actual_recieve = g.alipay_actual_recieve;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.refund = g.refund;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.alipay_strade_p = g.alipay_strade_p;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.alipay_strade_p_usd = g.alipay_strade_p_usd;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.alipay_strade_r = g.alipay_strade_r;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.alipay_strade_r_usd = g.alipay_strade_r_usd;
    
UPDATE t_order_amount o
INNER JOIN t_group_strade_info g
    ON o.order_id = g.order_id SET o.refund_usd = g.refund_usd;
    
UPDATE t_order_amount o
INNER JOIN t_group_fee_info g
    ON o.order_id = g.order_id SET o.order_fee = g.fee_amount;
    
UPDATE t_order_amount o
INNER JOIN t_group_fee_info g
    ON o.order_id = g.order_id SET o.order_fee_usd = g.fee_amount_usd;
    
UPDATE t_order_amount o
INNER JOIN t_group_myaccount_info g
    ON o.order_id = g.order_id SET o.account_fee = g.amount;
    
UPDATE t_order_amount o
INNER JOIN t_group_settledetails_info g
    ON o.order_id = g.order_id SET o.alipay_get = g.amount;
    
UPDATE t_order_amount o
INNER JOIN t_group_settledetails_info g
    ON o.order_id = g.order_id SET o.alipay_get_usd = g.amount_usd; 