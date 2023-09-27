SELECT
    p.id AS product_id,
    p.product_name,
    pt.id AS product_type_id,
    pt.product_type_desc
FROM
    products p
JOIN
    product_type pt ON p.product_type_id = pt.id;
