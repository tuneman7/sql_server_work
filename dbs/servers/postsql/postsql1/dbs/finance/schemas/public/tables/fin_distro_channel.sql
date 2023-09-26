-- Connect to the finance database
\c finance

-- Create the fin_distro_channel table
CREATE TABLE fin_distro_channel (
    id serial PRIMARY KEY,
    chnl_cd char(15),
    channel_desc char(400),
    created_by CHAR(100),
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by CHAR(100),
    updated_dt TIMESTAMP
);

-- Create a trigger function to update updated_by and updated_dt on any column update
CREATE OR REPLACE FUNCTION update_fin_distro_channel()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by = current_user;
    NEW.updated_dt = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on update of any column
CREATE TRIGGER fin_distro_channel_update_trigger
BEFORE UPDATE ON fin_distro_channel
FOR EACH ROW
EXECUTE FUNCTION update_fin_distro_channel();

--Some sentinal values
--"AIR","TH","STREAM","STREAMRTL","STREAMSUB","MOBILE","EDU","MPUB","HVID","HVIDR","EVNT","HVIDDVD"
--"Airlines","Theatrical","Streaming","Streaming Rental","Streaming Subscription","Mobile","Education","Music Publishing","Home Video","Home Video Rentals","Events","Home Video DVD"