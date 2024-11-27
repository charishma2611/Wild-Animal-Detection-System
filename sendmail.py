import smtplib
from email.message import EmailMessage
import imghdr
import geocoder
import urllib.parse
# Set up SMTP server details
smtp_server = "smpt mail"
smtp_port = port number  # For starttls
smtp_username = "username mail"
smtp_password = "password"
from datetime import datetime

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql password",
  database="database name"
)
import json
# Load the JSON file
with open('animal_type.json', 'r') as file:
    animals_data = json.load(file)
def find_animal_type(animal_name):
    print(animal_name)
    print(animals_data['wild_animals'])
    if animal_name in animals_data['wild_animals']:
        return 'Wild'
    elif animal_name in animals_data['domestic_animals']:
        return 'Domestic'
    else:
        return 'Unknown'

def inseerdata(email,detected_animal, detected_date, detected_location):
    mycursor = mydb.cursor()
    sql = "SELECT id FROM users WHERE email = %s"
    mycursor.execute(sql, (email,))
    result = mycursor.fetchone()
    user_id = result[0]
    mycursor.fetchall()
    sql = "INSERT INTO DetectionLog (UserId, detected_animal, detected_date, detected_location) VALUES (%s, %s, %s, %s)"
    val= [(user_id, detected_animal, detected_date, detected_location)]
    mycursor.executemany(sql, val)
    # Commit the changes
    mydb.commit()
    print(mycursor.rowcount, "record(s) inserted.")
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

def send_email(label,email):
    print(label)
    Sender_Email = "your mail"
    Reciever_Email = email
    Password = "password"
    newMessage = EmailMessage()    #creating an object of EmailMessage class
    newMessage['Subject'] = "Animal Detected" #Defining email subject
    newMessage['From'] = Sender_Email  #Defining sender email
    newMessage['To'] = Reciever_Email  #Defining reciever email
    atype=find_animal_type(label)
    g = geocoder.ip('me')
    location_query = urllib.parse.quote(f"{g.latlng[0]},{g.latlng[1]}")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={location_query}"
    newMessage.set_content(f'<h3>An animal has been detected</h3><br><p>Detected Animal Name: <b>{label}</b><br><p>Animal Type:<span="color:green"><b>{atype}<b></span></p><br> Detected Location: {g.city}, {g.state}, {g.country}</p><br>Google Maps Link: <a href="{maps_url}">Click here</a><p><b>Thanks and Regards</b><br><p>KVGCE Student,Sullia</p></p>', subtype='html') #Defining email body
    inseerdata(email,label,datetime.now().date(),g.city+","+g.state+","+g.country,)
    with open('images/' + label + '.png', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name[7:]

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    print("don1e")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password) #Login to SMTP server
        smtp.send_message(newMessage)      #Sending email using send_message method by passing EmailMessage object
        print("done")
def send_email_password(username, password, email):
    Sender_Email = "sender mail"
    Reciever_Email = email
    Password = "password"
    newMessage = EmailMessage()    # creating an object of EmailMessage class
    newMessage['Subject'] = "Forgot Password-Animal Detected" # Defining email subject
    newMessage['From'] = Sender_Email  # Defining sender email
    newMessage['To'] = Reciever_Email  # Defining receiver email
    newMessage.add_header('Content-Type', 'text/html; charset=utf-8')  # Setting the content type
    newMessage.set_content(f'''
        Forgot Password
        Username:{username}
        New Password:{password}
        Thanks and Regards
        KVGCE Student,Sullia
    ''', subtype='html')  # Defining email body
    print("done")
    with smtplib.SMTP_SSL('smtp mail', port number) as smtp:
        smtp.login(Sender_Email, Password) # Login to SMTP server
        smtp.send_message(newMessage)      # Sending email using send_message method by passing EmailMessage object
        print("done")
#send_email("tiger","gangadharasn98@gmail.com")

