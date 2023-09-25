-- Connect to the "finance" database (if not already connected)
\c finance

CREATE TABLE poplation_by_postalcode (
    postalcode VARCHAR(10) PRIMARY KEY,
    population INT,
    country VARCHAR(100) DEFAULT 'USA'
);
