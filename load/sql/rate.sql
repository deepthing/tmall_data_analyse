-- 税率计算
update tax_rate a,
(
	SELECT
period,
	SUM(alipay_settle),
	SUM(alipay_settle_usd),
	SUM(alipay_settle)/SUM(alipay_settle_usd) as rate
FROM
	t_settle_amount_info
GROUP BY period
)b
set a.tax = b.rate
where a.time = b.period
