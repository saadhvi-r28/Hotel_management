import mysql.connector
import random
# GLOBAL VARIABLES DECLARATION
myConnnection =""
cursor=""
roomrent =0
restaurentbill=0
totalAmount=0
cid=""
#MODULE TO CHECK MYSQL CONNECTIVITY
def MYSQLconnectionCheck ():
    myConnection=mysql.connector.connect(host="localhost",user="root",passwd="Saadhvir@28!")
    if myConnection:
        print("\n CONGRATULATIONS ! YOUR CONNECTION HAS BEEN ESTABLISHED !")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
        cursor.execute("COMMIT")
        cursor.close()
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")
#MODULE TO ESTABLISHED MYSQL CONNECTION
def MYSQLconnection():
    global myConnection
    global cid
    myConnection=mysql.connector.connect(host="localhost",user="root",passwd="Saadhvir@28!", database="school")
    if myConnection:
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")
        myConnection.close()

def userEntry():
    global cid
    if myConnection:
        cursor=myConnection.cursor()
        createTable ="CREATE TABLE IF NOT EXISTS C_DETAILS(CID VARCHAR(20),C_NAME VARCHAR(30),C_ADDRESS VARCHAR(30),C_AGE VARCHAR(30),C_COUNTRY VARCHAR(30) ,P_NO VARCHAR(30),C_EMAIL VARCHAR(30))"
        cursor.execute(createTable)
        cid = input("Enter Customer Identification Number : ")
        name = input("Enter Customer Name : ")
        address = input("Enter Customer Address : ")
        age= input("Enter Customer Age : ")
        nationality = input("Enter Customer Country : ")
        while True:
            phoneno= input("Enter Customer Contact Number : ")
            if len(phoneno)==10:
                break
            else:
                print("Please enter a 10-digit phone number")
                continue
        email = input("Enter Customer Email : ")
        sql = "INSERT INTO C_Details VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values= (cid,name,address,age,nationality,phoneno,email)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        print("\nNew Customer Entered In The System Successfully !")
        cursor.close()
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")

def roomRent():
    global cid
    customer=searchCustomer()
    if customer:
        global roomrent
        if myConnection:
            cursor=myConnection.cursor()
            createTable ="CREATE TABLE IF NOT EXISTS BOOKING_RECORD(CID VARCHAR(20),CHECK_IN DATE ,CHECK_OUT DATE)"
            cursor.execute(createTable)
            checkin=input("\nEnter Customer CheckIN Date [ YYYY-MM-DD ] : ")
            checkout=input("\nEnter Customer CheckOUT Date [ YYYY-MM-DD ] : ")
            ci=checkin.split('-')
            co=checkout.split('-')
            if int(co[0])>=int(ci[0]):
                y=int(co[0])-int(ci[0])
                if int(co[1])>=int(ci[1]):
                    m=int(co[1])-int(ci[1])
                    if int(co[2])>=int(ci[2]):
                        d=int(co[2])-int(ci[2])
                        sql= "INSERT INTO BOOKING_RECORD VALUES(%s,%s,%s)"
                        values= (cid,checkin,checkout)
                        cursor.execute(sql,values)
                        cursor.execute("COMMIT")
                        cursor=myConnection.cursor()
                        createTable ="CREATE TABLE IF NOT EXISTS ROOM_RENT(CID VARCHAR(20),ROOM_CHOICE INT,NO_OF_DAYS INT,ROOMNO INT ,ROOMRENT INT)"
                        cursor.execute(createTable)
                        print ("\n ##### We have The Following Rooms For You #####")
                        print (" 1. Ultra Royal	> 10000 Rs.")
                        print (" 2. Royal	> 5000 Rs. ")
                        print (" 3. Elite	> 3500 Rs. ")
                        print (" 4. Budget	> 2500 Rs. ")
                        roomchoice =int(input("Enter Your Option : "))
                        roomno=random.randint(1,1000)
                        noofdays=y*365+m*30+d
                        if roomchoice==1:
                            roomrent = noofdays * 10000
                            print("\nUltra Royal Room Rent : ",roomrent)
                        elif roomchoice==2:
                            roomrent = noofdays * 5000
                            print("\nRoyal Room Rent : ",roomrent)
                        elif roomchoice==3:
                            roomrent = noofdays * 3500
                            print("\nElite Royal Room Rent : ",roomrent)
                        elif roomchoice==4:
                            roomrent = noofdays * 2500
                            print("\nBudget Room Rent : ",roomrent)
                        else:
                            print("Sorry ,May Be You Are Giving Me Wrong Input, Please Try Again !!! ")
                            return
                        sql= "INSERT INTO ROOM_RENT VALUES(%s,%s,%s,%s,%s)"
                        values= (cid,roomchoice,noofdays,roomno,roomrent,)
                        cursor.execute(sql,values)
                        cursor.execute("COMMIT")
                        print("Thank You , Your Room Has Been Booked For : ",noofdays , "Days" )
                        print("Your room number is: ",roomno)
                        print("Your Total Room Rent is : Rs. ",roomrent)
                        cursor.close()
                    else:
                        print("\nInvalid date")
                else:
                    print("\nInvalid date")
            else:
                print("\nInvalid date")
        else:
            print("\nERROR ESTABLISHING MYSQL CONNECTION !")

