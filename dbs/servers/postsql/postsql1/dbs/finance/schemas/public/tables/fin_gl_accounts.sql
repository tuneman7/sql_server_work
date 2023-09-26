-- Connect to the finance database
\c finance

-- Create the fin_gl_accounts table
CREATE TABLE fin_gl_accounts (
    id serial PRIMARY KEY,
    account_code VARCHAR(20) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update updated_by and updated_dt on any column update
CREATE OR REPLACE FUNCTION update_fin_gl_accounts()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by = current_user;
    NEW.updated_dt = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on update of any column
CREATE TRIGGER fin_gl_accounts_update_trigger
BEFORE UPDATE ON fin_gl_accounts
FOR EACH ROW
EXECUTE FUNCTION update_fin_gl_accounts();