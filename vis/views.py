# -*- coding: utf-8 -*-

import datetime
import io
import json
import os
import time

import MySQLdb
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response,redirect
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

import load.service as service
import tmall_data_analyse.settings as setting
import vis.models as vismodels
from _ctypes import Union
from django.contrib.auth.decorators import login_required
from .models import TGoodsNumInfo
import load.mydb as mydb


def index(request):
    return render(request, "login.html")

@login_required
def loadcsv(request):
    print(request.LANGUAGE_CODE)
    return render(request, "load_csv_vis.html", locals())


def testd3(request):
    return render(request, "d3.html")


@login_required
def export_vis(request):
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    strr_order = """
        select left(fin_period,4) as yy from t_order_amount GROUP BY left(fin_period,4)
    """
    data.execute(strr_order)
    all_years = data.fetchall()
    content = {"all_years": all_years}

    return render(request, "export.html", content)


@login_required
def order_vis(request):
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    if request.session.get("lge") == "en":
        strr_order = """
        select 
        SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
        FORMAT(SUM(t1.order_num),0) as sum_order_num,
        FORMAT(SUM(t1.saled_num),0) as sum_saled_num,
        FORMAT(SUM(t1.closed_num),0) as sum_closed_num,
        FORMAT(SUM(t1.waiting_num),0) as sum_waiting_num,
        FORMAT(SUM(t1.close_unpaid_num),0) as sum_close_unpaid_num,
        FORMAT(SUM(t1.close_return_num),0) as sum_close_return_num,
        FORMAT(SUM(t1.order_amount/t2.tax),2) as sum_order_amount,
        FORMAT(SUM(t1.saled_amount/t2.tax),2) as sum_saled_amount,
        FORMAT(SUM(t1.closed_amount/t2.tax),2) as sum_closed_amount,
        FORMAT(SUM(t1.waiting_amount/t2.tax),2) as sum_waiting_amount,
        FORMAT(SUM(t1.close_unpaid_amount/t2.tax),2) sum_close_unpaid_amount,
        FORMAT(SUM(t1.close_return_amount/t2.tax),2) as sum_close_unpaid_amount
        from t_order_analyse as t1
        left join tax_rate as t2
        on SUBSTR(fin_period FROM 1 FOR 7)=t2.time
        GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
        desc
    """
    else:
        strr_order = """
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
        desc
    """
    data.execute(strr_order)
    order_analyse = data.fetchall()

    if request.session.get("lge") == "en":
        strr_buyer = """
        select 
        FORMAT(t1.total_count/t2.tax,0) as total_count,
        FORMAT(t1.new_count/t2.tax ,0) as new_count,
        FORMAT(t1.old_count/t2.tax ,0) as old_count,
        FORMAT(t1.no_account_orders/t2.tax ,0) as no_account_orders,
        FORMAT(t1.new_orders/t2.tax ,0) as new_orders,
        FORMAT(t1.old_orders/t2.tax ,0) as old_orders,
        FORMAT(t1.total_amount/t2.tax ,2) as total_amount,
        FORMAT(t1.no_account_amount/t2.tax ,2) as no_account_amount,
        FORMAT(t1.new_orders_amount/t2.tax ,2) as new_orders_amount,
        FORMAT(t1.old_orders_amount/t2.tax ,2) as old_orders_amount
        from t_member_alanlyse_info as t1
        left join tax_rate as t2
        on t1.period=t2.time
        order by period
        desc
    """
    else:
        strr_buyer = """
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
        order by period
        desc
    """
    data.execute(strr_buyer)
    status_analyse = data.fetchall()
    if request.session.get("lge") == "en":
        strr_region = """
    SELECT
        SUBSTR(t1.fin_period FROM 1 FOR 7) AS period,
        t1.area_info AS area,
        FORMAT(SUM(t1.order_number),0) AS num,
        FORMAT(SUM(t1.order_amount/t2.tax),2) AS amount
    FROM
        t_order_area as t1 
        left join  tax_rate as t2
        on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
    GROUP BY
        SUBSTR(t1.fin_period FROM 1 FOR 7),
        area_info
    ORDER BY period desc
    """
    else:
        strr_region = """
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
    ORDER BY period desc
    """
    data.execute(strr_region)
    status_region = data.fetchall()

    status_region_list = []
    period_index_temp = ""
    monthly_status = {}
    for index_status_region in status_region:

        period_index = index_status_region["period"]
        if period_index_temp == "":
            period_index_temp = period_index
            monthly_status["period"] = period_index
            monthly_status[index_status_region["area"][0:1]] = index_status_region[
                "num"
            ]
            # monthly_status['period'] = period_index
        elif (period_index_temp == period_index) is False:
            status_region_list.append(monthly_status)
            monthly_status = {}
            period_index_temp = period_index
            monthly_status[index_status_region["area"][0:1]] = index_status_region[
                "num"
            ]
            # monthly_status['period'] = period_index
        else:
            monthly_status["period"] = period_index
            monthly_status[index_status_region["area"][0:1]] = index_status_region[
                "num"
            ]

    status_region_list.append(monthly_status)

    status_region_amount_list = []
    period_amount_index_temp = ""
    monthly_amount_status = {}
    for index_status_region in status_region:

        period_amount_index = index_status_region["period"]
        if period_amount_index_temp == "":
            monthly_amount_status["period"] = period_amount_index
            period_amount_index_temp = period_amount_index
            monthly_amount_status[
                index_status_region["area"][0:1]
            ] = index_status_region["amount"]
            # monthly_status['period'] = period_index
        elif (period_amount_index_temp == period_amount_index) is False:
            status_region_amount_list.append(monthly_amount_status)
            monthly_amount_status = {}
            period_amount_index_temp = period_amount_index
            monthly_amount_status[
                index_status_region["area"][0:1]
            ] = index_status_region["amount"]
            # monthly_status['period'] = period_index
        else:
            monthly_amount_status["period"] = period_amount_index
            monthly_amount_status[
                index_status_region["area"][0:1]
            ] = index_status_region["amount"]

    status_region_amount_list.append(monthly_amount_status)
    content = {
        "order_status_list": order_analyse,
        "buyer_status_list": status_analyse,
        "region_status_list": status_region_list,
        "status_region_amount_list": status_region_amount_list,
    }
    if request.session.get("lge") == "en":
        return render(request, "order_vis1.html", content)
    else:
        return render(request, "order_vis.html", content)

