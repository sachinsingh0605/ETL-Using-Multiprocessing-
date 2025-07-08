# from sqlalchemy import create_engine
import transform
import os 

sql_pass = os.getenv('sql_pass')
uid =  'postgres'
server = "haq-PC"
# import packages
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def load(df,table,sql):
    # establish connections
    conn_string = f'postgresql://{uid}:{sql_pass}@127.0.0.1:5432/sales'

    db = create_engine(conn_string)
    conn = db.connect()
    conn1 = psycopg2.connect(
        database="sales",
    user=uid,
    password=sql_pass,
    host='127.0.0.1',
    port= '5432'
    )

    conn1.autocommit = True
    cursor = conn1.cursor()

    # drop table if it already exists
    cursor.execute(f'drop table if exists {table}')
    cursor.execute(sql)

    # import the csv file to create a dataframe
    data = df

    # converting data to sql
    data.to_sql(table, conn, if_exists= 'replace')

    conn1.commit()
    conn1.close()

sqlTransaction = '''create table transaction (
    product_code varchar(45), 
    customer_code varchar(45), 
    market_code varchar(45), 
    order_date date,
    sales_qty int, 
    sales_amount double precision, 
    currency varchar(45), 
    total_sales_amount double precision,
    transaction_id varchar(45));'''
sqlRevenue = '''CREATE TABLE revenue (
    order_year INT,
    total_sales DOUBLE);'''
load(transform.dfTransaction,'transaction',sqlTransaction)
load(transform.revenue,'revenue',sqlRevenue)

