-- 初始化tmallsodetail的时间字段，用于每个月的查找

UPDATE load_tmallsodetail_info t,load_tmallso_info t1  SET  t.order_create_time=t1.create_time WHERE t1.order_id=t.order_id;


-- 初始化tmallsodetail的口味信息

UPDATE load_tmallsodetail_info t set t.product_name=concat(t.product_name,'_',t.product_attr) WHERE t.product_attr like '%口味%';

UPDATE load_tmallsodetail_info t set t.product_attr='name' WHERE t.product_attr like '%口味%';



-- 初始化tmallsodetail的数据错误

UPDATE load_tmallsodetail_info t
SET t.product_name = concat(
	t.product_name,
	'_',
	t.product_attr
)
WHERE
	t.product_attr = '组合套餐：(graceland fruit 蔓越莓果干)*5'
AND t.order_id = '122716408110468200';

UPDATE load_tmallsodetail_info t
SET t.product_attr = 'name'
WHERE
	t.product_attr = '组合套餐：(graceland fruit 蔓越莓果干)*5'
AND t.order_id = '122716408110468200';



-- 初始化tmallsodetail的数据错误
UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1371519420561150';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1371544066766246';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1373767744246650';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1682213382002278';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1682592895038285';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1682593854522256';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1683486183224780';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '1688120270289969';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '2082759374275824';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '2084373771027208';

UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包_实际：酸樱桃果干 141.7克'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit蓝莓果干141g/包_食品口味：蓝莓干141.7g/包'
AND t.order_id = '2087966108592306';


-- 初始化tmallsodetail的数据错误
UPDATE load_tmallsodetail_info t
SET t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit酸樱桃果干141g/包_食品口味：酸樱桃干141.7g/包_实际：发3包'
WHERE
	t.product_name = '【指定ID购买，错拍无效】美国GracelandFruit酸樱桃果干141g/包_食品口味：酸樱桃干141.7g/包'
AND t.order_id = '2282261429766931';


UPDATE load_tmallsodetail_info t
SET t.number = '0'
WHERE
	t.order_status = '交易关闭'
AND t.order_id = '2198460197889762';


-- 初始化Myaccount的Remarks字段
UPDATE load_myaccount_info SET  Remarks=Alipay_Order    WHERE Remarks ='';

-- 初始化Myaccount的分类字段，用于sheet1的导出字段
UPDATE load_myaccount_info SET Myaccountfee = '仓储费'  where Order_No like '%adjust%';

UPDATE load_myaccount_info SET Myaccountfee = '仓储费'  where Order_No like '%BS%';

UPDATE load_myaccount_info SET Myaccountfee = '仓储费'  where Remarks like '%仓储费%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Order_No like '%YFX%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Remarks like '%保险%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Remarks like '%382709172%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Remarks like '%382931089%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Remarks like '%运费险%';

UPDATE load_myaccount_info SET Myaccountfee = '保险费'  where Amount = '-0.30';

UPDATE load_myaccount_info SET Myaccountfee = '商家赔付给消费者费用'  where Order_No like '%b2c%';

UPDATE load_myaccount_info SET Myaccountfee = '菜鸟赔付给商家费用（货款赔付）'  where Order_No LIKE '%LBX%' and Type = 'refund' and Remarks like '%Payer-%';

UPDATE load_myaccount_info SET Myaccountfee = '菜鸟赔付给商家费用（货款赔付）'  where Type = 'refund'and Remarks like '%货值赔付%';

UPDATE load_myaccount_info SET Myaccountfee = '菜鸟赔付商给家费用（保证金赔付）'  where Order_No LIKE '%LP%' and Type = 'refund' and Remarks like '%Payer-%';

UPDATE load_myaccount_info SET Myaccountfee = '菜鸟赔付商给家费用（保证金赔付）'  where Type = 'refund' and Remarks like '%服务赔付%';

UPDATE load_myaccount_info SET Myaccountfee = '推广补助'  where Type = 'refund' and Remarks like '%taobao%';

UPDATE load_myaccount_info SET Myaccountfee = '其他账户返还'  where Type = 'refund' and Myaccountfee is NULL;

UPDATE load_myaccount_info SET Myaccountfee = '天猫年费'  where Type = 'payments' and Remarks like '%taobao%' and Order_No NOT like '%B2C%' and Order_No like '%HJCOM%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫年费'  where Type = 'payments' and Remarks like '%天猫国际年费%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫广告推广费'  where Type = 'payments' and Remarks like '%taobao%' and Order_No NOT like '%B2C%' and Order_No not like '%HJCOM%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫广告推广费'  where Type = 'payments' and Remarks like '%淘宝客佣金扣款%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫广告推广费'  where Amount = '-3000.00' and Remarks like '%Payee-浙江天猫技术有限公司%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫广告推广费'  where Amount = '-30000.00' and Remarks like '%Payee-浙江天猫技术有限公司%';

UPDATE load_myaccount_info SET Myaccountfee = '天猫广告推广费'  where Type = 'payments' and Remarks like '%聚划算参团费扣除-海外{20105764}扣款%';

-- 初始化load_fee_info字段，用于sheet1的费用导出字段
-- select * from load_fee_info WHERE fee_desc_flag is null;
 
UPDATE load_fee_info set fee_desc_flag = 'logisitic_tax'  WHERE fee_desc LIKE '%进口关税%';  

UPDATE load_fee_info set fee_desc_flag = 'logisitic_service'  WHERE fee_desc LIKE '%菜鸟-保税_正向配送费%';  

UPDATE load_fee_info set fee_desc_flag = 'logisitic_service'  WHERE fee_desc LIKE '%服务费用%';  

UPDATE load_fee_info set fee_desc_flag = 'alipay_service'  WHERE fee_desc LIKE '%Alipay service fee%';  

UPDATE load_fee_info set fee_desc_flag = 'tmall'  WHERE fee_desc LIKE '%Tmall Global Commission%';  

UPDATE load_fee_info set fee_desc_flag = 'tmall'  WHERE fee_desc LIKE '%天猫收佣金%';  

UPDATE load_fee_info set fee_desc_flag = 'juhuasuan'  WHERE fee_desc LIKE '%Juhuasuan Overseas Commission%'; 

UPDATE load_fee_info set fee_desc_flag = 'taobaoke'  WHERE fee_desc LIKE '%Taobaoke%';  

