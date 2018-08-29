#!/usr/bin/python
# coding:UTF-8
import os
import sys
sys.path.append("..")
sys.path.append("../..")
import MySQLdb
import tmall_data_analyse.settings as settings
from decimal import *

# sys.setdefaultencoding('utf-8')


def updateBomTotalPrice(goods_code, price):
    print(goods_code, price)
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    detail = db.cursor(MySQLdb.cursors.DictCursor)

    value = [str(price), goods_code]
    detail.execute("update bom set price=%s where product_name=%s", value)
    db.commit()
    detail.close()
    db.close()


def getPriceBySku(goods_id):
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    detail = db.cursor(MySQLdb.cursors.DictCursor)
    value = [goods_id]
    detail.execute("select price from t_bas_sku_price where sku_id =%s", value)
    if detail.rowcount == 0:
        return "0"
    else:
        row = detail.fetchone()
        return row["price"]


def getPriceList():
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    pricelist = db.cursor(MySQLdb.cursors.DictCursor)
    pricelist.execute("desc bom")

    data = pricelist.fetchall()

    lst = []
    result = []
    fields = []
    for row in data:
        lst.append(row["Field"])
    for i in range(3, len(lst)):
        print("-->" + lst[i])

    price = getPriceBySku(lst[i])
    result.append(price)

    fields.append(lst[i])
    return result, fields


def getPriceDict():
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor(MySQLdb.cursors.DictCursor)
    data.execute("select * from t_bas_sku_price")
    price_list = data.fetchall()
    data.close()
    db.close
    res ={}
    for one_price in price_list:
        res[one_price['sku_id']] = one_price['price']
    return res

db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                        user=settings.DATABASES.get(
                            'default').get('USER'),
                        passwd=settings.DATABASES.get(
                            'default').get('PASSWORD'),
                        db=settings.DATABASES.get('default').get('NAME'),
                        charset="utf8",
                        local_infile=1)
data = db.cursor(MySQLdb.cursors.DictCursor)

#计算bom清单总价格
try:
    data.execute(
        "SELECT * FROM bom a LEFT JOIN bom_detail b ON a.product_name =b.product_name  where goods_count>0 ORDER BY Num desc")
    bom_data = data.fetchall()
    price_dict = getPriceDict()
    #print(price_dict)
    last_bom_product_name = ""
    price_temp = 0.00
    index = 0
    for one_bom_data in bom_data:
        if index == 0:
            last_bom_product_name = one_bom_data['product_name']
            print(one_bom_data)
            print(one_bom_data['goods_id'])
            price_temp = price_dict[one_bom_data['goods_id']]*one_bom_data['goods_count']
        else:
            if one_bom_data['product_name']==last_bom_product_name:
                price_temp = price_temp + price_dict[one_bom_data['goods_id']] * one_bom_data['goods_count']
            else:
                update_strr = "update bom set price=%s where product_name='%s'" %(price_temp,last_bom_product_name)
                print(update_strr)
                data.execute(update_strr)
                price_temp = price_dict[one_bom_data['goods_id']] * one_bom_data['goods_count']
                
            last_bom_product_name = one_bom_data['product_name']
        index = index+1
    #处理最后一条数据
    last_update_strr = "update bom set price=%s where product_name='%s'" %(price_temp,last_bom_product_name)
    data.execute(last_update_strr)
    data.close
    db.close()
    print("bom_price finish")
except Exception as e:
    print("error: unable fetch data", e.args)
    data.close
    db.close()
    raise

print("search complete")
