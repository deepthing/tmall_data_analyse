UPDATE load_tmallso_info
SET order_id = TRIM(REPLACE(order_id, '"', ''));

UPDATE load_tmallso_info
SET order_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (order_id, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

TRUNCATE TABLE tmp_tmall_monthly;

INSERT INTO tmp_tmall_monthly (
	order_id,
	period,
	product_name,
	number
) SELECT
	a.order_id,
	SUBSTR(b.create_time FROM 1 FOR 7),
	a.product_name,
	sum(number)
FROM
	load_tmallsodetail_info a,
	load_tmallso_info b
WHERE
	a.order_id = b.order_id
GROUP BY
	a.order_id,
	a.product_name,
	SUBSTR(b.create_time FROM 1 FOR 7);

UPDATE load_fee_info
SET Exchange_Rate = TRIM(
	REPLACE (Exchange_Rate, '"', '')
);

UPDATE load_fee_info
SET Exchange_Rate = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Exchange_Rate, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_fee_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		Partner_transaction_id,
		'"',
		''
	)
);

UPDATE load_fee_info
SET Transaction_id = TRIM(
	REPLACE (Transaction_id, '"', '')
);

UPDATE load_fee_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (
				Partner_transaction_id,
				'\t',
				''
			),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_fee_info
SET Transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Transaction_id, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

TRUNCATE TABLE t_buyer_info;

INSERT INTO t_buyer_info (
	buyer_account,
	buyer_name,
	is_mobile_order,
	create_time,
	mobile
) SELECT
	buyer_account,
	buyer_name,
	is_mobile_order,
	SUBSTR(create_time FROM 1 FOR 10),
	mobile
FROM
	load_tmallso_info
WHERE
	buyer_account IS NOT NULL
GROUP BY
	buyer_account;

UPDATE load_settledetails_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (
				Partner_transaction_id,
				'\t',
				''
			),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settledetails_info
SET Settle_batch_no = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Settle_batch_no, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settlefee_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (
				Partner_transaction_id,
				'\t',
				''
			),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settlefee_info
SET Transaction_id = TRIM(
	REPLACE (Transaction_id, '"', '')
);

UPDATE load_settlefee_info
SET Transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Transaction_id, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settlefee_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		Partner_transaction_id,
		'"',
		''
	)
);

UPDATE load_settlefee_info
SET Partner_transaction_id = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (
				Partner_transaction_id,
				'\t',
				''
			),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settlefee_info
SET Fee_type = TRIM(REPLACE(Fee_type, '"', ''));

UPDATE load_settlefee_info
SET Fee_type = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Fee_type, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

UPDATE load_settlefee_info
SET Currency = TRIM(REPLACE(Currency, '"', ''));

UPDATE load_settlefee_info
SET Currency = TRIM(
	REPLACE (
		REPLACE (
			REPLACE (Currency, '\t', ''),
			'\n',
			''
		),
		'\r',
		''
	)
);

