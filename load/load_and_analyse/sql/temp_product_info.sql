 TRUNCATE TABLE temp_product_info; INSERT INTO temp_product_info (product_name,cargo_code,num)
SELECT DISTINCT b1.product_name AS product_name,
         b1.cargo_code AS cargo_code,
         b1.N AS num
FROM 
    (SELECT -- DISTINCT COUNT(*) AS num,
         t.order_id,
         t.goods_name,
         t.cargo_code,
         t.goods_amount,
         td.product_name,
         td.number,
         t.goods_amount / td.number N
    FROM load_order_info t, load_tmallsodetail_info td
    WHERE t.order_id = td.order_id--
            AND t.goods_name=td.product_name --
            AND t.order_id=10568962125354731
    GROUP BY  t.order_id
    ORDER BY  num, t.order_id, goods_name) b1, 
    (SELECT DISTINCT(product_name) AS product_name
    FROM load_tmallsodetail_info
    WHERE product_name NOT IN 
        (SELECT DISTINCT(product_name)
        FROM BOM ) ) b2
    WHERE b1.num=1
        AND b1.product_name=b2.product_name ; 