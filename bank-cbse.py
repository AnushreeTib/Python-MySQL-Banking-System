import mysql.connector as mcon
from forex_python.converter import CurrencyRates
from matplotlib import pyplot as plt
import numpy as np

con=mcon.connect(host='localhost',user='root',password='Seldomtalk',buffered=True)
cur=con.cursor()
cur.execute("create database if not exists BankSystem")
cur.execute("use BankSystem")
cur.execute("create table if not exists bank_sys(name varchar(20), cust_ID int(6), password varchar(10), acc_no varchar(15) primary key, sex varchar(2), balance int(10) default null)")
con.commit()
cur.execute("create table if not exists loan_system(loan_ID varchar(6) PRIMARY KEY, amt int(15), emp_stat varchar(10), income int(10), mar varchar(15), y_n varchar(20))")
con.commit()
choice=None

while choice!=0:
    print("1. CREATE ACCOUNT")
    print("IF YOU ALREADY HAVE AN ACCOUNT:")
    print("2. DEPOSIT CASH")
    print("3. WITHDRAW CASH")
    print("4. CONVERT TO USD") 
    print("5. CONVERT TO POUND")
    print("6. CHANGE PASSWORD")
    print("7. APPLY FOR A LOAN")
    print("8. VIEW YOUR ACCOUNT DETAILS")
    print("{FOR ADMIN PUPOSES ONLY: 9. VIEW USER DETAILS}")
    #FOR ADMIN PURPOSE ONLY
    # 8. VIEW ALL RECORDS
    print("0. EXIT")
    choice=int(input("ENTER CHOICE: "))
    
#CREATES AN ACCOUNT
    if choice==1:
        name=input("ENTER NAME: ")
        cust_ID=int(input("ENTER ID NUMBER: "))
        password=input("ENTER PASSWORD: ")
        acc_no=input("ENTER ASSIGNED ACCOUNT NUMBER: ")
        sex=input("ENTER GENDER M/F: ")
        balance=int(input("ENTER AMOUNT BEING DEPOSITED: "))
        query="insert into bank_sys(name,cust_ID,password,acc_no,sex,balance) values('{}',{},'{}','{}','{}',{})".format(name,cust_ID,password,acc_no,sex,balance)
        cur.execute(query)
        con.commit()
        print(" ## DATA SAVED ## ")
        choice=1
   
#DEPOSITS AMOUNT INTO A USER'S ACCOUNT    
    elif choice==2:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE EXIT(0) OR CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=2
            else:
                x_dep=int(input("ENTER AMOUNT BEING DEPOSITED: "))
                query="update bank_sys set balance=balance+{} where acc_no='{}' and password='{}'".format(x_dep,x_user,x_pass)
                cur.execute(query)
                con.commit()
                query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                cur.execute(query)
                result=cur.fetchall()
                print("YOUR CURRENT BALANCE IS: ",result)
                print("## IF YOU HAVE ANY DOUBTS/QUESTIONS, PLEASE CONTACT THE ADMIN. THANK YOU FOR YOUR BUSINESS. ##")

#WITHDRAWS AMPUNT FROM USER'S ACCOUNT                
    elif choice==3:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=3
            else:
                x_wdr=int(input("ENTER AMOUNT BEING WITHDRAWN: "))
                query="update bank_sys set balance=balance-{} where acc_no='{}'".format(x_wdr,x_user)
                cur.execute(query)
                if cur.rowcount==0:
                    print("## REQUESTED TRANSACTION IS INVALID. PLEASE ENTER A VALID AMOUNT OR CONTACT THE ADMIN FOR ANY ENQUIRES. ##")
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    print("## IF YOU HAVE ANY DOUBTS/QUESTIONS, PLEASE CONTACT THE ADMIN. THANK YOU FOR YOUR BUSINESS. ##")
                    query="update bank_sys set balance=balance+{} where acc_no='{}' and password='{}'".format(x_wdr,x_user,x_pass)
                    cur.execute(query)
                    con.commit()
                    choice=3
                else:
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    print("## THANK YOU FOR YOUR BUSINESS ##")

