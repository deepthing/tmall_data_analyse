# -*- coding: utf-8 -*-

import datetime
import io
import json
import os
import time

import MySQLdb
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from numpy.f2py.auxfuncs import isfalse
from django.shortcuts import render_to_response
from django.template import RequestContext 

import load.service as service
import tmall_data_analyse.settings as setting

import vis.models as vismodels
from _ctypes import Union

from .models import TGoodsNumInfo

def index(request):
    return render(request, "nav.html")

def loadcsv(request):
    print(request.LANGUAGE_CODE)
    return render(request, 'load_csv_vis.html', locals())


def testd3(request):
    return render(request, "d3.html")


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


def order_export(request):

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
                select 
                SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
                SUBSTR(t1.fin_period FROM 6 FOR 2) as period1,
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
                where SUBSTR(t1.fin_period FROM 1 FOR 4)=%s
                GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
                asc
                """
    else:
        strr = """
            select 
            SUBSTR(fin_period FROM 1 FOR 7) as period,
            SUBSTR(fin_period FROM 6 FOR 2) as period1,
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
            where SUBSTR(fin_period FROM 1 FOR 4)=%s
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            order by fin_period asc
     
              """
    data.execute(strr, [t_year])
    inv_count = data.fetchall()
    ws = xlwt.Workbook(encoding="utf-8")
    if request.session.get("lge") == "en":
        w = ws.add_sheet("Order Analysis", cell_overwrite_ok=True)
    else:
        w = ws.add_sheet("订单分析", cell_overwrite_ok=True)
        # s = ws.add_sheet("金额分析",cell_overwrite_ok=True)
        # t = ws.add_sheet("货品分析",cell_overwrite_ok=True)
    style_yy = xlwt.easyxf(
        """
            font:
            name Arial,
            colour_index black,
            bold on,
            height 0xA0;
            align:
            wrap off,
            vert center,
            horiz center;
            pattern:
            pattern solid,
            fore-colour white;
            borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;  
            """
    )

    style_ss = xlwt.easyxf(
        """
            font:
            name Arial,
            colour_index black,
            bold on,
            height 0xA0;
            align:
            wrap off,
            vert center,
            horiz center;
            pattern:
            pattern solid,
            fore-colour orange
            """
    )
    style_heading = xlwt.easyxf(
        """
            font:
            name Arial,
            colour_index black,
            bold on,
            height 0xA0;
            align:
            wrap off,
            vert center,
            horiz center;
            pattern:
            pattern solid,
            fore-colour yellow;
            borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
            """
    )
    style_hh = xlwt.easyxf(
        """
            font:
            name SimSun,
            colour_index black,
            bold on,
            height 720;
            align:
            wrap off,
            vert center,
            horiz center;
            pattern:
            pattern solid,
            fore-colour white;
            borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
            """
    )

    style_body = xlwt.easyxf(
        """
            font:
            name Arial,
            bold off,
            height 0XA0;
            align:
            wrap on,
            vert center,
            horiz left;
            borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
            """
    )
    style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    first_row = w.row(0)
    tall_style = xlwt.easyxf("font:height 720;")
    first_row.set_style(tall_style)
    if request.session.get("lge") == "en":
        w.write_merge(
            0,
            6,
            0,
            15,
            "订单分析报表"
            + "\n"
            + "报表参数：订单分析/"
            + t_year
            + "\n"
            + "生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write_merge(8, 13, 0, 0, "Order Status (by Volume)", style_heading)
        w.write_merge(14, 19, 0, 0, "Order Status (by USD)", style_heading)
        w.write_merge(20, 25, 0, 0, "Buyers Analysis (by Vol)", style_heading)
        w.write_merge(26, 29, 0, 0, "Buyers Analysis (by USD)", style_heading)
        w.write_merge(30, 37, 0, 0, "Region Analysis (by Vol)", style_heading)
        w.write_merge(38, 45, 0, 0, "Region Analysis (By USD)", style_heading)
        w.write(7, 0, "统计维度", style_heading)
        w.col(0).width = 90 * 50
        w.write(7, 1, "统计项目", style_heading)
        w.write(7, 2, t_year + "01", style_ss)
        w.write(7, 3, t_year + "02", style_ss)
        w.write(7, 4, t_year + "03", style_ss)
        w.write(7, 5, t_year + "04", style_ss)
        w.write(7, 6, t_year + "05", style_ss)
        w.write(7, 7, t_year + "06", style_ss)
        w.write(7, 8, t_year + "07", style_ss)
        w.write(7, 9, t_year + "08", style_ss)
        w.write(7, 10, t_year + "09", style_ss)
        w.write(7, 11, t_year + "10", style_ss)
        w.write(7, 12, t_year + "11", style_ss)
        w.write(7, 13, t_year + "12", style_ss)
        w.col(1).width = 120 * 50
        w.write(8, 1, "Total Orders", style_heading)
        w.write(9, 1, "Successful Orders", style_heading)
        w.write(10, 1, "Closed Orders", style_heading)
        w.write(11, 1, "Open Orders", style_heading)
        w.write(12, 1, "Closed Orders due to no payment", style_heading)
        w.write(13, 1, "Closed orders due to refunds", style_heading)
        w.write(14, 1, "Total Orders", style_heading)
        w.write(15, 1, "Successful Orders", style_heading)
        w.write(16, 1, "Closed Orders", style_heading)
        w.write(17, 1, "Open Orders", style_heading)
        w.write(18, 1, "Closed Orders due to no payment", style_heading)
        w.write(19, 1, "Closed orders due to refunds", style_heading)
    else:
        w.write_merge(
            0,
            6,
            0,
            15,
            "订单分析报表"
            + "\n"
            + "报表参数：订单分析/"
            + t_year
            + "\n"
            + "生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write_merge(8, 13, 0, 0, "状态分析(数量)", style_heading)
        w.write_merge(14, 19, 0, 0, "状态分析金额", style_heading)
        w.write_merge(20, 25, 0, 0, "账号分析（数量）", style_heading)
        w.write_merge(26, 29, 0, 0, "账号分析（金额)", style_heading)
        w.write_merge(30, 37, 0, 0, "区域分析（数量)", style_heading)
        w.write_merge(38, 45, 0, 0, "区域分析（金额)", style_heading)
        w.write(7, 0, "统计维度", style_heading)
        w.col(0).width = 90 * 50
        w.write(7, 1, "统计项目", style_heading)
        w.write(7, 2, t_year + "01", style_ss)
        w.write(7, 3, t_year + "02", style_ss)
        w.write(7, 4, t_year + "03", style_ss)
        w.write(7, 5, t_year + "04", style_ss)
        w.write(7, 6, t_year + "05", style_ss)
        w.write(7, 7, t_year + "06", style_ss)
        w.write(7, 8, t_year + "07", style_ss)
        w.write(7, 9, t_year + "08", style_ss)
        w.write(7, 10, t_year + "09", style_ss)
        w.write(7, 11, t_year + "10", style_ss)
        w.write(7, 12, t_year + "11", style_ss)
        w.write(7, 13, t_year + "12", style_ss)
        w.col(1).width = 120 * 50
        w.write(8, 1, "订单总数量", style_heading)
        w.write(9, 1, "交易成功订单数量", style_heading)
        w.write(10, 1, "交易关闭订单数量", style_heading)
        w.write(11, 1, "其他状态订单数量", style_heading)
        w.write(12, 1, "关闭(买家未付款)订单数量", style_heading)
        w.write(13, 1, "关闭(退款)订单数量", style_heading)
        w.write(14, 1, "订单总金额", style_heading)
        w.write(15, 1, "交易成功订单金额", style_heading)
        w.write(16, 1, "交易关闭订单金额", style_heading)
        w.write(17, 1, "其他状态订单金额", style_heading)
        w.write(18, 1, "关闭(买家未付款)订单金额", style_heading)
        w.write(19, 1, "关闭(退款)订单金额", style_heading)
    Indexs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    nullIndexs = []
    for it in Indexs:
        isStu = False
        for iv in inv_count:
            period = int(iv["period1"]) + 1
            if period == it:
                isStu = True
        if isStu != True:
            nullIndexs.append(it)

    for nindex in nullIndexs:
        w.write(8, nindex, "0", style_yy)
        w.write(9, nindex, "0", style_yy)
        w.write(10, nindex, "0", style_yy)
        w.write(11, nindex, "0", style_yy)
        w.write(12, nindex, "0", style_yy)
        w.write(13, nindex, "0", style_yy)
        w.write(12, nindex, "0", style_yy)
        w.write(14, nindex, 0, style_yy)
        w.write(15, nindex, 0, style_yy)
        w.write(16, nindex, 0, style_yy)
        w.write(17, nindex, 0, style_yy)
        w.write(18, nindex, 0, style_yy)
        w.write(19, nindex, 0, style_yy)

    i = 2
    for it in inv_count:
        w.write(8, int(it["period1"]) + 1, it["sum_order_num"], style_yy)
        w.write(9, int(it["period1"]) + 1, it["sum_saled_num"], style_yy)
        w.write(10, int(it["period1"]) + 1, it["sum_closed_num"], style_yy)
        w.write(11, int(it["period1"]) + 1, it["sum_waiting_num"], style_yy)
        w.write(12, int(it["period1"]) + 1, it["sum_close_unpaid_num"], style_yy)
        w.write(13, int(it["period1"]) + 1, it["sum_close_return_num"], style_yy)
        if request.session.get("lge") == "en":
            w.write(14, int(it["period1"]) + 1, "$" + it["sum_order_amount"], style_yy)
            w.write(15, int(it["period1"]) + 1, "$" + it["sum_saled_amount"], style_yy)
            w.write(16, int(it["period1"]) + 1, "$" + it["sum_closed_amount"], style_yy)
            w.write(
                17, int(it["period1"]) + 1, "$" + it["sum_waiting_amount"], style_yy
            )
            w.write(
                18,
                int(it["period1"]) + 1,
                "$" + it["sum_close_unpaid_amount"],
                style_yy,
            )
            w.write(
                19,
                int(it["period1"]) + 1,
                "$" + it["sum_close_unpaid_amount"],
                style_yy,
            )

        else:
            w.write(14, int(it["period1"]) + 1, "￥" + it["sum_order_amount"], style_yy)
            w.write(15, int(it["period1"]) + 1, "￥" + it["sum_saled_amount"], style_yy)
            w.write(16, int(it["period1"]) + 1, "￥" + it["sum_closed_amount"], style_yy)
            w.write(
                17, int(it["period1"]) + 1, "￥" + it["sum_waiting_amount"], style_yy
            )
            w.write(
                18,
                int(it["period1"]) + 1,
                "￥" + it["sum_close_unpaid_amount"],
                style_yy,
            )
            w.write(
                19,
                int(it["period1"]) + 1,
                "￥" + it["sum_close_unpaid_amount"],
                style_yy,
            )

        w.col(i).width = 60 * 50
        i += 1

    if request.session.get("lge") == "en":
        strr_buyer = """
            select 
            period,
            FORMAT(t1.total_count/t2.tax,0) as total_count,
            SUBSTR(t1.period FROM 6 FOR 2) as period1,
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
            where SUBSTR(t1.period FROM 1 FOR 4)=%s
            order by period
            asc
            """
    else:
        strr_buyer = """
            select 
            period,
            SUBSTR(period FROM 6 FOR 2) as period1,
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
            where SUBSTR(period FROM 1 FOR 4)=%s
            order by period
            asc
        """
    data.execute(strr_buyer, [t_year])
    account_count = data.fetchall()
    if request.session.get("lge") == "en":
        w.write(20, 1, "Total Buyers", style_heading)
        w.write(21, 1, "New Buyers", style_heading)
        w.write(22, 1, "Repeat Buyers", style_heading)
        w.write(23, 1, "Orders from non-alipay accounts", style_heading)
        w.write(24, 1, "of orders from New buyers", style_heading)
        w.write(25, 1, "of orders from Repeat Buyers", style_heading)
        w.write(26, 1, "order amount from Total Buyers", style_heading)
        w.write(27, 1, "order amount from non alipay ID buyers", style_heading)
        w.write(28, 1, "order amount from new buyers", style_heading)
        w.write(29, 1, "Order amount from repeat buyers", style_heading)

    else:
        w.write(20, 1, "账号总数", style_heading)
        w.write(21, 1, "新账号数", style_heading)
        w.write(22, 1, "老账号数", style_heading)
        w.write(23, 1, "无账号订单数", style_heading)
        w.write(24, 1, "新账号订单数", style_heading)
        w.write(25, 1, "老账号订单数", style_heading)
        w.write(26, 1, "账号总订单金额", style_heading)
        w.write(27, 1, "无账号订单金额", style_heading)
        w.write(28, 1, "新账号订单金额", style_heading)
        w.write(29, 1, "老账号订单金额", style_heading)

    Index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    nullIndex = []
    for it in Index:
        isStu = False
        for iv in account_count:
            period = int(iv["period1"]) + 1
            if period == it:
                isStu = True
        if isStu != True:
            nullIndex.append(it)

    for it in nullIndex:
        w.write(20, it, 0, style_yy)
        w.write(21, it, 0, style_yy)
        w.write(22, it, 0, style_yy)
        w.write(23, it, 0, style_yy)
        w.write(24, it, 0, style_yy)
        w.write(25, it, 0, style_yy)
        w.write(26, it, 0, style_yy)
        w.write(27, it, 0, style_yy)
        w.write(28, it, 0, style_yy)
        w.write(29, it, 0, style_yy)
    e = 2
    for it in account_count:
        w.write(20, int(it["period1"]) + 1, it["total_count"], style_yy)
        w.write(21, int(it["period1"]) + 1, it["new_count"], style_yy)
        w.write(22, int(it["period1"]) + 1, it["old_count"], style_yy)
        w.write(23, int(it["period1"]) + 1, it["no_account_orders"], style_yy)
        w.write(24, int(it["period1"]) + 1, it["new_orders"], style_yy)
        w.write(25, int(it["period1"]) + 1, it["old_orders"], style_yy)
        w.write(26, int(it["period1"]) + 1, it["total_amount"], style_yy)
        if request.session.get("lge") == "en":
            w.write(27, int(it["period1"]) + 1, "$" + it["no_account_amount"], style_yy)
            w.write(28, int(it["period1"]) + 1, "$" + it["new_orders_amount"], style_yy)
            w.write(29, int(it["period1"]) + 1, "$" + it["old_orders_amount"], style_yy)
        else:
            w.write(27, int(it["period1"]) + 1, "￥" + it["no_account_amount"], style_yy)
            w.write(28, int(it["period1"]) + 1, "￥" + it["new_orders_amount"], style_yy)
            w.write(29, int(it["period1"]) + 1, "￥" + it["old_orders_amount"], style_yy)
        w.col(e).width = 60 * 50
        e += 1

    if request.session.get("lge") == "en":
        strr_region = """
            SELECT
            SUBSTR(t1.fin_period FROM 1 FOR 7) AS period,
            SUBSTR(t1.fin_period FROM 6 FOR 2) AS period1,
            t1.area_info AS area,
            FORMAT(SUM(t1.order_number),0) AS num,
            FORMAT(SUM(t1.order_amount/t2.tax),2) AS amount
            FROM
            t_order_area as t1 
            left join  tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            where SUBSTR(t1.fin_period FROM 1 FOR 4)=%s
            GROUP BY
            SUBSTR(t1.fin_period FROM 1 FOR 7),
            area_info
            ORDER BY period asc
            """
    else:
        strr_region = """
            SELECT
            SUBSTR(fin_period FROM 1 FOR 7) AS period,
            SUBSTR(fin_period FROM 6 FOR 2) AS period1,
            area_info AS area,
            FORMAT(SUM(order_number),0) AS num,
            FORMAT(SUM(order_amount),2) AS amount
            FROM
            t_order_area
            where SUBSTR(fin_period FROM 1 FOR 4)=%s
            GROUP BY
            SUBSTR(fin_period FROM 1 FOR 7),
            area_info
            ORDER BY period asc
            """
    data.execute(strr_region, [t_year])
    status_region = data.fetchall()
    status_region_list = []
    period_index_temp = ""
    monthly_status = {}
    for index_status_region in status_region:

        period_index = index_status_region["period1"]
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

    if request.session.get("lge") == "en":
        w.write(30, 1, "East Region", style_heading)
        w.write(31, 1, "Mid Region", style_heading)
        w.write(32, 1, "South Region", style_heading)
        w.write(33, 1, "Southwest Region", style_heading)
        w.write(34, 1, "Northeast Region", style_heading)
        w.write(35, 1, "North Region", style_heading)
        w.write(36, 1, "Northwest Region", style_heading)
        w.write(37, 1, "Others", style_heading)
        w.write(38, 1, "East Region", style_heading)
        w.write(39, 1, "Mid Region", style_heading)
        w.write(40, 1, "South Region", style_heading)
        w.write(41, 1, "Southwest Region", style_heading)
        w.write(42, 1, "Northeast Region", style_heading)
        w.write(43, 1, "North Region", style_heading)
        w.write(44, 1, "Northwest Region", style_heading)
        w.write(45, 1, "Others", style_heading)
    else:
        w.write(30, 1, "华东订单数量", style_heading)
        w.write(31, 1, "华中订单数量", style_heading)
        w.write(32, 1, "华南订单数量", style_heading)
        w.write(33, 1, "西南订单数量", style_heading)
        w.write(34, 1, "东北订单数量", style_heading)
        w.write(35, 1, "华北订单数量", style_heading)
        w.write(36, 1, "西北订单数量", style_heading)
        w.write(37, 1, "其他区域订单数量", style_heading)
        w.write(38, 1, "华东订单金额", style_heading)
        w.write(39, 1, "华中订单金额", style_heading)
        w.write(40, 1, "华南订单金额", style_heading)
        w.write(41, 1, "西南订单金额", style_heading)
        w.write(42, 1, "东北订单金额", style_heading)
        w.write(43, 1, "华北订单金额", style_heading)
        w.write(44, 1, "西北订单金额", style_heading)
        w.write(45, 1, "其他区域金额", style_heading)
    areas = ["1", "2", "3", "4", "5", "6", "7", "9"]
    e = 2
    for it in status_region_list:

        for iv in areas:
            if len(it) < 9:
                if (iv in it) == False:
                    it[iv] = "0"

        w.write(30, int(it["period"]) + 1, it["1"], style_yy)
        w.write(31, int(it["period"]) + 1, it["2"], style_yy)
        w.write(32, int(it["period"]) + 1, it["3"], style_yy)
        w.write(33, int(it["period"]) + 1, it["4"], style_yy)
        w.write(34, int(it["period"]) + 1, it["5"], style_yy)
        w.write(35, int(it["period"]) + 1, it["6"], style_yy)
        w.write(36, int(it["period"]) + 1, it["7"], style_yy)
        w.write(37, int(it["period"]) + 1, it["9"], style_yy)
        w.col(e).width = 60 * 50
        e += 1
    Id = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    nullIndex1 = []
    for it in Id:
        isStu = False
        for iv in status_region_list:
            period = int(iv["period"]) + 1
            if period == it:
                isStu = True
        if isStu != True:
            nullIndex1.append(it)

    for it in nullIndex1:
        w.write(30, it, 0, style_yy)
        w.write(31, it, 0, style_yy)
        w.write(32, it, 0, style_yy)
        w.write(33, it, 0, style_yy)
        w.write(34, it, 0, style_yy)
        w.write(35, it, 0, style_yy)
        w.write(36, it, 0, style_yy)
        w.write(37, it, 0, style_yy)
        w.write(38, it, 0, style_yy)
        w.write(39, it, 0, style_yy)
        w.write(40, it, 0, style_yy)
        w.write(41, it, 0, style_yy)
        w.write(42, it, 0, style_yy)
        w.write(43, it, 0, style_yy)
        w.write(41, it, 0, style_yy)
        w.write(42, it, 0, style_yy)
        w.write(43, it, 0, style_yy)
        w.write(44, it, 0, style_yy)
        w.write(45, it, 0, style_yy)

    status_region_amount_list = []
    period_amount_index_temp = ""
    monthly_amount_status = {}
    for index_status_region in status_region:

        period_amount_index = index_status_region["period1"]
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

    e = 2
    for it in status_region_amount_list:
        for iv in areas:
            if len(it) < 9:
                if (iv in it) == False:
                    it[iv] = "0"
        if request.session.get("lge") == "en":
            w.write(38, int(it["period"]) + 1, "$" + it["1"], style_yy)
            w.write(39, int(it["period"]) + 1, "$" + it["2"], style_yy)
            w.write(40, int(it["period"]) + 1, "$" + it["3"], style_yy)
            w.write(41, int(it["period"]) + 1, "$" + it["4"], style_yy)
            w.write(42, int(it["period"]) + 1, "$" + it["5"], style_yy)
            w.write(43, int(it["period"]) + 1, "$" + it["6"], style_yy)
            w.write(44, int(it["period"]) + 1, "$" + it["7"], style_yy)
            w.write(45, int(it["period"]) + 1, "$" + it["9"], style_yy)
        else:
            w.write(38, int(it["period"]) + 1, "￥" + it["1"], style_yy)
            w.write(39, int(it["period"]) + 1, "￥" + it["2"], style_yy)
            w.write(40, int(it["period"]) + 1, "￥" + it["3"], style_yy)
            w.write(41, int(it["period"]) + 1, "￥" + it["4"], style_yy)
            w.write(42, int(it["period"]) + 1, "￥" + it["5"], style_yy)
            w.write(43, int(it["period"]) + 1, "￥" + it["6"], style_yy)
            w.write(44, int(it["period"]) + 1, "￥" + it["7"], style_yy)
            w.write(45, int(it["period"]) + 1, "￥" + it["9"], style_yy)
        w.col(e).width = 60 * 50
        e += 1

    exist_file = os.path.exists("订单分析.xls")
    if exist_file:
        os.remove(r"order.xls")
        ws.save("order.xls")
    ############################
    sio = io.StringIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=order.xls"
    response.write(sio.getvalue())
    return response


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


def fee_vis(request):
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
        strr_fee_amount = """
        select 
        SUBSTR(t1.period FROM 1 FOR 7) as period ,
        FORMAT(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
        FORMAT(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
        FORMAT(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
        FORMAT(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
        FORMAT(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
        FORMAT(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
        FROM
        t_settle_amount_info as t1
        left join tax_rate as t2
        on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
        GROUP BY SUBSTR(period FROM 1 FOR 7)
        desc
    """
    else:
        strr_fee_amount = """
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
        desc
    """
    data.execute(strr_fee_amount)
    fee_amount_rows = data.fetchall()

    if request.session.get("lge") == "en":
        strr_fee_time = """
        select  
        CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
        FORMAT(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
        FORMAT(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
        FORMAT(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
        FORMAT(SUM(t1.tmall/t2.tax),2) as tmall,
        FORMAT(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
        FORMAT(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
        FORMAT(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
        FORMAT(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
        FORMAT(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
        FORMAT(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
        FROM
        t_settle_fee_info as t1
        left join tax_rate as t2
        on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
        GROUP BY fee_time
        desc
    """
    else:
        strr_fee_time = """
        select  
        CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
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
        GROUP BY fee_time
        desc
    """
    data.execute(strr_fee_time)
    fee_time_rows = data.fetchall()

    dictMergedRow = []
    for strr_fee_amount_index in fee_amount_rows:
        for strr_fee_time_index in fee_time_rows:
            if strr_fee_time_index["fee_time"] == strr_fee_amount_index["period"]:
                dictMerged = strr_fee_amount_index.copy()
                dictMerged.update(strr_fee_time_index)
                dictMergedRow.append(dictMerged)

    if request.session.get("lge") == "en":
        strr_fee_order = """
        select 
        SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
        FORMAT(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
        FORMAT(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
        FORMAT(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
        FORMAT(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
        FORMAT(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
        from t_order_amount  as t1
        left join tax_rate as t2
        on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
        GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
        desc
    """
    else:
        strr_fee_order = """
        select 
        SUBSTR(fin_period FROM 1 FOR 7) as period,
        FORMAT(SUM(tmall_refund+actual_paid),2) as tmall_order,
        FORMAT(SUM(tmall_refund),2) as tmall_order_refund,
        FORMAT(SUM(actual_paid),2) as tmall_order_actual_pay,
        FORMAT(SUM(order_fee*-1),2) as alipay_Fee,
        FORMAT(SUM(alipay_get*-1),2) as alipay_settlement
        from t_order_amount 
        GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
        desc
    """
    data.execute(strr_fee_order)
    fee_order = data.fetchall()
    if request.session.get("lge") == "en":
        strr_fee_order_detail = """
        select 
        SUBSTR(t1.payment_time FROM 1 FOR 7) as period,
        FORMAT(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
        FORMAT(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
        FORMAT(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
        FORMAT(SUM(t1.tmall/t2.tax),2) as tmall,
        FORMAT(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
        from t_fee_info as t1
        left join tax_rate as t2
        on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
        GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
        desc
    """
    else:
        strr_fee_order_detail = """
        select 
        SUBSTR(payment_time FROM 1 FOR 7) as period,
        FORMAT(SUM(t.logisitic_tax),2) as logisitic_tax,
        FORMAT(SUM(t.logisitic_service),2) as logisitic_service,
        FORMAT(SUM(t.alipay_service),2) as alipay_service,
        FORMAT(SUM(t.tmall),2) as tmall,
        FORMAT(SUM(t.juhuasuan),2) as juhuasuan
        from t_fee_info t
        GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
        desc
    """
    data.execute(strr_fee_order_detail)
    fee_order_detail = data.fetchall()

    fee_order_rows = []
    for fee_order_index in fee_order:
        for fee_order_detail_index in fee_order_detail:
            if fee_order_index["period"] == fee_order_detail_index["period"]:
                dictMerged = fee_order_index.copy()
                dictMerged.update(fee_order_detail_index)
                fee_order_rows.append(dictMerged)

    if request.session.get("lge") == "en":
        strr_fee_payment = """
        select 
        SUBSTR(t1.period FROM 1 FOR 7) as period,
        FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
        FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
        FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
        FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
        FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
        from t_myaccount_monthly_info as t1
        left join tax_rate as t2
        on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
        GROUP BY SUBSTR(period FROM 1 FOR 7)
        desc
    """
    else:
        strr_fee_payment = """
        select 
        SUBSTR(period FROM 1 FOR 7) as period,
        FORMAT(SUM(recharge),2) as Recharge,
        FORMAT(SUM(refund),2) as Refund,
        FORMAT(SUM(payment),2) as Payments,
        FORMAT(SUM(order_payment),2) as order_payment,
        FORMAT(SUM(not_order_payment),2) as not_order_payment
        from t_myaccount_monthly_info
        GROUP BY SUBSTR(period FROM 1 FOR 7)
        desc
    """
    data.execute(strr_fee_payment)
    fee_payment = data.fetchall()
    if request.session.get("lge") == "en":
        stt = """
        SELECT t1.trans_date,FORMAT(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,FORMAT(t1.insurance_fee/t2.tax,2) as insurance_fee,FORMAT(t1.destory_fee/t2.tax,2) as destory_fee ,FORMAT(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        FORMAT(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        FORMAT(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        FORMAT(t1.popularize_fee/t2.tax,2) as popularize_fee,
        FORMAT(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        FORMAT(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        FORMAT(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time order by t1.trans_date desc
        """
        data.execute(stt)
        other_fee_detail = data.fetchall()
    else:
        stt = """
          SELECT t1.trans_date,FORMAT(t1.tmall_warehouse_fee,2) as tmall_warehouse_fee ,FORMAT(t1.insurance_fee,2) as insurance_fee,FORMAT(t1.destory_fee,2) as destory_fee ,FORMAT(t1.merchant_pay_to_custom,2) as merchant_pay_to_custom,
          FORMAT(t1.cainiao_pay_goodsfee_to_merchant,2) as cainiao_pay_goodsfee_to_merchant ,
          FORMAT(t1.cainiao_pay_deposit_to_merchant,2)  as cainiao_pay_deposit_to_merchant,
          FORMAT(t1.popularize_fee,2) as popularize_fee,
          FORMAT(t1.other_payback_fee,2) as other_payback_fee,
          FORMAT(t1.tmall_popularize_fee,2) as tmall_popularize_fee,
          FORMAT(t1.return_cash,2) as return_cash
          from t_other_fee_info as t1  order by t1.trans_date desc
          """
        data.execute(stt)
        other_fee_detail = data.fetchall()
    if request.session.get("lge") == "en":
        # stt='''
        # select t1.fee_time,
        #  FORMAT(t1.out_stock/t2.tax,2) as out_stock ,FORMAT(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,FORMAT(t1.cainiao_service/t2.tax,2) as cainiao_service,
        # FORMAT(t1.alipay/t2.tax,2) as alipay,FORMAT(t1.tmall/t2.tax,2) as tmall,FORMAT(t1.juhuasuan/t2.tax,2) as juhuasuan ,
        #  FORMAT(t1.refund/t2.tax,2) as refund
        # from t_fee_detail_monthly_info as t1
        # left join tax_rate as t2 on t1.fee_time=t2.time order by t1.fee_time desc
        # '''

        union_rows = []
        stt = """
        SELECT
        FORMAT(SUM(so.actual_paid)/t3.tax,2) as actual_paid ,
        FORMAT(SUM(so.refund)/t3.tax,2) as refund,
        SUBSTR(t2.in_out_time FROM 1 FOR 7)  as time
        FROM
        load_tmallso_info so
        LEFT JOIN load_transaction_info as t2
        on so.order_id=t2.outter_order_id
        left join tax_rate as t3 on SUBSTR(t2.in_out_time FROM 1 FOR 7)=t3.time
        GROUP BY  SUBSTR(t2.in_out_time FROM 1 FOR 7)
        order BY SUBSTR(t2.in_out_time FROM 1 FOR 7) desc
          """
        data.execute(stt)
        fee_detail_monthly = data.fetchall()
        stt1 = """
           SELECT
           FORMAT(SUM(fee.logisitic_tax)/t3.tax,2) as logisitic_tax,
           FORMAT(SUM(fee.logisitic_service)/t3.tax,2) as logisitic_service,
           FORMAT(SUM(fee.alipay_service)/t3.tax,2) as alipay_service,
           FORMAT(SUM(fee.tmall)/t3.tax,2) as tmall,
           FORMAT(SUM(fee.juhuasuan)/t3.tax,2) as juhuasuan,
           SUBSTR(t2.in_out_time FROM 1 FOR 7)
           FROM
           t_fee_info fee
           LEFT JOIN load_transaction_info as t2
           on fee.order_id=t2.outter_order_id
           left join tax_rate as t3 on SUBSTR(t2.in_out_time FROM 1 FOR 7)=t3.time
           GROUP BY SUBSTR(t2.in_out_time FROM 1 FOR 7)
           ORDER BY SUBSTR(t2.in_out_time FROM 1 FOR 7) DESC
          """
        data.execute(stt1)
        fee_detail_monthly1 = data.fetchall()
        i = 0
        for fee in fee_detail_monthly:
            send_date = {}
            send_date["time"] = fee["time"]
            send_date["actual_paid"] = fee["actual_paid"]
            send_date["refund"] = fee["refund"]
            # send_date["logisitic_tax"]=fee_detail_monthly1[i]["logisitic_tax"]
            # send_date["logisitic_service"]=fee_detail_monthly1[i]["logisitic_service"]
            # send_date["tmall"]=fee_detail_monthly1[i]["tmall"]
            # send_date["juhuasuan"]=fee_detail_monthly1[i]["juhuasuan"]
            # send_date["alipay_service"]=fee_detail_monthly1[i]["alipay_service"]
            union_rows.append(send_date)
            i += 1

    else:

        union_rows = []
        stt = """
        SELECT
        FORMAT(SUM(so.actual_paid),2) as actual_paid ,
        FORMAT(SUM(so.refund),2) as refund,
        SUBSTR(t2.in_out_time FROM 1 FOR 7)  as time
        FROM
        load_tmallso_info so
        LEFT JOIN load_transaction_info as t2
        on so.order_id=t2.outter_order_id
        GROUP BY  SUBSTR(t2.in_out_time FROM 1 FOR 7)
        order BY SUBSTR(t2.in_out_time FROM 1 FOR 7) desc
          """
        data.execute(stt)
        fee_detail_monthly = data.fetchall()
        stt1 = """
           SELECT
           FORMAT(SUM(fee.logisitic_tax),2) as logisitic_tax,
           FORMAT(SUM(fee.logisitic_service),2) as ls,
           FORMAT(SUM(fee.alipay_service),2) as alipay_service,
           FORMAT(SUM(fee.tmall),2) as tmall,
           FORMAT(SUM(fee.juhuasuan),2) as juhuasuan,
           SUBSTR(t2.in_out_time FROM 1 FOR 7)
           FROM
           t_fee_info fee
           LEFT JOIN load_transaction_info as t2
           on fee.order_id=t2.outter_order_id
           GROUP BY SUBSTR(t2.in_out_time FROM 1 FOR 7)
           ORDER BY SUBSTR(t2.in_out_time FROM 1 FOR 7) DESC
          """
        data.execute(stt1)
        fee_detail_monthly1 = data.fetchall()
        i = 0
        for fee in fee_detail_monthly:
            send_date = {}
            send_date["date_time"] = fee["time"]
            send_date["actual_paid"] = fee["actual_paid"]
            send_date["refund"] = fee["refund"]
            # send_date["logisitic_tax"]=fee_detail_monthly1[i]["logisitic_tax"]
            # send_date["ls"]=fee_detail_monthly1[i]["ls"]
            # send_date["tmall"]=fee_detail_monthly1[i]["tmall"]
            # send_date["juhuasuan"]=fee_detail_monthly1[i]["juhuasuan"]
            # send_date["alipay_service"]=fee_detail_monthly1[i]["alipay_service"]
            union_rows.append(send_date)
            print(union_rows)
            i += 1

        # data.execute(stt)
        # fee_detail_monthly =data.fetchall()

    content = {
        "dictMergedRow": dictMergedRow,
        "fee_order_rows": fee_order_rows,
        "fee_payment": fee_payment,
        "other_fee_detail": other_fee_detail,
        "fee_detail_monthly": union_rows,
    }
    if request.session.get("lge") == "en":
        return render(request, "fee_vis1.html", content)
    else:
        return render(request, "fee_vis.html", content)


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
        group by period,goods_id,goods_name
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
        group by period,goods_id,goods_name
        ORDER BY period
        desc
    """
    data.execute(strr)
    inv_count = data.fetchall()
    content = {"inv_count": inv_count}
    if request.session.get("lge") == "en":
        print('en')
        return render(request, "inv_vis1.html", content)
    else:
        print('ch')
        return render(request, "inv_vis.html", content)


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
        #return render(request, "basics_vis.html", content)


def jump_to_load(request):
    try:
        service.loaddata(setting.BASE_FILE_PATH.get("upload_path"))
        return HttpResponse("success")
    except Exception as identifier:
        return HttpResponse("false")

@csrf_exempt
def get_bom_data(request):
    db = MySQLdb.connect(
    setting.DATABASES.get("default").get("HOST"),
    setting.DATABASES.get("default").get("USER"),
    setting.DATABASES.get("default").get("PASSWORD"),
    setting.DATABASES.get("default").get("NAME"),
    setting.DATABASES.get("default").get("PORT"),
    charset="utf8",
    )
    data = db.cursor(MySQLdb.cursors.DictCursor)
    strr_bom ="""
        select * from bom;
    """
    data.execute(strr_bom)
    
    bom_list = list(data.fetchall())
    bom_list_res = []
    
    for bom_index in bom_list:
        bom_row = {}
        
        strr_temp = ""
        i = 0
        for item in bom_index.keys():
            print(item)
            i = i+1
            if (i>=4 and bom_index[item]!=None and int(bom_index[item])>0):
                strr_temp = strr_temp+item+","
        
        bom_index['goods']=strr_temp

        bom_row['goods'] = bom_index['goods']
        bom_row['Num'] = bom_index['Num']
        bom_row['product_name'] = bom_index["product_name"]
        bom_row['price']=str(bom_index['price'])
        bom_list_res.append(bom_row)
    return HttpResponse(json.dumps(bom_list_res),content_type="application/json",)

@csrf_exempt
def update_bom_edit(request):
    if request.method == 'POST':
        Num = request.POST.__getitem__('Num')
        product_name = request.POST.__getitem__('product_name')
        price = request.POST.__getitem__('price')
        goods = request.POST.getlist('goods[]')
        print(request.POST)
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
        init_strr = "UPDATE bom SET X708390000326 = '0' , XY521067771349 = '0' , XY521068155265 = '0' , XY521073901132 = '0' , XY521074093868 = '0' , XY521074249153 = '0' , XY521074725008 = '0' , XY521077050523 = '0' , XY521077162825 = '0' , XY521077912497 = '0' , XY521078064529 = '0' , XY521078232623 = '0' , XY521078390258 = '0' WHERE Num = %s" %(Num)
        print(init_strr)
        data.execute(init_strr)
        for good in goods:
            update_strr = "update bom set %s = '1' where Num = %s" %(good,Num)   
            print(update_strr)
            
            data.execute(update_strr)
            
        db.commit()
        return HttpResponse("success")
    else:
        return HttpResponse("false")

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
    style_yy = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap off,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour white;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;  
        """
    )

    style_ss = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap off,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour orange
        """
    )
    style_heading = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap on,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour yellow;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    style_hh = xlwt.easyxf(
        """
        font:
        name SimSun,
        colour_index black,
        bold on,
        height 0x00C8;
        align:
        wrap on,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour white;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    style_body = xlwt.easyxf(
        """
        font:
        name Arial,
        bold off,
        height 0XA0;
        align:
        wrap on,
        vert center,
        horiz left;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    # 创建
    ws = xlwt.Workbook(encoding="utf-8")
    w = ws.add_sheet("货品分析报表")
    excel_row = 1
    first_row = w.row(0)
    tall_style = xlwt.easyxf("font:height 720;")
    first_row.set_style(tall_style)
    # 中英文切换第一行
    if request.session.get("lge") != "en":
        w.write_merge(
            0,
            0,
            0,
            14,
            "货品分析报表\n报表参数：货品分析/"
            + years
            + "\n生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write(excel_row, 0, "统计维度", style_heading)
        w.write(excel_row, 1, "货品", style_heading)
        w.write(excel_row, 2, "统计项目", style_heading)
    else:
        w.write_merge(
            0,
            0,
            0,
            14,
            "货品分析报表\n报表参数：货品分析/"
            + years
            + "\n生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write(excel_row, 0, "Statistical dimension", style_heading)
        w.write(excel_row, 1, "Goods", style_heading)
        w.write(excel_row, 2, "Statistical Item", style_heading)
    w.write(excel_row, 3, years + "01", style_ss)
    w.write(excel_row, 4, years + "02", style_ss)
    w.write(excel_row, 5, years + "03", style_ss)
    w.write(excel_row, 6, years + "04", style_ss)
    w.write(excel_row, 7, years + "05", style_ss)
    w.write(excel_row, 8, years + "06", style_ss)
    w.write(excel_row, 9, years + "07", style_ss)
    w.write(excel_row, 10, years + "08", style_ss)
    w.write(excel_row, 11, years + "09", style_ss)
    w.write(excel_row, 12, years + "10", style_ss)
    w.write(excel_row, 13, years + "11", style_ss)
    w.write(excel_row, 14, years + "12", style_ss)
    # 表头结束
    # 中英文切换查询数据
    if request.session.get("lge") != "en":
        all_goods = """
        select * from ((select  goods_id,goods_name,products,gpc,sku,'订单销售数量（拍下）' as lei,'1' as orde,
        sum(case when period='%(sel)s-01' then sale_num end) as '01',
        sum(case when period='%(sel)s-02' then sale_num end) as '02',
        sum(case when period='%(sel)s-03' then sale_num end) as '03',
        sum(case when period='%(sel)s-04' then sale_num end) as '04',
        sum(case when period='%(sel)s-05' then sale_num end) as '05',
        sum(case when period='%(sel)s-06' then sale_num end) as '06',
        sum(case when period='%(sel)s-07' then sale_num end) as '07',
        sum(case when period='%(sel)s-08' then sale_num end) as '08',
        sum(case when period='%(sel)s-09' then sale_num end) as '09',
        sum(case when period='%(sel)s-10' then sale_num end) as '10',
        sum(case when period='%(sel)s-11' then sale_num end) as '11',
        sum(case when period='%(sel)s-12' then sale_num end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m1 group by m1.goods_id ORDER BY m1.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'订单出库数量（仓库）' as lei,'2' as orde,
        sum(case when period='%(sel)s-01' then sale_out_number end) as '01',
        sum(case when period='%(sel)s-02' then sale_out_number end) as '02',
        sum(case when period='%(sel)s-03' then sale_out_number end) as '03',
        sum(case when period='%(sel)s-04' then sale_out_number end) as '04',
        sum(case when period='%(sel)s-05' then sale_out_number end) as '05',
        sum(case when period='%(sel)s-06' then sale_out_number end) as '06',
        sum(case when period='%(sel)s-07' then sale_out_number end) as '07',
        sum(case when period='%(sel)s-08' then sale_out_number end) as '08',
        sum(case when period='%(sel)s-09' then sale_out_number end) as '09',
        sum(case when period='%(sel)s-10' then sale_out_number end) as '10',
        sum(case when period='%(sel)s-11' then sale_out_number end) as '11',
        sum(case when period='%(sel)s-12' then sale_out_number end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m2 group by m2.goods_id ORDER BY m2.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'交易成功订单销售数量（最终成交）' as lei,'3' as orde,
        sum(case when period='%(sel)s-01' then order_deal_num end) as '01',
        sum(case when period='%(sel)s-02' then order_deal_num end) as '02',
        sum(case when period='%(sel)s-03' then order_deal_num end) as '03',
        sum(case when period='%(sel)s-04' then order_deal_num end) as '04',
        sum(case when period='%(sel)s-05' then order_deal_num end) as '05',
        sum(case when period='%(sel)s-06' then order_deal_num end) as '06',
        sum(case when period='%(sel)s-07' then order_deal_num end) as '07',
        sum(case when period='%(sel)s-08' then order_deal_num end) as '08',
        sum(case when period='%(sel)s-09' then order_deal_num end) as '09',
        sum(case when period='%(sel)s-10' then order_deal_num end) as '10',
        sum(case when period='%(sel)s-11' then order_deal_num end) as '11',
        sum(case when period='%(sel)s-12' then order_deal_num end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m3 group by m3.goods_id ORDER BY m3.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'订单销售金额（拍下）' as lei,'4' as orde,
        sum(case when period='%(sel)s-01' then sale_amount end) as '01',
        sum(case when period='%(sel)s-02' then sale_amount end) as '02',
        sum(case when period='%(sel)s-03' then sale_amount end) as '03',
        sum(case when period='%(sel)s-04' then sale_amount end) as '04',
        sum(case when period='%(sel)s-05' then sale_amount end) as '05',
        sum(case when period='%(sel)s-06' then sale_amount end) as '06',
        sum(case when period='%(sel)s-07' then sale_amount end) as '07',
        sum(case when period='%(sel)s-08' then sale_amount end) as '08',
        sum(case when period='%(sel)s-09' then sale_amount end) as '09',
        sum(case when period='%(sel)s-10' then sale_amount end) as '10',
        sum(case when period='%(sel)s-11' then sale_amount end) as '11',
        sum(case when period='%(sel)s-12' then sale_amount end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m4 group by m4.goods_id ORDER BY m4.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'订单出库金额（仓库）' as lei,'5' as orde,
        sum(case when period='%(sel)s-01' then sale_out_amount end) as '01',
        sum(case when period='%(sel)s-02' then sale_out_amount end) as '02',
        sum(case when period='%(sel)s-03' then sale_out_amount end) as '03',
        sum(case when period='%(sel)s-04' then sale_out_amount end) as '04',
        sum(case when period='%(sel)s-05' then sale_out_amount end) as '05',
        sum(case when period='%(sel)s-06' then sale_out_amount end) as '06',
        sum(case when period='%(sel)s-07' then sale_out_amount end) as '07',
        sum(case when period='%(sel)s-08' then sale_out_amount end) as '08',
        sum(case when period='%(sel)s-09' then sale_out_amount end) as '09',
        sum(case when period='%(sel)s-10' then sale_out_amount end) as '10',
        sum(case when period='%(sel)s-11' then sale_out_amount end) as '11',
        sum(case when period='%(sel)s-12' then sale_out_amount end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m5 group by m5.goods_id ORDER BY m5.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'交易成功订单销售金额（最终成交）' as lei,'6' as orde,
        sum(case when period='%(sel)s-01' then order_deal_amount end) as '01',
        sum(case when period='%(sel)s-02' then order_deal_amount end) as '02',
        sum(case when period='%(sel)s-03' then order_deal_amount end) as '03',
        sum(case when period='%(sel)s-04' then order_deal_amount end) as '04',
        sum(case when period='%(sel)s-05' then order_deal_amount end) as '05',
        sum(case when period='%(sel)s-06' then order_deal_amount end) as '06',
        sum(case when period='%(sel)s-07' then order_deal_amount end) as '07',
        sum(case when period='%(sel)s-08' then order_deal_amount end) as '08',
        sum(case when period='%(sel)s-09' then order_deal_amount end) as '09',
        sum(case when period='%(sel)s-10' then order_deal_amount end) as '10',
        sum(case when period='%(sel)s-11' then order_deal_amount end) as '11',
        sum(case when period='%(sel)s-12' then order_deal_amount end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m6 group by m6.goods_id ORDER BY m6.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间交易出库金额' as lei,'7' as orde,
        sum(case when period='%(sel)s-01' then trans_amount end) as '01',
        sum(case when period='%(sel)s-02' then trans_amount end) as '02',
        sum(case when period='%(sel)s-03' then trans_amount end) as '03',
        sum(case when period='%(sel)s-04' then trans_amount end) as '04',
        sum(case when period='%(sel)s-05' then trans_amount end) as '05',
        sum(case when period='%(sel)s-06' then trans_amount end) as '06',
        sum(case when period='%(sel)s-07' then trans_amount end) as '07',
        sum(case when period='%(sel)s-08' then trans_amount end) as '08',
        sum(case when period='%(sel)s-09' then trans_amount end) as '09',
        sum(case when period='%(sel)s-10' then trans_amount end) as '10',
        sum(case when period='%(sel)s-11' then trans_amount end) as '11',
        sum(case when period='%(sel)s-12' then trans_amount end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m7 group by m7.goods_id ORDER BY m7.goods_id)) t where t.goods_id!='' ORDER BY t.goods_id,t.orde
        """
    else:
        all_goods = """
         select * from ((select  id,goods_id,goods_name,gpc,'SALES QUANTITY  BASED ON ORDERS PLACED' as lei,'1' as orde,
        sum(case when period='%(sel)s-01' then sale_num end) as '01',
        sum(case when period='%(sel)s-02' then sale_num end) as '02',
        sum(case when period='%(sel)s-03' then sale_num end) as '03',
        sum(case when period='%(sel)s-04' then sale_num end) as '04',
        sum(case when period='%(sel)s-05' then sale_num end) as '05',
        sum(case when period='%(sel)s-06' then sale_num end) as '06',
        sum(case when period='%(sel)s-07' then sale_num end) as '07',
        sum(case when period='%(sel)s-08' then sale_num end) as '08',
        sum(case when period='%(sel)s-09' then sale_num end) as '09',
        sum(case when period='%(sel)s-10' then sale_num end) as '10',
        sum(case when period='%(sel)s-11' then sale_num end) as '11',
        sum(case when period='%(sel)s-12' then sale_num end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m1 group by m1.goods_id ORDER BY m1.goods_id) union 
        (select  id,goods_id,goods_name,gpc,'QUANTITY SHIPPED BASED ON ORDERS PLACED' as lei,'2' as orde,
        sum(case when period='%(sel)s-01' then sale_out_number end) as '01',
        sum(case when period='%(sel)s-02' then sale_out_number end) as '02',
        sum(case when period='%(sel)s-03' then sale_out_number end) as '03',
        sum(case when period='%(sel)s-04' then sale_out_number end) as '04',
        sum(case when period='%(sel)s-05' then sale_out_number end) as '05',
        sum(case when period='%(sel)s-06' then sale_out_number end) as '06',
        sum(case when period='%(sel)s-07' then sale_out_number end) as '07',
        sum(case when period='%(sel)s-08' then sale_out_number end) as '08',
        sum(case when period='%(sel)s-09' then sale_out_number end) as '09',
        sum(case when period='%(sel)s-10' then sale_out_number end) as '10',
        sum(case when period='%(sel)s-11' then sale_out_number end) as '11',
        sum(case when period='%(sel)s-12' then sale_out_number end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m2 group by m2.goods_id ORDER BY m2.goods_id) union 
        (select id,goods_id,goods_name,gpc,'SUCCESSFUL TRADE QUANTITY  BASED ON ORDERS PLACED' as lei,'3' as orde,
        sum(case when period='%(sel)s-01' then order_deal_num end) as '01',
        sum(case when period='%(sel)s-02' then order_deal_num end) as '02',
        sum(case when period='%(sel)s-03' then order_deal_num end) as '03',
        sum(case when period='%(sel)s-04' then order_deal_num end) as '04',
        sum(case when period='%(sel)s-05' then order_deal_num end) as '05',
        sum(case when period='%(sel)s-06' then order_deal_num end) as '06',
        sum(case when period='%(sel)s-07' then order_deal_num end) as '07',
        sum(case when period='%(sel)s-08' then order_deal_num end) as '08',
        sum(case when period='%(sel)s-09' then order_deal_num end) as '09',
        sum(case when period='%(sel)s-10' then order_deal_num end) as '10',
        sum(case when period='%(sel)s-11' then order_deal_num end) as '11',
        sum(case when period='%(sel)s-12' then order_deal_num end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m3 group by m3.goods_id ORDER BY m3.goods_id) union 
        (select  id,goods_id,goods_name,gpc,'SALES REVENUE BASED ON ORDERS PLACED' as lei,'4' as orde,
        sum(case when period='%(sel)s-01' then sale_amount end) as '01',
        sum(case when period='%(sel)s-02' then sale_amount end) as '02',
        sum(case when period='%(sel)s-03' then sale_amount end) as '03',
        sum(case when period='%(sel)s-04' then sale_amount end) as '04',
        sum(case when period='%(sel)s-05' then sale_amount end) as '05',
        sum(case when period='%(sel)s-06' then sale_amount end) as '06',
        sum(case when period='%(sel)s-07' then sale_amount end) as '07',
        sum(case when period='%(sel)s-08' then sale_amount end) as '08',
        sum(case when period='%(sel)s-09' then sale_amount end) as '09',
        sum(case when period='%(sel)s-10' then sale_amount end) as '10',
        sum(case when period='%(sel)s-11' then sale_amount end) as '11',
        sum(case when period='%(sel)s-12' then sale_amount end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m4 group by m4.goods_id ORDER BY m4.goods_id) union 
        (select  id,goods_id,goods_name,gpc,'REVENUE SHIPPED BASED ON ORDERS PLACED' as lei,'5' as orde,
        sum(case when period='%(sel)s-01' then sale_out_amount end) as '01',
        sum(case when period='%(sel)s-02' then sale_out_amount end) as '02',
        sum(case when period='%(sel)s-03' then sale_out_amount end) as '03',
        sum(case when period='%(sel)s-04' then sale_out_amount end) as '04',
        sum(case when period='%(sel)s-05' then sale_out_amount end) as '05',
        sum(case when period='%(sel)s-06' then sale_out_amount end) as '06',
        sum(case when period='%(sel)s-07' then sale_out_amount end) as '07',
        sum(case when period='%(sel)s-08' then sale_out_amount end) as '08',
        sum(case when period='%(sel)s-09' then sale_out_amount end) as '09',
        sum(case when period='%(sel)s-10' then sale_out_amount end) as '10',
        sum(case when period='%(sel)s-11' then sale_out_amount end) as '11',
        sum(case when period='%(sel)s-12' then sale_out_amount end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m5 group by m5.goods_id ORDER BY m5.goods_id) union 
        (select id,goods_id,goods_name,gpc,'SUCCESSFUL TRADE  REVENUE BASED ON ORDERS PLACED' as lei,'6' as orde,
        sum(case when period='%(sel)s-01' then order_deal_amount end) as '01',
        sum(case when period='%(sel)s-02' then order_deal_amount end) as '02',
        sum(case when period='%(sel)s-03' then order_deal_amount end) as '03',
        sum(case when period='%(sel)s-04' then order_deal_amount end) as '04',
        sum(case when period='%(sel)s-05' then order_deal_amount end) as '05',
        sum(case when period='%(sel)s-06' then order_deal_amount end) as '06',
        sum(case when period='%(sel)s-07' then order_deal_amount end) as '07',
        sum(case when period='%(sel)s-08' then order_deal_amount end) as '08',
        sum(case when period='%(sel)s-09' then order_deal_amount end) as '09',
        sum(case when period='%(sel)s-10' then order_deal_amount end) as '10',
        sum(case when period='%(sel)s-11' then order_deal_amount end) as '11',
        sum(case when period='%(sel)s-12' then order_deal_amount end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m6 group by m6.goods_id ORDER BY m6.goods_id) union 
        (select id,goods_id,goods_name,gpc,'SALES REVENUE BASED ON ORDERS SHIPPED' as lei,'7' as orde,
        sum(case when period='%(sel)s-01' then trans_amount end) as '01',
        sum(case when period='%(sel)s-02' then trans_amount end) as '02',
        sum(case when period='%(sel)s-03' then trans_amount end) as '03',
        sum(case when period='%(sel)s-04' then trans_amount end) as '04',
        sum(case when period='%(sel)s-05' then trans_amount end) as '05',
        sum(case when period='%(sel)s-06' then trans_amount end) as '06',
        sum(case when period='%(sel)s-07' then trans_amount end) as '07',
        sum(case when period='%(sel)s-08' then trans_amount end) as '08',
        sum(case when period='%(sel)s-09' then trans_amount end) as '09',
        sum(case when period='%(sel)s-10' then trans_amount end) as '10',
        sum(case when period='%(sel)s-11' then trans_amount end) as '11',
        sum(case when period='%(sel)s-12' then trans_amount end) as '12' 
        from (select t1.period,t2.products as goods_name,t2.gpc,t2.sku as goods_id,t1.goods_id as id,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        truncate(sum(t1.sale_amount/t3.tax),2) as sale_amount,
        truncate(sum(t1.sale_out_amount/t3.tax),2) as sale_out_amount,
        truncate(sum(t1.order_deal_amount/t3.tax),2) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        truncate(sum(trans_amount/t3.tax),2) as trans_amount 
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m7 group by m7.goods_id ORDER BY m7.goods_id)) t where t.goods_id!='' ORDER BY t.id,t.orde
        """
    all_goods = all_goods % dict(sel=years)
    data.execute(all_goods)
    all_goods_list = data.fetchall()
    excel_row += 1
    for obj in all_goods_list:
        goods_name = obj["goods_id"] + "\n(" + obj["goods_name"] + ")"
        lei = obj["lei"]
        M1 = obj["01"]
        M2 = obj["02"]
        M3 = obj["03"]
        M4 = obj["04"]
        M5 = obj["05"]
        M6 = obj["06"]
        M7 = obj["07"]
        M8 = obj["08"]
        M9 = obj["09"]
        M10 = obj["10"]
        M11 = obj["11"]
        M12 = obj["12"]
        if (
            obj["orde"] == "4"
            or obj["orde"] == "5"
            or obj["orde"] == "6"
            or obj["orde"] == "7"
        ):
            if request.session.get("lge") != "en":
                if M1 != None:
                    M1 = "￥" + str(M1)
                if M2 != None:
                    M2 = "￥" + str(M2)
                if M3 != None:
                    M3 = "￥" + str(M3)
                if M4 != None:
                    M4 = "￥" + str(M4)
                if M5 != None:
                    M5 = "￥" + str(M5)
                if M6 != None:
                    M6 = "￥" + str(M6)
                if M7 != None:
                    M7 = "￥" + str(M7)
                if M8 != None:
                    M8 = "￥" + str(M8)
                if M9 != None:
                    M9 = "￥" + str(M9)
                if M10 != None:
                    M10 = "￥" + str(M10)
                if M11 != None:
                    M11 = "￥" + str(M11)
                if M12 != None:
                    M12 = "￥" + str(M12)
            else:
                if M1 != None:
                    M1 = "$" + str(M1)
                if M2 != None:
                    M2 = "$" + str(M2)
                if M3 != None:
                    M3 = "$" + str(M3)
                if M4 != None:
                    M4 = "$" + str(M4)
                if M5 != None:
                    M5 = "$" + str(M5)
                if M6 != None:
                    M6 = "$" + str(M6)
                if M7 != None:
                    M7 = "$" + str(M7)
                if M8 != None:
                    M8 = "$" + str(M8)
                if M9 != None:
                    M9 = "$" + str(M9)
                if M10 != None:
                    M10 = "$" + str(M10)
                if M11 != None:
                    M11 = "$" + str(M11)
                if M12 != None:
                    M12 = "$" + str(M12)
        if obj["orde"] == "7":
            w.write_merge(excel_row - 6, excel_row, 1, 1, goods_name, style_heading)
        w.write(excel_row, 2, lei, style_heading)
        w.write(excel_row, 3, M1, style_yy)
        w.write(excel_row, 4, M2, style_yy)
        w.write(excel_row, 5, M3, style_yy)
        w.write(excel_row, 6, M4, style_yy)
        w.write(excel_row, 7, M5, style_yy)
        w.write(excel_row, 8, M6, style_yy)
        w.write(excel_row, 9, M7, style_yy)
        w.write(excel_row, 10, M8, style_yy)
        w.write(excel_row, 11, M9, style_yy)
        w.write(excel_row, 12, M10, style_yy)
        w.write(excel_row, 13, M11, style_yy)
        w.write(excel_row, 14, M12, style_yy)
        w.col(0).width = 100 * 50
        w.col(1).width = 120 * 50
        w.col(2).width = 220 * 50
        w.col(3).width = 60 * 50
        w.col(4).width = 60 * 50
        w.col(5).width = 60 * 50
        w.col(6).width = 60 * 50
        w.col(7).width = 60 * 50
        w.col(8).width = 60 * 50
        w.col(9).width = 60 * 50
        w.col(10).width = 60 * 50
        w.col(11).width = 60 * 50
        w.col(12).width = 60 * 50
        w.col(13).width = 60 * 50
        w.col(14).width = 60 * 50
        excel_row += 1
    endone = excel_row - 1
    # 中英文切换第一列
    if request.session.get("lge") != "en":
        w.write_merge(2, endone, 0, 0, "货品金额分析", style_heading)
    else:
        w.write_merge(2, endone, 0, 0, "Sum Analysis", style_heading)
    goods_kc = """
        select * from ((select  goods_id,goods_name,products,gpc,sku,'期初数量' as lei,'QUANTITY BEGINNING' as le,'1' as orde,
        sum(case when period='%(sel)s-01' then opening_inventory end) as '01',
        sum(case when period='%(sel)s-02' then opening_inventory end) as '02',
        sum(case when period='%(sel)s-03' then opening_inventory end) as '03',
        sum(case when period='%(sel)s-04' then opening_inventory end) as '04',
        sum(case when period='%(sel)s-05' then opening_inventory end) as '05',
        sum(case when period='%(sel)s-06' then opening_inventory end) as '06',
        sum(case when period='%(sel)s-07' then opening_inventory end) as '07',
        sum(case when period='%(sel)s-08' then opening_inventory end) as '08',
        sum(case when period='%(sel)s-09' then opening_inventory end) as '09',
        sum(case when period='%(sel)s-10' then opening_inventory end) as '10',
        sum(case when period='%(sel)s-11' then opening_inventory end) as '11',
        sum(case when period='%(sel)s-12' then opening_inventory end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m1 group by m1.goods_id ORDER BY m1.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间采购入库' as lei,'QUANTITY RECEIVED' as le,'2' as orde,
        sum(case when period='%(sel)s-01' then purchase_in end) as '01',
        sum(case when period='%(sel)s-02' then purchase_in end) as '02',
        sum(case when period='%(sel)s-03' then purchase_in end) as '03',
        sum(case when period='%(sel)s-04' then purchase_in end) as '04',
        sum(case when period='%(sel)s-05' then purchase_in end) as '05',
        sum(case when period='%(sel)s-06' then purchase_in end) as '06',
        sum(case when period='%(sel)s-07' then purchase_in end) as '07',
        sum(case when period='%(sel)s-08' then purchase_in end) as '08',
        sum(case when period='%(sel)s-09' then purchase_in end) as '09',
        sum(case when period='%(sel)s-10' then purchase_in end) as '10',
        sum(case when period='%(sel)s-11' then purchase_in end) as '11',
        sum(case when period='%(sel)s-12' then purchase_in end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m2 group by m2.goods_id ORDER BY m2.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间其他入库' as lei,'OTHER QUANTITY RECEIVED' as le,'3' as orde,
        sum(case when period='%(sel)s-01' then other_in end) as '01',
        sum(case when period='%(sel)s-02' then other_in end) as '02',
        sum(case when period='%(sel)s-03' then other_in end) as '03',
        sum(case when period='%(sel)s-04' then other_in end) as '04',
        sum(case when period='%(sel)s-05' then other_in end) as '05',
        sum(case when period='%(sel)s-06' then other_in end) as '06',
        sum(case when period='%(sel)s-07' then other_in end) as '07',
        sum(case when period='%(sel)s-08' then other_in end) as '08',
        sum(case when period='%(sel)s-09' then other_in end) as '09',
        sum(case when period='%(sel)s-10' then other_in end) as '10',
        sum(case when period='%(sel)s-11' then other_in end) as '11',
        sum(case when period='%(sel)s-12' then other_in end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m3 group by m3.goods_id ORDER BY m3.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间交易出库' as lei,'QUANTITY SHIPPED' as le,'4' as orde,
        sum(case when period='%(sel)s-01' then trade_out end) as '01',
        sum(case when period='%(sel)s-02' then trade_out end) as '02',
        sum(case when period='%(sel)s-03' then trade_out end) as '03',
        sum(case when period='%(sel)s-04' then trade_out end) as '04',
        sum(case when period='%(sel)s-05' then trade_out end) as '05',
        sum(case when period='%(sel)s-06' then trade_out end) as '06',
        sum(case when period='%(sel)s-07' then trade_out end) as '07',
        sum(case when period='%(sel)s-08' then trade_out end) as '08',
        sum(case when period='%(sel)s-09' then trade_out end) as '09',
        sum(case when period='%(sel)s-10' then trade_out end) as '10',
        sum(case when period='%(sel)s-11' then trade_out end) as '11',
        sum(case when period='%(sel)s-12' then trade_out end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m4 group by m4.goods_id ORDER BY m4.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间其他出库' as lei,'OTHER QUANTITY SHIPPED' as le,'5' as orde,
        sum(case when period='%(sel)s-01' then other_out end) as '01',
        sum(case when period='%(sel)s-02' then other_out end) as '02',
        sum(case when period='%(sel)s-03' then other_out end) as '03',
        sum(case when period='%(sel)s-04' then other_out end) as '04',
        sum(case when period='%(sel)s-05' then other_out end) as '05',
        sum(case when period='%(sel)s-06' then other_out end) as '06',
        sum(case when period='%(sel)s-07' then other_out end) as '07',
        sum(case when period='%(sel)s-08' then other_out end) as '08',
        sum(case when period='%(sel)s-09' then other_out end) as '09',
        sum(case when period='%(sel)s-10' then other_out end) as '10',
        sum(case when period='%(sel)s-11' then other_out end) as '11',
        sum(case when period='%(sel)s-12' then other_out end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m5 group by m5.goods_id ORDER BY m5.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期末数量' as lei,'QUANTITY ENDING' as le,'6' as orde,
        sum(case when period='%(sel)s-01' then ending_inventory end) as '01',
        sum(case when period='%(sel)s-02' then ending_inventory end) as '02',
        sum(case when period='%(sel)s-03' then ending_inventory end) as '03',
        sum(case when period='%(sel)s-04' then ending_inventory end) as '04',
        sum(case when period='%(sel)s-05' then ending_inventory end) as '05',
        sum(case when period='%(sel)s-06' then ending_inventory end) as '06',
        sum(case when period='%(sel)s-07' then ending_inventory end) as '07',
        sum(case when period='%(sel)s-08' then ending_inventory end) as '08',
        sum(case when period='%(sel)s-09' then ending_inventory end) as '09',
        sum(case when period='%(sel)s-10' then ending_inventory end) as '10',
        sum(case when period='%(sel)s-11' then ending_inventory end) as '11',
        sum(case when period='%(sel)s-12' then ending_inventory end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m6 group by m6.goods_id ORDER BY m6.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期末-期初' as lei,'ENDING - BEGINNING' as le,'7' as orde,
        sum(case when period='%(sel)s-01' then diff_inventory end) as '01',
        sum(case when period='%(sel)s-02' then diff_inventory end) as '02',
        sum(case when period='%(sel)s-03' then diff_inventory end) as '03',
        sum(case when period='%(sel)s-04' then diff_inventory end) as '04',
        sum(case when period='%(sel)s-05' then diff_inventory end) as '05',
        sum(case when period='%(sel)s-06' then diff_inventory end) as '06',
        sum(case when period='%(sel)s-07' then diff_inventory end) as '07',
        sum(case when period='%(sel)s-08' then diff_inventory end) as '08',
        sum(case when period='%(sel)s-09' then diff_inventory end) as '09',
        sum(case when period='%(sel)s-10' then diff_inventory end) as '10',
        sum(case when period='%(sel)s-11' then diff_inventory end) as '11',
        sum(case when period='%(sel)s-12' then diff_inventory end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m7 group by m7.goods_id ORDER BY m7.goods_id) union 
        (select  goods_id,goods_name,products,gpc,sku,'期间出入库流水总数量' as lei,'QUANTITY SOLD' as le,'8' as orde,
        sum(case when period='%(sel)s-01' then in_out_num end) as '01',
        sum(case when period='%(sel)s-02' then in_out_num end) as '02',
        sum(case when period='%(sel)s-03' then in_out_num end) as '03',
        sum(case when period='%(sel)s-04' then in_out_num end) as '04',
        sum(case when period='%(sel)s-05' then in_out_num end) as '05',
        sum(case when period='%(sel)s-06' then in_out_num end) as '06',
        sum(case when period='%(sel)s-07' then in_out_num end) as '07',
        sum(case when period='%(sel)s-08' then in_out_num end) as '08',
        sum(case when period='%(sel)s-09' then in_out_num end) as '09',
        sum(case when period='%(sel)s-10' then in_out_num end) as '10',
        sum(case when period='%(sel)s-11' then in_out_num end) as '11',
        sum(case when period='%(sel)s-12' then in_out_num end) as '12' 
        from (select t1.period,t1.goods_id,t1.goods_name,t2.products,t2.gpc,t2.sku,
        sum(t1.sale_num) as sale_num,
        sum(t1.sale_out_number*-1) as sale_out_number,
        sum(t1.order_deal_num) as order_deal_num,
        sum(t1.sale_amount) as sale_amount,
        sum(t1.sale_out_amount) as sale_out_amount,
        sum(t1.order_deal_amount) as order_deal_amount,
        sum(t1.opening_inventory) as opening_inventory,
        sum(t1.purchase_in) as purchase_in,
        sum(t1.other_in) as other_in,
        sum(t1.trade_out) as trade_out,
        sum(t1.other_out) as other_out,
        sum(t1.ending_inventory) as ending_inventory,
        sum(t1.diff_inventory) as diff_inventory,
        sum(t1.in_out_num) as in_out_num,
        sum(trans_amount) as trans_amount
        from t_goods_num_info as t1
        left join goods as t2
        on t1.goods_id=t2.goods_id
        left join tax_rate as t3 on
        t1.period=t3.time
        WHERE t1.goods_id is NOT null and LENGTH(t1.goods_id)>0
        group by period,goods_id,goods_name
        ORDER BY period
        desc) m8 group by m8.goods_id ORDER BY m8.goods_id)
        ) t where t.goods_id!='' ORDER BY t.goods_id,t.orde
    """
    goods_kc = goods_kc % dict(sel=years)
    data.execute(goods_kc)
    goods_kc_list = data.fetchall()
    for obj in goods_kc_list:
        if request.session.get("lge") != "en":
            goods_name = obj["goods_id"] + "\n(" + obj["goods_name"] + ")"
            lei = obj["lei"]
        else:
            goods_name = obj["sku"] + "\n(" + obj["products"] + ")"
            lei = obj["le"]
        M1 = obj["01"]
        M2 = obj["02"]
        M3 = obj["03"]
        M4 = obj["04"]
        M5 = obj["05"]
        M6 = obj["06"]
        M7 = obj["07"]
        M8 = obj["08"]
        M9 = obj["09"]
        M10 = obj["10"]
        M11 = obj["11"]
        M12 = obj["12"]
        if obj["orde"] == "8":
            w.write_merge(excel_row - 7, excel_row, 1, 1, goods_name, style_heading)
        w.write(excel_row, 2, lei, style_heading)
        w.write(excel_row, 3, M1, style_yy)
        w.write(excel_row, 4, M2, style_yy)
        w.write(excel_row, 5, M3, style_yy)
        w.write(excel_row, 6, M4, style_yy)
        w.write(excel_row, 7, M5, style_yy)
        w.write(excel_row, 8, M6, style_yy)
        w.write(excel_row, 9, M7, style_yy)
        w.write(excel_row, 10, M8, style_yy)
        w.write(excel_row, 11, M9, style_yy)
        w.write(excel_row, 12, M10, style_yy)
        w.write(excel_row, 13, M11, style_yy)
        w.write(excel_row, 14, M12, style_yy)
        excel_row += 1
    if request.session.get("lge") != "en":
        w.write_merge(endone + 1, excel_row - 1, 0, 0, "货品库存分析", style_heading)
    else:
        w.write_merge(
            endone + 1, excel_row - 1, 0, 0, "Inventory Analysis", style_heading
        )
    # 检测文件是够存在
    # 方框中代码是保存本地文件使用，如不需要请删除该代码
    ###########################
    exist_file = os.path.exists("goods.xls")
    if exist_file:
        os.remove(r"goods.xls")
    ws.save("goods.xls")
    ############################
    sio = io.StringIO()
    ws.save(sio)
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
    style_yy = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap off,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour white;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;  
        """
    )

    style_ss = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap off,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour orange
        """
    )
    style_heading = xlwt.easyxf(
        """
        font:
        name Arial,
        colour_index black,
        bold on,
        height 0xA0;
        align:
        wrap off,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour yellow;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    style_hh = xlwt.easyxf(
        """
        font:
        name SimSun,
        colour_index black,
        bold on,
        height 720;
        align:
        wrap on,
        vert center,
        horiz center;
        pattern:
        pattern solid,
        fore-colour white;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    style_body = xlwt.easyxf(
        """
        font:
        name Arial,
        bold off,
        height 0XA0;
        align:
        wrap on,
        vert center,
        horiz left;
        borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN;
        """
    )
    # 创建
    ws = xlwt.Workbook(encoding="utf-8")
    w = ws.add_sheet("金额分析报表")
    excel_row = 1
    # 中英文切换第一行
    if request.session.get("lge") != "en":
        w.write_merge(
            0,
            0,
            0,
            13,
            "金额分析报表\n报表参数：金额分析/"
            + years
            + "\n生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write(excel_row, 0, "统计维度", style_heading)
        w.write(excel_row, 1, "统计项目", style_heading)
    else:
        w.write_merge(
            0,
            0,
            0,
            13,
            "金额分析报表\n报表参数：金额分析/"
            + years
            + "\n生成日期："
            + time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())),
            style_hh,
        )
        w.write(excel_row, 0, "Statistical dimension", style_heading)
        w.write(excel_row, 1, "Statistical Item", style_heading)
    w.write(excel_row, 2, years + "01", style_ss)
    w.write(excel_row, 3, years + "02", style_ss)
    w.write(excel_row, 4, years + "03", style_ss)
    w.write(excel_row, 5, years + "04", style_ss)
    w.write(excel_row, 6, years + "05", style_ss)
    w.write(excel_row, 7, years + "06", style_ss)
    w.write(excel_row, 8, years + "07", style_ss)
    w.write(excel_row, 9, years + "08", style_ss)
    w.write(excel_row, 10, years + "09", style_ss)
    w.write(excel_row, 11, years + "10", style_ss)
    w.write(excel_row, 12, years + "11", style_ss)
    w.write(excel_row, 13, years + "12", style_ss)
    # 表头结束
    # 订单提取时间
    if request.session.get("lge") != "en":
        order_tq = """
            (select 1 as orde,'支付宝订单提取金额' as lei,'Settlement Amount (Alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Settlement end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Settlement end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Settlement end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Settlement end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Settlement end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Settlement end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Settlement end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Settlement end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Settlement end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Settlement end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Settlement end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Settlement end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 2 as orde,'支付宝订单收到金额' as lei,'Payment amount (alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Amount end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Amount end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Amount end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Amount end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Amount end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Amount end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Amount end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Amount end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Amount end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Amount end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Amount end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Amount end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 3 as orde,'支付宝订单费用扣除' as lei,'Fees deducted (alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Settlement_Fee end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Settlement_Fee end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Settlement_Fee end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Settlement_Fee end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Settlement_Fee end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Settlement_Fee end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Settlement_Fee end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Settlement_Fee end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Settlement_Fee end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Settlement_Fee end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Settlement_Fee end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Settlement_Fee end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            ( select 4 as orde,'菜鸟-税费' as lei,'Cross boarder Tax' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_tax end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_tax end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_tax end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_tax end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_tax end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_tax end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_tax end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_tax end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_tax end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_tax end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_tax end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_tax end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 5 as orde,'菜鸟-服务费' as lei,'Logistic Service Fee' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_service end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 6 as orde,'阿里费用' as lei,'Alipay Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_service end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 7 as orde,'天猫费用' as lei,'Tmall Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t) UNION 
            (select 8 as orde,'聚划算费用' as lei,'Great Deal Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.period='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.period='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.period='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.period='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.period='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.period='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.period='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.period='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.period='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.period='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.period='%(sel)s-12' then t.juhuasuan end) as '12' 
            from (select * from (select  
            CONCAT(SUBSTR(fee_time FROM 1 FOR 4),'-',SUBSTR(fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(logisitic_tax),2) as logisitic_tax,
            truncate(SUM(logisitic_service),2) as logisitic_service,
            truncate(SUM(alipay_service),2) as alipay_service,
            truncate(SUM(tmall),2) as tmall,
            truncate(SUM(juhuasuan),2) as juhuasuan,
            truncate(SUM(logisitic_tax_usd),2) as logisitic_tax_usd,
            truncate(SUM(logisitic_service_usd),2) as logisitic_service_usd,
            truncate(SUM(alipay_service_usd),2) as alipay_service_usd,
            truncate(SUM(tmall_usd),2) as tmall_usd,
            truncate(SUM(juhuasuan_usd),2) as juhuasuan_usd
            FROM
            t_settle_fee_info
            GROUP BY fee_time
            desc) t1,
            (select 
            SUBSTR(period FROM 1 FOR 7) as period ,
            truncate(SUM(alipay_settle),2) as Alipay_Settlement ,
            truncate(SUM(alipay_settle_p+alipay_settle_r),2) as Alipay_Amount ,
            truncate(SUM(account_fee*-1),2) as Alipay_Settlement_Fee,
            truncate(SUM(alipay_settle_usd),2) as Alipay_Settlement_Usd ,
            truncate(SUM(alipay_settle_p_usd+alipay_settle_r_usd),2) as Alipay_Amount_Usd,
            truncate(SUM(alipay_fee_usd*-1),2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t2 where t1.fee_time=t2.period) t)
        """
    else:
        order_tq = """
            (select 1 as orde,'支付宝订单提取金额' as lei,'Settlement Amount (Alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Settlement end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Settlement end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Settlement end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Settlement end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Settlement end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Settlement end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Settlement end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Settlement end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Settlement end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Settlement end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Settlement end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Settlement end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 2 as orde,'支付宝订单收到金额' as lei,'Payment amount (alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Amount end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Amount end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Amount end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Amount end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Amount end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Amount end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Amount end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Amount end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Amount end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Amount end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Amount end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Amount end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 3 as orde,'支付宝订单费用扣除' as lei,'Fees deducted (alipay)' as le,
            sum(case when t.period='%(sel)s-01' then t.Alipay_Settlement_Fee end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Alipay_Settlement_Fee end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Alipay_Settlement_Fee end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Alipay_Settlement_Fee end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Alipay_Settlement_Fee end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Alipay_Settlement_Fee end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Alipay_Settlement_Fee end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Alipay_Settlement_Fee end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Alipay_Settlement_Fee end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Alipay_Settlement_Fee end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Alipay_Settlement_Fee end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Alipay_Settlement_Fee end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            ( select 4 as orde,'菜鸟-税费' as lei,'Cross boarder Tax' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_tax end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_tax end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_tax end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_tax end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_tax end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_tax end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_tax end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_tax end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_tax end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_tax end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_tax end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_tax end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 5 as orde,'菜鸟-服务费' as lei,'Logistic Service Fee' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_service end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 6 as orde,'阿里费用' as lei,'Alipay Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_service end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 7 as orde,'天猫费用' as lei,'Tmall Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t) UNION 
            (select 8 as orde,'聚划算费用' as lei,'Great Deal Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.period='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.period='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.period='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.period='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.period='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.period='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.period='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.period='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.period='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.period='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.period='%(sel)s-12' then t.juhuasuan end) as '12' 
            from (select * from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period ,
            truncate(SUM(t1.alipay_settle/t2.tax),2) as Alipay_Settlement ,
            truncate(SUM((t1.alipay_settle_p+t1.alipay_settle_r)/t2.tax),2) as Alipay_Amount ,
            truncate(SUM((t1.account_fee*-1)/t2.tax),2) as Alipay_Settlement_Fee,
            truncate(SUM(t1.alipay_settle_usd/t2.tax),2) as Alipay_Settlement_Usd ,
            truncate(SUM((t1.alipay_settle_p_usd+t1.alipay_settle_r_usd)/t2.tax),2) as Alipay_Amount_Usd,
            truncate(SUM((t1.alipay_fee_usd*-1))/t2.tax,2) as Alipay_Settlement_Fee_Usd
            FROM
            t_settle_amount_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t3,
            (select  
            CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6)) as fee_time,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan,
            truncate(SUM(t1.logisitic_tax_usd/t2.tax),2) as logisitic_tax_usd,
            truncate(SUM(t1.logisitic_service_usd/t2.tax),2) as logisitic_service_usd,
            truncate(SUM(t1.alipay_service_usd/t2.tax),2) as alipay_service_usd,
            truncate(SUM(t1.tmall_usd/t2.tax),2) as tmall_usd,
            truncate(SUM(t1.juhuasuan_usd/t2.tax),2) as juhuasuan_usd
            FROM
            t_settle_fee_info as t1
            left join tax_rate as t2
            on  CONCAT(SUBSTR(t1.fee_time FROM 1 FOR 4),'-',SUBSTR(t1.fee_time FROM 5 FOR 6))=t2.time
            GROUP BY fee_time
            desc) t4 where t4.fee_time=t3.period) t)
        """
    order_tq = order_tq % dict(sel=years)
    data.execute(order_tq)
    order_tq_list = data.fetchall()
    all_list.extend(order_tq_list)
    # 订单生成时间
    if request.session.get("lge") != "en":
        order_sc = """
            (select 9 as orde,'买家拍下支付金额' as lei,'Total Orders' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 10 as orde,'买家拍下退款金额' as lei,'Refunds amount' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order_refund end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order_refund end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order_refund end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order_refund end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order_refund end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order_refund end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order_refund end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order_refund end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order_refund end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order_refund end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order_refund end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order_refund end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 11 as orde,'买家实际支付金额' as lei,'Payment Amount' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order_actual_pay end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order_actual_pay end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order_actual_pay end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order_actual_pay end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order_actual_pay end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order_actual_pay end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order_actual_pay end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order_actual_pay end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order_actual_pay end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order_actual_pay end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order_actual_pay end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order_actual_pay end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            ( select 12 as orde,'支付宝费用扣除' as lei,'Fees deducted by Alipay' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_Fee end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_Fee end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_Fee end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_Fee end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_Fee end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_Fee end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_Fee end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_Fee end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_Fee end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_Fee end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_Fee end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_Fee end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 13 as orde,'支付宝提取金额' as lei,'Alipay Orders' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_settlement end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_settlement end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_settlement end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_settlement end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_settlement end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_settlement end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_settlement end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_settlement end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_settlement end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_settlement end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_settlement end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_settlement end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 14 as orde,'菜鸟-税费' as lei,'Cross boarder Tax' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_tax end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_tax end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_tax end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_tax end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_tax end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_tax end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_tax end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_tax end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_tax end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_tax end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_tax end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_tax end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 15 as orde,'菜鸟-服务费' as lei,'Logistic Service Fee' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_service end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 16 as orde,'阿里费用' as lei,'Alipay Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_service end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 17 as orde,'天猫费用' as lei,'Tmall Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 18 as orde,'聚划算费用' as lei,'Great Deal Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.period='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.period='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.period='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.period='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.period='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.period='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.period='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.period='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.period='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.period='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.period='%(sel)s-12' then t.juhuasuan end) as '12' 
            from 
            (select * from (select 
            SUBSTR(payment_time FROM 1 FOR 7) as period,
            truncate(SUM(t.logisitic_tax),2) as logisitic_tax,
            truncate(SUM(t.logisitic_service),2) as logisitic_service,
            truncate(SUM(t.alipay_service),2) as alipay_service,
            truncate(SUM(t.tmall),2) as tmall,
            truncate(SUM(t.juhuasuan),2) as juhuasuan
            from t_fee_info t
            GROUP BY SUBSTR(payment_time FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(fin_period FROM 1 FOR 7) as period1,
            truncate(SUM(tmall_refund+actual_paid),2) as tmall_order,
            truncate(SUM(tmall_refund),2) as tmall_order_refund,
            truncate(SUM(actual_paid),2) as tmall_order_actual_pay,
            truncate(SUM(order_fee*-1),2) as alipay_Fee,
            truncate(SUM(alipay_get*-1),2) as alipay_settlement
            from t_order_amount 
            GROUP BY SUBSTR(fin_period FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t)
        """
    else:
        order_sc = """
            (select 9 as orde,'买家拍下支付金额' as lei,'Total Orders' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 10 as orde,'买家拍下退款金额' as lei,'Refunds amount' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order_refund end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order_refund end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order_refund end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order_refund end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order_refund end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order_refund end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order_refund end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order_refund end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order_refund end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order_refund end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order_refund end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order_refund end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 11 as orde,'买家实际支付金额' as lei,'Payment Amount' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall_order_actual_pay end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall_order_actual_pay end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall_order_actual_pay end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall_order_actual_pay end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall_order_actual_pay end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall_order_actual_pay end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall_order_actual_pay end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall_order_actual_pay end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall_order_actual_pay end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall_order_actual_pay end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall_order_actual_pay end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall_order_actual_pay end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            ( select 12 as orde,'支付宝费用扣除' as lei,'Fees deducted by Alipay' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_Fee end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_Fee end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_Fee end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_Fee end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_Fee end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_Fee end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_Fee end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_Fee end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_Fee end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_Fee end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_Fee end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_Fee end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 13 as orde,'支付宝提取金额' as lei,'Alipay Orders' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_settlement end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_settlement end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_settlement end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_settlement end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_settlement end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_settlement end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_settlement end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_settlement end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_settlement end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_settlement end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_settlement end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_settlement end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 14 as orde,'菜鸟-税费' as lei,'Cross boarder Tax' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_tax end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_tax end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_tax end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_tax end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_tax end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_tax end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_tax end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_tax end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_tax end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_tax end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_tax end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_tax end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 15 as orde,'菜鸟-服务费' as lei,'Logistic Service Fee' as le,
            sum(case when t.period='%(sel)s-01' then t.logisitic_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.logisitic_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.logisitic_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.logisitic_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.logisitic_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.logisitic_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.logisitic_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.logisitic_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.logisitic_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.logisitic_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.logisitic_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.logisitic_service end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 16 as orde,'阿里费用' as lei,'Alipay Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.alipay_service end) as '01',
            sum(case when t.period='%(sel)s-02' then t.alipay_service end) as '02',
            sum(case when t.period='%(sel)s-03' then t.alipay_service end) as '03',
            sum(case when t.period='%(sel)s-04' then t.alipay_service end) as '04',
            sum(case when t.period='%(sel)s-05' then t.alipay_service end) as '05',
            sum(case when t.period='%(sel)s-06' then t.alipay_service end) as '06',
            sum(case when t.period='%(sel)s-07' then t.alipay_service end) as '07',
            sum(case when t.period='%(sel)s-08' then t.alipay_service end) as '08',
            sum(case when t.period='%(sel)s-09' then t.alipay_service end) as '09',
            sum(case when t.period='%(sel)s-10' then t.alipay_service end) as '10',
            sum(case when t.period='%(sel)s-11' then t.alipay_service end) as '11',
            sum(case when t.period='%(sel)s-12' then t.alipay_service end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 17 as orde,'天猫费用' as lei,'Tmall Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.period='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.period='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.period='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.period='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.period='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.period='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.period='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.period='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.period='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.period='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.period='%(sel)s-12' then t.tmall end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t) UNION 
            (select 18 as orde,'聚划算费用' as lei,'Great Deal Comm' as le,
            sum(case when t.period='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.period='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.period='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.period='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.period='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.period='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.period='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.period='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.period='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.period='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.period='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.period='%(sel)s-12' then t.juhuasuan end) as '12' 
            from 
            (select * from 
            (select 
            SUBSTR(t1.fin_period FROM 1 FOR 7) as period,
            truncate(SUM((t1.tmall_refund+actual_paid)/t2.tax),2) as tmall_order,
            truncate(SUM(t1.tmall_refund/t2.tax),2) as tmall_order_refund,
            truncate(SUM(t1.actual_paid/t2.tax),2) as tmall_order_actual_pay,
            truncate(SUM((t1.order_fee*-1)/t2.tax),2) as alipay_Fee,
            truncate(SUM((t1.alipay_get*-1)/t2.tax),2) as alipay_settlement
            from t_order_amount  as t1
            left join tax_rate as t2
            on SUBSTR(t1.fin_period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.fin_period FROM 1 FOR 7)
            desc) t1,
            (select 
            SUBSTR(t1.payment_time FROM 1 FOR 7) as period1,
            truncate(SUM(t1.logisitic_tax/t2.tax),2) as logisitic_tax,
            truncate(SUM(t1.logisitic_service/t2.tax),2) as logisitic_service,
            truncate(SUM(t1.alipay_service/t2.tax),2) as alipay_service,
            truncate(SUM(t1.tmall/t2.tax),2) as tmall,
            truncate(SUM(t1.juhuasuan/t2.tax),2) as juhuasuan
            from t_fee_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.payment_time FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(t1.payment_time FROM 1 FOR 7)
            desc) t2 where t1.period=t2.period1) t)
        """
    order_sc = order_sc % dict(sel=years)
    data.execute(order_sc)
    order_sc_list = data.fetchall()
    all_list.extend(order_sc_list)
    # 订单发货时间
    if request.session.get("lge") != "en":
        order_fh = """
            (select 19 as orde,'期间交易出库金额' as lei,'Sales revenue' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.out_stock end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.out_stock end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.out_stock end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.out_stock end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.out_stock end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.out_stock end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.out_stock end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.out_stock end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.out_stock end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.out_stock end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.out_stock end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.out_stock end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 20 as orde,'菜鸟-税费' as lei,'Cross boarder Tax' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.cainiao_tax end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.cainiao_tax end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.cainiao_tax end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.cainiao_tax end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.cainiao_tax end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.cainiao_tax end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.cainiao_tax end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.cainiao_tax end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.cainiao_tax end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.cainiao_tax end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.cainiao_tax end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.cainiao_tax end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 21 as orde,'菜鸟-服务费' as lei,'Logistic Service Fee' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.cainiao_service end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.cainiao_service end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.cainiao_service end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.cainiao_service end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.cainiao_service end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.cainiao_service end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.cainiao_service end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.cainiao_service end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.cainiao_service end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.cainiao_service end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.cainiao_service end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.cainiao_service end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 22 as orde,'阿里费用' as lei,'Alipay Comm' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.alipay end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.alipay end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.alipay end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.alipay end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.alipay end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.alipay end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.alipay end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.alipay end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.alipay end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.alipay end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.alipay end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.alipay end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 23 as orde,'天猫费用' as lei,'Tmall Comm' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.tmall end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 24 as orde,'聚划算费用' as lei,'Great Deal Comm' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.juhuasuan end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t) UNION 
            (select 25 as orde,'期间退款金额' as lei,'CUSTOMER REFUNDS' as le,
            sum(case when t.fee_time='%(sel)s-01' then t.refund end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.refund end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.refund end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.refund end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.refund end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.refund end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.refund end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.refund end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.refund end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.refund end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.refund end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.refund end) as '12' 
            FROM (SELECT * from t_fee_detail_monthly_info) t)
        """
    else:
        order_fh = """
            (select '期间交易出库金额' as lei,'Sales revenue' as le,19 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.out_stock end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.out_stock end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.out_stock end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.out_stock end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.out_stock end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.out_stock end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.out_stock end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.out_stock end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.out_stock end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.out_stock end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.out_stock end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.out_stock end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '菜鸟-税费' as lei,'Cross boarder Tax' as le,20 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.cainiao_tax end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.cainiao_tax end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.cainiao_tax end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.cainiao_tax end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.cainiao_tax end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.cainiao_tax end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.cainiao_tax end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.cainiao_tax end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.cainiao_tax end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.cainiao_tax end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.cainiao_tax end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.cainiao_tax end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '菜鸟-服务费' as lei,'Logistic Service Fee' as le,21 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.cainiao_service end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.cainiao_service end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.cainiao_service end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.cainiao_service end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.cainiao_service end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.cainiao_service end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.cainiao_service end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.cainiao_service end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.cainiao_service end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.cainiao_service end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.cainiao_service end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.cainiao_service end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '阿里费用' as lei,'Alipay Comm' as le,22 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.alipay end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.alipay end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.alipay end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.alipay end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.alipay end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.alipay end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.alipay end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.alipay end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.alipay end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.alipay end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.alipay end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.alipay end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '天猫费用' as lei,'Tmall Comm' as le,23 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.tmall end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.tmall end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.tmall end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.tmall end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.tmall end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.tmall end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.tmall end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.tmall end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.tmall end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.tmall end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.tmall end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.tmall end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '聚划算费用' as lei,'Great Deal Comm' as le,24 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.juhuasuan end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.juhuasuan end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.juhuasuan end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.juhuasuan end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.juhuasuan end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.juhuasuan end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.juhuasuan end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.juhuasuan end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.juhuasuan end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.juhuasuan end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.juhuasuan end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.juhuasuan end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t) UNION 
            (select '期间退款金额' as lei,'CUSTOMER REFUNDS' as le,25 as orde,
            sum(case when t.fee_time='%(sel)s-01' then t.refund end) as '01',
            sum(case when t.fee_time='%(sel)s-02' then t.refund end) as '02',
            sum(case when t.fee_time='%(sel)s-03' then t.refund end) as '03',
            sum(case when t.fee_time='%(sel)s-04' then t.refund end) as '04',
            sum(case when t.fee_time='%(sel)s-05' then t.refund end) as '05',
            sum(case when t.fee_time='%(sel)s-06' then t.refund end) as '06',
            sum(case when t.fee_time='%(sel)s-07' then t.refund end) as '07',
            sum(case when t.fee_time='%(sel)s-08' then t.refund end) as '08',
            sum(case when t.fee_time='%(sel)s-09' then t.refund end) as '09',
            sum(case when t.fee_time='%(sel)s-10' then t.refund end) as '10',
            sum(case when t.fee_time='%(sel)s-11' then t.refund end) as '11',
            sum(case when t.fee_time='%(sel)s-12' then t.refund end) as '12' 
            FROM (select t1.fee_time,
            truncate(t1.out_stock/t2.tax,2) as out_stock ,truncate(t1.cainiao_tax/t2.tax,2) as cainiao_tax ,truncate(t1.cainiao_service/t2.tax,2) as cainiao_service,
            truncate(t1.alipay/t2.tax,2) as alipay,truncate(t1.tmall/t2.tax,2) as tmall,truncate(t1.juhuasuan/t2.tax,2) as juhuasuan ,
            truncate(t1.refund/t2.tax,2) as refund
            from t_fee_detail_monthly_info as t1
            left join tax_rate as t2 on t1.fee_time=t2.time) t)
        """
    order_fh = order_fh % dict(sel=years)
    data.execute(order_fh)
    order_fh_list = data.fetchall()
    all_list.extend(order_fh_list)
    # 我的账户支出
    if request.session.get("lge") != "en":
        my_out = """
            (SELECT 26 as orde,'充值' as lei,'Deposit' as le,
            sum(case when t.period='%(sel)s-01' then t.Recharge end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Recharge end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Recharge end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Recharge end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Recharge end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Recharge end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Recharge end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Recharge end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Recharge end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Recharge end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Recharge end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Recharge end) as '12' 
            from (select 
            SUBSTR(period FROM 1 FOR 7) as period,
            truncate(SUM(recharge),2) as Recharge,
            truncate(SUM(refund),2) as Refund,
            truncate(SUM(payment),2) as Payments,
            truncate(SUM(order_payment),2) as order_payment,
            truncate(SUM(not_order_payment),2) as not_order_payment
            from t_myaccount_monthly_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT 27 as orde,'退还' as lei,'Refunds from Tmall' as le,
            sum(case when t.period='%(sel)s-01' then t.Refund end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Refund end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Refund end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Refund end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Refund end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Refund end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Refund end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Refund end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Refund end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Refund end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Refund end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Refund end) as '12' 
            from (select 
            SUBSTR(period FROM 1 FOR 7) as period,
            truncate(SUM(recharge),2) as Recharge,
            truncate(SUM(refund),2) as Refund,
            truncate(SUM(payment),2) as Payments,
            truncate(SUM(order_payment),2) as order_payment,
            truncate(SUM(not_order_payment),2) as not_order_payment
            from t_myaccount_monthly_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT 28 as orde,'支付' as lei,'Total Payouts' as le,
            sum(case when t.period='%(sel)s-01' then t.Payments end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Payments end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Payments end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Payments end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Payments end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Payments end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Payments end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Payments end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Payments end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Payments end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Payments end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Payments end) as '12' 
            from (select 
            SUBSTR(period FROM 1 FOR 7) as period,
            truncate(SUM(recharge),2) as Recharge,
            truncate(SUM(refund),2) as Refund,
            truncate(SUM(payment),2) as Payments,
            truncate(SUM(order_payment),2) as order_payment,
            truncate(SUM(not_order_payment),2) as not_order_payment
            from t_myaccount_monthly_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT 29 as orde,'订单支付' as lei,'Payouts for Orders' as le,
            sum(case when t.period='%(sel)s-01' then t.order_payment end) as '01',
            sum(case when t.period='%(sel)s-02' then t.order_payment end) as '02',
            sum(case when t.period='%(sel)s-03' then t.order_payment end) as '03',
            sum(case when t.period='%(sel)s-04' then t.order_payment end) as '04',
            sum(case when t.period='%(sel)s-05' then t.order_payment end) as '05',
            sum(case when t.period='%(sel)s-06' then t.order_payment end) as '06',
            sum(case when t.period='%(sel)s-07' then t.order_payment end) as '07',
            sum(case when t.period='%(sel)s-08' then t.order_payment end) as '08',
            sum(case when t.period='%(sel)s-09' then t.order_payment end) as '09',
            sum(case when t.period='%(sel)s-10' then t.order_payment end) as '10',
            sum(case when t.period='%(sel)s-11' then t.order_payment end) as '11',
            sum(case when t.period='%(sel)s-12' then t.order_payment end) as '12' 
            from (select 
            SUBSTR(period FROM 1 FOR 7) as period,
            truncate(SUM(recharge),2) as Recharge,
            truncate(SUM(refund),2) as Refund,
            truncate(SUM(payment),2) as Payments,
            truncate(SUM(order_payment),2) as order_payment,
            truncate(SUM(not_order_payment),2) as not_order_payment
            from t_myaccount_monthly_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT 30 as orde,'非订单支付' as lei,'Non order related payouts' as le,
            sum(case when t.period='%(sel)s-01' then t.not_order_payment end) as '01',
            sum(case when t.period='%(sel)s-02' then t.not_order_payment end) as '02',
            sum(case when t.period='%(sel)s-03' then t.not_order_payment end) as '03',
            sum(case when t.period='%(sel)s-04' then t.not_order_payment end) as '04',
            sum(case when t.period='%(sel)s-05' then t.not_order_payment end) as '05',
            sum(case when t.period='%(sel)s-06' then t.not_order_payment end) as '06',
            sum(case when t.period='%(sel)s-07' then t.not_order_payment end) as '07',
            sum(case when t.period='%(sel)s-08' then t.not_order_payment end) as '08',
            sum(case when t.period='%(sel)s-09' then t.not_order_payment end) as '09',
            sum(case when t.period='%(sel)s-10' then t.not_order_payment end) as '10',
            sum(case when t.period='%(sel)s-11' then t.not_order_payment end) as '11',
            sum(case when t.period='%(sel)s-12' then t.not_order_payment end) as '12' 
            from (select 
            SUBSTR(period FROM 1 FOR 7) as period,
            truncate(SUM(recharge),2) as Recharge,
            truncate(SUM(refund),2) as Refund,
            truncate(SUM(payment),2) as Payments,
            truncate(SUM(order_payment),2) as order_payment,
            truncate(SUM(not_order_payment),2) as not_order_payment
            from t_myaccount_monthly_info
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t)
        """
    else:
        my_out = """
            (SELECT '充值' as lei,'Deposit' as le,26 as orde,
            sum(case when t.period='%(sel)s-01' then t.Recharge end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Recharge end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Recharge end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Recharge end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Recharge end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Recharge end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Recharge end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Recharge end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Recharge end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Recharge end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Recharge end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Recharge end) as '12' 
            from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period,
            FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
            FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
            FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
            FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
            FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
            from t_myaccount_monthly_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT '退还' as lei,'Refunds from Tmall' as le,27 as orde,
            sum(case when t.period='%(sel)s-01' then t.Refund end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Refund end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Refund end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Refund end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Refund end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Refund end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Refund end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Refund end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Refund end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Refund end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Refund end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Refund end) as '12' 
            from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period,
            FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
            FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
            FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
            FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
            FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
            from t_myaccount_monthly_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT '支付' as lei,'Total Payouts' as le,28 as orde,
            sum(case when t.period='%(sel)s-01' then t.Payments end) as '01',
            sum(case when t.period='%(sel)s-02' then t.Payments end) as '02',
            sum(case when t.period='%(sel)s-03' then t.Payments end) as '03',
            sum(case when t.period='%(sel)s-04' then t.Payments end) as '04',
            sum(case when t.period='%(sel)s-05' then t.Payments end) as '05',
            sum(case when t.period='%(sel)s-06' then t.Payments end) as '06',
            sum(case when t.period='%(sel)s-07' then t.Payments end) as '07',
            sum(case when t.period='%(sel)s-08' then t.Payments end) as '08',
            sum(case when t.period='%(sel)s-09' then t.Payments end) as '09',
            sum(case when t.period='%(sel)s-10' then t.Payments end) as '10',
            sum(case when t.period='%(sel)s-11' then t.Payments end) as '11',
            sum(case when t.period='%(sel)s-12' then t.Payments end) as '12' 
            from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period,
            FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
            FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
            FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
            FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
            FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
            from t_myaccount_monthly_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT '订单支付' as lei,'Payouts for Orders' as le,29 as orde,
            sum(case when t.period='%(sel)s-01' then t.order_payment end) as '01',
            sum(case when t.period='%(sel)s-02' then t.order_payment end) as '02',
            sum(case when t.period='%(sel)s-03' then t.order_payment end) as '03',
            sum(case when t.period='%(sel)s-04' then t.order_payment end) as '04',
            sum(case when t.period='%(sel)s-05' then t.order_payment end) as '05',
            sum(case when t.period='%(sel)s-06' then t.order_payment end) as '06',
            sum(case when t.period='%(sel)s-07' then t.order_payment end) as '07',
            sum(case when t.period='%(sel)s-08' then t.order_payment end) as '08',
            sum(case when t.period='%(sel)s-09' then t.order_payment end) as '09',
            sum(case when t.period='%(sel)s-10' then t.order_payment end) as '10',
            sum(case when t.period='%(sel)s-11' then t.order_payment end) as '11',
            sum(case when t.period='%(sel)s-12' then t.order_payment end) as '12' 
            from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period,
            FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
            FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
            FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
            FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
            FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
            from t_myaccount_monthly_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t) UNION 
            (SELECT '非订单支付' as lei,'Non order related payouts' as le,30 as orde,
            sum(case when t.period='%(sel)s-01' then t.not_order_payment end) as '01',
            sum(case when t.period='%(sel)s-02' then t.not_order_payment end) as '02',
            sum(case when t.period='%(sel)s-03' then t.not_order_payment end) as '03',
            sum(case when t.period='%(sel)s-04' then t.not_order_payment end) as '04',
            sum(case when t.period='%(sel)s-05' then t.not_order_payment end) as '05',
            sum(case when t.period='%(sel)s-06' then t.not_order_payment end) as '06',
            sum(case when t.period='%(sel)s-07' then t.not_order_payment end) as '07',
            sum(case when t.period='%(sel)s-08' then t.not_order_payment end) as '08',
            sum(case when t.period='%(sel)s-09' then t.not_order_payment end) as '09',
            sum(case when t.period='%(sel)s-10' then t.not_order_payment end) as '10',
            sum(case when t.period='%(sel)s-11' then t.not_order_payment end) as '11',
            sum(case when t.period='%(sel)s-12' then t.not_order_payment end) as '12' 
            from (select 
            SUBSTR(t1.period FROM 1 FOR 7) as period,
            FORMAT(SUM(t1.recharge/t2.tax),2) as Recharge,
            FORMAT(SUM(t1.refund/t2.tax),2) as Refund,
            FORMAT(SUM(t1.payment/t2.tax),2) as Payments,
            FORMAT(SUM(t1.order_payment/t2.tax),2) as order_payment,
            FORMAT(SUM(t1.not_order_payment/t2.tax),2) as not_order_payment
            from t_myaccount_monthly_info as t1
            left join tax_rate as t2
            on SUBSTR(t1.period FROM 1 FOR 7)=t2.time
            GROUP BY SUBSTR(period FROM 1 FOR 7)
            desc) t)
        """
    my_out = my_out % dict(sel=years)
    data.execute(my_out)
    my_out_list = data.fetchall()
    all_list.extend(my_out_list)
    # 账户费用分析
    if request.session.get("lge") != "en":
        my_fx = """
            (select 31 as orde,'仓储费' as lei,'TMALL WAREHOUSE FEES' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.tmall_warehouse_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.tmall_warehouse_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.tmall_warehouse_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.tmall_warehouse_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.tmall_warehouse_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.tmall_warehouse_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.tmall_warehouse_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.tmall_warehouse_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.tmall_warehouse_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.tmall_warehouse_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.tmall_warehouse_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.tmall_warehouse_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 32 as orde,'保险费' as lei,'INSURANCE FEES' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.insurance_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.insurance_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.insurance_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.insurance_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.insurance_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.insurance_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.insurance_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.insurance_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.insurance_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.insurance_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.insurance_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.insurance_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 33 as orde,'销毁费' as lei,'DESTROY FEES' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.destory_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.destory_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.destory_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.destory_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.destory_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.destory_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.destory_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.destory_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.destory_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.destory_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.destory_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.destory_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 34 as orde,'商家赔付给消费者费用' as lei,'To Consumer' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.merchant_pay_to_custom end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.merchant_pay_to_custom end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.merchant_pay_to_custom end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.merchant_pay_to_custom end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.merchant_pay_to_custom end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.merchant_pay_to_custom end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.merchant_pay_to_custom end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.merchant_pay_to_custom end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.merchant_pay_to_custom end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.merchant_pay_to_custom end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.merchant_pay_to_custom end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.merchant_pay_to_custom end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 35 as orde,'菜鸟赔付给商家费用(货款赔付)' as lei,'Refund for Goods' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.cainiao_pay_goodsfee_to_merchant end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.cainiao_pay_goodsfee_to_merchant end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.cainiao_pay_goodsfee_to_merchant end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.cainiao_pay_goodsfee_to_merchant end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.cainiao_pay_goodsfee_to_merchant end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.cainiao_pay_goodsfee_to_merchant end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.cainiao_pay_goodsfee_to_merchant end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.cainiao_pay_goodsfee_to_merchant end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.cainiao_pay_goodsfee_to_merchant end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.cainiao_pay_goodsfee_to_merchant end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.cainiao_pay_goodsfee_to_merchant end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.cainiao_pay_goodsfee_to_merchant end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 36 as orde,'菜鸟赔付商给家费用(保证金赔付)' as lei,'Refund for Bond' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.cainiao_pay_deposit_to_merchant end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.cainiao_pay_deposit_to_merchant end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.cainiao_pay_deposit_to_merchant end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.cainiao_pay_deposit_to_merchant end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.cainiao_pay_deposit_to_merchant end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.cainiao_pay_deposit_to_merchant end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.cainiao_pay_deposit_to_merchant end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.cainiao_pay_deposit_to_merchant end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.cainiao_pay_deposit_to_merchant end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.cainiao_pay_deposit_to_merchant end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.cainiao_pay_deposit_to_merchant end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.cainiao_pay_deposit_to_merchant end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 37 as orde,'推广补助' as lei,'Refund for Extension subsidy' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.popularize_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.popularize_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.popularize_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.popularize_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.popularize_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.popularize_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.popularize_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.popularize_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.popularize_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.popularize_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.popularize_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.popularize_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 38 as orde,'其他账户返还' as lei,'OTHER' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.other_payback_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.other_payback_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.other_payback_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.other_payback_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.other_payback_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.other_payback_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.other_payback_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.other_payback_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.other_payback_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.other_payback_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.other_payback_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.other_payback_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 39 as orde,'天猫广告推广费' as lei,'BANNER/KEYWORDS ADVERTISING' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.tmall_popularize_fee end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.tmall_popularize_fee end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.tmall_popularize_fee end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.tmall_popularize_fee end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.tmall_popularize_fee end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.tmall_popularize_fee end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.tmall_popularize_fee end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.tmall_popularize_fee end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.tmall_popularize_fee end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.tmall_popularize_fee end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.tmall_popularize_fee end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.tmall_popularize_fee end) as '12' 
            from (SELECT * from t_other_fee_info) t) union 
            (select 40 as orde,'返现金额和CRM' as lei,'IN STORE MARKETING PROMOTIONS' as le,
            sum(case when t.trans_date='%(sel)s-01' then t.return_cash end) as '01',
            sum(case when t.trans_date='%(sel)s-02' then t.return_cash end) as '02',
            sum(case when t.trans_date='%(sel)s-03' then t.return_cash end) as '03',
            sum(case when t.trans_date='%(sel)s-04' then t.return_cash end) as '04',
            sum(case when t.trans_date='%(sel)s-05' then t.return_cash end) as '05',
            sum(case when t.trans_date='%(sel)s-06' then t.return_cash end) as '06',
            sum(case when t.trans_date='%(sel)s-07' then t.return_cash end) as '07',
            sum(case when t.trans_date='%(sel)s-08' then t.return_cash end) as '08',
            sum(case when t.trans_date='%(sel)s-09' then t.return_cash end) as '09',
            sum(case when t.trans_date='%(sel)s-10' then t.return_cash end) as '10',
            sum(case when t.trans_date='%(sel)s-11' then t.return_cash end) as '11',
            sum(case when t.trans_date='%(sel)s-12' then t.return_cash end) as '12' 
            from (SELECT * from t_other_fee_info) t)
        """
    else:
        my_fx = """
        (select '仓储费' as lei,'TMALL WAREHOUSE FEES' as le,31 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.tmall_warehouse_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.tmall_warehouse_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.tmall_warehouse_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.tmall_warehouse_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.tmall_warehouse_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.tmall_warehouse_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.tmall_warehouse_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.tmall_warehouse_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.tmall_warehouse_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.tmall_warehouse_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.tmall_warehouse_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.tmall_warehouse_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '保险费' as lei,'INSURANCE FEES' as le,32 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.insurance_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.insurance_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.insurance_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.insurance_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.insurance_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.insurance_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.insurance_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.insurance_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.insurance_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.insurance_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.insurance_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.insurance_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '销毁费' as lei,'DESTROY FEES' as le,33 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.destory_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.destory_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.destory_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.destory_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.destory_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.destory_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.destory_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.destory_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.destory_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.destory_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.destory_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.destory_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '商家赔付给消费者费用' as lei,'To Consumer' as le,34 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.merchant_pay_to_custom end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.merchant_pay_to_custom end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.merchant_pay_to_custom end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.merchant_pay_to_custom end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.merchant_pay_to_custom end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.merchant_pay_to_custom end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.merchant_pay_to_custom end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.merchant_pay_to_custom end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.merchant_pay_to_custom end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.merchant_pay_to_custom end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.merchant_pay_to_custom end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.merchant_pay_to_custom end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '菜鸟赔付给商家费用(货款赔付)' as lei,'Refund for Goods' as le,35 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.cainiao_pay_goodsfee_to_merchant end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.cainiao_pay_goodsfee_to_merchant end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.cainiao_pay_goodsfee_to_merchant end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.cainiao_pay_goodsfee_to_merchant end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.cainiao_pay_goodsfee_to_merchant end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.cainiao_pay_goodsfee_to_merchant end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.cainiao_pay_goodsfee_to_merchant end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.cainiao_pay_goodsfee_to_merchant end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.cainiao_pay_goodsfee_to_merchant end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.cainiao_pay_goodsfee_to_merchant end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.cainiao_pay_goodsfee_to_merchant end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.cainiao_pay_goodsfee_to_merchant end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '菜鸟赔付商给家费用(保证金赔付)' as lei,'Refund for Bond' as le,36 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.cainiao_pay_deposit_to_merchant end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.cainiao_pay_deposit_to_merchant end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.cainiao_pay_deposit_to_merchant end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.cainiao_pay_deposit_to_merchant end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.cainiao_pay_deposit_to_merchant end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.cainiao_pay_deposit_to_merchant end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.cainiao_pay_deposit_to_merchant end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.cainiao_pay_deposit_to_merchant end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.cainiao_pay_deposit_to_merchant end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.cainiao_pay_deposit_to_merchant end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.cainiao_pay_deposit_to_merchant end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.cainiao_pay_deposit_to_merchant end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '推广补助' as lei,'Refund for Extension subsidy' as le,37 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.popularize_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.popularize_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.popularize_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.popularize_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.popularize_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.popularize_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.popularize_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.popularize_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.popularize_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.popularize_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.popularize_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.popularize_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '其他账户返还' as lei,'OTHER' as le,38 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.other_payback_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.other_payback_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.other_payback_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.other_payback_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.other_payback_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.other_payback_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.other_payback_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.other_payback_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.other_payback_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.other_payback_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.other_payback_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.other_payback_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '天猫广告推广费' as lei,'BANNER/KEYWORDS ADVERTISING' as le,39 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.tmall_popularize_fee end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.tmall_popularize_fee end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.tmall_popularize_fee end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.tmall_popularize_fee end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.tmall_popularize_fee end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.tmall_popularize_fee end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.tmall_popularize_fee end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.tmall_popularize_fee end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.tmall_popularize_fee end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.tmall_popularize_fee end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.tmall_popularize_fee end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.tmall_popularize_fee end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t) union 
        (select '返现金额和CRM' as lei,'IN STORE MARKETING PROMOTIONS' as le,40 as orde,
        sum(case when t.trans_date='%(sel)s-01' then t.return_cash end) as '01',
        sum(case when t.trans_date='%(sel)s-02' then t.return_cash end) as '02',
        sum(case when t.trans_date='%(sel)s-03' then t.return_cash end) as '03',
        sum(case when t.trans_date='%(sel)s-04' then t.return_cash end) as '04',
        sum(case when t.trans_date='%(sel)s-05' then t.return_cash end) as '05',
        sum(case when t.trans_date='%(sel)s-06' then t.return_cash end) as '06',
        sum(case when t.trans_date='%(sel)s-07' then t.return_cash end) as '07',
        sum(case when t.trans_date='%(sel)s-08' then t.return_cash end) as '08',
        sum(case when t.trans_date='%(sel)s-09' then t.return_cash end) as '09',
        sum(case when t.trans_date='%(sel)s-10' then t.return_cash end) as '10',
        sum(case when t.trans_date='%(sel)s-11' then t.return_cash end) as '11',
        sum(case when t.trans_date='%(sel)s-12' then t.return_cash end) as '12' 
        from (SELECT t1.trans_date,truncate(t1.tmall_warehouse_fee/t2.tax,2) as tmall_warehouse_fee ,truncate(t1.insurance_fee/t2.tax,2) as insurance_fee,truncate(t1.destory_fee/t2.tax,2) as destory_fee ,truncate(t1.merchant_pay_to_custom/t2.tax,2) as merchant_pay_to_custom,
        truncate(t1.cainiao_pay_goodsfee_to_merchant/t2.tax,2) as cainiao_pay_goodsfee_to_merchant ,
        truncate(t1.cainiao_pay_deposit_to_merchant/t2.tax,2)  as cainiao_pay_deposit_to_merchant,
        truncate(t1.popularize_fee/t2.tax,2) as popularize_fee,
        truncate(t1.other_payback_fee/t2.tax,2) as other_payback_fee,
        truncate(t1.tmall_popularize_fee/t2.tax,2) as tmall_popularize_fee,
        truncate(t1.return_cash/t2.tax,2) as return_cash
        from t_other_fee_info as t1  left join tax_rate as t2
        on t1.trans_date=t2.time) t)
        """
    my_fx = my_fx % dict(sel=years)
    data.execute(my_out)
    my_fx_list = data.fetchall()
    all_list.extend(my_fx_list)
    # 写入数据
    excel_row += 1
    for obj in all_list:
        M1 = obj["01"]
        M2 = obj["02"]
        M3 = obj["03"]
        M4 = obj["04"]
        M5 = obj["05"]
        M6 = obj["06"]
        M7 = obj["07"]
        M8 = obj["08"]
        M9 = obj["09"]
        M10 = obj["10"]
        M11 = obj["11"]
        M12 = obj["12"]
        if request.session.get("lge") != "en":
            lei = obj["lei"]
            if obj["orde"] == 8:
                w.write_merge(excel_row - 7, excel_row, 0, 0, "订单提取时间", style_heading)
            if obj["orde"] == 18:
                w.write_merge(excel_row - 9, excel_row, 0, 0, "订单生成时间", style_heading)
            if obj["orde"] == 25:
                w.write_merge(excel_row - 6, excel_row, 0, 0, "订单发货时间", style_heading)
            if obj["orde"] == 30:
                w.write_merge(excel_row - 4, excel_row, 0, 0, "我的账户支出", style_heading)
            if obj["orde"] == 40:
                w.write_merge(excel_row - 9, excel_row, 0, 0, "账户费用分析", style_heading)
            if M1 != None:
                M1 = "￥" + str(M1)
            if M2 != None:
                M2 = "￥" + str(M2)
            if M3 != None:
                M3 = "￥" + str(M3)
            if M4 != None:
                M4 = "￥" + str(M4)
            if M5 != None:
                M5 = "￥" + str(M5)
            if M6 != None:
                M6 = "￥" + str(M6)
            if M7 != None:
                M7 = "￥" + str(M7)
            if M8 != None:
                M8 = "￥" + str(M8)
            if M9 != None:
                M9 = "￥" + str(M9)
            if M10 != None:
                M10 = "￥" + str(M10)
            if M11 != None:
                M11 = "￥" + str(M11)
            if M12 != None:
                M12 = "￥" + str(M12)
        else:
            lei = obj["le"]
            if obj["orde"] == 8:
                w.write_merge(
                    excel_row - 7,
                    excel_row,
                    0,
                    0,
                    "Based on Order settled time",
                    style_heading,
                )
            if obj["orde"] == 18:
                w.write_merge(
                    excel_row - 9,
                    excel_row,
                    0,
                    0,
                    "Based on order placed time",
                    style_heading,
                )
            if obj["orde"] == 25:
                w.write_merge(
                    excel_row - 6,
                    excel_row,
                    0,
                    0,
                    "Based on order shipped time",
                    style_heading,
                )
            if obj["orde"] == 30:
                w.write_merge(
                    excel_row - 4,
                    excel_row,
                    0,
                    0,
                    "Balance in Alipay's MyAccount",
                    style_heading,
                )
            if obj["orde"] == 40:
                w.write_merge(
                    excel_row - 9, excel_row, 0, 0, "MyAccount Analysis", style_heading
                )
            if M1 != None:
                M1 = "$" + str(M1)
            if M2 != None:
                M2 = "$" + str(M2)
            if M3 != None:
                M3 = "$" + str(M3)
            if M4 != None:
                M4 = "$" + str(M4)
            if M5 != None:
                M5 = "$" + str(M5)
            if M6 != None:
                M6 = "$" + str(M6)
            if M7 != None:
                M7 = "$" + str(M7)
            if M8 != None:
                M8 = "$" + str(M8)
            if M9 != None:
                M9 = "$" + str(M9)
            if M10 != None:
                M10 = "$" + str(M10)
            if M11 != None:
                M11 = "$" + str(M11)
            if M12 != None:
                M12 = "$" + str(M12)
        w.write(excel_row, 1, lei, style_heading)
        w.write(excel_row, 2, M1, style_yy)
        w.write(excel_row, 3, M2, style_yy)
        w.write(excel_row, 4, M3, style_yy)
        w.write(excel_row, 5, M4, style_yy)
        w.write(excel_row, 6, M5, style_yy)
        w.write(excel_row, 7, M6, style_yy)
        w.write(excel_row, 8, M7, style_yy)
        w.write(excel_row, 9, M8, style_yy)
        w.write(excel_row, 10, M9, style_yy)
        w.write(excel_row, 11, M10, style_yy)
        w.write(excel_row, 12, M11, style_yy)
        w.write(excel_row, 13, M12, style_yy)
        w.col(0).width = 120 * 50
        w.col(1).width = 160 * 50
        w.col(2).width = 60 * 50
        w.col(3).width = 60 * 50
        w.col(4).width = 60 * 50
        w.col(5).width = 60 * 50
        w.col(6).width = 60 * 50
        w.col(7).width = 60 * 50
        w.col(8).width = 60 * 50
        w.col(9).width = 60 * 50
        w.col(10).width = 60 * 50
        w.col(11).width = 60 * 50
        w.col(12).width = 60 * 50
        w.col(13).width = 60 * 50

        excel_row += 1
    # 检测文件是够存在
    # 方框中代码是保存本地文件使用，如不需要请删除该代码
    ###########################
    exist_file = os.path.exists("sum.xls")
    if exist_file:
        os.remove(r"sum.xls")
    ws.save("sum.xls")
    ############################
    sio = io.StringIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=sum.xls"
    response.write(sio.getvalue())
    return response

def test1_view(request):
      # 获得系统本地时间，返回的格式是 UTC 中的 struct_time 数据
    t = time.localtime()
 # 第 6 个元素是 tm_wday , 范围为 [0,6], 星期一 is 0
    n = t[6]
 # 星期一到星期日字符串，每个字符串用 _() 标识出来。
    weekdays = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'),
            _('Friday'), _('Saturday'), _('Sunday')]
# 返回一个 HttpResponse

    return HttpResponse(weekdays[n])
