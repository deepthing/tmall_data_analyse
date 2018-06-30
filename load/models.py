# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models


class Bom(models.Model):
    num = models.AutoField(
        db_column="Num", primary_key=True
    )  # Field name made lowercase.
    product_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    xy521077050523 = models.CharField(
        db_column="XY521077050523", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521077162825 = models.CharField(
        db_column="XY521077162825", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521078232623 = models.CharField(
        db_column="XY521078232623", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521067771349 = models.CharField(
        db_column="XY521067771349", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521073901132 = models.CharField(
        db_column="XY521073901132", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521078064529 = models.CharField(
        db_column="XY521078064529", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521074093868 = models.CharField(
        db_column="XY521074093868", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521078390258 = models.CharField(
        db_column="XY521078390258", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521077912497 = models.CharField(
        db_column="XY521077912497", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521074249153 = models.CharField(
        db_column="XY521074249153", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521074725008 = models.CharField(
        db_column="XY521074725008", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    xy521068155265 = models.CharField(
        db_column="XY521068155265", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    number_708390000203 = models.CharField(
        db_column="708390000203", max_length=255, blank=True, null=True
    )  # Field renamed because it wasn't a valid Python identifier.
    number_708390000210 = models.CharField(
        db_column="708390000210", max_length=255, blank=True, null=True
    )  # Field renamed because it wasn't a valid Python identifier.
    number_708390000227 = models.CharField(
        db_column="708390000227", max_length=255, blank=True, null=True
    )  # Field renamed because it wasn't a valid Python identifier.
    number_7290108800098 = models.CharField(
        db_column="7290108800098", max_length=255, blank=True, null=True
    )  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = "BOM"


class Item(models.Model):
    num = models.CharField(
        db_column="Num", primary_key=True, max_length=255
    )  # Field name made lowercase.
    field_field = models.CharField(
        db_column="\u8d27\u54c1\u7f16\u7801", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_field_0 = models.CharField(
        db_column="\u8d27\u54c1\u540d\u79f0", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_id = models.CharField(
        db_column="\u8d27\u54c1id", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_field_1 = models.CharField(
        db_column="\u54c1\u7c7b\u540d\u79f0", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_2 = models.CharField(
        db_column="\u54c1\u724c\u540d\u79f0", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_3 = models.CharField(
        db_column="\u4ea7\u54c1\u7f16\u7801", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_4 = models.CharField(
        db_column="\u6761\u5f62\u7801", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_5 = models.CharField(
        db_column="\u8d27\u54c1\u7c7b\u578b", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_6 = models.CharField(
        db_column="\u540a\u724c\u4ef7", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_7 = models.CharField(
        db_column="\u96f6\u552e\u4ef7", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_8 = models.CharField(
        db_column="\u6210\u672c\u4ef7", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_9 = models.CharField(
        db_column="\u533a\u57df\u9500\u552e", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_10 = models.CharField(
        db_column="\u6613\u788e\u54c1", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_11 = models.CharField(
        db_column="\u5371\u9669\u54c1", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_12 = models.CharField(
        db_column="\u6548\u671f\u7ba1\u7406", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_13 = models.CharField(
        db_column="\u6709\u6548\u671f\uff08\u5929\uff09",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_14 = models.CharField(
        db_column="\u4e34\u671f\u9884\u8b66\uff08\u5929\uff09",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_15 = models.CharField(
        db_column="\u7981\u552e\u5929\u6570\uff08\u5929\uff09",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_16 = models.CharField(
        db_column="\u7981\u6536\u5929\u6570\uff08\u5929\uff09",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_cm3_field = models.CharField(
        db_column="\u4f53\u79ef\uff08cm3\uff09", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_field_17 = models.CharField(
        db_column="\u957f", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_18 = models.CharField(
        db_column="\u5bbd", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_19 = models.CharField(
        db_column="\u9ad8", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_20 = models.CharField(
        db_column="\u91cd\u91cf", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_21 = models.CharField(
        db_column="\u6bdb\u91cd", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_22 = models.CharField(
        db_column="\u51c0\u91cd", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_23 = models.CharField(
        db_column="\u76ae\u91cd", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_24 = models.CharField(
        db_column="\u7bb1\u88c5\u6570", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_25 = models.CharField(
        db_column="\u4f53\u79ef-\u8fd0\u8f93\u5355\u5143",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_26 = models.CharField(
        db_column="\u957f-\u8fd0\u8f93\u5355\u5143",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_27 = models.CharField(
        db_column="\u5bbd-\u8fd0\u8f93\u5355\u5143",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_28 = models.CharField(
        db_column="\u9ad8-\u8fd0\u8f93\u5355\u5143",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_29 = models.CharField(
        db_column="\u91cd\u91cf-\u8fd0\u8f93\u5355\u5143",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_30 = models.CharField(
        db_column="\u7a0e\u7387", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_31 = models.CharField(
        db_column="\u7a0e\u7387\u5206\u7c7b\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_32 = models.CharField(
        db_column="\u5305\u542b\u7535\u6c60", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_33 = models.CharField(
        db_column="\u751f\u4ea7\u6279\u53f7\u7ba1\u7406",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_field_34 = models.CharField(
        db_column="\u5305\u88c5\u65b9\u5f0f", max_length=255, blank=True, null=True
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_1_field = models.CharField(
        db_column="\u5b50\u8d27\u54c11\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_1_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c11\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_2_field = models.CharField(
        db_column="\u5b50\u8d27\u54c12\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_2_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c12\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_3_field = models.CharField(
        db_column="\u5b50\u8d27\u54c13\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_3_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c13\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_4_field = models.CharField(
        db_column="\u5b50\u8d27\u54c14\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_4_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c14\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_5_field = models.CharField(
        db_column="\u5b50\u8d27\u54c15\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_5_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c15\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_6_field = models.CharField(
        db_column="\u5b50\u8d27\u54c16\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_6_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c16\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_7_field = models.CharField(
        db_column="\u5b50\u8d27\u54c17\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_7_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c17\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_8_field = models.CharField(
        db_column="\u5b50\u8d27\u54c18\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_8_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c18\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_9_field = models.CharField(
        db_column="\u5b50\u8d27\u54c19\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_9_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c19\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_10_field = models.CharField(
        db_column="\u5b50\u8d27\u54c110\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_10_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c110\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_11_field = models.CharField(
        db_column="\u5b50\u8d27\u54c111\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_11_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c111\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_12_field = models.CharField(
        db_column="\u5b50\u8d27\u54c112\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_12_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c112\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_13_field = models.CharField(
        db_column="\u5b50\u8d27\u54c113\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_13_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c113\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_14_field = models.CharField(
        db_column="\u5b50\u8d27\u54c114\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_14_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c114\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_15_field = models.CharField(
        db_column="\u5b50\u8d27\u54c115\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_15_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c115\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_16_field = models.CharField(
        db_column="\u5b50\u8d27\u54c116\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_16_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c116\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_17_field = models.CharField(
        db_column="\u5b50\u8d27\u54c117\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_17_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c117\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_18_field = models.CharField(
        db_column="\u5b50\u8d27\u54c118\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_18_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c118\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_19_field = models.CharField(
        db_column="\u5b50\u8d27\u54c119\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_19_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c119\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    field_20_field = models.CharField(
        db_column="\u5b50\u8d27\u54c120\u7f16\u7801",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    field_20_field_0 = models.CharField(
        db_column="\u5b50\u8d27\u54c120\u6570\u91cf",
        max_length=255,
        blank=True,
        null=True,
    )  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = "ITEM"


class BomDetail(models.Model):
    product_name = models.CharField(max_length=255, blank=True, null=True)
    goods_id = models.CharField(max_length=255, blank=True, null=True)
    goods_name = models.CharField(max_length=255, blank=True, null=True)
    goods_count = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "bom_detail"


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class LoadFeeInfo(models.Model):
    fee_date = models.CharField(
        db_column="Fee_date", max_length=20, blank=True, null=True
    )  # Field name made lowercase.
    payment_time = models.DateTimeField(
        db_column="Payment_time", blank=True, null=True
    )  # Field name made lowercase.
    transaction_id = models.CharField(
        db_column="Transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    partner_transaction_id = models.CharField(
        db_column="Partner_transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    foreign_amount = models.DecimalField(
        db_column="Foreign_amount",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    exchange_rate = models.DecimalField(
        db_column="Exchange_Rate",
        max_digits=18,
        decimal_places=8,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    fee_type = models.CharField(
        db_column="Fee_type", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    fee_amount = models.DecimalField(
        db_column="Fee_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    foreign_fee_amount = models.DecimalField(
        db_column="Foreign_fee_amount",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    fee_desc = models.CharField(
        db_column="Fee_desc", max_length=200, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_fee_info"


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
        db_table = "load_inventory_info"


class LoadMyaccountInfo(models.Model):
    order_no = models.CharField(
        db_column="Order_No", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    partner_transaction_id = models.CharField(
        db_column="Partner_Transaction_ID", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    transaction_id = models.CharField(
        db_column="Transaction_ID", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    type = models.CharField(
        db_column="Type", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    balance = models.DecimalField(
        db_column="Balance", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    trans_date = models.DateTimeField(
        db_column="Trans_Date", blank=True, null=True
    )  # Field name made lowercase.
    remarks = models.CharField(
        db_column="Remarks", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    alipay_order = models.CharField(
        db_column="Alipay_Order", max_length=200, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_myaccount_info"


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
        db_table = "load_order_info"
        unique_together = (("id", "logistic_id", "order_id"),)


class LoadSettlebatchInfo(models.Model):
    settle_batch_no = models.CharField(
        db_column="Settle_batch_no", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    settle_date = models.DateTimeField(
        db_column="Settle_date", blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    fee = models.DecimalField(
        db_column="Fee", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    settlement = models.DecimalField(
        db_column="Settlement", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_settlebatch_info"


class LoadSettledetailsInfo(models.Model):
    partner_transaction_id = models.CharField(
        db_column="Partner_transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_amount = models.DecimalField(
        db_column="Rmb_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    fee = models.DecimalField(
        db_column="Fee", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    settlement = models.DecimalField(
        db_column="Settlement", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_settlement = models.DecimalField(
        db_column="Rmb_settlement",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    rate = models.DecimalField(
        db_column="Rate", max_digits=18, decimal_places=8, blank=True, null=True
    )  # Field name made lowercase.
    payment_time = models.DateTimeField(
        db_column="Payment_time", blank=True, null=True
    )  # Field name made lowercase.
    settlement_time = models.DateTimeField(
        db_column="Settlement_time", blank=True, null=True
    )  # Field name made lowercase.
    type = models.CharField(
        db_column="Type", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    statu = models.CharField(
        db_column="Statu", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    stem_from = models.CharField(
        db_column="Stem_from", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    remarks = models.CharField(
        db_column="Remarks", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    settle_batch_no = models.CharField(
        db_column="Settle_batch_no", max_length=50, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_settledetails_info"


class LoadSettledetailsInfoCopy(models.Model):
    partner_transaction_id = models.CharField(
        db_column="Partner_transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_amount = models.DecimalField(
        db_column="Rmb_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    fee = models.DecimalField(
        db_column="Fee", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    settlement = models.DecimalField(
        db_column="Settlement", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_settlement = models.DecimalField(
        db_column="Rmb_settlement",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    rate = models.DecimalField(
        db_column="Rate", max_digits=18, decimal_places=8, blank=True, null=True
    )  # Field name made lowercase.
    payment_time = models.DateTimeField(
        db_column="Payment_time", blank=True, null=True
    )  # Field name made lowercase.
    settlement_time = models.DateTimeField(
        db_column="Settlement_time", blank=True, null=True
    )  # Field name made lowercase.
    type = models.CharField(
        db_column="Type", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    statu = models.CharField(
        db_column="Statu", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    stem_from = models.CharField(
        db_column="Stem_from", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    remarks = models.CharField(
        db_column="Remarks", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    settle_batch_no = models.CharField(
        db_column="Settle_batch_no", max_length=50, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_settledetails_info_copy"


class LoadSettlefeeInfo(models.Model):
    payment_time = models.CharField(
        db_column="Payment_time", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    transaction_id = models.CharField(
        db_column="Transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    partner_transaction_id = models.CharField(
        db_column="Partner_transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    gross_amount = models.DecimalField(
        db_column="Gross_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_gross_amount = models.DecimalField(
        db_column="Rmb_gross_amount",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    fee_type = models.CharField(
        db_column="Fee_type", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    fee_amount = models.DecimalField(
        db_column="Fee_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    fee_rmb_amount = models.DecimalField(
        db_column="Fee_rmb_amount",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    rate = models.DecimalField(
        db_column="Rate", max_digits=18, decimal_places=8, blank=True, null=True
    )  # Field name made lowercase.
    remark = models.CharField(
        db_column="Remark", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    settle_time = models.CharField(
        db_column="Settle_time", max_length=10, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_settlefee_info"


class LoadStradeInfo(models.Model):
    partner_transaction_id = models.CharField(
        db_column="Partner_transaction_id", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    transaction_id = models.CharField(
        db_column="Transaction_id", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    amount = models.DecimalField(
        db_column="Amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_amount = models.DecimalField(
        db_column="Rmb_amount", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    fee = models.DecimalField(
        db_column="Fee", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    refund = models.DecimalField(
        db_column="Refund", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    settlement = models.DecimalField(
        db_column="Settlement", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    rmb_settlement = models.DecimalField(
        db_column="Rmb_settlement",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    currency = models.CharField(
        db_column="Currency", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    rate = models.DecimalField(
        db_column="Rate", max_digits=18, decimal_places=8, blank=True, null=True
    )  # Field name made lowercase.
    payment_time = models.DateTimeField(
        db_column="Payment_time", blank=True, null=True
    )  # Field name made lowercase.
    settlement_time = models.CharField(
        db_column="Settlement_time", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    type = models.CharField(
        db_column="Type", max_length=3, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "load_strade_info"


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
        db_table = "load_tmallso_info"
        unique_together = (("id", "order_id"),)


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
        db_table = "load_tmallsodetail_info"


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
        db_table = "load_transaction_info"


class TBasAreaInfo(models.Model):
    seq_no = models.AutoField(primary_key=True)
    area_code = models.CharField(max_length=1, blank=True, null=True)
    area_name = models.CharField(max_length=60, blank=True, null=True)
    province = models.CharField(max_length=60, blank=True, null=True)
    other_info = models.CharField(max_length=224, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_bas_area_info"


class TBasSkuPrice(models.Model):
    seq_no = models.AutoField(primary_key=True)
    sku_id = models.CharField(max_length=80, blank=True, null=True)
    sku_name = models.CharField(max_length=80, blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_bas_sku_price"


class TBuyerInfo(models.Model):
    buyer_name = models.CharField(max_length=80, blank=True, null=True)
    buyer_account = models.CharField(max_length=120, blank=True, null=True)
    is_mobile_order = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_buyer_info"


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
        db_table = "t_fee_info"


class TFeeMonthlyInfo(models.Model):
    fee_time = models.CharField(max_length=20, blank=True, null=True)
    logisitic_tax = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tmall = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    order_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    account_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_fee_monthly_info"


class TFeetypeInfo(models.Model):
    fee_name = models.CharField(max_length=60, blank=True, null=True)
    fee_desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_feetype_info"


class TGoodsNumInfo(models.Model):
    period = models.CharField(max_length=10)
    goods_id = models.CharField(max_length=30)
    goods_name = models.CharField(max_length=200)
    products = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    gpc = models.CharField(max_length=255)
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
        db_table = "t_goods_num_info"


class TGroupFeeInfo(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)
    fee_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    fee_amount_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_group_fee_info"


class TGroupMyaccountInfo(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    amount_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_group_myaccount_info"


class TGroupSettledetailsInfo(models.Model):
    order_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    amount_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_group_settledetails_info"


class TGroupStradeInfo(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=True)
    alipay_actual_recieve = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    refund = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alipay_strade_p = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_strade_r = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_actual_recieve_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    refund_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_strade_p_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_strade_r_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_group_strade_info"


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
        db_table = "t_member_alanlyse_info"


class TMonthlyOrderAmount(models.Model):
    fin_period = models.CharField(max_length=20, blank=True, null=True)
    actual_paid = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_actual_recieve = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    refund = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    account_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_get = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_monthly_order_amount"


class TMyaccountMonthlyInfo(models.Model):
    period = models.CharField(max_length=10)
    recharge = models.DecimalField(max_digits=18, decimal_places=2)
    refund = models.DecimalField(max_digits=18, decimal_places=2)
    payment = models.DecimalField(max_digits=18, decimal_places=2)
    order_payment = models.DecimalField(max_digits=18, decimal_places=2)
    not_order_payment = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = "t_myaccount_monthly_info"


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
        db_table = "t_order_amount"
        unique_together = (("id", "order_id"),)


class TOrderAnalyse(models.Model):
    fin_period = models.CharField(max_length=20, blank=True, null=True)
    area_info = models.CharField(max_length=255, blank=True, null=True)
    order_num = models.CharField(max_length=18, blank=True, null=True)
    saled_num = models.CharField(max_length=18, blank=True, null=True)
    closed_num = models.CharField(max_length=18, blank=True, null=True)
    waiting_num = models.CharField(max_length=18, blank=True, null=True)
    close_unpaid_num = models.CharField(max_length=18, blank=True, null=True)
    close_return_num = models.CharField(max_length=18, blank=True, null=True)
    order_amount = models.CharField(max_length=18, blank=True, null=True)
    saled_amount = models.CharField(max_length=18, blank=True, null=True)
    closed_amount = models.CharField(max_length=18, blank=True, null=True)
    waiting_amount = models.CharField(max_length=18, blank=True, null=True)
    close_unpaid_amount = models.CharField(max_length=18, blank=True, null=True)
    close_return_amount = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_order_analyse"


class TOrderArea(models.Model):
    fin_period = models.CharField(max_length=20)
    area_info = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    order_number = models.IntegerField()
    order_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = "t_order_area"


class TPeriodNumsInfo(models.Model):
    goods_id = models.CharField(max_length=80, blank=True, null=True)
    goods_name = models.CharField(max_length=200, blank=True, null=True)
    fee_order = models.CharField(max_length=2, blank=True, null=True)
    fee_type = models.CharField(max_length=200, blank=True, null=True)
    p201509 = models.DecimalField(
        db_column="P201509", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201510 = models.DecimalField(
        db_column="P201510", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201511 = models.DecimalField(
        db_column="P201511", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201512 = models.DecimalField(
        db_column="P201512", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201601 = models.DecimalField(
        db_column="P201601", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201602 = models.DecimalField(
        db_column="P201602", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201603 = models.DecimalField(
        db_column="P201603", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201604 = models.DecimalField(
        db_column="P201604", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201605 = models.DecimalField(
        db_column="P201605", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201606 = models.DecimalField(
        db_column="P201606", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201607 = models.DecimalField(
        db_column="P201607", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201608 = models.DecimalField(
        db_column="P201608", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201609 = models.DecimalField(
        db_column="P201609", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201610 = models.DecimalField(
        db_column="P201610", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201611 = models.DecimalField(
        db_column="P201611", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201612 = models.DecimalField(
        db_column="P201612", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201701 = models.DecimalField(
        db_column="P201701", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201702 = models.DecimalField(
        db_column="P201702", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201703 = models.DecimalField(
        db_column="P201703", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201704 = models.DecimalField(
        db_column="P201704", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201705 = models.DecimalField(
        db_column="P201705", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201706 = models.DecimalField(
        db_column="P201706", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    p201707 = models.DecimalField(
        db_column="P201707", max_digits=18, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "t_period_nums_info"


class TRecieverInfo(models.Model):
    buyer_account = models.CharField(max_length=120, blank=True, null=True)
    reciever_name = models.CharField(max_length=255, blank=True, null=True)
    recieve_address = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=80, blank=True, null=True)
    create_date = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_reciever_info"


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
        db_table = "t_settle_amount_info"


class TSettleFeeInfo(models.Model):
    seq_no = models.AutoField(primary_key=True)
    fee_time = models.CharField(max_length=20, blank=True, null=True)
    logisitic_tax = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tmall = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_tax_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_service_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_service_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tmall_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    juhuasuan_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    order_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    account_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_settle_fee_info"


class TSettlefeeMonthlyInfo(models.Model):
    fee_time = models.CharField(max_length=20, blank=True, null=True)
    logisitic_tax = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_service = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tmall = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    juhuasuan = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_tax_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    logisitic_service_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    alipay_service_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tmall_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    juhuasuan_usd = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    order_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    account_fee = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_settlefee_monthly_info"


class TTmallBomDetail(models.Model):
    period = models.CharField(max_length=10, blank=True, null=True)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    goods_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    order_status = models.CharField(max_length=40, blank=True, null=True)
    deal_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_tmall_bom_detail"


class TTmallGroupBomDetail(models.Model):
    period = models.CharField(max_length=7, blank=True, null=True)
    goods_code = models.CharField(max_length=60, blank=True, null=True)
    order_id = models.CharField(max_length=60, blank=True, null=True)
    in_out_number = models.IntegerField(blank=True, null=True)
    deal_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t_tmall_group_bom_detail"


class TTransactionGroupInfo(models.Model):
    goods_code = models.CharField(max_length=60, blank=True, null=True)
    order_id = models.CharField(max_length=60, blank=True, null=True)
    in_out_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_transaction_group_info"


class TempProductInfo(models.Model):
    product_name = models.CharField(max_length=255, blank=True, null=True)
    cargo_code = models.CharField(max_length=255, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "temp_product_info"


class TempTmalldetailRateInfo(models.Model):
    order_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    number = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    goods_rate = models.DecimalField(
        max_digits=18, decimal_places=4, blank=True, null=True
    )
    goods_total = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "temp_tmalldetail_rate_info"


class TempTmallsoRateInfo(models.Model):
    order_id = models.CharField(max_length=50)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    actual_paid = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    refund = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "temp_tmallso_rate_info"
        unique_together = (("id", "order_id"),)


class TmpTmallMonthly(models.Model):
    period = models.CharField(max_length=10, blank=True, null=True)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    goods_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(max_length=40, blank=True, null=True)
    deal_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "tmp_tmall_monthly"


class Taxrate(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(db_column="time", blank=True, null=True)
    deal_amount = models.DecimalField(
        max_digits=18, decimal_places=6, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "tax_rate"


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.CharField(max_length=255, blank=True, null=True)
    goods_name = models.CharField(max_length=255, blank=True, null=True)
    gpc = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    products = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "goods"

