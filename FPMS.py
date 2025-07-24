import datetime
import sqlite3
import re

def connect_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
    
    CREATE TABLE IF NOT EXISTS investment(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user TEXT,
                   asset  TEXT,
                   type TEXT,
                   amount REAL,
                   status TEXT,
                   date  TEXT)''') 
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
                   username TEXT PRIMARY KEY ,
                   password TEXT)''')
    
    conn.commit()
    return conn,cursor

def register_user(cursor, conn):
    username = input("Enter username: ")

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        print("Invalid username. Must be 3-20 characters long")
        return None
    
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different one.")
        return None
    
    password = input("Enter password: ")
    
    cursor.execute("INSERT INTO user (username,password) VAlUES(?,?)",(username,password))
    print("User registered successfully!")
    conn.commit()
    return username

def login_user(cursor, conn):
    username = input("Enter username")
    password = input("Enter password")

    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?",(username,password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome {username}! ")
        return username
    else:
        print("Invalid Credentials")
        return None

def auth(cursor,conn):
    while True:
        print(f"\n1. Register \n2. Login \n3. Exit")

        try:
            choose = int(input("Choose(1,2,3) :  "))
        except ValueError:
            print("Invalid number")
            return auth(cursor,conn)


        if choose == 1 :
            user = register_user(cursor,conn)
            if user:
                return user
        elif choose == 2:
            user = login_user(cursor,conn)
            if user:
                return user
        elif choose==3 :
             print("okeyda")
             break


def add_investment(cursor, conn,username):
    
    asset = input("Enter Asset Name (eg: apple stock) ")
    type_ = input(" Enter which type (eg:stock,crypto etc) ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Must be a number.")
        return
    
    date  = datetime.date.today().strftime("%Y-%m-%d")

    cursor.execute('''INSERT INTO investment(user,asset,type,amount,status,date) 
                   VALUES(?,?,?,?,?,?


                   
                   
                   )''',(username,asset,type_,amount,"active",date))
    conn.commit()
    print("Investment Added Succesfully !!")

    
def view_investment(cursor,conn,username):
    cursor.execute("SELECT * FROM investment WHERE user = ?",(username,))
    result = cursor.fetchall()

    if not result:
        print("No Data in table!")
        return
    
    print("ID | Asset | Type | Amount | Status | Date")
    print()
    for i in result:
        print(f"{i[0]} | {i[1]} | {i[2]} | {i[3]} | {i[4]} | {i[5]}")
    print("\n")

def mark_status(cursor,conn,username):
    view_investment(cursor,conn,username)
    id = int(input("Enter the id"))
    cursor.execute(''' UPDATE investment SET status = ? WHERE id=? ''',("Sold",id))
    print("Status Updated!!")

    conn.commit()

def update_investment(cursor,conn,username):
    view_investment(cursor,conn,username)
    list = ["asset","type","amount","status"]
    id = int(input("Enter the id of table to update! :"))

    print("What do you want to update (asset,type,amount,status)")
    field = input("Choose a field to update: ").lower()

    if field not in list:
        print("Invalid choice ! Please choose a valid option")
        return

    if field == "amount":
        try:
            new_value = float(input("Enter new amount: "))
        except ValueError:
            print("Invalid amount. Must be a number.")
            return
    else:
        new_value = input(f"Enter the new value for {field}")

    cursor.execute(f"UPDATE investment SET {field} = ? WHERE id =?",(new_value,id))
    conn.commit()

def delete_investment(cursor,conn,username):
    view_investment(cursor,conn,username)
    id = int(input("Enter the id for delete"))
    cursor.execute("DELETE FROM investment WHERE id = ?",(id,))
    conn.commit()



def main():
    conn, cursor = connect_db()
    username = auth(cursor,conn)

    while True:
        print("Financial Portfolio Management System")
        print("1.ADD INVESTMENT")
        print("2.VIEW PORTFOLIO")
        print("3.MARK SOLD")
        print("4.EDIT INVESTMENT")
        print("5.DELETE INVESTMENT")
        print("6.EXIT")

        try:
            choice = int(input("choose any number 1-6 :"))
            if choice < 1 or choice > 6:
                print("Not Valid Number!")
                continue
        except ValueError:
            print("Please select valid number.")
            continue
        
        if choice == 6:
            print("Exiting the program.")
            break

        
        match choice:
            case 1:
                add_investment(cursor, conn, username)  
            case 2:
                view_investment(cursor, conn, username)
            case 3:
                mark_status(cursor, conn,username)
            case 4:
                update_investment(cursor, conn, username)
            case 5:
                delete_investment(cursor, conn,username)

    conn.close()
    print("Thank you for using the Financial Portfolio Management System!")  
main()