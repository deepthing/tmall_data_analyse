-- 缺失BOM分析
SELECT DISTINCT
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
order by product_name;

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
update bom set bom.XY521077050523=NULL where bom.XY521077050523 <0.1;
update bom set bom.XY521077162825=NULL where bom.XY521077162825 <0.1;
update bom set bom.XY521078232623=NULL where bom.XY521078232623 <0.1;
update bom set bom.XY521067771349=NULL where bom.XY521067771349 <0.1;
update bom set bom.XY521073901132=NULL where bom.XY521073901132 <0.1;
update bom set bom.XY521078064529=NULL where bom.XY521078064529 <0.1;
update bom set bom.XY521074093868=NULL where bom.XY521074093868 <0.1;
update bom set bom.XY521078390258=NULL where bom.XY521078390258 <0.1;
update bom set bom.XY521077912497=NULL where bom.XY521077912497 <0.1;
update bom set bom.XY521074249153=NULL where bom.XY521074249153 <0.1;
update bom set bom.XY521074725008=NULL where bom.XY521074725008 <0.1;
update bom set bom.XY521068155265=NULL where bom.XY521068155265 <0.1;
update bom set bom.708390000203=NULL where bom.708390000203 <0.1;
update bom set bom.708390000210=NULL where bom.708390000210 <0.1;
update bom set bom.708390000227=NULL where bom.708390000227 <0.1;
update bom set bom.7290108800098=NULL where bom.7290108800098 <0.1;
update bom set bom.8802534778019=NULL where bom.8802534778019 <0.1;
update bom set bom.8802534778002=NULL where bom.8802534778002 <0.1;
update bom set bom.9999=NULL where bom.9999 <0.1;


