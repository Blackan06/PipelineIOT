CREATE DATABASE iot_data WITH OWNER postgres TEMPLATE template0
WHERE NOT EXISTS (
  SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('iot_data')
);

CREATE TABLE IF NOT EXISTS astro_version_check (
  singleton BOOLEAN NOT NULL, 
  last_checked TIMESTAMP WITH TIME ZONE, 
  last_checked_by TEXT, 
  CONSTRAINT astro_version_check_pkey PRIMARY KEY (singleton)
);
