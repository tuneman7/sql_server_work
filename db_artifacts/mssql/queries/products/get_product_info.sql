SELECT
    p.id,
    p.product_name,
    pt.product_type_desc as product_type
from products p
JOIN
    product_type pt
--on pt.id = p.id
on pt.id = p.product_type_id
