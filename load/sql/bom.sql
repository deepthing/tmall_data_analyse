-- 缺失BOM分析，前端bom修改
/* SELECT DISTINCT
	(product_name)
FROM
	load_tmallsodetail_info
WHERE
	product_name NOT IN (
		SELECT DISTINCT
			(product_name)
		FROM
			bom
	)
order by product_name; */


-- BOM去空格字符问题
UPDATE bom
SET product_name= TRIM(REPLACE(product_name, '"', ''));

UPDATE bom
SET product_name = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (product_name, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);


-- 空值的问题


