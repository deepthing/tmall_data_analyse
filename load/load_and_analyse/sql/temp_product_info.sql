
TRUNCATE TABLE temp_product_info;
INSERT INTO temp_product_info (product_name,cargo_code,num)
select DISTINCT
b1.product_name as product_name,
b1.cargo_code as cargo_code,
b1.N as num
 from (
SELECT
	-- DISTINCT 
	COUNT(*) AS num,
	t.order_id,
	t.goods_name,
	t.cargo_code,
	t.goods_amount,
	td.product_name,
	td.number,
	t.goods_amount / td.number N
FROM
	load_order_info t,
	load_tmallsodetail_info td
WHERE
	t.order_id = td.order_id-- and t.goods_name=td.product_name
	-- and t.order_id=10568962125354731
GROUP BY
	t.order_id
ORDER BY
	num,
	t.order_id,
	goods_name) b1,
(
select DISTINCT(product_name) as product_name  from load_tmallsodetail_info where product_name not in (
select DISTINCT(product_name) from BOM )
) b2
where b1.num=1
and b1.product_name=b2.product_name
;



