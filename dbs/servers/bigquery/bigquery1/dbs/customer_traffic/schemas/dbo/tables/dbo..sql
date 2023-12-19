CREATE OR REPLACE TABLE `site_traffic.product_views`
(
  product_id INT64,
  customer_id INT64,
  view_start DATETIME,
  view_end DATETIME,
  view_id INT64,
  geography_id INT64
);
