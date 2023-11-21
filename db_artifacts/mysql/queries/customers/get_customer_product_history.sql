-- select * from customer_info limit 10;
-- select * from customer_product limit 10;
-- select * from customer_product_history limit 10;

-- DROP TEMPORARY TABLE IF EXISTS tmp_product_history;

-- CREATE TEMPORARY TABLE IF NOT EXISTS tmp_product_history as 
-- (
select 
    c.id,
    c.f_name, 
    c.l_name,
    cp.product_id,
    cp.purchase_dt,
    cp.expiration_dt,
    cp.created_dt
from 
    customer_info c
join 
    customer_product cp
on 
    c.id = cp.customer_id
UNION ALL
select 
    c.id,
    c.f_name, 
    c.l_name,
    cp.product_id,
    cp.purchase_dt,
    cp.expiration_dt,
    cp.created_dt
from 
    customer_info c
join 
    customer_product_history cp
on 
    c.id = cp.customer_id
-- );

--select * from tmp_product_history ORDER BY id, product_id DESC, purchase_dt ASC;