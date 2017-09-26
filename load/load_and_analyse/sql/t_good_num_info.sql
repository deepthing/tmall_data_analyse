TRUNCATE TABLE t_goods_num_info;

TRUNCATE TABLE tmp_tmall_monthly;

TRUNCATE TABLE t_tmall_bom_detail;

TRUNCATE TABLE t_transaction_group_info;

TRUNCATE TABLE t_tmall_group_bom_detail;

-- 订单商品占比(Sum(订单单价*订单数据))

update load_tmallsodetail_info a ,( select order_id , sum(price) as total from load_tmallsodetail_info group BY order_id) t1 set goods_total = total , goods_rate =(price / total) where a.order_id = t1.order_id;

-- 生成中间表，记录订单明细商品

insert into tmp_tmall_monthly( order_id , period , product_name , number , amount , deal_amount , order_status) select a.order_id , SUBSTR(b.create_time FROM 1 FOR 7) , a.product_name , sum(number) ,(b.actual_paid * a.goods_rate) +(b.refund * a.goods_rate) , b.actual_paid * a.goods_rate , b.order_status from load_tmallsodetail_info a , load_tmallso_info b where a.order_id = b.order_id group BY a.order_id , a.product_name , SUBSTR(b.create_time FROM 1 FOR 7) , b.order_status;

-- 中间表数据转成订单BOM明细商品

insert into t_tmall_bom_detail( period , order_id , goods_id , product_name , number , amount , deal_amount , order_status) select period , order_id , a.goods_id , b.product_name , a.goods_count * b.number as number ,(b.amount * IFNULL(a.rate , 100)) / 100 as amount ,( b.deal_amount * IFNULL(a.rate , 100)) / 100 as deal_amount , order_status from tmp_tmall_monthly b INNER join bom_detail a on a.product_name = b.product_name;

-- 汇总商品信息

insert into t_goods_num_info( period , goods_id , sale_num , order_deal_num , order_close_num , order_other_num , opening_inventory , ending_inventory , diff_inventory , in_out_num , trade_out , other_out , purchase_in , other_in , sale_amount , order_deal_amount) select period , goods_id , sum(sale_num) , sum(order_deal_num) , sum(order_close_num) , sum(order_other_num) , sum(opening_inventory) , sum(ending_inventory) , sum(diff_inventory) , sum(in_out_num) , sum(trade_out) , sum(other_out) , sum(purchase_in) , sum(other_in) , sum(sale_amount) , sum(order_deal_amount) from( select period , goods_id , sum(number) as sale_num , 0 as order_deal_num , 0 as order_close_num , 0 as order_other_num , 0 as opening_inventory , 0 ending_inventory , 0 diff_inventory , 0 in_out_num , 0 as trade_out , 0 as other_out , 0 as purchase_in , 0 as other_in , sum(amount) as sale_amount , 0 as order_deal_amount from t_tmall_bom_detail group BY period , goods_id union select period , goods_id , 0 , sum(number) , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(deal_amount) from t_tmall_bom_detail where order_status = '交易成功' group BY period , goods_id union select period , goods_id , 0 , 0 , sum(number) , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 from t_tmall_bom_detail where order_status = '交易关闭' group BY period , goods_id union select period , goods_id , 0 , 0 , 0 , sum(number) , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 from t_tmall_bom_detail where order_status <> '交易关闭' and order_status <> '交易成功' group BY period , goods_id UNION select SUBSTR(in_out_time FROM 1 FOR 7) , goods_code , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(in_out_number) , 0 , 0 , 0 , 0 , 0 , 0 from load_transaction_info GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) , goods_code union select SUBSTR(in_out_time FROM 1 FOR 7) , goods_code , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(in_out_number) , 0 , 0 , 0 , 0 , 0 from load_transaction_info where paper_type = '交易出库' GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) , goods_code union select SUBSTR(in_out_time FROM 1 FOR 7) , goods_code , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(in_out_number) , 0 , 0 , 0 , 0 from load_transaction_info where paper_type <> '交易出库' and paper_type like '%出库%' GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) , goods_code union select SUBSTR(in_out_time FROM 1 FOR 7) , goods_code , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(in_out_number) , 0 , 0 , 0 from load_transaction_info where paper_type = '采购入库' GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) , goods_code union select SUBSTR(in_out_time FROM 1 FOR 7) , goods_code , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , sum(in_out_number) , 0 , 0 from load_transaction_info where paper_type <> '采购入库' and paper_type like '%入库%' GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) , goods_code) t group BY period , goods_id;

-- 更新商品名称

update t_goods_num_info INNER JOIN ITEM on t_goods_num_info.goods_id = ITEM.`货品编码` set t_goods_num_info.goods_name = ITEM.`货品名称`;

-- 

insert into t_transaction_group_info( goods_code , order_id , in_out_number) select goods_code , outter_order_id , IFNULL(sum(in_out_number) , 0) as in_out_number from load_transaction_info group BY outter_order_id , goods_code;

insert into t_tmall_group_bom_detail( period , order_id , goods_code , in_out_number , deal_amount) SELECT period , order_id , goods_id , sum(number) , sum(deal_amount) FROM t_tmall_bom_detail group by period , order_id , goods_id;

