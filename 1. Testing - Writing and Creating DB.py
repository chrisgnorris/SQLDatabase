#https://datatofish.com/pandas-dataframe-to-sql/
#https://www.dataquest.io/blog/sql-insert-tutorial/
#https://stackoverflow.com/questions/62340498/open-database-files-db-using-python
#https://sqlitebrowser.org/dl/
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

import sqlite3
from pandas import DataFrame

#Connect to DB (or creates new one)-------------------------------------------------------------------------------------
conn = sqlite3.connect('TestDB1.db') #just opens connection, doesnt query it
c = conn.cursor() #Creating Cursor - which is needed to fetch results (get rows back) https://stackoverflow.com/questions/6318126/why-do-you-need-to-create-a-cursor-when-querying-a-sqlite-database



# #Create new table (blank this out if already created, else error)-------------------------------------------------------
# c.execute('CREATE TABLE CARS (Brand text, Price number)') #This can just be all columns in DF - name,type
# conn.commit()




#Shows all tables
table_list = [a for a in c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# here is you table list
print(table_list)

#Create Test DF - if already exists will append to bottom---------------------------------------------------------------

Cars = {'Brand': ['Ford Civic','Toyota Corolla','Ford Focus','Audi A4'],
        'Price': [22000,25000,27000,35000]
        }

df = DataFrame(Cars, columns= ['Brand', 'Price'])

#Copy dataframe to SQL - need to change table names---------------------------------------------------------------------
df.to_sql('CARS', conn, if_exists = 'append', index = False,chunksize = 1000)

#Fetches all rows - next line of code will then do something with it. --------------------------------------------------
c.execute('''
SELECT * FROM CARS
          ''') #Returns all of DB

# c.execute('''
# SELECT Brand, max(price) FROM CARS
#           ''') # Just fetches highest price

# for row in c.fetchall():
#     print (row)

#Put back into  DF - from what was fetched above------------------------------------------------------------------------
df = DataFrame(c.fetchall(), columns=['Brand','Price'])
print (df)

#c.execute('DROP TABLE CARS') # This deletes Table.