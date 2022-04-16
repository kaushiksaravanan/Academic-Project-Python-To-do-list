import random
import streamlit as st
import mysql.connector
import pandas as pd
import time
host_name='localhost'
user_n='root'
pwd='1234'
db='todolist'

def myFunction_runonce():
	mydb = mysql.connector.connect(host=host_name,user=user_n,password=pwd)
	mycursor = mydb.cursor()
		# "CREATE DATABASE IF NOT EXISTS "+db,
	table_creation_queries=[
		"USE "+db,
	"DROP TABLE IF EXISTS TASKS","CREATE TABLE IF NOT EXISTS TASKS(task VARCHAR(60),completed int);"]
	for query in table_creation_queries:
		mycursor.execute(query)
	mydb.close()

# run_once = 0 #comment after 1st run
# if run_once == 0:
#         myFunction_runonce()
#         run_once = 1


#SQL SCHEMEA

#Tasks
#contains task,completed


#got to user's table and delete the certain taks
def delete(task_to_be_deleted):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="DELETE FROM TASKS WHERE task='"+task_to_be_deleted+"';"
	# query="DELETE FROM TASKS WHERE task='hello';"
	Mycursor.execute(query)
	Mydb.commit()
	Mydb.close()
	return True

def add(add):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="INSERT INTO TASKS (task,completed) VALUES ('"+add+"','0');"
	Mycursor.execute(query)
	Mydb.commit()
	Mydb.close()
	return True

def complete_db_update(complete):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="TRUNCATE TABLE TASKS;"
	Mycursor.execute(query)
	# print(complete)
	for to_add in complete:
		query="INSERT INTO TASKS (task,completed) VALUES ('"+to_add+"','1');"
		Mycursor.execute(query)
		Mydb.commit()	
	Mydb.commit()
	Mydb.close()
	return True

def incomplete_db_update(incomplete):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="TRUNCATE TABLE TASKS;"
	Mycursor.execute(query)
	# print(incomplete)
	for to_add in incomplete:
		query="INSERT INTO TASKS (task,completed) VALUES ('"+to_add+"','0');"
		Mycursor.execute(query)
		Mydb.commit()	
	Mydb.commit()
	Mydb.close()
	return True

def getdata():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT * FROM TASKS;")
	t=[]
	res=Mycursor.fetchall()
	for i in res:
		t.append([i[0],i[1]])
	Mydb.close()
	return t

def view():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT * FROM TASKS;")
	res=Mycursor.fetchall()
	print('RESULTS-')
	print(res)
	for i in res:
		print(i)
	print()
	Mydb.close()

def view_tab():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT * FROM TASKS;")
	res=Mycursor.fetchall()
	df=pd.DataFrame(res,columns=['Task name','Completed(1) / Not Completed(0)'])
	Mydb.close()
	return df

def clear():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="TRUNCATE TABLE TASKS;"
	Mycursor.execute(query)	
	Mydb.commit()
	Mydb.close()
	return True

def main():
	# if st.checkbox('Start'):
		st.title("TO-DO LIST")
		st.write('----------------------')
		st.markdown('## TASKS')
		incomplete=[]
		complete=[]	
		d={}	
		for i in getdata():
			if i[1]=='0' or i[1]==0:
				key_gen=random.randrange(0,100)
				# while key_gen not in d:
				# 	key_gen=random.randrange(0,100)
				try:
					d[key_gen]=i[0]
				except:
					key_gen=random.randrange(100,200)
					d[key_gen]=i[0]
				agree = st.checkbox(i[0])
				if agree:
					complete.append(i[0])
				else:	
					incomplete.append(i[0])
			if i[1]=='1'  or i[1]==1:
				complete.append(i[0])

		# print(complete,incomplete)
		#reverse the order od asking fo tasks

		# st.write('----------------------')
		# st.markdown('## Manipulate')


		todelete_toadd=st.text_input('Enter task name to manipluate')
		col1, col2 = st.columns([16,8])
		with col1:
			if st.button('Save state'):
				# state_run:
					st.markdown('## *COMPLETED TASKS ARE:*')
					for i in complete:
						k='* '
						k+=i
						st.markdown(k)
					complete_db_update(complete)
					st.markdown('## *INCOMPLETE TASKS ARE:*')
					for i in incomplete:
						k='* '
						k+=i
						st.markdown(k)
					incomplete_db_update(incomplete)
		with col2:
			if st.button('Insert task'):
				if len(todelete_toadd)>0:
					try:
						add(todelete_toadd)
						complete=[]
						incomplete=[]
						for i in getdata():
							if i[1]=='0' or i[1]==0:
									incomplete.append(i[0])
							if i[1]=='1'  or i[1]==1:
								complete.append(i[0])
						complete_db_update(complete)
						incomplete_db_update(incomplete)
						st.success('Successfully added')
						# Goto state_run;
					except:
						st.error('Retry')
				else:
					st.error('Empty')
			if st.button('Delete task'):
				if len(todelete_toadd)>0:
					try:
						delete(todelete_toadd)
						complete=[]
						incomplete=[]
						for i in getdata():
							if i[1]=='0' or i[1]==0:
									incomplete.append(i[0])
							if i[1]=='1'  or i[1]==1:
								complete.append(i[0])
						complete_db_update(complete)
						incomplete_db_update(incomplete)
						st.success('Successfully removed')
						# Goto state_run;
					except:
						st.error('Retry')
				else:
					st.error('Empty')
		# with col3:
		if st.button('Clear All'):
				if clear():
					st.success("Successfully cleared all tasks")
				else:
					st.error('Try clearing again')
		# with col4:
		st.write('----------------')
		if st.button('view all data in terminal'):
				view()
		# with col5:
		if st.button('View data as a table'):
				df=view_tab()
				st.table(df)
main()