@login_required
def inv_vis(request):
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    if request.session.get("lge") == "en":
        strr = """
        select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        FORMAT(sum(t1.sale_num),0) as sale_num,
        FORMAT(sum(t1.sale_out_number*-1),0) as sale_out_number,
        FORMAT(sum(t1.order_deal_num),0) as order_deal_num,
        FORMAT(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        FORMAT(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        FORMAT(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        FORMAT(sum(t1.opening_inventory),0) as opening_inventory,
        FORMAT(sum(t1.purchase_in),0) as purchase_in,
        FORMAT(sum(t1.other_in),0) as other_in,
        FORMAT(sum(t1.trade_out),0) as trade_out,
        FORMAT(sum(t1.other_out),0) as other_out,
        FORMAT(sum(t1.ending_inventory),0) as ending_inventory,
        FORMAT(sum(t1.diff_inventory),0) as diff_inventory,
        FORMAT(sum(t1.in_out_num),0) as in_out_num,
        FORMAT(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name,gpc
        ORDER BY period
        desc
    """
    else:
        strr = """
        select t1.period,t1.goods_id,t1.goods_name,t2.gpc,
        FORMAT(sum(t1.sale_num),0) as sale_num,
        FORMAT(sum(t1.sale_out_number*-1),0) as sale_out_number,
        FORMAT(sum(t1.order_deal_num),0) as order_deal_num,
        FORMAT(sum(t1.sale_amount),2) as sale_amount,
        FORMAT(sum(t1.sale_out_amount),2) as sale_out_amount,
        FORMAT(sum(t1.order_deal_amount),2) as order_deal_amount,
        FORMAT(sum(t1.opening_inventory),0) as opening_inventory,
        FORMAT(sum(t1.purchase_in),0) as purchase_in,
        FORMAT(sum(t1.other_in),0) as other_in,
        FORMAT(sum(t1.trade_out),0) as trade_out,
        FORMAT(sum(t1.other_out),0) as other_out,
        FORMAT(sum(t1.ending_inventory),0) as ending_inventory,
        FORMAT(sum(t1.diff_inventory),0) as diff_inventory,
        FORMAT(sum(t1.in_out_num),0) as in_out_num,
        FORMAT(sum(t1.trans_amount),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name,gpc
        ORDER BY period
        desc
    """
    data.execute(strr)
    inv_count = data.fetchall()
    content = {"inv_count": inv_count}
    if request.session.get("lge") == "en":
        print("en")
        return render(request, "inv_vis1.html", content)
    else:
        print("ch")
        return render(request, "inv_vis.html", content)


