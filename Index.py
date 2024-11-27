#import modules
 
from tkinter import *
import os
import detection
import sendmail
import random
import string
import mysql.connector
import getclases
from tkinter import Tk, Label, Button, filedialog, Entry
import shutil
import os
from history import fetch_and_display_data
import queue
monitor_queue = queue.Queue()
import threading

# Designing window for registration
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin@123",
  database="wildanimal"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()


def start_monitor(username, email):
    monitor_queue.put("start")
    monitor_thread = threading.Thread(target=monitor, args=(username, email, monitor_queue), daemon=True)
    monitor_thread.start()

def stop_monitor():
    monitor_queue.put("stop")


def monitor(username,email,monitor_queue):
    detection.monitor(username,email,monitor_queue)

def admin(username,email,phone):
    global admin_screen
    admin_screen = Toplevel(dashboard)
    admin_screen.title("Register")
    admin_screen.configure(bg="#333333")
    admin_screen.geometry("700x600")
    Label(admin_screen,text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="0", font=("Calibri", 9)).pack()
    global admin_username
    global admin_password
    global classl
    global admin_email
    global admin_phone
    global classl_entry
    global admin_username_entry
    global admin_password_entry
    global admin_email_entry
    global admin_phone_entry
    admin_username = StringVar()
    admin_password = StringVar()
    admin_email=StringVar()
    admin_phone=StringVar()
    classl = StringVar()
    Label(admin_screen, text="Update details", bg="#333333",fg='red',underline=True).pack()
    Label(admin_screen, text="Email *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    admin_email_entry = Entry(admin_screen, textvariable=admin_email, width="30")
    admin_email_entry.pack()

    Label(admin_screen, text="",bg="#333333").pack()
    Label(admin_screen, text="Phone *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    admin_phone_entry = Entry(admin_screen, textvariable=admin_phone, width="30")
    admin_phone_entry.pack()
    Label(admin_screen, text="",bg="#333333").pack()
    Button(admin_screen, text="Update Info", width=10, height=1, bg="blue", command = lambda:update_info(username)).pack()

    Label(admin_screen, text="",bg="#333333").pack()
    Label(admin_screen, text="Change Password",  bg="#333333",fg='red',underline=True).pack()
    Label(admin_screen, text="Password *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    admin_password_entry = Entry(admin_screen,show="*", textvariable=admin_password, width="30")
    admin_password_entry.pack()
    Label(admin_screen, text="",bg="#333333").pack()
    Button(admin_screen, text="Update Info", width=10, height=1, bg="#333333",fg="green", command = lambda:update_password(username)).pack()

    Label(admin_screen, text="",bg="#333333").pack()
    Label(admin_screen, text="Configure Animal Data",  bg="#333333",fg='red',underline=True).pack()
    Label(admin_screen, text="Animal Name                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    classl_entry = Entry(admin_screen, textvariable=classl, width="30")
    classl_entry.pack()
    Label(admin_screen, text="",bg="#333333").pack()
    Button(admin_screen, text="Config and Browse Animal Image", width=10, height=1, bg="#333333",fg="green", command = lambda:browse_file_and_move()).pack()
    
def browse_file_and_move():
    class_name=classl.get()
    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename()
    update_config()
    if file_path:
        # Get the folder name from the entry widget (assuming the user has entered it)
        folder_name = "C:/Users/gangadhara.n/AppData/Local/Programs/Python/Python312/Wild Animal Detection/images"
        # Create the image folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # Move the file to the specified folder
        shutil.move(file_path, os.path.join(folder_name, os.path.basename(file_path)))
        print("File moved successfully to:", os.path.join(folder_name, os.path.basename(file_path)))


def update_info(username):
    email_info=admin_email.get()
    phone_info=admin_phone.get()
    # Insert data into the table
    sql = "UPDATE users SET email = %s, phone = %s WHERE username = %s"
    val = (email_info,phone_info,username)
    mycursor.execute(sql, val)
    # Commit the transaction
    mydb.commit()
    # Print the number of inserted rows
    print(mycursor.rowcount, "record inserted.")
    Label(admin_screen, text="User detail updated", fg="green", font=("calibri", 11)).pack()

def update_config():
    class_name=classl.get()
    cl=getclases.getclases()
    cl.append(class_name)
    with open('classes.txt', 'w') as file:
        for class_n in cl:
            file.write(f"{class_n}\n")

def update_password(username):
    email_info=admin_password.get()
    # Insert data into the table
    sql = "UPDATE users SET password = %s WHERE username = %s"
    val = (email_info,username)
    mycursor.execute(sql, val)
    # Commit the transaction
    mydb.commit()
    # Print the number of inserted rows
    print(mycursor.rowcount, "record inserted.")
    Label(admin_screen, text="Password Updated", fg="green", font=("calibri", 11)).pack()

def history(userid,username,email,phone):
    print(userid)
    fetch_and_display_data(userid)


def dashboard(username,email,phone,userid):
    global dashboard
    main_screen.destroy()
    dashboard = Tk()
    dashboard.configure(bg="#333333")
    dashboard.geometry("700x600")
    dashboard.title("Wild Animal Detection")
    Label(text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 9)).pack()
    Label(text="", bg="#333333").pack()
    Label(text="Wild Animal Detection", bg="#333333",fg='#e1eaea', width="300", height="2", font=("Calibri", 25)).pack()
    # Create a PhotoImage object
    script_dir = os.getcwd()
    image_path = os.path.join(script_dir, "cam.gif")
    image = PhotoImage(file=image_path)
    # Display the image below the "Register" button
    Label(dashboard, image=image).pack()
    Button(text="Start Monitor",bg='green', fg='#ffffff', height="1", width="25",font=("Calibri", 13), command=lambda: start_monitor(username,email)).pack()
    Label(text="Detection", bg="#333333",fg='red', width="300", height="1", font=("Calibri", 15)).pack()
    Label(text="detect wild animals using sensors or cameras", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 10)).pack()
    Label(text="Sound Generation", bg="#333333",fg='red', width="300", height="1", font=("Calibri", 15)).pack()
    Label(text=" When a wild animal is detected,application produce a sound alert.", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 10)).pack()
    Label(text="Email Alerting", bg="#333333",fg='red', width="300", height="1", font=("Calibri", 15)).pack()
    Label(text="Send an email alert to the owner when a wild animal is detected", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 10)).pack()
    Label(text="", bg="#333333").pack()
    Button(text="Admin Config",bg='red', fg='#ffffff', height="1", width="25",font=("Calibri", 13),command=lambda: admin(username,email,phone)).pack()
    Button(text="History Data",bg='red', fg='#ffffff', height="1", width="25",font=("Calibri", 13),command=lambda: history(userid,username,email,phone)).pack()
    dashboard.mainloop()



