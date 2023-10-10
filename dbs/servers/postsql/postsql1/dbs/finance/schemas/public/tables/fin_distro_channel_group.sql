-- Connect to the finance database
\c finance

-- Create the fin_distro_channel_group table
CREATE TABLE fin_distro_channel_group (
    id serial PRIMARY KEY,
    group_desc CHAR(400),
    fin_distro_channel_id INT,
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update updated_by and updated_dt on any column update
CREATE OR REPLACE FUNCTION update_fin_distro_channel_group()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by = current_user;
    NEW.updated_dt = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on update of any column
CREATE TRIGGER fin_distro_channel_group_update_trigger
BEFORE UPDATE ON fin_distro_channel_group
FOR EACH ROW
EXECUTE FUNCTION update_fin_distro_channel_group();