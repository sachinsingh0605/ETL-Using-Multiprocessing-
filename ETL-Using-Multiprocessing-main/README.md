# ETL-Using-Multiprocessing

## Introduction 
ETL, which stands for extract, transform and load, is a data integration process that combines data from multiple data sources into a single, consistent data store that is loaded into a data warehouse or other target system.

This project performs ETL using SQL and python. Python is slower than SQL for this purpose as python is a high-level programming language while SQL is high-performance programming language specifically made to deal with data. However, to make ETL faster in python, multiprocessing can be used to execute the processes in parallel to each other.

There are three stages in this project:
- Stage 1 - SQL
- Stage 2 - Python
- Stage 3 - Python with multiprocessing

## Data
The relation between the tables of the database before applying transform oprations are shown in the below image.

![Model - before transformation](https://user-images.githubusercontent.com/78223588/217797790-24163fa9-a380-4c1a-8c00-4bd001e91fc5.png)

## Pipeline
### Extract
Data is initially loaded to the MYSQL server using db_dump.sql file and then extracted.

For SQL in Stage 1, temporary tables are created to process the data which are later deleted and for python in Stages 2 and 3, dataframes are created to process the data.

### Transform
Following seven transformation operations are appplied on the data:
1. Removing rows with sales amount<=0 in temp_transaction table
2. Removing duplicate records with incorrect currency values and correcting currency type
3. Converting USD to INR
4. Converting codes to integer values
5. Adding transcation_id column to give each transaction a unique value
6. adding total sales amount column in transaction
7. Calculating yearly revenue and storing it into another table

### Load
The transformed data is then loaded to PostgreSql server.

- For SQL, a new database is created form the transformed data which is then loaded to PostgreSql server using pgloader.
- For python, the newly created dataframes are loaded to PostgreSql server using Psycopg2.

# Time taken
SQL took the least amount of time in all of the cases. However, the time required by python was reduced significantly after implementing multithreading. Time taken is recorded against number of records in the table to track the progress of each method. 

![Time taken by different methods vs number of records](https://user-images.githubusercontent.com/78223588/217801400-e01d73c3-e390-4a39-8771-6281297c6d70.png)

Least amount of time taken in multiprocessing was recorded when the number of processes were set to eight, which is equal to the number of threads in the processor.

![Time taken according to number of processes](https://user-images.githubusercontent.com/78223588/217802876-91d6e67a-4f26-41ae-a9a4-fa5dadf632fe.png)
