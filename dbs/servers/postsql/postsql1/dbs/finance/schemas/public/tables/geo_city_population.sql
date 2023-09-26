-- Connect to the "finance" database (if not already connected)
\c finance

CREATE TABLE geo_city_population (
    id serial PRIMARY KEY,
    city_name VARCHAR(100),
    population INT,
    country VARCHAR(100) DEFAULT 'USA'
);
