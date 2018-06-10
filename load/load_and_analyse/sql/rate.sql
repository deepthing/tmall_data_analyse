-- Ë°ÂÊ¼ÆËã
SELECT
period,
	SUM(alipay_settle),
	SUM(alipay_settle_usd),
	SUM(alipay_settle)/SUM(alipay_settle_usd)
FROM
	t_settle_amount_info
GROUP BY period

