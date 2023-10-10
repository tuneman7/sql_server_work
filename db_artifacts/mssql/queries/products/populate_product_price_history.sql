-- Insert data into product_price_history from product_price
INSERT INTO [dbo].[product_price_history] (product_id, usd_price, pricing_start_dt, pricing_end_dt, created_by, created_dt, updated_by, updated_dt)
SELECT
    p.product_id,
    ROUND(p.usd_price * 0.8, 2), -- 20% lower usd_price
    p.pricing_start_dt,
    DATEADD(DAY, -1, p.pricing_start_dt) AS pricing_end_dt, -- One day before pricing_start_dt
    p.created_by,
    p.created_dt,
    p.updated_by,
    p.updated_dt
FROM
    [dbo].[product_price] p;
