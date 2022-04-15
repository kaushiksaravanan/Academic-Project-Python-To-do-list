import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
import time
import mysql.connector


host_name='localhost'
user_n='root'
pwd=1234
db='TO-DO-LIST'


# FOR FIRST TIME 
# conn = sqlite3.connect('test_database') 
# c = conn.cursor()

# c.execute('''
#           CREATE TABLE IF NOT EXISTS products
#           ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT, [price] INTEGER)
#           ''')
          
# c.execute('''
#           INSERT INTO products (product_id, product_name, price)

#                 VALUES
#                 (1,'Computer',800),
#                 (2,'Printer',200),
#                 (3,'Tablet',300),
#                 (4,'Desk',450),
#                 (5,'Chair',150)
#           ''')                     

# conn.commit()
def myFunction_runonce():
	mydb = mysql.connector.connect(host=host_name,user=user_n,password=pwd)
	mycursor = mydb.cursor()
	query="CREATE DATABASE "+db
	mycursor.execute(query)
	mydb.close()

run_once = 0
while 1:
    if run_once == 0:
        myFunction_runonce()
        run_once = 1:


#SQL SCHEMEA
#BASE 
#contains usr,pwd,adm

#USR_name
#contains task,completed

#query for usr
def getdata(usr):
	try:
		data=[]
		Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
		Mycursor=Mydb.cursor()
		query="SELECT * FROM "+usr+';'
		Mycursor.execute(query)
		for i in Mycursor.fetchall():
			data.append([i[0],i[1]])
		Mydb.close()
		return data
	except:
		return []

#check from MAIN table where we got username,user's password and (admin or not)
def check(usr,pwd):
	try:
		Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
		Mycursor=Mydb.cursor()
		query="SELECT pwd FROM BASE WHERE usr="+usr+';'
		Mycursor.execute(query)
		for i in Mycursor.fetchall():
			if i==pwd:
				return True
			else:
				return False
		Mydb.close()
	except:
		return False

#check if username is avaiable do count(*)
def check_username(usr):
	try:
		Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
		Mycursor=Mydb.cursor()
		query="SELECT COUNT(*) FROM BASE WHERE usr="+usr+';'
		Mycursor.execute(query)
		cus=Mycursor.fetchall()
		if len(cus)==1:
			return False
		else:
			query='CREATE TABLE '+usr+'(task VARCHAR2(40),complete int);'
			Mycursor.execute(query)
			return True
		Mydb.close()
	except:
		return False

#got to user's table and delete the certain taks
def delete(usr,task_to_be_deleted):
	try:
		Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
		Mycursor=Mydb.cursor()

		query="SELECT COUNT(*) FROM "+usr+"WHERE task="+task+";"
		Mycursor.execute(query)
		cus=Mycursor.fetchall()
		if len(cus)==0:
			return False
		else:
			query="DELETE FROM "+usr+"WHERE task="+task+";"
			Mycursor.execute(query)
			return True
		Mydb.close()
	except:
		return False

#add task
def add(usr,add):
	try:
		Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
		Mycursor=Mydb.cursor()
		query="INSERT INTO "+usr'+(task,complete)'+'VALUES ('+add+',1);'
		Mycursor.execute(query)
		Mydb.close()
		return True
	except:
		return False
		
def change_pwd(usr,old,new):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT usr,pwd FROM BASE")
	for i in Mycursor:
		print(i)
	Mydb.close()
	return True
def complete_db_update(login_usr,complete):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT usr,pwd FROM BASE")
	for i in Mycursor:
		print(i)
	Mydb.close()
	return True
def incomplete_db_update(login_usr,incomplete):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT usr,pwd FROM BASE")
	for i in Mycursor:
		print(i)
	Mydb.close()
	return True
def getdata(usr):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT usr,pwd FROM BASE")
	for i in Mycursor:
		print(i)
	Mydb.close()
	return []
def check_adm(admin_ursn,admin_pwd):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT usr,pwd FROM BASE")
	for i in Mycursor:
		print(i)
	Mydb.close()
	return True

login_usr=''
login_pwd=''


st.title("TO-DO LIST")

with st.expander("LOGIN"):
		login_usr = st.text_input("ENTER USERNAME", '')
		login_pwd = st.text_input("ENTER PASSWORD", '')
		button_usr=st.button('Enter')
		if check(login_usr,login_pwd):
								st.write('----------------------')
								st.markdown('## TASKS')
								incomplete=[]
								complete=[]
								for i,j in getdata(login_usr):
									if j==0:
										agree = st.checkbox(i)
										if agree:
											complete.append(i)
										else:
											incomplete.append(i)
									if j==1:
										complete.append(i)
								st.markdown('## *COMPLETED TASKS ARE:*')
								for i in complete:
									k='* '
									k+=i
									st.markdown(k)
								complete_db_update(login_usr,complete)
								st.markdown('## *INCOMPLETE TASKS ARE:*')
								for i in incomplete:
									k='* '
									k+=i
									st.markdown(k)
								incomplete_db_update(login_usr,incomplete)
								st.write('----------------------')
								st.markdown('## Manipulate')
		if st.button('Insert task'):
										add_task=st.text_input('Enter task name to Add')
										if add(login_usr,add_task):
											st.success("Success")
										else:
											st.error('Error')
		if st.button('Delete task'):
										delete_task=st.text_input('Enter task name to delete')
										if delete(login_usr,delete_task):
											st.success("Success")
										else:
											st.error('Error')
		if st.button('Change password'):
										old_pwd=st.text_input('Enter old password')
										new_pwd=st.text_input('Enter new password')
										if change_pwd(login_usr,old_pwd,new_pwd):
											st.success("Password changed successfully")
										else:
											st.error('Error')
		if st.button('Root access'):
										admin_ursn=st.text_input("Enter Admin's Unsername")
										admin_pwd=st.text_input('Enter Admin pwd')
										if check_adm(admin_ursn,admin_pwd):
											if st.button('Get indivdual resources used by a user'):
												username_tgd=st.text_input('Enter name of user to retive tasks for')
												try:
													st.table(getdata(usr_data))  ## as data frame 
												except:
													st.write("User doesn't exists")
										else:
											st.write('Wrong credentials')




			
with st.expander('REGISTER'):
		login_usr = st.text_input("ENTER USERNAME", '',key='1')
		login_pwd = st.text_input("ENTER PASSWORD", '',key='1')
		if check_username(login_usr):
			st.success('User available')
			if st.button('save'):
				st.success('Registered successfully') 

		else:
			st.error('Username already exists')
