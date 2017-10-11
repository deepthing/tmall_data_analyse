# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from django.http import HttpResponse
import tmall_data_analyse.settings as settings
import load.service as service
import MySQLdb 
from django.template import loader
import tmall_data_analyse.settings as setting


def index(request):
    return render(request,'nav.html')

def testd3(request):
    return render(request,'d3.html')


def order_vis(request):
    db = MySQLdb.connect(setting.DATABASES.get('default').get('HOST'),
                    setting.DATABASES.get('default').get('USER'),
                    setting.DATABASES.get('default').get('PASSWORD'),
                    setting.DATABASES.get('default').get('NAME'),
                    charset='utf8')
    data = db.cursor(MySQLdb.cursors.DictCursor)
    strr_order = '''
        select 
        SUBSTR(fin_period FROM 1 FOR 7) as period,
        FORMAT(SUM(order_num),0) as sum_order_num,
        FORMAT(SUM(saled_num),0) as sum_saled_num,
        FORMAT(SUM(closed_num),0) as sum_closed_num,
        FORMAT(SUM(waiting_num),0) as sum_waiting_num,
        FORMAT(SUM(close_unpaid_num),0) as sum_close_unpaid_num,
        FORMAT(SUM(close_return_num),0) as sum_close_return_num,
        FORMAT(SUM(order_amount),2) as sum_order_amount,
        FORMAT(SUM(saled_amount),2) as sum_saled_amount,
        FORMAT(SUM(closed_amount),2) as sum_closed_amount,
        FORMAT(SUM(waiting_amount),2) as sum_waiting_amount,
        FORMAT(SUM(close_unpaid_amount),2) sum_close_unpaid_amount,
        FORMAT(SUM(close_return_amount),2) as sum_close_unpaid_amount
        from t_order_analyse
        GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
    '''
    data.execute(strr_order)
    order_analyse = data.fetchall()

    strr_buyer = '''
        select 
        period,
        FORMAT(total_count,0) as total_count,
        FORMAT(new_count ,0) as new_count,
        FORMAT(old_count ,0) as old_count,
        FORMAT(no_account_orders ,0) as no_account_orders,
        FORMAT(new_orders ,0) as new_orders,
        FORMAT(old_orders ,0) as old_orders,
        FORMAT(total_amount ,2) as total_amount,
        FORMAT(no_account_amount ,2) as no_account_amount,
        FORMAT(new_orders_amount ,2) as new_orders_amount,
        FORMAT(old_orders_amount ,2) as old_orders_amount
        from t_member_alanlyse_info
        order by period;
    '''
    data.execute(strr_buyer)
    status_analyse = data.fetchall()

    strr_region = '''
    SELECT
        SUBSTR(fin_period FROM 1 FOR 7) AS period,
        area_info AS area,
        FORMAT(SUM(order_number),0) AS num,
        FORMAT(SUM(order_amount),2) AS amount
    FROM
        t_order_area
    GROUP BY
        SUBSTR(fin_period FROM 1 FOR 7),
        area_info
    '''
    data.execute(strr_region)
    status_region = data.fetchall()

    status_region_list = []
    period_index_temp = ''
    monthly_status = {}
    for index_status_region in status_region:
        
        period_index = index_status_region['period']
        if period_index_temp == '':
            period_index_temp = period_index
            monthly_status['period'] = period_index
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']
            # monthly_status['period'] = period_index
        elif (period_index_temp == period_index) is False:
            status_region_list.append(monthly_status)
            monthly_status = {}
            period_index_temp = period_index
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']
            # monthly_status['period'] = period_index
        else:
            monthly_status['period'] = period_index
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']

    status_region_list.append(monthly_status)

    status_region_amount_list = []
    period_amount_index_temp = ''
    monthly_amount_status = {}
    for index_status_region in status_region:
        
        period_amount_index = index_status_region['period']
        if period_amount_index_temp == '':
            monthly_amount_status['period'] = period_amount_index
            period_amount_index_temp = period_amount_index
            monthly_amount_status[index_status_region['area'][0:1]] = index_status_region['amount']
            # monthly_status['period'] = period_index
        elif (period_amount_index_temp == period_amount_index) is False:
            status_region_amount_list.append(monthly_amount_status)
            monthly_amount_status = {}
            period_amount_index_temp = period_amount_index
            monthly_amount_status[index_status_region['area'][0:1]] = index_status_region['amount']
            # monthly_status['period'] = period_index
        else:
            monthly_amount_status['period'] = period_amount_index
            monthly_amount_status[index_status_region['area'][0:1]] = index_status_region['amount']

    status_region_amount_list.append(monthly_amount_status)

    content = {'order_status_list':order_analyse,'buyer_status_list':status_analyse,'region_status_list':status_region_list,'status_region_amount_list':status_region_amount_list}
    return render(request,'order_vis.html',content)


