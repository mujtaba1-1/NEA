import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LoginPage:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Database Connection")
        self.root.geometry("300x150")

        self.password_label = tk.Label(self.root, text="Enter Database Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.root, show="*")  # Entry widget to input password
        self.password_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)
    
    def connect_to_database(self, host, port, user, password, database):
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

    def on_submit(self):
        entered_password = self.password_entry.get()
        return self.connect_to_database("127.0.0.1", 3306, "root", entered_password, "facialrecognition")