@login_required
def basics_vis(request):
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)

    strr_tax = """
        select id,time,tax 
        from tax_rate 
        ORDER BY time 
        desc
    """
    data.execute(strr_tax)
    tax_list = data.fetchall()

    strr_goods = """
        select id,goods_id,goods_name,gpc,sku,products 
        from goods 
        ORDER BY goods_id 
    """
    data.execute(strr_goods)
    goods_list = data.fetchall()

    strr_sku = """
        select seq_no,sku_id,sku_name,price,products  
        from t_bas_sku_price 
        ORDER BY seq_no 
    """
    data.execute(strr_sku)
    sku_list = data.fetchall()

    content = {"tax": tax_list, "goods": goods_list, "sku": sku_list}

    return render(request, "basics_vis.html", content)
    # return render(request, "basics_vis.html", content)


def jump_to_load(request):
    try:
        service.loaddata(setting.BASE_FILE_PATH.get("upload_path"))
        return HttpResponse("success")
    except Exception as identifier:
        return HttpResponse("false")


@csrf_exempt
def get_bom_data(request):
    add_bom()
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    strr_bom = """
        SELECT * FROM bom a LEFT JOIN bom_detail b ON a.product_name =b.product_name ORDER BY Num desc
    """
    data.execute(strr_bom)

    bom_list = data.fetchall()
    bom_list_res = []
    bom_num = 0
    strr_temp = ''
    bom_row = {}
    i = 0
    for bom_index in bom_list:
        
        if i==0:
            bom_row['Num'] = bom_index["Num"]
            bom_row['product_name'] = bom_index["product_name"]
            bom_row['price'] = str(bom_index["price"])
            
        else:
            if bom_num == bom_index['Num']:
                if(i<len(bom_list)-1):
                    strr_temp = strr_temp +","+ bom_index['goods_id']+"("+str(bom_index['goods_count'])+")"
                else:
                    strr_temp = strr_temp + "," + bom_index['goods_id'] + "("+str(bom_index['goods_count'])+")"
                    print (strr_temp)
                    bom_row["goods"] = strr_temp
                    bom_list_res.append(bom_row)
            else:
                bom_row["goods"] = strr_temp
                bom_list_res.append(bom_row)
                bom_row = {}
                if bom_index['goods_id'] is not None :
                    strr_temp = bom_index['goods_id']+"("+str(bom_index['goods_count'])+")"
                else:
                    strr_temp = bom_index['goods_id']

        bom_num = bom_index["Num"]
        i = i+1
        bom_row['Num'] = bom_index["Num"]
        bom_row['product_name'] = bom_index["product_name"]
        bom_row['price'] = str(bom_index["price"])
    return HttpResponse(json.dumps(bom_list_res), content_type="application/json")


@csrf_exempt
def update_bom_edit(request):
    if request.method == "POST":
        print(request.POST)
        product_name = request.POST.__getitem__("product_name")
        Num = request.POST.__getitem__("Num")
        price = request.POST.__getitem__("price")
        goods = request.POST.__getitem__("goods")
        
        print(goods)
        db = MySQLdb.connect(
            setting.DATABASES.get("default").get("HOST"),
            setting.DATABASES.get("default").get("USER"),
            setting.DATABASES.get("default").get("PASSWORD"),
            setting.DATABASES.get("default").get("NAME"),
            setting.DATABASES.get("default").get("PORT"),
            charset="utf8",
        )
        data = db.cursor(MySQLdb.cursors.DictCursor)

        delete_strr = "DELETE from bom_detail WHERE product_name = '%s'" % (product_name)
        data.execute(delete_strr)
        goods_list = goods.split(',')
        for good in goods_list:
            print(good[0:good.find('(')])
            print(int(good[good.find('(')+1:good.find(')')]))
            insert_strr = "INSERT into bom_detail (product_name,goods_id,goods_count) VALUES ('%s','%s',%d) " % (
                product_name, good[0:good.find('(')], int(good[good.find('(')+1:good.find(')')]))

            print(insert_strr)

            data.execute(insert_strr)

        db.commit()
        print("update success")
        return HttpResponse("success")
    else:
        print("update false")
        return HttpResponse("false")


