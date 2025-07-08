-- making temporary customer, market and transaction tables
CREATE TABLE temp_transaction AS SELECT  * FROM
    transactions LIMIT 50000;

