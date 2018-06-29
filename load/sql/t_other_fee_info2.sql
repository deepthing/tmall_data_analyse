TRUNCATE TABLE t_other_fee_info;

INSERT INTO t_other_fee_info (
	trans_date,
	tmall_warehouse_fee,
	insurance_fee,
	merchant_pay_to_custom,
	cainiao_pay_goodsfee_to_merchant,
	cainiao_pay_deposit_to_merchant,
	popularize_fee,
	other_payback_fee,
	annual_service,
	tmall_popularize_fee
) SELECT
	trans_date,
	sum(Amount1) AS tmall_warehouse_fee,
	sum(Amount2) AS insurance_fee,
	sum(Amount3) AS merchant_pay_to_custom,
	sum(Amount4) AS cainiao_pay_goodsfee_to_merchant,
	sum(Amount5) AS cainiao_pay_deposit_to_merchant,
	sum(Amount6) AS popularize_fee,
	sum(Amount7) AS other_payback_fee,
	sum(Amount8) AS annual_service,
	sum(Amount9) AS tmall_popularize_fee
FROM
	(
		SELECT
			SUBSTR(trans_date FROM 1 FOR 7) AS Trans_Date,
			sum(Amount) AS Amount1,
			0 AS Amount2,
			0 AS Amount3,
			0 AS Amount4,
			0 AS Amount5,
			0 AS Amount6,
			0 AS Amount7,
			0 AS Amount8,
			0 AS Amount9
		FROM
			load_myaccount_info
		WHERE
			Myaccountfee LIKE '%仓储费%'
		GROUP BY
			SUBSTR(trans_date FROM 1 FOR 7)
		UNION
			SELECT
				SUBSTR(trans_date FROM 1 FOR 7) AS Trans_Date,
				0,
				sum(Amount) AS Amount,
				0,
				0,
				0,
				0,
				0,
				0,
				0
			FROM
				load_myaccount_info
			WHERE
				Myaccountfee LIKE '%保险费%'
			GROUP BY
				SUBSTR(trans_date FROM 1 FOR 7)
			UNION
				SELECT
					SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
					0,
					0,
					sum(Amount) AS Amount,
					0,
					0,
					0,
					0,
					0,
					0
				FROM
					load_myaccount_info
				WHERE
					Myaccountfee LIKE '%商家赔付给消费者费用%'
				GROUP BY
					SUBSTR(trans_date FROM 1 FOR 7)
				UNION
					SELECT
						SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
						0,
						0,
						0,
						sum(Amount) AS Amount,
						0,
						0,
						0,
						0,
						0
					FROM
						load_myaccount_info
					WHERE
						Myaccountfee LIKE '%菜鸟赔付给商家费用（货款赔付）%'
					GROUP BY
						SUBSTR(trans_date FROM 1 FOR 7)
					UNION
						SELECT
							SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
							0,
							0,
							0,
							0,
							sum(Amount) AS Amount,
							0,
							0,
							0,
							0
						FROM
							load_myaccount_info
						WHERE
							Myaccountfee LIKE '%菜鸟赔付商给家费用（保证金赔付）%'
						GROUP BY
							SUBSTR(trans_date FROM 1 FOR 7)
						UNION
							SELECT
								SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
								0,
								0,
								0,
								0,
								0,
								sum(Amount) AS Amount,
								0,
								0,
								0
							FROM
								load_myaccount_info
							WHERE
								Myaccountfee LIKE '%推广补助%'
							GROUP BY
								SUBSTR(trans_date FROM 1 FOR 7)
							UNION
								SELECT
									SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
									0,
									0,
									0,
									0,
									0,
									0,
									sum(Amount) AS Amount,
									0,
									0
								FROM
									load_myaccount_info
								WHERE
									Myaccountfee LIKE '%其他账户返还%'
								GROUP BY
									SUBSTR(trans_date FROM 1 FOR 7)
								UNION
									SELECT
										SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
										0,
										0,
										0,
										0,
										0,
										0,
										0,
										sum(Amount) AS Amount,
										0
									FROM
										load_myaccount_info
									WHERE
										Myaccountfee LIKE '%天猫年费%'
									GROUP BY
										SUBSTR(trans_date FROM 1 FOR 7)
									UNION
										SELECT
											SUBSTR(Trans_Date FROM 1 FOR 7) AS Trans_Date,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											0,
											sum(Amount) AS Amount
										FROM
											load_myaccount_info
										WHERE
											Myaccountfee LIKE '%天猫广告推广费%'
										GROUP BY
											SUBSTR(trans_date FROM 1 FOR 7)
	) t1
GROUP BY
	trans_date