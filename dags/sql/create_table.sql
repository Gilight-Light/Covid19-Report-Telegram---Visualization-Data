CREATE TABLE IF NOT EXISTS covid19 (
    province_state VARCHAR(50),
    country_region VARCHAR(50),
    lat FLOAT4,
    long FLOAT4,
    date VARCHAR(50),
    confirmed INT4,
    deaths INT4,
    recovered INT4,
    active INT4,
    who_region VARCHAR(50)
);