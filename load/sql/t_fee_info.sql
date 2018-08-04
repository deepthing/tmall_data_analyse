TRUNCATE TABLE t_fee_info;

INSERT INTO t_fee_info (
	order_id,
	fee_time,
	payment_time,
	logisitic_tax,
	logisitic_service,
	alipay_service,
	tmall,
	juhuasuan,
	taobaoke,
	order_fee,
	account_fee,
	logisitic_tax_usd,
	logisitic_service_usd,
	alipay_service_usd,
	tmall_usd,
	juhuasuan_usd,
	taobaoke_usd,
	order_fee_usd,
	account_fee_usd
) SELECT
	t.order_id,
	t.Fee_date,
	t.Payment_date,
	sum(t.logisitic_tax),
	sum(t.logisitic_service),
	SUM(t.alipay_service),
	sum(t.tmall),
	sum(t.juhuasuan),
	sum(t.taobaoke),
	sum(t.order_fee),
	sum(t.account_fee),
	sum(t.logisitic_tax_usd),
	sum(t.logisitic_service_usd),
	SUM(t.alipay_service_usd),
	sum(t.tmall_usd),
	sum(t.juhuasuan_usd),
	sum(t.taobaoke_usd),
	sum(t.order_fee_usd),
	sum(t.account_fee_usd)
FROM
	(
		SELECT
			a.Partner_transaction_id AS order_id,
			a.Fee_date,
			substr(a.Payment_time, 1, 10) AS Payment_date,
			a.Fee_amount AS logisitic_tax,
			0 AS logisitic_service,
			0 AS alipay_service,
			0 AS tmall,
			0 AS juhuasuan,
			0 AS taobaoke,
			0 AS order_fee,
			0 AS account_fee,
			a.Foreign_fee_amount AS logisitic_tax_usd,
			0 AS logisitic_service_usd,
			0 AS alipay_service_usd,
			0 AS tmall_usd,
			0 AS juhuasuan_usd,
			0 AS taobaoke_usd,
			0 AS order_fee_usd,
			0 AS account_fee_usd
		FROM
			load_fee_info a
		WHERE
			a.Fee_desc_flag = 'logisitic_tax'
		UNION
			SELECT
				a.Partner_transaction_id AS order_id,
				a.Fee_date,
				substr(a.Payment_time, 1, 10) AS Payment_date,
				0,
				a.Fee_amount,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				a.Foreign_fee_amount,
				0,
				0,
				0,
				0,
				0,
				0
			FROM
				load_fee_info a
			WHERE
				a.Fee_desc_flag = 'logisitic_service'
			UNION
				SELECT
					a.Partner_transaction_id AS order_id,
					a.Fee_date,
					substr(a.Payment_time, 1, 10) AS Payment_date,
					0,
					0,
					a.Fee_amount,
					0,
					0,
					0,
					0,
					0,
					0,
					0,
					a.Foreign_fee_amount,
					0,
					0,
					0,
					0,
					0
				FROM
					load_fee_info a
				WHERE
					a.Fee_desc_flag = 'alipay_service'
				UNION
					SELECT
						a.Partner_transaction_id AS order_id,
						a.Fee_date,
						substr(a.Payment_time, 1, 10) AS Payment_date,
						0,
						0,
						0,
						a.Fee_amount,
						0,
						0,
						0,
						0,
						0,
						0,
						0,
						a.Foreign_fee_amount,
						0,
						0,
						0,
						0
					FROM
						load_fee_info a
					WHERE
						a.Fee_desc_flag = 'tmall'
					UNION
						SELECT
							a.Partner_transaction_id AS order_id,
							a.Fee_date,
							substr(a.Payment_time, 1, 10) AS Payment_date,
							0,
							0,
							0,
							0,
							a.Fee_amount,
							0,
							0,
							0,
							0,
							0,
							0,
							0,
							a.Foreign_fee_amount,
							0,
							0,
							0
						FROM
							load_fee_info a
						WHERE
							a.Fee_desc_flag = 'juhuasuan'
						UNION
							SELECT
								a.Partner_transaction_id AS order_id,
								a.Fee_date,
								substr(a.Payment_time, 1, 10) AS Payment_date,
								0,
								0,
								0,
								0,
								0,
								a.Fee_amount,
								0,
								0,
								0,
								0,
								0,
								0,
								0,
								a.Foreign_fee_amount,
								0,
								0
							FROM
								load_fee_info a
							WHERE
								a.Fee_desc_flag = 'taobaoke' -- 								UNION
								-- 									SELECT
								-- 										b.order_id,
								-- 										SUBSTR(b.fin_period FROM 1 FOR 10) AS Fee_date,
								-- 										SUBSTR(b.fin_period FROM 1 FOR 10) AS Payment_date,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										b.order_fee,
								-- 										b.account_fee,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										0,
								-- 										b.account_fee_usd
								-- 									FROM
								-- 										t_order_amount b
	) AS t
GROUP BY
	t.order_id,
	fee_date,
	Payment_date
order by fee_date