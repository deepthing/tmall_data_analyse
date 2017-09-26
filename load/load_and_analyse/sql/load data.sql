TRUNCATE TABLE tmall.load_tmallsodetail_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/2017-5-货品.csv' INTO TABLE tmall.load_tmallsodetail_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	@order_id ,
	product_name ,
	price ,
	number ,
	reff_id ,
	product_attr ,
	suit_info ,
	memo ,
	order_status ,
	shop_code
)
SET order_id = MID(
	@order_id ,
	3 ,
	LENGTH(@order_id) - 3
);

TRUNCATE TABLE tmall.load_tmallso_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/2017-6-订单.csv' INTO TABLE tmall.load_tmallso_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	@order_id ,
	buyer_name ,
	buyer_account ,
	buyer_needpay ,
	buyer_post_fee ,
	buery_point ,
	amount ,
	return_point ,
	actual_paid ,
	actual_point ,
	order_status ,
	buyer_msg ,
	reciever_name ,
	recieve_address ,
	deliver_type ,
	telphone ,
	mobile ,
	create_time ,
	paid_time ,
	title ,
	category ,
	logistic_id ,
	logisitise ,
	order_memo ,
	order_counts ,
	shop_id ,
	shop_name ,
	close_reason ,
	sales_service_fee ,
	buyer_service_fee ,
	invoice_title ,
	is_mobile_order ,
	order_msg ,
	priliage_order_id ,
	is_contract_photo ,
	is_tick ,
	is_dai ,
	earnest_range ,
	changed_sku ,
	changed_address ,
	unnormal_msg ,
	tmall_coupon ,
	jufengbao_coupon ,
	is_o2o ,
	is_idcard ,
	refund ,
	shop
)
SET order_id = MID(
	@order_id ,
	3 ,
	LENGTH(@order_id) - 3
);

TRUNCATE TABLE load_transaction_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/2017年7月/Transaction201707.csv' INTO TABLE tmall.load_transaction_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	order_id ,
	goods_code ,
	goods_name ,
	inventory_name ,
	in_out_time ,
	paper_type ,
	inventory_type ,
	in_out_number ,
	deposit_number ,
	erp_order_id ,
	outter_order_id
);

TRUNCATE TABLE load_inventory_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/2017年7月/Inventory201707.csv' INTO TABLE tmall.load_inventory_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	
	period ,
	goods_id ,
	goods_code ,
	goods_name ,
	inventory_name ,
	init_total ,
	init_goods ,
	init_bad ,
	in_total ,
	in_good ,
	in_bad ,
	check_good ,
	check_bad ,
	out_total ,
	out_sales ,
	out_other ,
	out_bac ,
	check_good_need ,
	check_bac_need ,
	final_total ,
	final_goods ,
	final_bad ,
	purchase_onway ,
	change_onway ,
	back_changeber ,
	bill_out_total ,
	bill_out_good ,
	bill_out_bad ,
	adjust_out_total ,
	adjust_out_good ,
	adjust_out_bac ,
	bill_in_total ,
	adjust_in_good ,
	bill_in_bad ,
	adjust_in_total ,
	adjust_in_good1 ,
	adjust_in_bad
);

TRUNCATE TABLE load_order_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/Order0506.csv' INTO TABLE tmall.load_order_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	@num ,
	shop_name ,
	warehouse_name ,
	order_time ,
	pay_time ,
	dispatch_time ,
	order_status ,
	logistic_id ,
	order_id ,
	warehouse_id ,
	dispatch_company ,
	dispatch_no ,
	buyer_nickname ,
	receiver_name ,
	province ,
	city ,
	area ,
	street ,
	phone ,
	order_amount ,
	freight ,
	goods_amount ,
	cargo_id ,
	cargo_code ,
	goods_id ,
	goods_code ,
	goods_name ,
	tax
);

TRUNCATE TABLE load_myaccount_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/2017年7月/Myaccount201707.csv' INTO TABLE tmall.load_myaccount_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Order_No ,
	Partner_Transaction_ID ,
	Transaction_ID ,
	Type ,
	Currency ,
	Amount ,
	Balance ,
	Trans_Date ,
	Remarks,
	Alipay_Order
);

TRUNCATE TABLE load_fee_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/2088021020858327_fee_201705_1.csv' INTO TABLE load_fee_info CHARACTER
SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Payment_time ,
	Transaction_id ,
	Partner_transaction_id ,
	Amount ,
	Foreign_amount ,
	Currency ,
	Exchange_Rate ,
	Fee_type ,
	Fee_amount ,
	Foreign_fee_amount ,
	Fee_desc
);

UPDATE load_fee_info SET Partner_transaction_id = trim('\t' from Partner_transaction_id);

TRUNCATE TABLE load_strade_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/2088021020858327_strade_201706_1.csv' INTO TABLE tmall.load_strade_info CHARACTER SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Partner_transaction_id ,
	Transaction_id ,
	Amount ,
	Rmb_amount ,
	Fee ,
	Refund ,
	Settlement ,
	Rmb_settlement ,
	Currency ,
	Rate ,
	Payment_time ,
	Settlement_time ,
	Type
);

TRUNCATE TABLE load_settlefee_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/2017年7月/Settlefee201707.csv' INTO TABLE tmall.load_settlefee_info CHARACTER SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Payment_time ,
	Transaction_id ,
	Partner_transaction_id ,
	Gross_amount ,
	Rmb_gross_amount ,
	Fee_type ,
	Fee_amount ,
	Fee_rmb_amount ,
	Currency ,
	Rate ,
	Remark
) SET Settle_time = '201706';

TRUNCATE TABLE load_settledetails_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/Settle_201706.csv/2088021020858327_settle_201706_50002017060900032007000004034820.csv' INTO TABLE tmall.load_settledetails_info CHARACTER SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Partner_transaction_id ,
	Amount ,
	Rmb_amount ,
	Fee ,
	Settlement ,
	Rmb_settlement ,
	Currency ,
	Rate ,
	Payment_time ,
	Settlement_time ,
	Type ,
	Statu ,
	Stem_from ,
	Remarks
) SET Settle_batch_no = '50002017060900032007000004034820';

TRUNCATE TABLE load_settlebatch_info;

LOAD DATA LOCAL INFILE '/Users/liang.deng/Documents/果瑞氏56月份/Settle_201706.csv/2088021020858327_settlebatch_201706.csv' INTO TABLE tmall.load_settlebatch_info CHARACTER SET 'gbk' FIELDS ESCAPED BY '\\' TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES(
	Settle_batch_no ,
	Settle_date ,
	Amount ,
	Fee ,
	Settlement ,
	Currency
);

TRUNCATE TABLE tmall.load_tmallsodetail_info;
TRUNCATE TABLE tmall.load_tmallso_info;
TRUNCATE TABLE load_transaction_info;
TRUNCATE TABLE load_inventory_info;
TRUNCATE TABLE load_order_info;
TRUNCATE TABLE load_myaccount_info;
TRUNCATE TABLE load_fee_info;
TRUNCATE TABLE load_strade_info;
TRUNCATE TABLE load_settlefee_info;
TRUNCATE TABLE load_settledetails_info;
TRUNCATE TABLE load_settlebatch_info;
