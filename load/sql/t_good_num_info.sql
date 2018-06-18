TRUNCATE TABLE t_goods_num_info;

TRUNCATE TABLE tmp_tmall_monthly;

TRUNCATE TABLE t_tmall_bom_detail;

TRUNCATE TABLE t_transaction_group_info;

TRUNCATE TABLE t_tmall_group_bom_detail;

TRUNCATE TABLE temp_tmalldetail_rate_info;

TRUNCATE TABLE temp_tmallso_rate_info;

-- 订单商品占比(Sum(订单单价*订单数据)) 
INSERT INTO temp_tmalldetail_rate_info (
	order_id,
	product_name,
	number,
	price,
	goods_rate,
	goods_total
) SELECT
	order_id,
	product_name,
	number,
	price,
	0,
	0
FROM
	load_tmallsodetail_info;

UPDATE temp_tmalldetail_rate_info a,
 (
	SELECT
		order_id,
		sum(price*number) AS total
	FROM
		temp_tmalldetail_rate_info
	GROUP BY
		order_id
) t1
SET goods_total = total,
 goods_rate = (price*number / total)
WHERE
	a.order_id = t1.order_id;

INSERT INTO temp_tmallso_rate_info (
	order_id,
	create_time,
	actual_paid,
	refund,
	order_status
) SELECT
	order_id,
	SUBSTR(create_time FROM 1 FOR 7),
	actual_paid,
	refund,
	order_status
FROM
	load_tmallso_info;

-- 生成中间表，记录订单明细商品 
INSERT INTO tmp_tmall_monthly (
	order_id,
	period,
	product_name,
	number,
	amount,
	deal_amount,
	order_status
) SELECT
	a.order_id,
	b.create_time,
	a.product_name,
	sum(a.number),
	(
		b.actual_paid * sum(a.goods_rate)
	) + (b.refund * sum(a.goods_rate)),
	b.actual_paid * sum(a.goods_rate),
	b.order_status
FROM
	temp_tmalldetail_rate_info a,
	temp_tmallso_rate_info b
WHERE
	a.order_id = b.order_id
GROUP BY
	a.order_id,
	a.product_name,
	b.create_time,
	b.order_status;

-- 中间表数据转成订单BOM明细商品 
INSERT INTO t_tmall_bom_detail (
	period,
	order_id,
	goods_id,
	product_name,
	number,
	amount,
	deal_amount,
	order_status
) SELECT
	period,
	order_id,
	a.goods_id,
	b.product_name,
	a.goods_count * b.number AS number,
	(
		b.amount * IFNULL(a.rate, 100)
	) / 100 AS amount,
	(
		b.deal_amount * IFNULL(a.rate, 100)
	) / 100 AS deal_amount,
	order_status
FROM
	tmp_tmall_monthly b
LEFT JOIN bom_detail a ON a.product_name = b.product_name;

-- 汇总商品信息 
INSERT INTO t_goods_num_info (
	period,
	goods_id,
	sale_num,
	order_deal_num,
	order_close_num,
	order_other_num,
	opening_inventory,
	ending_inventory,
	diff_inventory,
	in_out_num,
	trade_out,
	other_out,
	purchase_in,
	other_in,
	sale_amount,
	order_deal_amount
) SELECT
	period,
	goods_id,
	sum(sale_num),
	sum(order_deal_num),
	sum(order_close_num),
	sum(order_other_num),
	sum(opening_inventory),
	sum(ending_inventory),
	sum(diff_inventory),
	sum(in_out_num),
	sum(trade_out),
	sum(other_out),
	sum(purchase_in),
	sum(other_in),
	sum(sale_amount),
	sum(order_deal_amount)
