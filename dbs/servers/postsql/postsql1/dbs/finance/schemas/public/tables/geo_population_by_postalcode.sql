-- Connect to the "finance" database (if not already connected)
\c finance

CREATE TABLE geo_population_by_postalcode (
    postalcode VARCHAR(20),
    population INT,
    country VARCHAR(100) DEFAULT 'USA'
);
