-- Connect to the finance database
\c finance

-- Create the distro_partner table
CREATE TABLE distro_partner (
    id serial PRIMARY KEY,
    partner_desc char(200) NOT NULL,
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update updated_by and updated_dt on any column update
CREATE OR REPLACE FUNCTION update_distro_partner()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by = current_user;
    NEW.updated_dt = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on update of any column
CREATE TRIGGER distro_partner_update_trigger
BEFORE UPDATE ON distro_partner
FOR EACH ROW
EXECUTE FUNCTION update_distro_partner();