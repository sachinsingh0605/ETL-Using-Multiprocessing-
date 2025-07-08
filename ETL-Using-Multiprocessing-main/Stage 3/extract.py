import mysql.connector as connection
import pandas as pd
import os 
import time

sTime = time.time()
sql_pass = os.getenv('sql_pass')

try:
    mydb = connection.connect(host="localhost", database = 'sales',user="root", passwd=sql_pass,use_pure=True)
    q_transaction = "Select * from transactions;"
    transaction = pd.read_sql(q_transaction,mydb)

    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))

print(f'Time taken = {time.time()-sTime}')