def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.configure(bg="#333333")
    register_screen.geometry("700x600")
    Label(register_screen,text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 9)).pack()
    Label(register_screen,text="", bg="#333333").pack()
    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="Please enter details below to login",bg='#333333',fg='red',font=("Calibri", 12)).pack()
    Label(register_screen, text="",bg="#333333").pack()
    global username
    global password
    global email
    global phone
    global username_entry
    global password_entry
    global email_entry
    global phone_entry
    username = StringVar()
    password = StringVar()
    email=StringVar()
    phone=StringVar()

 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="Username *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    username_entry = Entry(register_screen, textvariable=username, width="30")
    username_entry.pack()
    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="Password *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    password_entry = Entry(register_screen, textvariable=password, show= '*', width="30")
    password_entry.pack()

    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="Email *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    email_entry = Entry(register_screen, textvariable=email, width="30")
    email_entry.pack()

    Label(register_screen, text="",bg="#333333").pack()
    Label(register_screen, text="Phone *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    phone_entry = Entry(register_screen, textvariable=phone, width="30")
    phone_entry.pack()
    
    Label(register_screen, text="",bg="#333333").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login 

def forgot_password():
    global forgot_password_screen
    forgot_password_screen = Toplevel(main_screen)
    forgot_password_screen.title("Login")
    forgot_password_screen.configure(bg="#333333")
    forgot_password_screen.geometry("700x600")
    Label(forgot_password_screen,text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 9)).pack()
    Label(forgot_password_screen,text="", bg="#333333").pack()
    Label(forgot_password_screen, text="",bg="#333333").pack()
    Label(forgot_password_screen, text="",bg="#333333").pack()
    Label(forgot_password_screen, text="Please enter username you will get new password",bg='#333333',fg='red',font=("Calibri", 12)).pack()
    Label(forgot_password_screen, text="",bg="#333333").pack()
 
    global fusername_verify
    fusername_verify = StringVar()
    global fusername_login_entry
 
    Label(forgot_password_screen, text="Username *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    fusername_login_entry = Entry(forgot_password_screen, textvariable=fusername_verify, width="30")
    fusername_login_entry.pack()
    Label(forgot_password_screen, text="",bg="#333333").pack()
    Button(forgot_password_screen,text="Send Password",bg='green', fg='#ffffff', height="1", width="20",font=("Calibri", 13), command=updatepass).pack()
# Implementing event on register button


def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.configure(bg="#333333")
    login_screen.geometry("700x600")
    Label(login_screen,text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 9)).pack()
    Label(login_screen,text="", bg="#333333").pack()
    Label(login_screen, text="",bg="#333333").pack()
    Label(login_screen, text="",bg="#333333").pack()
    Label(login_screen, text="Please enter details below to login",bg='#333333',fg='red',font=("Calibri", 12)).pack()
    Label(login_screen, text="",bg="#333333").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify, width="30")
    username_login_entry.pack()
    Label(login_screen, text="",bg="#333333").pack()
    Label(login_screen, text="Password *                          ",bg="#333333",fg='#e1eaea', width="300", height="0", font=("Calibri", 12)).pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*', width="30")
    password_login_entry.pack()
    Label(login_screen, text="",bg='#333333').pack()
    Button(login_screen,text="Login",bg='green', fg='#ffffff', height="1", width="20",font=("Calibri", 13), command=login_verify).pack()
    Label(login_screen, text="",bg='#333333').pack()
    Button(login_screen,text="Forgot Password",bg='green', fg='#ffffff', height="1", width="20",font=("Calibri", 13), command=forgot_password).pack()
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
    email_info=email.get()
    phone_info=phone.get()
    # Insert data into the table
    sql = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
    val = (username_info,password_info,email_info,phone_info)
    mycursor.execute(sql, val)
    # Commit the transaction
    mydb.commit()
    # Print the number of inserted rows
    print(mycursor.rowcount, "record inserted.")
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    phone_entry.delete(0,END)
    email_entry.delete(0,END)
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

