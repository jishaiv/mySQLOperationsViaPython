""" This file is last updated on 18-Feb 2022
@author : jisha.iv"""

import mysql.connector
import pandas as pd
from mysql.connector import (connection)
from mysql.connector import errorcode
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import csv
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class mysqlOperations:
    """
    This class is created to demonstate various mysql operations in python
    """
    def __init__(self,dbname):
        self.dbname=dbname
        self.my_connection = None
        try:
            self.my_connection = connection.MySQLConnection(user='dhoni', password='dhoni07', host='127.0.0.1',
                                         database=dbname)  #connecting to the databse
            self.mycursor = self.my_connection.cursor()    #creating cursor object
            logging.info("DB Connection established successfully")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.critical("Incorrect credentials entered for db connection, program terminated")
                # print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # print("Database does not exist")
                logging.critical("Wrong db name entered , program terminated ")
                # print(err)
            else:
                # print(err)
                logging.critical(err)

    def create_table(self):
        """
        This method is created to demonstrate  mysql create table operations via python
        """
        try:
            while True:
                table_name=input("Enter the table name to create : ") #getting the table name from the user
                query="""SHOW TABLES"""  #query to fetch all the tablenames available in the db
                self.mycursor.execute(query)
                all_tables = self.mycursor.fetchall()  #this variable contain all the tables available in the db.
                for i in all_tables:
                    str_i = ''.join(i)
                    if str_i == table_name: #checking if the entered table is present in the database
                        choice=input(("Sorry !! Table  already exists in the database , do you want to create table with new name ? y/n \n")) #giving a chance for the user to continue with another table name if needed
                        break  #exit from forloop
                    else:
                        continue  #continue for loop
                else:
                    no_column=int(input("Please enter the number of columns : ")) #getting column number from user
                    query_base="""CREATE TABLE  {}(""".format(table_name) #table creation base query
                    for i in range(no_column):
                        column_i=input("Enter the details of column no {} : Enter columnname datatype constraints separated by space: ".format(i+1)) #getting the column details from user
                        query_base=query_base+column_i+"," #adding column fields to base query
                    query_base=query_base[:-1] #Removing the last entry(,) from string
                    query=query_base+")" #final table creation query
                    self.mycursor.execute(query) #create query execution
                    logging.info("{x} table created successfully in {y} database".format(x=table_name,y=self.dbname)) #logging successful message
                    self.send_mail("Create",table_name,self.dbname) #calling send mail to notify about table creation
                    choice=""
                if choice.upper() == "Y":  #checking user decision whether to proceed with table creation or not
                    continue # continue while loop
                elif choice.upper() == "N":
                    logging.info("Table creation operation is terminated by the user as the entered table name already exists in {} db".format(self.dbname)) #logging info
                    break  #break while
                else:
                    break #break while
        except Exception as e:
            logging.error("Error occured during table creation ") #logging error
            logging.error(e)
    def insert_table(self):
        """
        This method is created to demonstate  mysql insert table operations in python
        """
        try:
            table_name=input("Enter the table name to insert values :") #This variable stores user input value of table for insert operation
            query1="""SELECT * FROM {}""".format(table_name) #this is executed for getting table column names
            self.mycursor.execute(query1) #executing query
            data = self.mycursor.fetchall()
            num_fields = len(self.mycursor.description) #cursor.description  will give column metadata as list . first entry is column name. storing length in variable
            columns_name= [i[0] for i in self.mycursor.description] #getting column name(first element) from list
            logging.info("Successfully extracted the column name from {} table".format(table_name)) #logging info
            queryBase = "INSERT INTO {} values (%s)".format(table_name) #base query for insert data
            final_query = queryBase %(",".join('%s' for i in range(0, num_fields))) # formating with as many fields as required
            user_choice=int(input("Please select the  input method : \n 1. csv file \n 2. user input \n")) #user choice of input method (csv/user input) saving here
            if user_choice == 1: # insert with csv starts here
                root = tkinter.Tk()
                root.withdraw()
                tkinter.messagebox.showinfo("File ","Please select the file containing data")
                input_file = filedialog.askopenfilename() #asking the user to select the file containing data
                with open(input_file,'r') as fin:
                    csvfile = csv.reader(fin, delimiter=",") #reading csv file
                    headings = next(csvfile) #omitting the header row as that is not required
                    # all_value=[]
                    for row in csvfile:
                        # print(row)
                        self.mycursor.execute(final_query,row)
                print("Values inserted into the table successfully!!")
                logging.info("Values inserted from {x} csv file to {y} table successfully".format(x=input_file,y=table_name)) #loging successful message
                self.send_mail("Insert") #calling sending mail function
                self.print_data(table_name) #Printing the data to verify insert operation
            elif user_choice == 2: #insert with user input starts here
                all_value = []
                tup = ()
                for i in range(len(columns_name)):
                    value=input("Enter value for {}: ".format(columns_name[i])) #getting column entries one by one using for loop
                    tup = tup + (value,) #making tuple of values
                all_value.append(tup) #adding tuple to list (input format should list of tuples)
                self.mycursor.executemany(final_query,all_value) #executing the insert query
                logging.info("Values inserted into {x} table successfullu using manual input method ".format(x=table_name)) #Logging successful message
                self.send_mail("Insert",table_name,self.dbname) #Calling send email function
                self.print_data(table_name) #Printing the data to verify insert operation
            else:
                logging.info("Invalid input received for input method inside insert operation")

        except Exception as e:
            logging.critical("Error occured during inserting data into table") #logging error
            logging.critical(e) #logging error

    def print_data(self,table):
        """
        This method is created to demonstate  mysql select table operations in python
        """
        try:
            query = """SELECT * FROM {}""".format(table) #Query to fetch data
            self.mycursor.execute(query) #executing query
            data = self.mycursor.fetchall() #fetching value from cursor
            print("Printing the data ......")
            for x in data:
                print(x) #printing the data
        except Exception as e:
            logging.critical("Error while retreiving the data") #logging the error
            logging.critical(e)  #logging the error

    def delete_data(self):
        """
        This method is created to demonstate  mysql delete table operations in python
        """
        try:
            query=""
            input_table=input("Please enter the table name to delete : ")
            criteria=int(input("Enter the criteria to delete  :\n 1. All data \n 2.Based on a column\n")) #asking the user the criteria for deleting
            if criteria == 1:
                query="""DELETE FROM {s}""".format(s=input_table) #query to delete all data
            elif criteria == 2:
                column_name=input("Enter the column name: ") #asking the criteria column
                column_value=input("Enter the value: ") #asking the condition value
                query = """DELETE FROM {s} WHERE {c}={v}""".format(s=input_table,c=column_name,v=column_value) # query for delete based on condition
            else:
                print("Invalid input, Delete operation terminated !!")
                logging.info("Entered invalid input by the user for delete criteria") #logging
            if query != "":
                self.mycursor.execute(query) #executing delete query
                print("Successfully deleted !!")
                logging.info("Successfully deleted the records from table !") #logging successful message
                self.send_mail("Delete",input_table,self.dbname) #calling send mail to send notification after delete operation
                self.print_data(input_table) #printing data to verify delete operation
        except Exception as e:
            logging.critical("Error occured while deleting the record") #logging exception
            logging.critical(e) #logging exception
    def update_table(self):
        """
        This method is created to demonstate  mysql update table operations in python
         """
        try:
            input_table=input("Enter the table name to update : ") #getting table name to update
            update_condition_column=input("Enter the update condition column: ") # getting condition column , ideally primary key column
            update_condition_value=input("Enter the update condition column value: ") #getting the condition value
            update_column=input("Enter the column which need to be updated : ") #getting the column which needs to be updated
            update_column_value=input("Enter the new value for {}: ".format(update_column)) #getting new value
            query = """UPDATE {_a} SET {_b}={_c} WHERE {_d}={_e}""".format(_a=input_table,_b=update_column,_c=update_column_value,_d=update_condition_column,_e=update_condition_value)
            self.mycursor.execute(query) #executing query
            print("Table updated successfully !!")
            logging.info("Table updated successfully !!") #logging the successful message as info
            self.send_mail("Update",input_table,self.dbname) #calling send mail function to notify successful update operation
            self.print_data(input_table)#Printing the data to verify update operation
        except Exception as e:
            logging.critical("Error occured while updating the record") #logging the error
            logging.critical(e)

    def send_mail(self,op_code,table_name,db_name):
        """
        This method is created to demonstate  sending mail after  each crud operations
        """
        try:
            email_df=pd.read_csv("email_for_crud.csv") #reading the csv file containing email corresponding to each CRUD operation
            for i in range(len(email_df)):
                if email_df.iloc[i,0].upper() == op_code.upper(): #checking the codes
                    toaddr=email_df.iloc[i,1] #getting email for corresponding operation
                    username = toaddr.split("@")[0] #getting username
            fromaddr = "jishaiv23@gmail.com"
            msg = MIMEMultipart() # instance of MIMEMultipart
            msg['From'] = fromaddr # storing the senders email address
            msg['To'] = toaddr  # storing the receivers email address
            msg['Subject'] = "{x} Operation is successfully performed!!".format(x=op_code,y=table_name,z=db_name) #setting subject line
            body = "Hi {name}, \n{x} operation is successfully performed on {y} table of {z} database \n".format(x=op_code,y=table_name,z=db_name,name=username) #setting body
            msg.attach(MIMEText(body, 'plain')) #attaching body
            s = smtplib.SMTP('smtp.gmail.com', 587) # creates SMTP session
            s.starttls() # start TLS for security
            with open("password.txt","r") as file_obj:  #opening password file
                password=file_obj.read()
            s.login(fromaddr,password)  # Authentication
            text = msg.as_string() # Converts the Multipart msg into a string
            s.sendmail(fromaddr, toaddr, text) # sending the mail
            s.quit() # terminating the session
        except Exception as e:
            print("Error occured while sending mail to the user after the {} operation".format(op_code))
            print(e)
            logging.critical("Error occured while sending mail to the user after the {} operation".format(op_code)) #logging the error
            logging.critical(e) #logging the error

    def commit_close(self):
        """
                This function is created for closing the db connection
                         """
        try:
            if self.my_connection != None: #checking if there connection is open
                self.my_connection.commit() #commiting changes
                self.my_connection.close() #closing connection
                logging.info("DB connection closed successfully . ")  # logging the successful message
        except Exception as e:
            logging.critical("Error occured while closing db connection ")  # logging the error if occured
            logging.critical(e)


