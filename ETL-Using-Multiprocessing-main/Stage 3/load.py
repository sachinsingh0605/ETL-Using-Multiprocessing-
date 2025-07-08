import os
import pandas as pd

path = 'dataframes'
os.chdir(path)

n = len(os.listdir())/2

transaction_list = []
revenue_list = []

# iterate through all file
for file in os.listdir():
    file_path = f"{path}/{file}"
    # print(file[0:11])
    # print(file_path)
    if(file[0:7]=='revenue'):
        os.chdir('..')
        revenue_list.append(pd.read_csv(file_path))  
        os.chdir(path)    
    if(file[0:11]=='transaction'):
        os.chdir('..')
        transaction_list.append(pd.read_csv(file_path))
        os.chdir(path)

# combining dataframes
transaction = pd.concat(transaction_list)

temp = pd.concat(revenue_list,axis=1)
revenue = pd.DataFrame([[2017,0],[2018,0],[2019,0],[2020,0]],columns = ['year','total_sales'])
revenue['total_sales'] = temp['total_sales'].sum(axis=1).values

# Loading tables to postgresql server
import os 

sql_pass = os.getenv('sql_pass')
uid =  'postgres'
server = "haq-PC"
# import packages
import psycopg2
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
load(transaction,'transaction',sqlTransaction)
load(revenue,'revenue',sqlRevenue)