def fee_vis(request):
    db = MySQLdb.connect(setting.DATABASES.get('default').get('HOST'),
                setting.DATABASES.get('default').get('USER'),
                setting.DATABASES.get('default').get('PASSWORD'),
                setting.DATABASES.get('default').get('NAME'),
                charset='utf8')
    data = db.cursor(MySQLdb.cursors.DictCursor)
    strr_fee_amount = '''
        select 
        SUBSTR(period FROM 1 FOR 7) as period ,
        FORMAT(SUM(alipay_settle),2) as Alipay_Settlement ,
        FORMAT(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
        FORMAT(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
        FORMAT(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
        FORMAT(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
        FORMAT(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
        FROM
        t_settle_amount_info
        GROUP BY SUBSTR(period FROM 1 FOR 7)
    '''
    data.execute(strr_fee_amount)
    fee_amount = data.fetchall()

    strr_fee_time = '''
        select  
        fee_time,
        FORMAT(SUM(logisitic_tax),2) as logisitic_tax,
        FORMAT(SUM(logisitic_service),2) as logisitic_service,
        FORMAT(SUM(alipay_service),2) as alipay_service,
        FORMAT(SUM(tmall),2) as tmall,
        FORMAT(SUM(juhuasuan),2) as juhuasuan,
        FORMAT(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
        FORMAT(SUM(logisitic_service_usd),2) as logisitic_service_usd,
        FORMAT(SUM(alipay_service_usd),2) as alipay_service_usd,
        FORMAT(SUM(tmall_usd),2) as tmall_usd,
        FORMAT(SUM(juhuasuan_usd),2) as juhuasuan_usd
        FROM
        t_settle_fee_info
        GROUP BY fee_time;
    '''
    data.execute(strr_fee_time)
    fee_time = data.fetchall()

    strr_fee_order = '''
        select 
        SUBSTR(fin_period FROM 1 FOR 7) as period,
        FORMAT(SUM(tmall_refund+actual_paid),2) as tmall_order,
        FORMAT(SUM(tmall_refund),2) as tmall_order_refund,
        FORMAT(SUM(actual_paid),2) as tmall_order_actual_pay,
        FORMAT(SUM(order_fee*-1),2) as alipay_Fee,
        FORMAT(SUM(alipay_get*-1),2) as alipay_settlement
        -- SUM(account_fee)
        from t_order_amount 
        GROUP BY SUBSTR(fin_period FROM 1 FOR 7);
    '''
    data.execute(strr_fee_order)
    fee_order = data.fetchall()

    strr_fee_order_detail = '''
        select 
        SUBSTR(payment_time FROM 1 FOR 7) as period,
        FORMAT(SUM(t.logisitic_tax),2) as logisitic_tax,
        FORMAT(SUM(t.logisitic_service),2) as logisitic_service,
        FORMAT(SUM(t.alipay_service),2) as alipay_service,
        FORMAT(SUM(t.tmall),2) as tmall,
        FORMAT(SUM(t.juhuasuan),2) as juhuasuan
        from t_fee_info t
        GROUP BY SUBSTR(payment_time FROM 1 FOR 7);
    '''
    data.execute(strr_fee_order_detail)
    fee_order_detail = data.fetchall()

    strr_fee_payment = '''
        select 
        SUBSTR(period FROM 1 FOR 7) as period,
        FORMAT(SUM(recharge),2) as Recharge,
        FORMAT(SUM(refund),2) as Refund,
        FORMAT(SUM(payment),2) as Payments,
        FORMAT(SUM(order_payment),2) as order_payment,
        FORMAT(SUM(not_order_payment),2) as not_order_payment
        from t_myaccount_monthly_info
        GROUP BY SUBSTR(period FROM 1 FOR 7);
    '''
    data.execute(strr_fee_payment)
    fee_payment =  data.fetchall()

    content = {'fee_amount':fee_amount,'fee_time':fee_time,'fee_order':fee_order,'fee_order_detail':fee_order_detail,'fee_payment':fee_payment}

    return render(request,'fee_vis.html',content)

def inv_vis(request):
    db = MySQLdb.connect(setting.DATABASES.get('default').get('HOST'),
            setting.DATABASES.get('default').get('USER'),
            setting.DATABASES.get('default').get('PASSWORD'),
            setting.DATABASES.get('default').get('NAME'),
            charset='utf8')
    data = db.cursor(MySQLdb.cursors.DictCursor)

    strr = '''
        select period,goods_id,goods_name,
        sum(sale_num) as sale_num,
        sum(sale_out_number*-1) as sale_out_number,
        sum(order_deal_num) as order_deal_num,
        sum(sale_amount) as sale_amount,
        sum(sale_out_amount) as sale_out_amount,
        sum(order_deal_amount) as order_deal_amount,
        sum(opening_inventory) as opening_inventory,
        sum(purchase_in) as purchase_in,
        sum(other_in) as other_in,
        sum(trade_out) as trade_out,
        sum(other_out) as other_out,
        sum(ending_inventory) as ending_inventory,
        sum(diff_inventory) as diff_inventory,
        sum(in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info
        group by period,goods_id,goods_name
        ORDER BY period;
    '''

    data.execute(strr)
    inv_count = data.fetchall()
    content = {'inv_count':inv_count}

    return render(request,'inv_vis.html',content)


def jump_to_load(request):
    try:
        service.loaddata(settings.BASE_FILE_PATH.get('upload_path'))
        return HttpResponse("success")
    except Exception as identifier:
        return HttpResponse("false")


def upload(request):
    
    if request.method == "POST":
        zipfile = request.FILES.get("zipfile",None)
        if not zipfile:
            return HttpResponse("empty")
        storefile = open(os.path.join(settings.BASE_FILE_PATH.get('upzip_path')),'wb+')
        for chunk in zipfile.chunks():
            storefile.write(chunk)
        storefile.close()
        
        return HttpResponse("success")
    else:
        return HttpResponse("wrong")