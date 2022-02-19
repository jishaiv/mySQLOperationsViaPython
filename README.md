# mySQLOperationsViaPython

Basic tasks invloved in this project :

1. Implement basic sql operations dynamically by using python . 
2. Let the user choose the databse , operations, and he should be able to perform create, insert, update ,print data and delete operation on any table . 
3. Create separate functions for CREATE, UPDATE ,INSERT, DELETE and SELECT
5. Notify the user by nail after each of these operations. user email ids for respective operation  are available in a csv file. 
6. Implement logging 

Implementation : 

1. User has givern th eoption to choose any of the following options: CREATE, INSERT,UPDATE ,DELETE and FETCH data .
2. A class is created for these operationas and for each operation, one function is made inside the class.
3. Based on user selection specific function will be called from main. 
4. CREATE : ---> User can enter table name , column numbers , column name, datatype and contraints for each of the column . The table will be created as per the entered                     
             inputs. If the table already exists in the db , user will be asked to procced with another name , or to terminate the create operation.

5.INSERT :  ---> Usr can enter table name . The prgramme will ask the mode of insert. Two options were given. 1. input from csv. 2. manual input by the user  
                
                ---> 1. input from csv : THe user will be prompted to choose the csv file from system. the values from csv will be inserted into the db table. 
                
                ---> 2. Manual input : User will be asked to enter values for each of the column. Those values will be inserted into the the table.
                 

6.UPDATE:----> User can enter the table name ,the program will ask the update conditions (column name and value) ,and the column which needs to be updated ,and the value.
  

7.DELETE :---> Two options were given for delete. 1. To delete all the records. 2. To delete based on condition. 

             ---> All the records will be deleted if first option is chosen by the user.
             
             ----> Condition column and value will be asked for second option, and specfic row(s) can be deleted based on user input
             
 8.PRINT   ----> This method enable to view data present in a particular table. table name is passing as an arguement
 
 9.SENT MAIL :--> After each of the operation (except print) , a mail will be sent to the responsible person , saying that particular operation has performed on table. 
 
                  ---> Mail ids and operations were stored as csv file , which will be fetched by the program. 
              
10. User has given the chance to continue/terminate after each of the operation . Program will terminate if he domt want to continue. 

11. Logging is implemented to ease the tracking purpose. 

12. Eception were catched by using try-catch-finally block 

13. mysql.connector is used for establishing connection with the databse                     




             

        





