-- Connect to the finance database
\c finance

-- Create the account_activity table
CREATE TABLE account_activity (
    id serial PRIMARY KEY,
    product_id INT NOT NULL,
    customer_id INT,
    account_id int NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amt_usd money,
    geography_id INT NOT NULL,
    distro_channel_id INT NOT NULL,
    distro_partner_id INT NOT NULL,
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update updated_by and updated_dt on any column update
CREATE OR REPLACE FUNCTION update_account_activity()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by = current_user;
    NEW.updated_dt = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on update of any column
CREATE TRIGGER account_activity_update_trigger
BEFORE UPDATE ON account_activity
FOR EACH ROW
EXECUTE FUNCTION update_account_activity();