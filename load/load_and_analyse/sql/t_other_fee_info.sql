TRUNCATE TABLE t_other_fee_info;
INSERT INTO t_other_fee_info(
	trans_date ,
	tmall_warehouse_fee ,
	insurance_fee ,
	destory_fee ,
	merchant_pay_to_custom ,
	cainiao_pay_goodsfee_to_merchant ,
	cainiao_pay_deposit_to_merchant ,
	popularize_fee ,
	other_payback_fee ,
	tmall_popularize_fee ,
	return_cash
) SELECT
	trans_date ,
	sum(Amount1) AS tmall_warehouse_fee ,
	sum(Amount2) AS insurance_fee ,
	sum(Amount3) AS destory_fee ,
	sum(Amount4) AS merchant_pay_to_custom ,
	sum(Amount5) AS cainiao_pay_goodsfee_to_merchant ,
	sum(Amount6) AS cainiao_pay_deposit_to_merchant ,
	sum(Amount7) AS popularize_fee ,
	sum(Amount8) AS other_payback_fee ,
	sum(Amount9) AS tmall_popularize_fee ,
	sum(Amount10) AS return_cash
FROM
	(
		SELECT
			SUBSTR(trans_date FROM 1 FOR 7) AS Trans_Date ,
			sum(Amount) AS Amount1 ,
			0 AS Amount2 ,
			0 AS Amount3 ,
			0 AS Amount4 ,
			0 AS Amount5 ,
			0 AS Amount6 ,
			0 AS Amount7 ,
			0 AS Amount8 ,
			0 AS Amount9 ,
			0 AS Amount10
		FROM
			load_myaccount_info
		WHERE
			Order_No LIKE '%adjust%'
		OR Order_No LIKE '%BS%'
		GROUP BY
			SUBSTR(trans_date FROM 1 FOR 7)
		UNION
			SELECT
				SUBSTR(trans_date FROM 1 FOR 7) AS Trans_Date ,
				0 ,
				sum(Amount) AS Amount ,
				0 ,
				0 ,
				0 ,
				0 ,
				0 ,
				0 ,
				0 ,
				0
			FROM
				load_myaccount_info
			WHERE
				Order_No LIKE '%YFX%'
			OR Remarks LIKE '%保险%'
			GROUP BY
				SUBSTR(trans_date FROM 1 FOR 7)
			UNION
				SELECT
					SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date ,
					0 ,
					0 ,
					0 ,
					sum(Amount) AS Amount ,
					0 ,
					0 ,
					0 ,
					0 ,
					0 ,
					0
				FROM
					load_myaccount_info
				WHERE
					Order_No LIKE '%B2C%'
				GROUP BY
					SUBSTR(trans_date FROM 1 FOR 7)
				UNION
					SELECT
						SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date ,
						0 ,
						0 ,
						0 ,
						0 ,
						sum(Amount) AS Amount ,
						0 ,
						0 ,
						0 ,
						0 ,
						0
					FROM
						load_myaccount_info
					WHERE
						Order_No LIKE '%LBX%'
					AND type = 'refund'
					GROUP BY
						SUBSTR(trans_date FROM 1 FOR 7)
					UNION
						SELECT
							SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date ,
							0 ,
							0 ,
							0 ,
							0 ,
							0 ,
							sum(Amount) AS Amount ,
							0 ,
							0 ,
							0 ,
							0
						FROM
							load_myaccount_info
						WHERE
							Order_No LIKE '%LP%'
						AND type = 'refund'
						GROUP BY
							SUBSTR(trans_date FROM 1 FOR 7)
						UNION
							SELECT
								SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date ,
								0 ,
								0 ,
								0 ,
								0 ,
								0 ,
								0 ,
								sum(Amount) AS Amount ,
								0 ,
								0 ,
								0
							FROM
								load_myaccount_info
							WHERE
								Remarks LIKE '%taobao%'
							AND type = 'refund'
							GROUP BY
								SUBSTR(trans_date FROM 1 FOR 7)
							UNION
								SELECT
									SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date ,
									0 ,
									0 ,
									0 ,
									0 ,
									0 ,
									0 ,
									0 ,
									0 ,
									sum(Amount) AS Amount ,
									0
								FROM
									load_myaccount_info
								WHERE
									Remarks LIKE '%taobao%'
								AND type = 'payments'
								GROUP BY
									SUBSTR(trans_date FROM 1 FOR 7)
	) t1
GROUP BY
	trans_date