#CONVERSION TO DOLLARS                
    elif choice==4:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cursor = con.cursor(buffered=True)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=4
            else:
                x_amt=int(input("ENTER AMOUNT(INR) TO BE EXCHANGED TO USD: "))
                c = CurrencyRates()                                                 
                rate = c.get_rate('INR', 'USD')                                     
                print("THE CURRENT EXCHANGE RATE IS", rate) 
                value = float(("{0:.2f}").format(float(x_amt)*rate))                
                print("MAXIMUM WITHDRAWAL OF USD POSSIBLE FROM YOUR ACCOUNT IS: $","\u20ac " + str(value))
                query="update bank_sys set balance=balance-{} where acc_no='{}'".format(x_amt,x_user)
                cur.execute(query)
                con.commit()
                if cur.rowcount==0:
                    print("## REQUESTED TRANSACTION IS INVALID. PLEASE ENTER A VALID AMOUNT OR CONTACT THE ADMIN FOR ANY ENQUIRES. ##")
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    value = float(("{0:.2f}").format(float(x_amt)*rate))                
                    print("MAXIMUM WITHDRAWAL OF USD POSSIBLE FROM YOUR ACCOUNT IS: $","\u20ac " + str(value))
                    print("## IF YOU HAVE ANY DOUBTS/QUESTIONS, PLEASE CONTACT THE ADMIN. THANK YOU FOR YOUR BUSINESS. ##")
                    query="update bank_sys set balance=balance+{} where acc_no='{}' and password='{}'".format(x_amt,x_user,x_pass)
                    cur.execute(query)
                    con.commit()
                    choice=4
                else:
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    print("## THANK YOU FOR YOUR BUSINESS ##")
                
#CONVERSION TO POUNDS 
    elif choice==5:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=5
            else:
                x_amt=int(input("ENTER AMOUNT(INR) TO BE EXCHANGED TO POUND(EUR): "))
                c = CurrencyRates()                                                 
                rate = c.get_rate('INR', 'GBP')  
                print("THE CURRENT EXCHANGE RATE IS: ",rate) 
                value = float(("{0:.2f}").format(float(x_amt)*rate))                
                print("MAXIMUM WITHDRAWAL OF USD POSSIBLE FROM YOUR ACCOUNT IS: $","\u20ac " + str(value))
                query="update bank_sys set balance=balance-{} where acc_no='{}' and password='{}'".format(x_amt,x_user,x_pass)
                cur.execute(query)
                con.commit()
                if cur.rowcount==0:
                    print("## REQUESTED TRANSACTION IS INVALID. PLEASE ENTER A VALID AMOUNT OR CONTACT THE ADMIN FOR ANY ENQUIRES. ##")
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    c = CurrencyRates()                                                 
                    rate = c.get_rate('INR', 'GBP')    
                    value = float(("{0:.2f}").format(float(result)*rate))                
                    print("MAXIMUM WITHDRAWAL OF GBP POSSIBLE FROM YOUR ACCOUNT IS: $","\u20ac " + str(value))
                    print("## IF YOU HAVE ANY DOUBTS/QUESTIONS, PLEASE CONTACT THE ADMIN. THANK YOU FOR YOUR BUSINESS. ##")
                    query="update bank_sys set balance=balance+{} where acc_no='{}' and password='{}'".format(x_amt,x_user,x_pass)
                    cur.execute(query)
                    con.commit()
                    choice=5
                else:
                    query="select balance from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                    cur.execute(query)
                    result=cur.fetchall()
                    print("YOUR CURRENT BALANCE IS: ",result)
                    print("## THANK YOU FOR YOUR BUSINESS ##")
    
#FOR UPDATING A USER'S PASSWORD    
    elif choice==6:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR CURRENT PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=6
            else:
                n_pass=input("ENTER YOUR NEW PASSWORD: ")
                n_conf=input("CONFIRM YOUR NEW PASSWORD: ")
                if n_pass==n_conf:
                    query="update bank_sys set password='{}' where acc_no='{}'".format(n_pass,x_user)
                    cur.execute(query)
                    con.commit()
                    print("## YOUR PASSWORD HAS BEEN UPDATED ##")
                    print("## THANK YOU FOR YOUR BUSINESS ##")
                else:
                    print("YOUR ENTRIES DO NOT MATCH. PLEASE TRY AGAIN.")
                    choice=6

