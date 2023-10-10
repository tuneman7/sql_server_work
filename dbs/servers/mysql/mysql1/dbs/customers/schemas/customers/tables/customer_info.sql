DROP TABLE IF EXISTS customers.customer_info;

CREATE TABLE customers.customer_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    f_name CHAR(100),
    l_name CHAR(100),
    email_address CHAR(200),
    country CHAR(100),
    postalcode CHAR(100),
    city_name CHAR(100),
    province CHAR(100),
    created_by CHAR(100),
    created_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt DATETIME
);


USE customers;

DELIMITER //

CREATE TRIGGER customers_before_update
BEFORE UPDATE ON customers.customer_info FOR EACH ROW
BEGIN
    SET NEW.updated_by = CURRENT_USER();
    SET NEW.updated_dt = CURRENT_TIMESTAMP;    
END;

//

DELIMITER ;

DELIMITER //

CREATE TRIGGER customers_insert_trigger
BEFORE INSERT ON customers.customer_info
FOR EACH ROW
BEGIN
    SET NEW.created_by = CURRENT_USER();
END;

//

DELIMITER ;
