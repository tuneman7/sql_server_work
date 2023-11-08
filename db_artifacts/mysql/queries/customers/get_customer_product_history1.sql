
select * from 
(
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
)a order by id asc, purchase_dt desc

