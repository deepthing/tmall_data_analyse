-- sheet1订单分析 -- 状态分析SELECT SUM(order_num) 总数量,
         SUM(saled_num) 成功数量,
         SUM(closed_num) 关闭数量,
         SUM(waiting_num) 其他数量,
         SUM(close_unpaid_num) 未付款关闭,
         SUM(close_return_num) 退款关闭,
         SUM(order_amount) 总金额,
         SUM(saled_amount) 成功金额,
         SUM(closed_amount) 关闭金额,
         SUM(waiting_amount) 其他金额,
         SUM(close_unpaid_amount) 未付款关闭金额,
         SUM(close_return_amount) 退款关闭金额
FROM t_order_analyse
WHERE fin_period LIKE '2017-05%' ; -- 会员分析SELECT period,
         total_count 总数,
         new_count 新账号数,
         old_count 老账号数,
         no_account_orders 无账号订单数,
         new_orders 新账号订单数,
         old_orders 老账号订单数,
         total_amount 总金额,
         no_account_amount 无账号订单金额,
         new_orders_amount 新账号订单金额,
         old_orders_amount 老账号订单金额
FROM t_member_alanlyse_info
ORDER BY  period; -- 区域分析SELECT area_info 区域,
         SUM(order_number) 数量,
         SUM(order_amount) 金额
FROM t_order_area
WHERE 1=1
        AND fin_period LIKE '2017-06%'
GROUP BY  area_info; -- sheet2金额分析 -- 金额 （提取时间）SELECT SUM(alipay_settle),
         SUM(alipay_settle_p+alipay_settle_r),
         -- SUM(alipay_settle_r),
         SUM(account_fee*-1),
         SUM(alipay_settle_usd),
         SUM(alipay_settle_p_usd+alipay_settle_r_usd),
         -- SUM(alipay_settle_r_usd),
         SUM(alipay_fee_usd*-1)
FROM t_settle_amount_info
WHERE 1=1
        AND t_settle_amount_info.period LIKE '2017-06%' ; -- 提取时间维度的费用SELECT SUM(logisitic_tax),
         SUM(logisitic_service),
         SUM(alipay_service),
         SUM(tmall),
         SUM(juhuasuan),
         SUM(logisitic_tax_usd),
         SUM(logisitic_service_usd),
         SUM(alipay_service_usd),
         SUM(tmall_usd),
         SUM(juhuasuan_usd)
FROM t_settle_fee_info
WHERE 1=1
        AND t_settle_fee_info.fee_time LIKE '201706%' ; -- 订单金额分析（订单生成时间）SELECT SUM(tmall_refund+actual_paid),
         SUM(tmall_refund),
         SUM(actual_paid),
         SUM(order_fee*-1),
         SUM(alipay_get*-1) -- SUM(account_fee)
FROM t_order_amount
WHERE fin_period LIKE '2017-06%' ; -- -- 单个订单查错误 --SELECT -- order_id,
         -- actual_paid,
         -- order_fee*-1,
         -- alipay_get*-1 --
FROM t_order_amount --
WHERE fin_period LIKE '2016-07%' ; -- -- 订单费用明细（订单生成时间）SELECT SUM(t.logisitic_tax),
         SUM(t.logisitic_service),
         SUM(t.alipay_service),
         SUM(t.tmall),
         SUM(t.juhuasuan)
FROM t_fee_info t
WHERE payment_time LIKE '2017-06%' ; -- -- 月度金额分析 --SELECT SUBSTR(fin_period
FROM 1 FOR 7),sum(actual_paid),sum(alipay_actual_recieve), -- sum(refund*-1),sum(order_fee*-1),sum(alipay_get*-1), sum(account_fee) --
FROM t_monthly_order_amount
WHERE SUBSTR(fin_period
FROM 1 FOR 7) = '2017-02' --
GROUP BY  SUBSTR(fin_period
FROM 1 FOR 7); -- -- -- 月度费用明细 --SELECT sum(logisitic_tax),
         sum(logisitic_service),
         sum(alipay_service),
         sum(tmall),
         sum(juhuasuan) --
FROM t_fee_monthly_info
WHERE fee_time LIKE '2017-01%'; -- -- -- 账户维度SELECT SUM(recharge),
         SUM(refund),
         SUM(payment),
         SUM(order_payment),
         SUM(not_order_payment)
FROM t_myaccount_monthly_info
WHERE 1=1
        AND t_myaccount_monthly_info.period LIKE '2017-06%' ; -- sheet3库存数量分析 -- 库存数量SELECT goods_id,
         goods_name,
         sum(sale_num) 销售数量,
         sum(sale_out_number*-1) 出库数量,
         sum(order_deal_num) 交易成功数量,
         sum(sale_amount) 销售金额,
         sum(sale_out_amount) 出库金额,
         sum(order_deal_amount) 交易成功金额,
         sum(opening_inventory) 期初,
         sum(purchase_in) 采购入库,
         sum(other_in) 其他入库,
         sum(trade_out) 交易出库,
         sum(other_out) 其他出库,
         sum(ending_inventory) 期末,
         sum(diff_inventory) 期末减期初,
         sum(in_out_num) 流水,
         sum(trans_amount) 期间交易出库金额
FROM t_goods_num_info
WHERE 1=1
        AND period ='2017-06'
GROUP BY  period,goods_id,goods_name
ORDER BY  goods_id; -- -- 库存数量总计，不包括椰枣 --SELECT period,
         -- sum(sale_num) 销售数量,
         -- sum(sale_out_number*-1) 出库数量,
         -- sum(order_deal_num) 交易成功数量,
         -- sum(opening_inventory) 期初,
         -- sum(purchase_in) 采购入库,
         -- sum(other_in) 其他入库,
         -- sum(trade_out) 交易出库,
         -- sum(other_out) 其他出库,
         -- sum(ending_inventory) 期末,
         -- sum(diff_inventory) 期末减期初,
         -- sum(in_out_num) 流水 --
FROM t_goods_num_info
WHERE 1=1 --
        AND period ='2017-01' --
GROUP BY  period --
ORDER BY  goods_id; -- 总表SELECT *
FROM t_period_num_info pn
WHERE 1=1 --
        AND pn.goods_id='XY521067771349'
ORDER BY  pn.goods_id,
         pn.fee_order ; -- 总表总计，不算椰果SELECT fee_order,
         fee_type,
         SUM(P201509),
         SUM(P201510),
         SUM(P201511),
         SUM(P201512),
         SUM(P201601),
         SUM(P201602),
         SUM(P201603),
         SUM(P201604),
         SUM(P201605),
         SUM(P201606),
         SUM(P201607),
         SUM(P201608),
         SUM(P201609),
         SUM(P201610),
         SUM(P201611),
         SUM(P201612),
         SUM(P201701),
         SUM(P201702),
         SUM(P201703),
         SUM(P201704),
         SUM(P201705),
         SUM(P201706)
FROM t_period_num_info
WHERE 1=1
        AND goods_id <>'7290108800098' --
        AND pn.goods_id='XY521067771349'
GROUP BY  fee_order ; 