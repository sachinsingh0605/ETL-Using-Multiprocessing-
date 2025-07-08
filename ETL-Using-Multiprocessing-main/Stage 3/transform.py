import pandas as pd
import re
import string
import random, math
import multiprocessing,time

# print("Program Started....")

# ----------------------SPLITTING DATASET-----------------------------
master_df = pd.read_csv('master_df').iloc[:50000]
n = master_df.shape[0]
processes = 8

list_df = []

master_df.iloc[:math.floor(n/processes)]
master_df.iloc[math.floor((processes-1)*n/processes)+1:]
for i in range(processes):
    list_df.append(master_df.iloc[math.floor(i*n/processes):math.floor((i+1)*n/processes)])

# ------------------------DEFINGING TASK---------------------------

def task(df,k):
    startTime = time.time()
    print(f"Process {k} started")
    df.reset_index(inplace=True)
    transaction_id = []     # saves unique transaction values
    sales = []

    # Stores codes converted to int
    product_c = []
    customer_c = []
    market_c = []

    curr = []

    revenue = pd.DataFrame([[2017,0],[2018,0],[2019,0],[2020,0]],columns = ['year','total_sales'])
    total_sales_amount = [] # saves the total sales amount of each transaction
    drop_index = []         # saves indices to be dropped

    for i in range(df.shape[0]):
        # Removing rows with sales amount<=0 in dfTransaction and correcting currency type
        if df.iloc[i]['sales_amount'] <= 0 or df.iloc[i]['currency'] == 'INR' or df.iloc[i]['currency'] == 'USD':
            drop_index.append(i)

        # changing USD to INR
        if df.iloc[i]['currency'] == 'USD\r':
            sales.append(df.iloc[i]['sales_amount']*82.23)
        else:
            sales.append(df.iloc[i]['sales_amount'])
        
        # changing all currency values to INR
        curr.append('INR')

        # converting codes to integer values
        product_c.append(int(re.findall(r'\d+', df.iloc[i]['product_code'])[0]))
        customer_c.append(int(re.findall(r'\d+', df.iloc[i]['customer_code'])[0])) 
        market_c.append(int(re.findall(r'\d+', df.iloc[i]['market_code'])[0])) 

        # Giving each transaction a unique value
        transaction_id.append(''.join(random.choices(string.ascii_lowercase + string.digits, k=18)))

        # calculating total sales amount
        total_sales_amount.append(df.iloc[i]['sales_qty']*sales[i])

        # adding total sales amount to revenue
        if i not in drop_index:
            date = df.iloc[i]['order_date']
            revenue.iloc[int(date[0:4])-2017]['total_sales'] += total_sales_amount[i]

    df['total_sales_amount'] = total_sales_amount
    df['transaction_id'] = transaction_id
    df['product_code'] = product_c
    df['market_code'] = market_c
    df['customer_code'] = customer_c
    df['currency'] = curr
    df['sales_amount'] = sales

    df.drop(drop_index,inplace=True)
    df.to_csv(f'./dataframes/transaction{k}.csv')
    revenue.to_csv(f'./dataframes/revenue{k}.csv')
    
    print(f"Process {k} end")
    print(f"Total Time {round( time.time() - startTime,4)} sec for process {k}")
    return(df)

# ------------------RUNNING MULTIPROCESSING--------------------------
if __name__ == '__main__':
    for i in range(processes):
        cmd = str(i+1)
        print(f" Process {cmd} starts")
        t = multiprocessing.Process(target=task , args=(list_df[i],i,))
        t.start()