def add_bom():
    tamll_detail = mydb.exec_sql_select("""
    SELECT DISTINCT
	(product_name)
    FROM
	load_tmallsodetail_info
    """)
    bom_list = mydb.exec_sql_select("""
    SELECT
        (product_name)
    FROM
        bom
    """)
    res = []
    detail_value_list = list(tamll_detail)
    bom_value_list = list(bom_list)
    for one_detail in detail_value_list:
        if one_detail not in bom_value_list:
            res.append(one_detail)
    print(res)
    sqllist=[]
    for oneres in res:
        sqlstr = "insert into bom (product_name) values ('%s')" %oneres['product_name']
        sqllist.append(sqlstr)
    mydb.exec_sql_list(sqllist)

@csrf_exempt
def upload(request):
    try:
        if request.method == "POST":
            reqfiles = request.FILES.getlist("file", None)
            if not reqfiles:
                return HttpResponse("empty")
            for file in reqfiles:
                storefile = open(
                    os.path.join(
                        setting.BASE_DIR,
                        setting.BASE_FILE_PATH.get("upload_path"),
                        file.name,
                    ),
                    "wb+",
                )
                for chunk in file.chunks():
                    storefile.write(chunk)
                storefile.close()
                csvfilename = os.path.join(
                    setting.BASE_DIR,
                    setting.BASE_FILE_PATH.get("upload_path"),
                    file.name,
                )
                print(csvfilename)
                fileupload = vismodels.FileUpload(file_name=file.name)
                fileupload.file_path = csvfilename
                fileupload.file_type = request.POST.get("type")
                fileupload.upload_time = datetime.datetime.now()
                fileupload.del_mark = "N"
                fileupload.save()
            return HttpResponse(
                json.dumps(service.readcsv(csvfilename)),
                content_type="application/json",
            )

        else:
            return HttpResponse("wrong")
    except UnicodeDecodeError as identifier:
        return HttpResponse("decodeError")


@csrf_exempt
def UndoUpload(request):
    print("undoUpload")
    fileuploadobj = vismodels.FileUpload.objects.filter(
        file_type=request.POST.get("type"), file_name=request.POST.get("filename", None)
    )
    fileuploadobj.delete()

    return HttpResponse("撤回")


num_process = 0


@csrf_exempt
def load_data_to_db(request):
    filenamelist = request.POST.get("filenamelist").split(",")
    print(filenamelist)
    print(len(filenamelist))
    global num_process
    len_filelist = len(filenamelist)
    num_process = 0
    i = 0
    for filename in filenamelist:
        print(filename)
        filepath = vismodels.FileUpload.objects.filter(
            file_name=filename[filename.rfind("/") + 1 : len(filename)]
        )
        print(filepath[0].file_path)
        service.load_csv_file(filepath[0].file_path, filename)
        num_process = i * 100 / len_filelist
    num_process = 100
    return HttpResponse("success")


@csrf_exempt
def load_data_to_db_process(request):
    global num_process
    return HttpResponse(num_process)


@csrf_exempt
def analyse_data(request):
    try:
        service.analyse_data()
        return HttpResponse("success")
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))


@csrf_exempt
def analyse_data_process(request):
    print(service.analyse_data_process())
    return HttpResponse(service.analyse_data_process())


def test1_view(request):
    # 获得系统本地时间，返回的格式是 UTC 中的 struct_time 数据
    t = time.localtime()
    # 第 6 个元素是 tm_wday , 范围为 [0,6], 星期一 is 0
    n = t[6]
    # 星期一到星期日字符串，每个字符串用 _() 标识出来。
    weekdays = [
        _("Monday"),
        _("Tuesday"),
        _("Wednesday"),
        _("Thursday"),
        _("Friday"),
        _("Saturday"),
        _("Sunday"),
    ]
    # 返回一个 HttpResponse

    return HttpResponse(weekdays[n])


@csrf_exempt
def login(request):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.method == "POST":
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        print(password)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)

            return HttpResponse(json.dumps({'status': True, 'nowtime': nowtime}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': False, 'nowtime': nowtime, 'msg': 'username or password is wrong'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': False, 'nowtime': nowtime, 'msg': 'http method is not POST'}), content_type="application/json")

