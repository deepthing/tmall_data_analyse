import MySQLdb
import sys
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as settings

def insert_fee_monthly_detail_info():
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    detail = db.cursor(MySQLdb.cursors.DictCursor)
    delivery_fee_strr = """
    INSERT INTO t_fee_monthly_detail_info(
    SELECT
	r.time as a1,
	-- r.tax,

    sum(so.actual_paid) / r.tax ,
    min(b2.a1 / r.tax) *- 1 , 
    min(b2.a2 / r.tax) *- 1 , 
    min(b2.a3 / r.tax) *- 1 , 
    min(b2.a4 / r.tax) *- 1 , 
    min(b2.a5 / r.tax) *- 1 , 
    min(b2.a6 / r.tax) *- 1 , 
    sum(so.refund) / r.tax ,
    min(b3.a11 / r.tax) 
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
    AND r.time LIKE '%@datetime%'
    GROUP BY r.time,r.tax)
    """
    detail.execute("TRUNCATE TABLE t_fee_monthly_detail_info;")
    
    detail.execute(
            "SELECT SUBSTR(in_out_time FROM 1 FOR 7) as date_str from load_transaction_info GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) desc")
    list_date = detail.fetchall()
    delivery_fee_res = []
    print(list_date)
    for one_date in list(list_date):
        print(one_date)
        strexec =delivery_fee_strr.replace("@datetime", one_date['date_str'])
        
        detail.execute(strexec)
        print("------------------插入一条--------------------")
    db.commit()
    detail.close()
    db.close()
    print("---------------------插入完毕---------------------")

insert_fee_monthly_detail_info()
