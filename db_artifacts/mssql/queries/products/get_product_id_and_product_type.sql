SELECT
    p.id AS product_id,
    p.product_name,
    pt.product_type AS product_type
FROM
    [products].[dbo].[products] AS p
JOIN
    [dbo].[product_type] AS pt
ON
    p.product_type = pt.id;