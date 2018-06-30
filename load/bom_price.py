#!/usr/bin/python
# coding:UTF-8
import MySQLdb
import numpy as np
import sys
from decimal import *
import imp

imp.reload(sys)
# sys.setdefaultencoding('utf-8')


def updateBomTotalPrice(goods_code, price):
    print(goods_code, price)
    db = MySQLdb.connect("127.0.0.1", "bsztz", "bsztz", "tmall", charset="utf8")
    detail = db.cursor(MySQLdb.cursors.DictCursor)

    value = [str(price), goods_code]
    detail.execute("update bom set price=%s where product_name=%s", value)
    db.commit()
    detail.close()
    db.close()


def getPriceBySku(goods_id):
    db = MySQLdb.connect("127.0.0.1", "bsztz", "bsztz", "tmall", charset="utf8")
    detail = db.cursor(MySQLdb.cursors.DictCursor)
    value = [goods_id]
    detail.execute("select price from t_bas_sku_price where sku_id =%s", value)
    if detail.rowcount == 0:
        return "0"
    else:
        row = detail.fetchone()
        return row["price"]


def getPriceList():
    db = MySQLdb.connect("127.0.0.1", "bsztz", "bsztz", "tmall", charset="utf8")
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


if __name__ == "__main__":
    db = MySQLdb.connect("127.0.0.1", "bsztz", "bsztz", "tmall", charset="utf8")
    bom = db.cursor(MySQLdb.cursors.DictCursor)

    try:
        bom.execute("select * from bom")
        bom_data = bom.fetchall()
        priceList, fields = getPriceList()
        print(priceList, fields)
        bomGoodsNum = []
        bomProductLst = []
        for row in bom_data:
            row_goods_num = []
            bomProductLst.append(row["product_name"])
        for i in range(0, len(fields)):
            goods_num = row[fields[i]]

            if goods_num != "" and goods_num is not None:
                row_goods_num.append(int(goods_num))
            else:
                row_goods_num.append(0)
        print(row_goods_num)

        bomGoodsNum.append(row_goods_num)

        bomPrice = np.dot(bomGoodsNum, priceList)

        print(priceList, bomPrice)
        for i in range(len(bomProductLst)):
            updateBomTotalPrice(bomProductLst[i], bomPrice[i])

    except Exception as e:
        print("error: unable fetch data", e.args)
        raise

    db.close()
    print("search complete")
