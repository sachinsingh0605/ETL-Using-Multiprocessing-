-- Database: sales

-- DROP DATABASE IF EXISTS sales;

CREATE DATABASE sales
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Australia.1252'
    LC_CTYPE = 'English_Australia.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE sales TO PUBLIC;

GRANT CONNECT ON DATABASE sales TO etl;

GRANT ALL ON DATABASE sales TO postgres;