def Restaurent():
    global cid
    customer=searchCustomer()
    if customer:
        global restaurentbill
        if myConnection:
            cursor=myConnection.cursor()
            createTable ="CREATE TABLE IF NOT EXISTS RESTAURENT(CID VARCHAR(20),CUISINE VARCHAR(30),QUANTITY VARCHAR(30),BILL VARCHAR(30))"
            cursor.execute(createTable)
            print("1 Vegetarian Combo	> 300 Rs.")
            print("2 Non-Vegetarian Combo	> 500 Rs.")
            print("3 Vegetarian & Non-Vegetarian Combo	> 750 Rs.")
            cursor.execute("SELECT * FROM FOOD")
            c=4
            item=cursor.fetchall()
            for i in item:
                print(c,i[0],"  >",i[1],"Rs.")
                c+=1
            choice_dish = int(input("Enter Your Cusine : "))
            quantity=int(input("Enter Quantity : "))
            if choice_dish==1:
                print("\nSO YOU HAVE ORDER: Vegetarian Combo ")
                restaurentbill = quantity * 300
            elif choice_dish==2:
                print("\nSO YOU HAVE ORDER: Non-Vegetarian Combo ")
                restaurentbill = quantity * 500
            elif choice_dish==3:
                print("\nSO YOU HAVE ORDER: Vegetarian & Non-Vegetarian Combo ")
                restaurentbill= quantity * 750
            else:
                print("Sorry ,May Be You Are Giving Me Wrong Input, Please Try Again !!! ")
                return
            sql= "INSERT INTO RESTAURENT VALUES(%s,%s,%s,%s)"
            values= (cid,choice_dish,quantity,restaurentbill)
            cursor.execute(sql,values)
            cursor.execute("COMMIT")
            print("Your Total Bill Amount Is : Rs. ",restaurentbill)
            print("\n\n**** WE HOPE YOU WILL ENJOY YOUR MEAL ***\n\n" )
            cursor.close()
        else:
            print("\nERROR ESTABLISHING MYSQL CONNECTION !")

def totalAmount():
    global cid
    customer=searchCustomer()
    if customer:
        global grandTotal
        global roomrent
        global restaurentbill
        if myConnection:
            cursor=myConnection.cursor()
            createTable ="CREATE TABLE IF NOT EXISTS TOTAL1 (CID CHAR(20), C_NAME CHAR(30), ROOMRENT INT , RESTAURENTBILL INT, TOTALAMOUNT INT)"
            cursor.execute(createTable)
            name = input("Enter Customer Name : ")
            grandTotal=roomrent + restaurentbill
            sql= "INSERT INTO TOTAL1 VALUES(%s,%s,%s,%s,%s)"
            values= (cid,name,roomrent,restaurentbill,grandTotal)
            cursor.execute(sql,values)
            cursor.execute("COMMIT")
            cursor.close()
            print("\n ****CUSTOMER BIILING ****")
            print("\nCUSTOMER NAME   : " ,name)
            print("\nROOM RENT       : Rs. ",roomrent)
            print("\nRESTAURENT BILL : Rs. ",restaurentbill)
            print("_____________________________________")
            print("\nTOTAL AMOUNT	: Rs. ",grandTotal)
            cursor.close()
        else:
            print("\nERROR ESTABLISHING MYSQL CONNECTION !")

def searchCustomer():
    global cid
    if myConnection:
        cursor=myConnection.cursor()
        cid=input("ENTER CUSTOMER ID : ")
        sql="SELECT * FROM C_DETAILS WHERE CID= %s"
        cursor.execute(sql,(cid,))
        data=cursor.fetchall()
        if data:
            for i in data:
                print("Customer ID:", i[0])
                print("Customer Name:", i[1])
                print("Address:",i[2])
                print("Age:",i[3])
                print("Country:",i[4])
                print("Phone Number:",i[5])
                print("Email-id:",i[6])
                return True
        else:
            print("Record Not Found Try Again !")
            return False
        cursor.close()
    else:
        print("\nSomthing Went Wrong ,Please Try Again !")

