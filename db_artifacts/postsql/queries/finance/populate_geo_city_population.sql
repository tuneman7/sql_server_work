\c finance
INSERT INTO geo_city_population (city_name, population)
SELECT
    g.location_name AS city_name,
    SUM(p.population) AS population
FROM
    geo_geography g
JOIN
    geo_population_by_postalcode p
ON
    g.postalcode = p.postalcode
GROUP BY
    g.location_name;
