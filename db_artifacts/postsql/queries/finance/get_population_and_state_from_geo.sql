SELECT gg.postalcode, gcp.city_name, gcp.population as city_population, gzp.population as zip_population, zip2state.province as province
FROM geo_geography gg
INNER JOIN geo_postalcode_to_county_state zip2state
    on zip2state.postalcode=gg.postalcode
INNER JOIN geo_city_population gcp ON gg.location_name = gcp.city_name
INNER JOIN geo_population_by_postalcode gzp on gg.postalcode = gzp.postalcode
ORDER BY gcp.population DESC;
