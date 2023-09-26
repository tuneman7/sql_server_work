-- Connect to the "finance" database (if not already connected)
\c finance

CREATE TABLE geo_postalcode_to_county_state (
    postalcode VARCHAR(20),
    countyname varchar(80),
    province varchar(60),
    country VARCHAR(100) DEFAULT 'USA'
);
