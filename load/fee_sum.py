import MySQLdb

def insert_fee_monthly_detail_info():
    db = MySQLdb.connect("127.0.0.1", "bsztz", "bsztz","tmall", charset='utf8')
    detail = db.cursor(MySQLdb.cursors.DictCursor)
    delivery_fee_strr = """
    INSERT INTO t_fee_monthly_detail_info(
    SELECT
	r.time as a1,
	-- r.tax,

	format(SUM(so.actual_paid) / r.tax , 2) as a2,
	format(b2.a1 / r.tax *- 1 , 2) as a3,
	format(b2.a2 / r.tax *- 1 , 2)  as a4,
	format(b2.a3 / r.tax *- 1 , 2) as a5,
	format(b2.a4 / r.tax *- 1 , 2) as a6,
	format(b2.a5 / r.tax *- 1 , 2) as a7,
	format(b2.a6 / r.tax *- 1 , 2) as a8,
	format(SUM(so.refund) / r.tax , 2) as a9,
	format(b3.a11 / r.tax , 2) as a10
    FROM
    load_tmallso_info so,
    tax_rate r,
    (
    SELECT
    SUM(fee.logisitic_tax) AS a1,
    SUM(fee.logisitic_service) AS a2,
    SUM(fee.alipay_service) AS a3,
    SUM(fee.tmall) AS a4,
    SUM(fee.juhuasuan) AS a5,
    SUM(fee.taobaoke) AS a6
    FROM
    t_fee_info fee
    WHERE
    fee.order_id IN (
        SELECT DISTINCT
        t.outter_order_id outt
        FROM
        load_transaction_info t
        WHERE
        t.in_out_time LIKE '%@datetime%'
        AND t.paper_type = '交易出库'
    and t.goods_code<>'7290108800098'
    )
    ) b2,
    (
    SELECT
    SUM(alipay_settle) AS a11,SUM(alipay_settle_p + alipay_settle_r) AS a22,SUM(account_fee *- 1) AS a33
    FROM
    t_settle_amount_info
    WHERE
    1 = 1
    AND t_settle_amount_info.period LIKE '@datetime%'
    ) b3
    WHERE
    so.order_id IN (
    SELECT DISTINCT
    t.outter_order_id outt
    FROM
    load_transaction_info t
    WHERE
    t.in_out_time LIKE '%@datetime%'
    AND t.paper_type = '交易出库'
    and t.goods_code<>'7290108800098'
    )
    AND r.time LIKE '%@datetime%')
    """
    detail.execute("TRUNCATE TABLE t_fee_monthly_detail_info;")
    
    detail.execute(
            "SELECT SUBSTR(in_out_time FROM 1 FOR 7) as date_str from load_transaction_info GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) desc")
    list_date = detail.fetchall()
    delivery_fee_res = []
    for one_date in list(list_date):
        print(one_date)
        detail.execute(delivery_fee_strr.replace("@datetime", one_date['date_str']))
        count = detail.execute(
            "select count(*) from t_other_fee_add_info where date_str = '%s'" % (one_date['date_str']))
        if count == 0:
            detail.execute("insert into t_other_fee_add_info (date_str) values('%s')" % (
                one_date['date_str']))
    db.commit()
    detail.close()
    db.close()


insert_fee_monthly_detail_info()