def main():

    logging.basicConfig(filename='mysqlCrudOperationsViaPython.log',
                        encoding='utf-8',
                        filemode='a',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt="%Y-%m-%d:%H-%M-%S",
                        level=logging.DEBUG
                        ) # log file basic configuration
    try:
        dbname= input("Enter the database name : ") #getting database name from the user
        my_sql=mysqlOperations(dbname) # creating instance for mysqlOperations class
        if my_sql.my_connection != None: #checking if connection is open
            while True :
                operation = int(input(
                    "Please choose the db operation to be performed : \n 1. Create Table \n 2. Update Table \n 3. Insert Table \n 4. Fetch Data From Table \n 5.Delete data \n")) #asking the user th eoperation to be performed
                if operation == 1:
                    my_sql.create_table() #calling create table function
                elif operation == 2:
                    my_sql.update_table()  #calling update table function
                elif operation == 3:
                    my_sql.insert_table()  #calling insert table function
                elif operation == 4:
                    input_table=input("Enter the table name : ") #getting the table name for printing
                    my_sql.print_data(input_table)  #calling print table function
                elif operation ==5:
                    my_sql.delete_data() #calling delete table function

                else:
                    print("Invalid Selection !!")
                    logging.critical("Invalid input for operation selection, user entered {}".format(operation)) #logging the invlid input from user
                choice=input("Do you want to continue with a new operation: Y/N \n ") #asking the user to continue with new operation
                if choice.upper() == "Y":
                    continue
                else:
                    break

    except Exception as e:
        logging.critical(e)
    finally:
        my_sql.commit_close() #calling the function to commit the chnages and closing the db connection

if __name__=="__main__":
    main()
