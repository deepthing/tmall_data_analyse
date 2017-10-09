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
        SUM(order_num) as sum_order_num,
        SUM(saled_num) as sum_saled_num,
        SUM(closed_num) as sum_closed_num,
        SUM(waiting_num) as sum_waiting_num,
        SUM(close_unpaid_num) as sum_close_unpaid_num,
        SUM(close_return_num) as sum_close_return_num,
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
        total_count,
        new_count ,
        old_count ,
        no_account_orders ,
        new_orders ,
        old_orders ,
        total_amount ,
        no_account_amount ,
        new_orders_amount ,
        old_orders_amount 
        from t_member_alanlyse_info
        order by period;
    '''
    data.execute(strr_buyer)
    status_analyse = data.fetchall()

    strr_region = '''
    select SUBSTR(fin_period FROM 1 FOR 7) as period,area_info  as area,SUM(order_number) as num,SUM(order_amount) as amount from t_order_area
GROUP BY  SUBSTR(fin_period FROM 1 FOR 7),area_info
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
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']
            # monthly_status['period'] = period_index
        elif (period_index_temp == period_index) is False:
            status_region_list.append(monthly_status)
            monthly_status = {}
            period_index_temp = period_index
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']
            # monthly_status['period'] = period_index
        else:
            monthly_status[index_status_region['area'][0:1]] = index_status_region['num']


    status_region_amount_list = []
    period_amount_index_temp = ''
    monthly_amount_status = {}
    for index_status_region in status_region:
        
        period_amount_index = index_status_region['period']
        if period_amount_index_temp == '':
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
            monthly_amount_status[index_status_region['area'][0:1]] = index_status_region['amount']

            

    content = {'order_status_list':order_analyse,'buyer_status_list':status_analyse,'region_status_list':status_region_list,'status_region_amount_list':status_region_amount_list}
    return render(request,'order_vis.html',content)


def fee_vis(request):
    return render(request,'fee_vis.html')

def inv_vis(request):
    return render(request,'inv_vis.html')

def inv_mon_vis(request):
    return render(request,'inv_mon_vis.html')

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