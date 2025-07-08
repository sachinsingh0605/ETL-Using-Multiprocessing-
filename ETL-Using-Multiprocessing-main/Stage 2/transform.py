import extract as extract
import pandas as pd
import random, string, re, time

dfTransaction = extract.transaction
dfTransaction = dfTransaction.iloc[:50000]
sTime = time.time()

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

for i in range(dfTransaction.shape[0]):
    # Removing rows with sales amount<=0 in dfTransaction and correcting currency type
    if dfTransaction.iloc[i]['sales_amount'] <= 0 or dfTransaction.iloc[i]['currency'] == 'INR' or dfTransaction.iloc[i]['currency'] == 'USD':
        drop_index.append(i)

    # changing USD to INR
    if dfTransaction.iloc[i]['currency'] == 'USD\r':
        sales.append(dfTransaction.iloc[i]['sales_amount']*82.23)
    else:
        sales.append(dfTransaction.iloc[i]['sales_amount'])
    
    # changing all currency values to INR
    curr.append('INR')

    # converting codes to integer values
    product_c.append(int(re.findall(r'\d+', dfTransaction.iloc[i]['product_code'])[0]))
    customer_c.append(int(re.findall(r'\d+', dfTransaction.iloc[i]['customer_code'])[0])) 
    market_c.append(int(re.findall(r'\d+', dfTransaction.iloc[i]['market_code'])[0])) 

    # Giving each transaction a unique value
    transaction_id.append(''.join(random.choices(string.ascii_lowercase + string.digits, k=18)))

    # calculating total sales amount
    total_sales_amount.append(dfTransaction.iloc[i]['sales_qty']*sales[i])

    # adding total sales amount to revenue
    if i not in drop_index:
        revenue.iloc[dfTransaction.iloc[i]['order_date'].year-2017]['total_sales'] += total_sales_amount[i]

dfTransaction['total_sales_amount'] = total_sales_amount
dfTransaction['transaction_id'] = transaction_id
dfTransaction['product_code'] = product_c
dfTransaction['market_code'] = market_c
dfTransaction['customer_code'] = customer_c
dfTransaction['currency'] = curr
dfTransaction['sales_amount'] = sales

dfTransaction.drop(drop_index,inplace=True)

eTime = time.time()
print(eTime-sTime)