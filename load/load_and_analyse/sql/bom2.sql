-- 检查是否漏
SELECT
	t2.paper_type,
  t2.outter_order_id,
	t1.*
FROM
	(
		SELECT
			b.id AS transaction_id,
			b.goods_code AS transaction_goods_code,
			b.order_id AS transaction_order_id,
			b.in_out_number AS transaction_in_out_number,
			a.id AS tmall_id,
			a.period AS tmall_period,
			a.goods_code AS tmall_goods_code,
			a.order_id AS tmall_order_id,
			a.in_out_number AS tmall_in_out_number,
			a.deal_amount AS tmall_deal_amount
		FROM
			t_transaction_group_info b
		LEFT JOIN t_tmall_group_bom_detail a ON b.order_id = a.order_id
		AND a.goods_code = b.goods_code
		WHERE
			a.id IS NULL
		AND b.order_id <> '0'
	) t1,
	(
		SELECT DISTINCT
			t.paper_type AS paper_type,
			t.outter_order_id AS outter_order_id
		FROM
			load_transaction_info t
	) t2
WHERE
	t1.transaction_order_id = t2.outter_order_id
and t2.paper_type='交易出库';

-- 检查是否数量不对
		SELECT
			b.id AS transaction_id,
			b.goods_code AS transaction_goods_code,
			b.order_id AS transaction_order_id,
			b.in_out_number AS transaction_in_out_number,
			a.id AS tmall_id,
			a.period AS tmall_period,
			a.goods_code AS tmall_goods_code,
			a.order_id AS tmall_order_id,
			a.in_out_number AS tmall_in_out_number,
			a.deal_amount AS tmall_deal_amount
		FROM
			t_transaction_group_info b
		LEFT JOIN t_tmall_group_bom_detail a ON b.order_id = a.order_id
		AND a.goods_code = b.goods_code
    where b.in_out_number+a.in_out_number<>0;


-- 检查是否BOM分解有但事务处理没有
SELECT
			a.id AS tmall_id,
			a.period AS tmall_period,
			a.goods_code AS tmall_goods_code,
			a.order_id AS tmall_order_id,
			a.in_out_number AS tmall_in_out_number,
			a.deal_amount AS tmall_deal_amount,
			b.id AS transaction_id,
			b.goods_code AS transaction_goods_code,
			b.order_id AS transaction_order_id,
			b.in_out_number AS transaction_in_out_number
		FROM
			 t_tmall_group_bom_detail a
		LEFT JOIN t_transaction_group_info b ON b.order_id = a.order_id
		AND a.goods_code = b.goods_code
	WHERE
			b.order_id IS NULL
-- AND a.goods_code <> '9999'
-- and a.deal_amount<>'0'
and a.order_id IN (
				SELECT DISTINCT
					t.outter_order_id outt
				FROM
					load_transaction_info t
				WHERE t.paper_type = '交易出库'
			);

