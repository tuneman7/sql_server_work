-- Connect to the "finance" database (if not already connected)
\c finance

-- Create the "geography" table with columns
CREATE TABLE geography (
    id serial PRIMARY KEY,
    zipcode VARCHAR(10),
    country VARCHAR(100),
    location_name VARCHAR(100),
    msa VARCHAR(100),
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT current_timestamp,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update created_by, created_dt, updated_by, and updated_dt on any insert or update
CREATE OR REPLACE FUNCTION update_geography()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.created_by = current_user;
        NEW.created_dt = current_timestamp;
    ELSIF TG_OP = 'UPDATE' THEN
        NEW.updated_by = current_user;
        NEW.updated_dt = current_timestamp;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on insert or update of any column
CREATE TRIGGER geography_insert_update_trigger
BEFORE INSERT OR UPDATE ON geography
FOR EACH ROW
EXECUTE FUNCTION update_geography();
