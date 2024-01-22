import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LoginPage:

    def connect_to_database(host, port, user, password, database):
        try:
            connection = mysql.connector.connect(
                host = host,
                port = port,
                user = user,
                password = password,
                database = database
            )
            messagebox.showinfo("Success", "Connected to the database successfully!")

            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to the database: {err}")

    def on_submit():
        entered_password = password_entry.get()
        return connect_to_database("127.0.0.1", 3306, "root", entered_password, "facialrecognition")

    # GUI setup
    root = tk.Tk()
    root.title("Database Connection")
    root.geometry("300x150")

    # Create and pack widgets
    password_label = tk.Label(root, text="Enter Database Password:")
    password_label.pack(pady=10)

    password_entry = tk.Entry(root, show="*")  # Entry widget to input password
    password_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    # Start the GUI
    root.mainloop()