FROM
	(
		SELECT
			period,
			goods_id,
			sum(number) AS sale_num,
			0 AS order_deal_num,
			0 AS order_close_num,
			0 AS order_other_num,
			0 AS opening_inventory,
			0 ending_inventory,
			0 diff_inventory,
			0 in_out_num,
			0 AS trade_out,
			0 AS other_out,
			0 AS purchase_in,
			0 AS other_in,
			sum(amount) AS sale_amount,
			0 AS order_deal_amount
		FROM
			t_tmall_bom_detail
		GROUP BY
			period,
			goods_id
		UNION
			SELECT
				period,
				goods_id,
				0,
				sum(number),
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				sum(deal_amount)
			FROM
				t_tmall_bom_detail
			WHERE
				order_status = '交易成功'
			GROUP BY
				period,
				goods_id
			UNION
				SELECT
					period,
					goods_id,
					0,
					0,
					sum(number),
					0,
					0,
					0,
					0,
					0,
					0,
					0,
					0,
					0,
					0,
					0
				FROM
					t_tmall_bom_detail
				WHERE
					order_status = '交易关闭'
				GROUP BY
					period,
					goods_id
				UNION
					SELECT
						period,
						goods_id,
						0,
						0,
						0,
						sum(number),
						0,
						0,
						0,
						0,
						0,
						0,
						0,
						0,
						0,
						0
					FROM
						t_tmall_bom_detail
					WHERE
						order_status <> '交易关闭'
					AND order_status <> '交易成功'
					GROUP BY
						period,
						goods_id
					UNION
						SELECT
							SUBSTR(in_out_time FROM 1 FOR 7),
							goods_code,
							0,
							0,
							0,
							0,
							0,
							0,
							0,
							sum(in_out_number),
							0,
							0,
							0,
							0,
							0,
							0
						FROM
							load_transaction_info
						GROUP BY
							SUBSTR(in_out_time FROM 1 FOR 7),
							goods_code
						UNION
							SELECT
								SUBSTR(in_out_time FROM 1 FOR 7),
								goods_code,
								0,
								0,
								0,
								0,
								0,
								0,
								0,
								0,
								sum(in_out_number),
								0,
								0,
								0,
								0,
								0
							FROM
								load_transaction_info
							WHERE
								paper_type = '交易出库'
							GROUP BY
								SUBSTR(in_out_time FROM 1 FOR 7),
								goods_code
							UNION
								SELECT
									SUBSTR(in_out_time FROM 1 FOR 7),
									goods_code,
									0,
									0,
									0,
									0,
									0,
									0,
									0,
									0,
									0,
									sum(in_out_number),
									0,
									0,
									0,
									0
								FROM
									load_transaction_info
								WHERE
									paper_type <> '交易出库'
								AND paper_type LIKE '%出库%'
								GROUP BY
									SUBSTR(in_out_time FROM 1 FOR 7),
									goods_code
								UNION
									SELECT
										SUBSTR(in_out_time FROM 1 FOR 7),
										goods_code,
										0,
										0,
										0,
										0,
										0,
										0,
										0,
										0,
										0,
										0,
										sum(in_out_number),
										0,
										0,
										0
									FROM
										load_transaction_info
									WHERE
										paper_type = '采购入库'
									GROUP BY
										SUBSTR(in_out_time FROM 1 FOR 7),
										goods_code
									UNION
										SELECT
											SUBSTR(in_out_time FROM 1 FOR 7),
											goods_code,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											sum(in_out_number),
											0,
											0
										FROM
											load_transaction_info
										WHERE
											paper_type <> '采购入库'
										AND paper_type LIKE '%入库%'
										GROUP BY
											SUBSTR(in_out_time FROM 1 FOR 7),
											goods_code
	) t
GROUP BY
	period,
	goods_id;

-- 更新商品名称
UPDATE t_goods_num_info
INNER JOIN ITEM ON t_goods_num_info.goods_id = ITEM.`货品编码`
SET t_goods_num_info.goods_name = ITEM.`货品名称`;

UPDATE load_transaction_info
SET outter_order_id = trim('\r' FROM outter_order_id);

INSERT INTO t_transaction_group_info (
	goods_code,
	order_id,
	in_out_number
) SELECT
	goods_code,
	outter_order_id,
	IFNULL(sum(in_out_number), 0) AS in_out_number
FROM
	load_transaction_info
GROUP BY
	outter_order_id,
	goods_code;

INSERT INTO t_tmall_group_bom_detail (
	period,
	order_id,
	goods_code,
	in_out_number,
	deal_amount
) SELECT
	period,
	order_id,
	goods_id,
	sum(number),
	sum(deal_amount)
FROM
	t_tmall_bom_detail
GROUP BY
	period,
	order_id,
	goods_id;

