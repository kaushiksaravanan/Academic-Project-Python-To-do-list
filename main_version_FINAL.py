import streamlit as st
import mysql.connector
import pandas as pd

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
	print(query)
	# query="DELETE FROM TASKS WHERE task='hello';"
	Mycursor.execute(query)
	Mydb.commit()
	Mydb.close()
	return True

def add(add):
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="INSERT INTO TASKS (task,completed) VALUES ('"+add+"','0');"
	print(query)
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
		print(query)
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
		print(query)
		Mycursor.execute(query)
		Mydb.commit()	
	Mydb.commit()
	Mydb.close()
	return True

def getdata():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	Mycursor.execute("SELECT * FROM TASKS;")
	print('SELECT * FROM TASKS;')
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
	print('SELECT * FROM TASKS;')
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
	print('SELECT * FROM TASKS;')
	res=Mycursor.fetchall()
	df=pd.DataFrame(res,columns=['Task name','Completed(1) / Not Completed(0)'])
	Mydb.close()
	return df

def check():
	st.write('TASKS')
	complete=[]
	incomplete=[]
	for i in getdata():
			if i[1]=='0' or i[1]==0:
				
				agree = st.checkbox(i[0])
				if agree:
					i[0]=str(i[0])
					i[0]='~~'+i[0]+'~~'
					complete.append(i[0])
				else:	
					incomplete.append(i[0])
			if i[1]=='1'  or i[1]==1:
				i[0]=str(i[0])
				i[0]='~~'+i[0]+'~~'
				complete.append(i[0])
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

def clear():
	Mydb = mysql.connector.connect (host=host_name, user=user_n,password=pwd,database=db)
	Mycursor=Mydb.cursor()
	query="TRUNCATE TABLE TASKS;"
	print(query)
	Mycursor.execute(query)	
	Mydb.commit()
	Mydb.close()
	return True

def main():
		st.title("TO-DO LIST")
		st.write('----------------------')
		st.markdown('## TASKS')
		incomplete=[]
		complete=[]

		todelete_toadd=st.text_input('Enter task name to manipluate')
		col1, col2 = st.columns([16,8])
		with col1:
			# check()
			if st.button('Insert task'):
				if len(todelete_toadd)>0:
					try:
						add(todelete_toadd)
						st.success('Successfully added')
					except:
						st.error('Retry')
				else:
					st.error('Empty')
			if st.button('Delete task'):
				if len(todelete_toadd)>0:
					try:
						delete(todelete_toadd)
						st.success('Successfully removed')
					except:
						st.error('Retry')
				else:
					st.error('Empty')
			check()
		st.write('----------------')
		if st.button('Clear All'):
				if clear():
					st.success("Successfully cleared all tasks")
				else:
					st.error('Try clearing again')
		if st.button('view all data in terminal'):
				view()
		if st.button('View data as a table'):
				df=view_tab()
				st.table(df)
main()