#PREDICTS IF A USER IS ELIGIBLE FOR A LOAN    
    elif choice==7:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=7
            else:
                loan_ID=input("ENTER LOAN ID: ")
                amt=int(input("ENTER LOAN AMOUNT: "))
                emp_stat=input("ENTER EMPLOYMENT STATUS (EMPOYED/ NOT EMPLOYED): ")
                income=int(input("ENTER ANNUAL INCOME: "))
                mar=input("ENTER MARITAL STATUS: ")
                y_n=input("granted? : ")
                query="insert into loan_system(loan_ID,amt,emp_stat,income,mar,y_n) values ('{}',{},'{}',{},'{}','{}')".format(loan_ID,amt,emp_stat,income,mar,y_n)
                cur.execute(query)
                con.commit()
                print(" ## DATA SAVED ## ")                
               
                credit=0
                term=[6,12,18,24,30,36]
                if(emp_stat == "EMPLOYED"):
                    credit+=1
                if(mar == "MARRIED"):
                    credit+=1
                interest=0
                if(amt < 1000000):
                    interest=0.13
                elif( amt < 2000000):
                    interest= 0.12
                elif( amt < 3000000):
                    interest= 0.11
                elif(amt < 4000000):
                    interest = 0.1
                elif( amt < 5000000):
                    interest = 0.09
                else:
                    interest = 0.08
                print( " LOANS CAN BE PAID BACK AS PER 6 PLANS : 6 MONTH, 12 MONTHS, 18 MONTHS, 24 MONTHS, 30 MONTHS, 36 MONTHS ")
                print(" THE FOLLOWING GRAPH CHARTS THE AMOUNT THAT YOU ARE REQUIRED TO PAY PER MONTH, ACCORDING TO THE EACH PLAN ")

                plt.xlabel("TERM (MONTHS)")
                plt.ylabel("AMOUNT TO BE PAID PER MONTH")
                plt.bar(term,[((amt+interest*amt)//i) for i in term])
                plt.xticks(np.arange(0, 40, 6))
                plt.yticks(np.arange(0, 10000, 500))
                plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
                plt.show() 
                
                term_choice=0
                while(True):
                    term_choice = int(input("PLEASE SELECT THE PLAN THAT IS SIUTABLE FOR YOU (6,12,18,24,30,36): "))
                    if( term_choice in term ):
                        break
                    else:
                        term_choice=int(input("INVALID. PLEASE SELECT BETWEEN THE 6,12,24,36 MONTH PLANS"))
                if credit >= 1 and (income * (term_choice//12) >= (amt + interest * amt * term_choice)):
                    print("CONGRATULATIONS, LOAN APPROVED. PLEASE KEEP UP TO DATE WITH YOUR MONTHLY REPAYMENT SCHEDULE. ")
                    print("## THANK YOU FOR YOUR BUSINESS ##")   
                    query="update loan_system set y_n='GRANTED'"
                    cur.execute(query)
                    con.commit()
                else:
                    print("YOUR REQUEST HAS BEEN DENIED. PLEASE TRY AGAIN WITH A BETTER TERM PLAN.") 
                    print("## THANK YOU FOR YOUR BUSINESS ##")

#FOR ONE USER TO VIEW RECORDS
    elif choice==8:
        x_user=input("PLEASE ENTER YOUR ACCOUNT NUMBER: ")
        query="select acc_no from bank_sys where acc_no='{}'".format(x_user)
        cur.execute(query)
        result=cur.fetchall()
        if cur.rowcount==0:
            print(" ## THIS ACCOUNT DOES NOT EXIST ## ")
            print(" ## TO CONTINUE, PLEASE CREATE AN ACCOUNT(1)  ##")
            choice=1
        else:
            x_pass=input("ENTER YOUR PASSWORD: ")
            query="select password from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
            cur.execute(query)
            result=cur.fetchall()
            if cur.rowcount==0:
                print("## INCORRECT PASSWORD. PLEASE TRY AGAIN ##")
                choice=8
            else:
                query="select * from bank_sys where acc_no='{}' and password='{}'".format(x_user,x_pass)
                cur.execute(query)
                result=cur.fetchall()
                print("%5s"%"NAME","%15s"%"ID NUM`BER","%10s"%"PASSWORD","%15s"%"ACCOUNT NUMBER","%10s"%"GENDER","%10s"%"BALANCE")
                for row in result:
                    print("%5s"%row[0],"%15s"%row[1],"%10s"%row[2],"%15s"%row[3],"%10s"%row[4],"%10s"%row[5])

#TO VIEW ALL RECORDS (ADMIN ONLY)                   
    elif choice==9:
        query="select * from bank_sys "
        cur.execute(query)
        result=cur.fetchall()
        print("%15s"%"NAME","%15s"%"ID NUMBER","%10s"%"PASSWORD","%15s"%"ACCOUNT NUMBER","%10s"%"GENDER","%10s"%"BALANCE")
        for row in result:
           print("%15s"%row[0],"%15s"%row[1],"%10s"%row[2],"%15s"%row[3],"%10s"%row[4],"%10s"%row[5])
        query="select * from loan_system"
        cur.execute(query)
        result=cur.fetchall()
        print("%5s"%"LOAN ID","%15s"%"AMOUNT","%10s"%"EMPLOYMENT STATUS","%15s"%"INCOME","%10s"%"MARITAL STATUS","%5s"%"YES/NO")
        for row in result:
           print("%5s"%row[0],"%15s"%row[1],"%10s"%row[2],"%15s"%row[3],"%10s"%row[4],"%10s"%row[5])
    
#EXIT      
    elif choice==0:
       con.close()
       print("## EXIT ##")
    else:
       print("##INVALID CHOICE##")
       choice=0
                
                
                
                
                
                
                
                
                