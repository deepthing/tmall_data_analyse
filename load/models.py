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

