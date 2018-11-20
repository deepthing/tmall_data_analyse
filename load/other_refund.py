#!/usr/bin/python
#coding:UTF-8
import MySQLdb
import sys 
import decimal
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as setting


db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                        user=settings.DATABASES.get(
                            'default').get('USER'),
                        passwd=settings.DATABASES.get(
                            'default').get('PASSWORD'),
                        db=settings.DATABASES.get('default').get('NAME'),
                        charset="utf8",
                        local_infile=1)
con = db.cursor(MySQLdb.cursors.DictCursor)
sql_str = '''
    SELECT trans_date,sum(amount) as amount from 
    (SELECT SUBSTR(trans_date FROM 1 FOR 7) as trans_date,sum(amount) as amount  from load_myaccount_info WHERE (Order_No like '%adjust%' or Order_No like '%BS%') and Type ='refund' GROUP BY SUBSTR(trans_date FROM 1 FOR 7)
    Union
    SELECT SUBSTR(trans_date FROM 1 FOR 7) ,sum(Amount)  from load_myaccount_info WHERE (Order_No like '%YFX%' or Remarks like '%保险%') and Type = 'refund' GROUP BY SUBSTR(trans_date FROM 1 FOR 7)
    Union
    SELECT trans_date,popularize_fee from t_other_fee_info WHERE popularize_fee > 0
    UNION
    SELECT trans_date,cainiao_pay_goodsfee_to_merchant from t_other_fee_info WHERE cainiao_pay_goodsfee_to_merchant>0
    UNION
    SELECT trans_date,cainiao_pay_deposit_to_merchant from t_other_fee_info WHERE cainiao_pay_deposit_to_merchant >0)t1
    GROUP BY trans_date
'''

sql_all_str ='''SELECT SUBSTR(trans_date FROM 1 FOR 7) as trans_date,sum(amount) as amount from load_myaccount_info where Type ='refund' GROUP BY SUBSTR(trans_date FROM 1 FOR 7);'''
con.execute(sql_str)
data = con.fetchall()
con.execute(sql_all_str)
data_all = con.fetchall()

update_date_list = []
for data_index in data:
    update_data = {}
    strr = ""
    for data_all_index in data_all:
        if data_index['trans_date'] == data_all_index['trans_date']:
            update_data['trans_date'] = data_index['trans_date']
            decimal.getcontext().prec = 10
            # print str(data_all_index['amount']-data_index['amount'])
            update_data['other_refund'] = str(data_all_index['amount']-data_index['amount'])
            

    update_date_list.append(update_data)

for update_date_list_index in update_date_list:
    strr = "update t_other_fee_info set other_payback_fee = "+update_date_list_index['other_refund']+" where trans_date = '"+update_date_list_index['trans_date'] +"'"
    print(strr)
    con.execute(strr)
db.commit()
con.close()
db.close()

