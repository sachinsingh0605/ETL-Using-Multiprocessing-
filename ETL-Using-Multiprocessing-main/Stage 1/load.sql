-- creating new database to load into postgresql using pgloader
create database sales_new;

CREATE TABLE sales_new.temp_transaction SELECT * FROM sales.temp_transaction;
CREATE TABLE sales_new.revenue SELECT * FROM sales.revenue;

-- dropping new tables from original database
drop table sales.temp_transaction;
drop table sales.revenue;
