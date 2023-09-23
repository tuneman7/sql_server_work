DROP TABLE IF EXISTS customers.customer_product_history;

CREATE TABLE customers.customer_product_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    product_type CHAR(100),
    created_by CHAR(100),
    created_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt DATETIME,
    expiration_dt DATETIME
);


USE customers;

DELIMITER //

CREATE TRIGGER customer_product_history_before_update
BEFORE UPDATE ON customers.customer_product_history FOR EACH ROW
BEGIN
    SET NEW.updated_by = CURRENT_USER();
    SET NEW.updated_dt = CURRENT_TIMESTAMP;    
END;

//

DELIMITER ;

DELIMITER //

CREATE TRIGGER customer_product_history_insert_trigger
BEFORE INSERT ON customers.customer_product_history
FOR EACH ROW
BEGIN
    SET NEW.created_by = CURRENT_USER();
END;

//

DELIMITER ;
