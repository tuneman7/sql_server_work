INSERT INTO customers.customer_product_history
    (product_id, customer_id, product_type_desc, purchase_dt, expiration_dt, created_by, created_dt, updated_by, updated_dt)
SELECT
    product_id,
    customer_id,
    product_type_desc,
    (expiration_dt - INTERVAL (DATEDIFF(expiration_dt, purchase_dt) + 1) DAY) AS purchase_dt,
    (purchase_dt) AS expiration_dt,
    created_by,
    created_dt,
    updated_by,
    updated_dt
FROM
    customers.customer_product
WHERE
    RAND() <= 0.8; -- Select 80% of records randomly    

