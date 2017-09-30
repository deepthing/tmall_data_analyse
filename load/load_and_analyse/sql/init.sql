
update load_tmallso_info set order_id = TRIM( Replace(order_id,'"',''));
update load_tmallso_info set order_id = TRIM(Replace(Replace(Replace(order_id,'\t',''),'\n',''),'\r',''));

TRUNCATE TABLE tmp_tmall_monthly;
insert into tmp_tmall_monthly (order_id,period,product_name,number) 
select a.order_id,SUBSTR(b.create_time FROM 1 FOR 7),a.product_name,sum(number) 
from load_tmallsodetail_info a, load_tmallso_info b where a.order_id = b.order_id
group BY a.order_id,a.product_name,SUBSTR(b.create_time FROM 1 FOR 7);



-- make sure you have import data and change SQL statement on the view -> v_fee_info 


update load_fee_info set Exchange_Rate = TRIM( Replace(Exchange_Rate,'"',''));
update load_fee_info set Exchange_Rate = TRIM(Replace(Replace(Replace(Exchange_Rate,'\t',''),'\n',''),'\r',''));
update load_fee_info set Partner_transaction_id = TRIM( Replace(Partner_transaction_id,'"',''));
update load_fee_info set Transaction_id = TRIM( Replace(Transaction_id,'"',''));
update load_fee_info set Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,'\t',''),'\n',''),'\r',''));
update load_fee_info set Transaction_id = TRIM(Replace(Replace(Replace(Transaction_id,'\t',''),'\n',''),'\r',''));

TRUNCATE TABLE t_buyer_info;
insert into t_buyer_info(buyer_account,buyer_name,is_mobile_order,create_time ,mobile)
select buyer_account,buyer_name,is_mobile_order,SUBSTR(create_time FROM 1 FOR 10) ,mobile from load_tmallso_info
where buyer_account is not NULL 
group by buyer_account;


update load_settledetails_info set Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,'\t',''),'\n',''),'\r',''));
update load_settledetails_info set Settle_batch_no = TRIM(Replace(Replace(Replace(Settle_batch_no,'\t',''),'\n',''),'\r',''));


-- make sure you have import data to new table like Settlefee**** and change SQL statement on the view -> v_fee_info 
update load_fee_info set Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,'\t',''),'\n',''),'\r',''));


update load_settlefee_info set Transaction_id = TRIM( Replace(Transaction_id,'"',''));
update load_settlefee_info set Transaction_id = TRIM(Replace(Replace(Replace(Transaction_id,'\t',''),'\n',''),'\r',''));
update load_settlefee_info set Partner_transaction_id = TRIM( Replace(Partner_transaction_id,'"',''));
update load_settlefee_info set Partner_transaction_id = TRIM(Replace(Replace(Replace(Partner_transaction_id,'\t',''),'\n',''),'\r',''));
update load_settlefee_info set Fee_type = TRIM( Replace(Fee_type,'"',''));
update load_settlefee_info set Fee_type = TRIM(Replace(Replace(Replace(Fee_type,'\t',''),'\n',''),'\r',''));
update load_settlefee_info set Currency = TRIM( Replace(Currency,'"',''));
update load_settlefee_info set Currency = TRIM(Replace(Replace(Replace(Currency,'\t',''),'\n',''),'\r',''));

-- make sure you have import table myaccount*** and change SQL statement on the view -> v_myaccount_info