def updatepass():
    filename = fusername_verify.get()
    print(filename)
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Update the second line
    password = ''.join(random.choices(string.digits, k=5))
    sql = "UPDATE users SET password = %s WHERE username = %s"
    val = (password, filename)
    mycursor.execute(sql, val)
    # Commit the transaction
    mydb.commit()
    # Print the number of updated rows
    print(mycursor.rowcount, "record(s) updated.")
    email=fetchuser(filename)
    sendmail.send_email_password(filename,password,email)
    email_sent(email)
    
def fetchuser(filename):
    sql1 = "SELECT * FROM users WHERE username = %s"
    val1 = (filename,)
    mycursor.execute(sql1, val1)
    user = mycursor.fetchone()
    print(user[3])
    mycursor.fetchall()
    return user[3]

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username1, password1)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    print(user)
    if user:
        print(user[0])
        login_sucess(username1,user[3],user[2],user[0])
    else:
        password_not_recognised()
    mycursor.fetchall()
 
# Designing popup for login success
 
def login_sucess(username,email,phone,userid):
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("300x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=lambda: delete_login_success(username,email,phone,userid)).pack()
    
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("300x100")
    Label(password_not_recog_screen, text="Invalid Username or Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def email_sent(email):
    global password_not_recog_screen1
    password_not_recog_screen1 = Toplevel(login_screen)
    password_not_recog_screen1.title("Success")
    password_not_recog_screen1.geometry("300x100")
    Label(password_not_recog_screen1, text="New Password generated success \n Please check your mail \n"+email).pack()
    Button(password_not_recog_screen1, text="OK", command=delete_password_not_recognised1).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success(username,email,phone,userid):
    login_success_screen.destroy()
    dashboard(username,email,phone,userid)
   
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
def delete_password_not_recognised1():
    password_not_recog_screen1.destroy()
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.configure(bg="#333333")
    main_screen.geometry("700x600")
    main_screen.title("Wild Animal Detection")
    Label(text="KVG College of Engineering,Sullia", bg="#333333",fg='#ffffff', width="300", height="1", font=("Calibri", 9)).pack()
    Label(text="", bg="#333333").pack()
    Label(text="Wild Animal Detection", bg="#333333",fg='#e1eaea', width="300", height="2", font=("Calibri", 25)).pack()
    # Create a PhotoImage object
    script_dir = os.getcwd()
    image_path = os.path.join(script_dir, "Wild_animals.png")
    image = PhotoImage(file=image_path)
    # Display the image below the "Register" button
    Label(main_screen, image=image).pack()
    Label(text="", bg="#333333").pack()
    Button(text="Login",bg='#92b9b9', fg='#ffffff', height="1", width="30", font=("Calibri", 13),command = login).pack()
    Label(text="", bg="#333333").pack()
    Button(text="Register",bg='#92b9b9', fg='#ffffff', height="1", width="30",font=("Calibri", 13), command=register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()
