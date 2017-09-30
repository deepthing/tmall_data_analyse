ßdrop TABLE if EXISTS t_period_nums_info; create table t_period_nums_info( id int auto_increment , goods_id varchar(80) COMMENT '商品编码' , goods_name varchar(200) COMMENT '商品名称' , fee_order varchar(2) COMMENT '费用顺序' , fee_type varchar(200) COMMENT '费用名称' ,
         PRIMARY KEY(id)) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci; insert into t_period_nums_info( goods_id ,
         goods_name ,
         fee_order ,
         fee_type)
SELECT goods_id ,
         goods_name ,
         '01' , 'sale_num'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '02' , 'sale_out_number'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '03' , 'order_deal_num'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '04' , 'sale_amount'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '05' , 'sale_out_amount'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '06' , 'order_deal_amount'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '07' , 'opening_inventory'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '08' , 'purchase_in'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '09' , 'other_in'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '10' , 'trade_out'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '11' , 'other_out'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '12' , 'ending_inventory'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '13' , 'diff_inventory'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '14' , 'in_out_num'
FROM t_goods_num_info
WHERE goods_id is NOT NULL
UNION
SELECT goods_id ,
         goods_name ,
         '15' , 'trans_amount'
FROM t_goods_num_info
WHERE goods_id is NOT NULL; 