def fee_vis(request):


    storage_fee_strr = """
    SELECT 
    t_other_fee_info.trans_date,
    format(tmall_warehouse_fee/tax_rate.tax,2) as a,
    0.00 as b,
    0.00 as c,
    0.00 as d,
    format(insurance_fee/tax_rate.tax,2) as e,
    0.00 as f,
    0.00 as g
    from t_other_fee_info,
    tax_rate
    where 1=1
    -- and trans_date LIKE '2018-01%'
    and tax_rate.time=t_other_fee_info.trans_date
    order by t_other_fee_info.trans_date
    desc
    ;
    """

    other_fee_strr = """
    SELECT 
    t_other_fee_info.trans_date,
    format(merchant_pay_to_custom/tax_rate.tax,2) as a,
    format(cainiao_pay_goodsfee_to_merchant/tax_rate.tax,2) as b,
    format(cainiao_pay_deposit_to_merchant/tax_rate.tax,2) as c,
    format(popularize_fee/tax_rate.tax,2) as d,
    format(other_payback_fee/tax_rate.tax,2) as e,
    format(annual_service/tax_rate.tax,2) as f,
    format(tmall_popularize_fee/tax_rate.tax,2) as g
    from t_other_fee_info,
    tax_rate
    where 1=1
    -- and trans_date LIKE '2018-01%'
    and tax_rate.time=t_other_fee_info.trans_date
    order by t_other_fee_info.trans_date
    desc
    ;
    """

    list_date = mydb.exec_sql_select("SELECT SUBSTR(in_out_time FROM 1 FOR 7) as date_str from load_transaction_info GROUP BY SUBSTR(in_out_time FROM 1 FOR 7) desc")
    delivery_fee_res = mydb.exec_sql_select(
        "select * from t_fee_monthly_detail_info ORDER BY month_str desc")

    fee_payment = mydb.exec_sql_select(
        "SELECT * from t_other_fee_add_info ORDER BY date_str desc")

    stroage_fee_res = mydb.exec_sql_select(storage_fee_strr)
    #print(stroage_fee_res)
    other_fee_res = mydb.exec_sql_select(other_fee_strr)
    content = {"storage_fee_res": stroage_fee_res,
               "other_fee_res": other_fee_res, "delivery_fee_res": delivery_fee_res, "fee_payment": fee_payment}
    return render(request, "fee_vis.html",content)

@csrf_exempt
def update_stroage_table(request):
    if request.method == "POST":
        print(request.POST.__getitem__('0'))
        
        #mydb.exec_sql("update t_other_fee_info set ")
        return HttpResponse("")

@csrf_exempt
def update_fee_table(request):
    if request.method == "POST":
        print(request.POST.__getitem__('0'))
        exec_sql_str = "update t_other_fee_add_info set marketing_fee = %s,crm = %s,tmall_software = %s where date_str = '%s'" % (str(request.POST.__getitem__('1'))[1:], str(request.POST.__getitem__('2'))[1:], str(request.POST.__getitem__('3'))[1:], str(request.POST.__getitem__('0')))
        print(exec_sql_str)
        mydb.exec_sql(exec_sql_str)
        return HttpResponse("success")


def order_export(request):
    
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    t_year = request.GET.get('sel')
    data = db.cursor(MySQLdb.cursors.DictCursor)

    ############################
    sio = io.StringIO()
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=order.xls"
    response.write(sio.getvalue())
    return response


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    # style.borders = borders

    return style


# 导出excel表格
def excel_export(request):
    years = request.GET.get("sel")
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    
    ############################
    sio = io.StringIO()
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=goods.xls"
    response.write(sio.getvalue())
    return response


def excel_export2(request):
    years = request.GET.get("sel")
    all_list = []
    db = MySQLdb.connect(
        setting.DATABASES.get("default").get("HOST"),
        setting.DATABASES.get("default").get("USER"),
        setting.DATABASES.get("default").get("PASSWORD"),
        setting.DATABASES.get("default").get("NAME"),
        setting.DATABASES.get("default").get("PORT"),
        charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    
    ############################
    sio = io.StringIO()
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=sum.xls"
    response.write(sio.getvalue())
    return response
