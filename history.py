from tkinter import Tk, Label, Button, Frame
from tkinter.ttk import Treeview
import mysql.connector

def fetch_and_display_data(userid):
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="wildanimal"
        )
    mycursor = mydb.cursor()
    print(userid)
    # Fetch data from the database
    sql = "SELECT * FROM detectionlog WHERE userid = %s"
    mycursor.execute(sql, (userid,))
    data = mycursor.fetchall()

    # Create a new window for displaying the table
    display_window = Tk()
    display_window.title("Data Display")

    # Create a frame for the table
    frame = Frame(display_window)
    frame.pack(pady=20)

    # Create a Treeview widget
    tree = Treeview(frame, columns=(1, 2, 3, 4,5), show="headings", height="5")
    tree.pack(side="left")

    # Define the column headings
    tree.heading(1, text="ID")
    tree.heading(2, text="User Id")
    tree.heading(3, text="Detected Animal")
    tree.heading(4, text="Date")
    tree.heading(5, text="Place")
    # Insert data into the table
    for record in data:
        tree.insert("", "end", values=record)

    display_window.mainloop()