def cancel():
    global cid
    customer=searchCustomer()
    cursor=myConnection.cursor()
    if customer:
        choice=input("Do you wish to cancel your booking?? (yes/no): ")
        if choice=="yes":
            sql="DELETE FROM C_DETAILS WHERE CID= %s"
            cursor.execute(sql,(cid,))
            cursor.execute("COMMIT")
            sql1="DELETE FROM BOOKING_RECORD WHERE CID= %s"
            cursor.execute(sql1,(cid,))
            cursor.execute("COMMIT")
            sql2="DELETE FROM RESTAURENT WHERE CID= %s"
            cursor.execute(sql2,(cid,))
            cursor.execute("COMMIT")
            sql3="DELETE FROM ROOM_RENT WHERE CID= %s"
            cursor.execute(sql3,(cid,))
            cursor.execute("COMMIT")
            sql4="DELETE FROM TOTAL1 WHERE CID= %s"
            cursor.execute(sql4,(cid,))
            cursor.execute("COMMIT")
            cursor.close()
            print("Room Cancelled Successfully")
        else:
            print("")

def user():
    myConnection = MYSQLconnectionCheck ()
    if myConnection:
        MYSQLconnection ()
        while(True):
            print("""
            1--->ENTER CUSTOMER DETAILS
            2--->CALCULATE ROOM RENT
            3--->CALCULATE RESTAURENT BILL
            4--->DISPLAY CUSTOMER DETAILS
            5--->GENERATE TOTAL BILL AMOUNT DURING CURRENT LOGIN
            6--->CANCEL ROOM
            7--->EXIT\n """)
            choice = int(input("Enter Your Choice: "))
            if choice == 1:
                userEntry()
            elif choice ==2:
                roomRent()
            elif choice ==3:
                Restaurent()
            elif choice ==4:
                searchCustomer()
            elif choice ==5:
                totalAmount()
            elif choice ==6:
                cancel()
            elif choice ==7:
                break
            else:
                print("Sorry, May Be You Are Giving Me Wrong Input, Please Try Again !!!  ")
        else:
            print("\nERROR ESTABLISHING CONNECTION !")

def admin():
    myConnection = MYSQLconnectionCheck ()
    if myConnection:
        MYSQLconnection ()
        cursor=myConnection.cursor()
        cursor.execute("USE school")
        cursor.execute("CREATE TABLE IF NOT EXISTS FOOD(item_name varchar(30),price int)")
        while True:
            print('''
            1--->ADD FOOD ITEMS
            2--->DELETE FOOD ITEMS
            3--->MODIFY FOOD ITEMS
            4--->DISPLAY ALL the FOOD ITEMS\n''')
            ch=int(input("Enter your choice: "))
            if ch==1:
                i1=input("Enter item name to ADD: ")
                p1=int(input("Enter Price: "))
                cursor.execute(f"INSERT INTO FOOD VALUES('{i1}',{p1})")
                print("ADDED SUCCESSFULLY")
                cursor.execute("COMMIT")

            elif ch==2:
                i2=input("Enter FOOD item to DELETE: ")
                cursor.execute("SELECT item_name FROM FOOD")
                f=cursor.fetchall()
                for i in f:
                    for j in i:
                        if j==i2:
                            cursor.execute(f"DELETE FROM FOOD WHERE item_name='{i2}'")
                            print("DELETED SUCCESSFULLY")

            elif ch==3:
                i3=input("Enter item name to MODIFY: ")
                cursor.execute("SELECT item_name FROM FOOD")
                f1=cursor.fetchall()
                for i in f1:
                    for j in i:
                        if j==i3:
                            ch1=int(input("Press 1 to modify item name \nPress 2 to modify price"))
                            if ch1==1:
                                i4=input("Enter new Item Name: ")
                                cursor.execute(f"UPDATE FOOD SET item_name='{i4}' WHERE item_name='{i3}'")
                                print("UPDATED SUCCESSFULLY")
                            elif ch1==2:
                                p2=int(input("Enter new Price: "))
                                cursor.execute(f"UPDATE FOOD SET price='{p2}' WHERE item_name='{i3}'")
                                print("UPDATED SUCCESSFULLY")
                                cursor.execute("COMMIT")

            elif ch==4:
                cursor.execute("SELECT * FROM FOOD")
                f1=cursor.fetchall()
                for i in f1:
                    for j in i:
                        print(j, end="\t")
                    print()
            else:
                break

def login():
    username=input("Enter username: ")
    if username=="Admin":
        password=input("Enter your password: ")
        if password=="Admin@123":
            admin()
        else:
            print("Incorrect Password")
    elif username.isspace() or username=="":
        print("Invalid Username!!")
    else:
        user()
login()
# END OF PROJECT
