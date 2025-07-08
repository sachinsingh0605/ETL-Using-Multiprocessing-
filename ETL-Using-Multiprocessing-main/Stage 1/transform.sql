-- 1. Removing rows with sales amount<=0 in temp_transaction table
DELETE FROM temp_transaction 
WHERE
    sales_amount <= 0;

-- 2. Removing duplicate records with incorrect currency values and correcting currency type
DELETE FROM temp_transaction 
WHERE
    currency = 'INR' OR currency = 'USD';
UPDATE temp_transaction 
SET 
    currency = 'INR'
WHERE
    currency = 'INR\r'
;
UPDATE temp_transaction 
SET 
    currency = 'USD'
WHERE
    currency = 'USD\r'
;

-- 3. Converting USD to INR
UPDATE temp_transaction 
SET 
    sales_amount = sales_amount * 82.23
WHERE
    currency = 'USD';
UPDATE temp_transaction 
SET 
    currency = 'INR'
WHERE
    currency = 'USD';

-- 4. Converting codes to integer values
UPDATE temp_transaction 
SET 
    product_code = CAST((SELECT REGEXP_REPLACE(product_code, '[^0-9]+', ''))
        AS UNSIGNED),
    customer_code = CAST((SELECT REGEXP_REPLACE(customer_code, '[^0-9]+', ''))
        AS UNSIGNED),
    market_code = CAST((SELECT REGEXP_REPLACE(market_code, '[^0-9]+', ''))
        AS UNSIGNED);

-- 5. Adding transcation_id column in temp_transaction to give each transaction a unique value
alter table temp_transaction add transaction_id varchar(20);
UPDATE temp_transaction 
SET 
    transaction_id = SUBSTR(MD5(RAND()), 1, 18);

-- 6. adding total sales amount column in transaction
alter table temp_transaction add total_sales_amount double;
UPDATE temp_transaction 
SET 
    total_sales_amount = sales_qty * sales_amount;

-- 7. Calculating yearly revenue and storing it into another table
CREATE TABLE revenue (
    order_year INT,
    total_sales DOUBLE
);
insert into revenue(order_year) values (2017),(2018),(2019),(2020);

UPDATE revenue 
SET 
    total_sales = (SELECT 
            SUM(total_sales_amount)
        FROM
            temp_transaction
        WHERE
            YEAR(order_date) = 2017)
WHERE
    order_year = 2017;
UPDATE revenue 
SET 
    total_sales = (SELECT 
            SUM(total_sales_amount)
        FROM
            temp_transaction
        WHERE
            YEAR(order_date) = 2018)
WHERE
    order_year = 2018;
UPDATE revenue 
SET 
    total_sales = (SELECT 
            SUM(total_sales_amount)
        FROM
            temp_transaction
        WHERE
            YEAR(order_date) = 2019)
WHERE
    order_year = 2019;
UPDATE revenue 
SET 
    total_sales = (SELECT 
            SUM(total_sales_amount)
        FROM
            temp_transaction
        WHERE
            YEAR(order_date) = 2020)
WHERE
    order_year = 2020;