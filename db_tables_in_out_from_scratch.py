#!/usr/bin/env python
# coding: utf-8

# # Connect to SQL Server Driver and Create Database



import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-B6VOM33\SQLEXPRESS;'
                      #'Database=;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('CREATE DATABASE testDB;')


# # Connect to Database and Create First Table




conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-B6VOM33\SQLEXPRESS;'
                      'Database=testDB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute("""

    CREATE TABLE Persons (
        PersonID int,
        LastName varchar(255),
        FirstName varchar(255),
        Address varchar(255),
        City varchar(255)
                            );

                                """)


# # Insert First Row Into Table




cursor.execute("""

                INSERT INTO Persons (PersonID, LastName, FirstName, Address, City)
                VALUES (1, 'Cardinal', 'Tom', '19 Stranger St', 'Tiz-ouwn');

                                """)


# # Run First Query Against The Table




cursor.execute('select * from testDB.dbo.Persons')


# # Print Results By Row



for row in cursor:
    print(row)


# # Insert Python List Into Table as Row



SQLCommand = ("INSERT INTO Persons(PersonID, LastName, FirstName, Address, City) VALUES (?,?,?,?,?)")    

Values = [1, 'Berry', 'Joe', '65 Jan', 'Wellston'] 

#Processing Query    
cursor.execute(SQLCommand,Values)     

#Commiting any pending transaction to the database.    
conn.commit()  


# # Print Table By Row One At A Time Append to List




persons = []
for row in cursor.execute('select * from testDB.dbo.Persons').fetchall():
    persons.append(row)
    print(row)


# # Print List

# In[9]:


persons


# # Make Numpy Array and Print

# In[16]:


import numpy as np
np.array(persons)[2]


# # Make Pandas DF and Print




import pandas as pd
pd.DataFrame(np.array(persons), columns=['ID', 'LastName', 'FirstName', 'Address', 'City']).sort_values(by=['Address'])


# # Delete Top 5 Rows in Table



cursor.execute('delete top (2) from testDB.dbo.Persons')




for row in cursor.execute('select * from testDB.dbo.Persons').fetchall():
    print(row)


# No output because they are gone!

# # Looped Entry Of Previously Pulled Values




SQLCommand = r"INSERT INTO Persons(PersonID, LastName, FirstName, Address, City) VALUES (?,?,?,?,?)"
pull = cursor.execute('select * from testDB.dbo.Persons').fetchall()


i = 0
for row in pull:
    Values = [2,'James', 'Brian', '54 Westpoint', 'Killaz']
    
    cursor.execute(SQLCommand,Values)
    conn.commit()  
    
    i = i + 1
    
    if i > 10:
        break
        
for row in cursor.execute('select * from testDB.dbo.Persons'):
    print(row)




cursor.execute('delete top (30) from testDB.dbo.Persons')







