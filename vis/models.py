# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class LoadFeeInfo(models.Model):
    payment_time = models.DateTimeField(db_column='Payment_time', blank=True, null=True)  # Field name made lowercase.
    transaction_id = models.CharField(db_column='Transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    partner_transaction_id = models.CharField(db_column='Partner_transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foreign_amount = models.DecimalField(db_column='Foreign_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10, blank=True, null=True)  # Field name made lowercase.
    exchange_rate = models.DecimalField(db_column='Exchange_Rate', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fee_type = models.CharField(db_column='Fee_type', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fee_amount = models.DecimalField(db_column='Fee_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foreign_fee_amount = models.DecimalField(db_column='Foreign_fee_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee_desc = models.CharField(db_column='Fee_desc', max_length=200, blank=True, null=True)  # Field name made lowercase.
    load_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_fee_info'


class LoadInventoryInfo(models.Model):
    period = models.CharField(max_length=10)
    goods_id = models.CharField(max_length=80)
    goods_code = models.CharField(max_length=80)
    goods_name = models.CharField(max_length=80)
    inventory_name = models.CharField(max_length=80)
    init_total = models.IntegerField()
    init_goods = models.IntegerField()
    init_bad = models.IntegerField()
    in_total = models.IntegerField()
    in_good = models.IntegerField()
    in_bad = models.IntegerField()
    check_good = models.IntegerField()
    check_bad = models.IntegerField()
    out_total = models.IntegerField()
    out_sales = models.IntegerField()
    out_other = models.IntegerField()
    out_bac = models.IntegerField()
    check_good_need = models.IntegerField()
    check_bac_need = models.IntegerField()
    final_total = models.IntegerField()
    final_goods = models.IntegerField()
    final_bad = models.IntegerField()
    purchase_onway = models.IntegerField()
    change_onway = models.IntegerField()
    back_changeber = models.IntegerField()
    bill_out_total = models.IntegerField()
    bill_out_good = models.IntegerField()
    bill_out_bad = models.IntegerField()
    adjust_out_total = models.IntegerField()
    adjust_out_good = models.IntegerField()
    adjust_out_bac = models.IntegerField()
    bill_in_total = models.IntegerField()
    adjust_in_good = models.IntegerField()
    bill_in_bad = models.IntegerField()
    adjust_in_total = models.IntegerField()
    adjust_in_good1 = models.IntegerField()
    adjust_in_bad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'load_inventory_info'


class LoadMyaccountInfo(models.Model):
    order_no = models.CharField(db_column='Order_No', max_length=200, blank=True, null=True)  # Field name made lowercase.
    partner_transaction_id = models.CharField(db_column='Partner_Transaction_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transaction_id = models.CharField(db_column='Transaction_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    balance = models.DecimalField(db_column='Balance', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    trans_date = models.DateTimeField(db_column='Trans_Date', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'load_myaccount_info'


class LoadOrderInfo(models.Model):
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    warehouse_name = models.CharField(max_length=50, blank=True, null=True)
    order_time = models.CharField(max_length=50, blank=True, null=True)
    pay_time = models.CharField(max_length=50, blank=True, null=True)
    dispatch_time = models.CharField(max_length=50, blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True)
    logistic_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    warehouse_id = models.CharField(max_length=50, blank=True, null=True)
    dispatch_company = models.CharField(max_length=50, blank=True, null=True)
    dispatch_no = models.CharField(max_length=50, blank=True, null=True)
    buyer_nickname = models.CharField(max_length=50, blank=True, null=True)
    receiver_name = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    order_amount = models.CharField(max_length=50, blank=True, null=True)
    freight = models.CharField(max_length=50, blank=True, null=True)
    goods_amount = models.CharField(max_length=50, blank=True, null=True)
    cargo_id = models.CharField(max_length=50, blank=True, null=True)
    cargo_code = models.CharField(max_length=50, blank=True, null=True)
    goods_id = models.CharField(max_length=50, blank=True, null=True)
    goods_code = models.CharField(max_length=50, blank=True, null=True)
    goods_name = models.CharField(max_length=200, blank=True, null=True)
    tax = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_order_info'
        unique_together = (('id', 'logistic_id', 'order_id'),)


class LoadSettlebatchInfo(models.Model):
    settle_batch_no = models.CharField(db_column='Settle_batch_no', max_length=50, blank=True, null=True)  # Field name made lowercase.
    settle_date = models.DateTimeField(db_column='Settle_date', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee = models.DecimalField(db_column='Fee', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    settlement = models.DecimalField(db_column='Settlement', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'load_settlebatch_info'


class LoadSettledetailsInfo(models.Model):
    partner_transaction_id = models.CharField(db_column='Partner_transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmb_amount = models.DecimalField(db_column='Rmb_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee = models.DecimalField(db_column='Fee', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    settlement = models.DecimalField(db_column='Settlement', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmb_settlement = models.DecimalField(db_column='Rmb_settlement', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    payment_time = models.DateTimeField(db_column='Payment_time', blank=True, null=True)  # Field name made lowercase.
    settlement_time = models.DateTimeField(db_column='Settlement_time', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=3, blank=True, null=True)  # Field name made lowercase.
    statu = models.CharField(db_column='Statu', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stem_from = models.CharField(db_column='Stem_from', max_length=3, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=200, blank=True, null=True)  # Field name made lowercase.
    settle_batch_no = models.CharField(db_column='Settle_batch_no', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'load_settledetails_info'


class LoadSettlefeeInfo(models.Model):
    payment_time = models.CharField(db_column='Payment_time', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transaction_id = models.CharField(db_column='Transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    partner_transaction_id = models.CharField(db_column='Partner_transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gross_amount = models.DecimalField(db_column='Gross_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmb_gross_amount = models.DecimalField(db_column='Rmb_gross_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee_type = models.CharField(db_column='Fee_type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fee_amount = models.DecimalField(db_column='Fee_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee_rmb_amount = models.DecimalField(db_column='Fee_rmb_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200, blank=True, null=True)  # Field name made lowercase.
    settle_time = models.CharField(db_column='Settle_time', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'load_settlefee_info'


class LoadStradeInfo(models.Model):
    partner_transaction_id = models.CharField(db_column='Partner_transaction_id', max_length=100, blank=True, null=True)  # Field name made lowercase.
    transaction_id = models.CharField(db_column='Transaction_id', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmb_amount = models.DecimalField(db_column='Rmb_amount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fee = models.DecimalField(db_column='Fee', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    refund = models.DecimalField(db_column='Refund', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    settlement = models.DecimalField(db_column='Settlement', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmb_settlement = models.DecimalField(db_column='Rmb_settlement', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    payment_time = models.DateTimeField(db_column='Payment_time', blank=True, null=True)  # Field name made lowercase.
    settlement_time = models.CharField(db_column='Settlement_time', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'load_strade_info'


class LoadTmallsoInfo(models.Model):
    order_id = models.CharField(max_length=50)
    buyer_name = models.CharField(max_length=50)
    buyer_account = models.CharField(max_length=50)
    buyer_needpay = models.CharField(max_length=50)
    buyer_post_fee = models.DecimalField(max_digits=18, decimal_places=2)
    buery_point = models.DecimalField(max_digits=18, decimal_places=2)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    return_point = models.DecimalField(max_digits=18, decimal_places=2)
    actual_paid = models.DecimalField(max_digits=18, decimal_places=2)
    actual_point = models.DecimalField(max_digits=18, decimal_places=2)
    order_status = models.CharField(max_length=20)
    buyer_msg = models.CharField(max_length=200)
    reciever_name = models.CharField(max_length=50)
    recieve_address = models.CharField(max_length=50)
    deliver_type = models.CharField(max_length=50)
    telphone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    create_time = models.CharField(max_length=50)
    paid_time = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    logistic_id = models.CharField(max_length=50)
    logisitise = models.CharField(max_length=50)
    order_memo = models.CharField(max_length=50)
    order_counts = models.CharField(max_length=50)
    shop_id = models.CharField(max_length=50)
    shop_name = models.CharField(max_length=50)
    close_reason = models.CharField(max_length=50)
    sales_service_fee = models.DecimalField(max_digits=18, decimal_places=2)
    buyer_service_fee = models.DecimalField(max_digits=18, decimal_places=2)
    invoice_title = models.CharField(max_length=50)
    is_mobile_order = models.CharField(max_length=50)
    order_msg = models.CharField(max_length=50)
    priliage_order_id = models.CharField(max_length=50)
    is_contract_photo = models.CharField(max_length=50)
    is_tick = models.CharField(max_length=50)
    is_dai = models.CharField(max_length=50)
    earnest_range = models.CharField(max_length=50)
    changed_sku = models.CharField(max_length=50)
    changed_address = models.CharField(max_length=200)
    unnormal_msg = models.CharField(max_length=200)
    tmall_coupon = models.CharField(max_length=20)
    jufengbao_coupon = models.CharField(max_length=20)
    is_o2o = models.CharField(max_length=20)
    is_idcard = models.CharField(max_length=20)
    refund = models.DecimalField(max_digits=18, decimal_places=2)
    shop = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_tmallso_info'
        unique_together = (('id', 'order_id'),)


class LoadTmallsodetailInfo(models.Model):
    order_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    number = models.IntegerField()
    reff_id = models.CharField(max_length=20)
    product_attr = models.CharField(max_length=20)
    suit_info = models.CharField(max_length=20)
    memo = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    shop_code = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'load_tmallsodetail_info'
        unique_together = (('id', 'order_id'),)


class LoadTransactionInfo(models.Model):
    order_id = models.CharField(max_length=50)
    goods_code = models.CharField(max_length=50)
    goods_name = models.CharField(max_length=200)
    inventory_name = models.CharField(max_length=200)
    in_out_time = models.CharField(max_length=20)
    paper_type = models.CharField(max_length=200)
    inventory_type = models.CharField(max_length=200)
    in_out_number = models.IntegerField()
    deposit_number = models.IntegerField()
    erp_order_id = models.CharField(max_length=50)
    outter_order_id = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'load_transaction_info'
        unique_together = (('id', 'order_id'),)


class TBasAreaInfo(models.Model):
    area_code = models.CharField(max_length=1, blank=True, null=True)
    area_name = models.CharField(max_length=60, blank=True, null=True)
    province = models.CharField(max_length=60, blank=True, null=True)
    other_info = models.CharField(max_length=224, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_bas_area_info'


class TBasSkuPrice(models.Model):
    sku_id = models.CharField(max_length=80, blank=True, null=True)
    sku_name = models.CharField(max_length=80, blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_bas_sku_price'


class TBuyerInfo(models.Model):
    buyer_name = models.CharField(max_length=80, blank=True, null=True)
    buyer_account = models.CharField(max_length=120, blank=True, null=True)
    is_mobile_order = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_buyer_info'


class TFeeInfo(models.Model):
    order_id = models.CharField(max_length=50)
    fee_time = models.CharField(max_length=20)
    payment_time = models.CharField(max_length=20)
    logisitic_tax = models.DecimalField(max_digits=18, decimal_places=2)
    logisitic_service = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_service = models.DecimalField(max_digits=18, decimal_places=2)
    tmall = models.DecimalField(max_digits=18, decimal_places=2)
    juhuasuan = models.DecimalField(max_digits=18, decimal_places=2)
    order_fee = models.DecimalField(max_digits=18, decimal_places=2)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2)
    logisitic_tax_usd = models.DecimalField(max_digits=18, decimal_places=2)
    logisitic_service_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_service_usd = models.DecimalField(max_digits=18, decimal_places=2)
    tmall_usd = models.DecimalField(max_digits=18, decimal_places=2)
    juhuasuan_usd = models.DecimalField(max_digits=18, decimal_places=2)
    order_fee_usd = models.DecimalField(max_digits=18, decimal_places=2)
    account_fee_usd = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_fee_info'


class TFeeMonthlyInfo(models.Model):
    fee_time = models.CharField(max_length=20, blank=True, null=True)
    logisitic_tax = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    logisitic_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tmall = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_fee_monthly_info'


class TFeetypeInfo(models.Model):
    fee_name = models.CharField(max_length=60, blank=True, null=True)
    fee_desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_feetype_info'


class TGoodsNumInfo(models.Model):
    period = models.CharField(max_length=10)
    goods_id = models.CharField(max_length=30)
    goods_name = models.CharField(max_length=200)
    sale_num = models.IntegerField()
    order_deal_num = models.DecimalField(max_digits=18, decimal_places=2)
    order_close_num = models.DecimalField(max_digits=18, decimal_places=2)
    order_other_num = models.DecimalField(max_digits=18, decimal_places=2)
    sale_out_number = models.IntegerField()
    opening_inventory = models.IntegerField()
    ending_inventory = models.IntegerField()
    diff_inventory = models.IntegerField()
    in_out_num = models.IntegerField()
    trade_out = models.IntegerField()
    other_out = models.IntegerField()
    purchase_in = models.IntegerField()
    other_in = models.IntegerField()
    sale_amount = models.DecimalField(max_digits=18, decimal_places=2)
    sale_out_amount = models.DecimalField(max_digits=18, decimal_places=2)
    trans_amount = models.DecimalField(max_digits=18, decimal_places=2)
    order_deal_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_goods_num_info'


class TGroupFeeInfo(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)
    fee_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    fee_amount_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_group_fee_info'


class TGroupMyaccountInfo(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_group_myaccount_info'


class TGroupSettledetailsInfo(models.Model):
    order_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_group_settledetails_info'


class TGroupStradeInfo(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=True)
    alipay_actual_recieve = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    refund = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipy_strade_p = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipy_strade_r = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_actual_recieve_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    refund_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_strade_p_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_strade_r_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_group_strade_info'


class TMemberAlanlyseInfo(models.Model):
    period = models.CharField(max_length=10)
    total_count = models.IntegerField()
    new_count = models.IntegerField()
    old_count = models.IntegerField()
    new_orders = models.IntegerField()
    old_orders = models.IntegerField()
    no_account_orders = models.IntegerField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    no_account_amount = models.DecimalField(max_digits=18, decimal_places=2)
    new_orders_amount = models.DecimalField(max_digits=18, decimal_places=2)
    old_orders_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_member_alanlyse_info'


class TMonthlyOrderAmount(models.Model):
    fin_period = models.CharField(max_length=20, blank=True, null=True)
    actual_paid = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_actual_recieve = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    refund = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_get = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_monthly_order_amount'


class TMyaccountMonthlyInfo(models.Model):
    period = models.CharField(max_length=10)
    recharge = models.DecimalField(max_digits=18, decimal_places=2)
    refund = models.DecimalField(max_digits=18, decimal_places=2)
    payment = models.DecimalField(max_digits=18, decimal_places=2)
    order_payment = models.DecimalField(max_digits=18, decimal_places=2)
    not_order_payment = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_myaccount_monthly_info'


class TOrderAmount(models.Model):
    order_id = models.CharField(max_length=50)
    fin_period = models.CharField(max_length=20)
    actual_paid = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_actual_recieve = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_strade_p = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_strade_r = models.DecimalField(max_digits=18, decimal_places=2)
    refund = models.DecimalField(max_digits=18, decimal_places=2)
    order_fee = models.DecimalField(max_digits=18, decimal_places=2)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_get = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_strade_p_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_strade_r_usd = models.DecimalField(max_digits=18, decimal_places=2)
    refund_usd = models.DecimalField(max_digits=18, decimal_places=2)
    order_fee_usd = models.DecimalField(max_digits=18, decimal_places=2)
    account_fee_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_get_usd = models.DecimalField(max_digits=18, decimal_places=2)
    tmall_refund = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_order_amount'


class TOrderAnalyse(models.Model):
    fin_period = models.CharField(max_length=20)
    area_info = models.CharField(max_length=255)
    order_num = models.CharField(max_length=18)
    saled_num = models.CharField(max_length=18)
    closed_num = models.CharField(max_length=18)
    waiting_num = models.CharField(max_length=18)
    close_unpaid_num = models.CharField(max_length=18)
    close_return_num = models.CharField(max_length=18)
    order_amount = models.CharField(max_length=18)
    saled_amount = models.CharField(max_length=18)
    closed_amount = models.CharField(max_length=18)
    waiting_amount = models.CharField(max_length=18)
    close_unpaid_amount = models.CharField(max_length=18)
    close_return_amount = models.CharField(max_length=18)

    class Meta:
        managed = False
        db_table = 't_order_analyse'


class TOrderArea(models.Model):
    fin_period = models.CharField(max_length=20)
    area_info = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    order_number = models.DecimalField(max_digits=18, decimal_places=2)
    order_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_order_area'


class TPeriodNumInfo(models.Model):
    goods_id = models.CharField(max_length=80, blank=True, null=True)
    goods_name = models.CharField(max_length=200, blank=True, null=True)
    fee_order = models.CharField(max_length=2, blank=True, null=True)
    fee_type = models.CharField(max_length=200, blank=True, null=True)
    p201509 = models.DecimalField(db_column='P201509', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201510 = models.DecimalField(db_column='P201510', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201511 = models.DecimalField(db_column='P201511', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201512 = models.DecimalField(db_column='P201512', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201601 = models.DecimalField(db_column='P201601', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201602 = models.DecimalField(db_column='P201602', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201603 = models.DecimalField(db_column='P201603', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201604 = models.DecimalField(db_column='P201604', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201605 = models.DecimalField(db_column='P201605', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201606 = models.DecimalField(db_column='P201606', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201607 = models.DecimalField(db_column='P201607', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201608 = models.DecimalField(db_column='P201608', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201609 = models.DecimalField(db_column='P201609', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201610 = models.DecimalField(db_column='P201610', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201611 = models.DecimalField(db_column='P201611', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201612 = models.DecimalField(db_column='P201612', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201701 = models.DecimalField(db_column='P201701', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201702 = models.DecimalField(db_column='P201702', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201703 = models.DecimalField(db_column='P201703', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201704 = models.DecimalField(db_column='P201704', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201705 = models.DecimalField(db_column='P201705', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    p201706 = models.DecimalField(db_column='P201706', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_period_num_info'


class TRecieverInfo(models.Model):
    buyer_account = models.CharField(max_length=120, blank=True, null=True)
    reciever_name = models.CharField(max_length=255, blank=True, null=True)
    recieve_address = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=80, blank=True, null=True)
    create_date = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_reciever_info'


class TSettleAmountInfo(models.Model):
    period = models.CharField(max_length=10)
    alipay_settle = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_settle_p = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_settle_r = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_settle_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_settle_p_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_settle_r_usd = models.DecimalField(max_digits=18, decimal_places=2)
    alipay_fee_usd = models.DecimalField(max_digits=18, decimal_places=2)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 't_settle_amount_info'


class TSettlefeeMonthlyInfo(models.Model):
    fee_time = models.CharField(max_length=20, blank=True, null=True)
    logisitic_tax = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    logisitic_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tmall = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    logisitic_tax_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    logisitic_service_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_service_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tmall_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan_usd = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    account_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_settlefee_monthly_info'


class TTmallBomDetail(models.Model):
    period = models.CharField(max_length=10, blank=True, null=True)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    goods_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    order_status = models.CharField(max_length=40, blank=True, null=True)
    deal_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tmall_bom_detail'


class TTmallGroupBomDetail(models.Model):
    period = models.CharField(max_length=7, blank=True, null=True)
    goods_code = models.CharField(max_length=60, blank=True, null=True)
    order_id = models.CharField(max_length=60, blank=True, null=True)
    in_out_number = models.IntegerField(blank=True, null=True)
    deal_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tmall_group_bom_detail'


class TTransactionGroupInfo(models.Model):
    goods_code = models.CharField(max_length=60, blank=True, null=True)
    order_id = models.CharField(max_length=60, blank=True, null=True)
    in_out_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_transaction_group_info'
