import cv2
import tkinter as tk
import numpy as np
import PIL.Image, PIL.ImageTk
import sqlite3
import mysql.connector

from keras.models import load_model
from tkinter import ACTIVE, DISABLED, ttk, messagebox
from datetime import datetime, date

class LoginPage:

    def __init__(self, root):
        self.root = root
        self.root.title("Database Connection")
        self.root.geometry("300x150")
        self.root.resizable(0, 0)

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

            return connection, True
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to the database: {err}")
            return None, False

    def on_submit(self):
        entered_password = self.password_entry.get()
        connection, connected = self.connect_to_database("127.0.0.1", 3306, "root", entered_password, "facialrecognition")
        if connected:
            self.root.destroy()
            app_root = tk.Tk()
            app = FaceAttendance(app_root, "Face Detection App", connection)
            app_root.mainloop()
            

class FaceAttendance:
    def __init__(self, window, window_title, connection):
        self.window = window
        self.window.title(window_title)
        self.window.state('zoomed')
        self.window.configure(bg = "#202020")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.connection = connection
        self.cursor = self.connection.cursor()

        self.canvas = tk.Canvas(
            window,
            bg='#202020',
            height=720,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief='ridge'
            )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            30.0,
            29.0,
            1200.0,
            720.0,
            fill='#D9D9D9',
            outline=""
            )

        self.output_text_image = tk.PhotoImage(file='entry_2.png')
        self.output_text_bg = tk.Label(
            self.window, 
            image=self.output_text_image,
            background='#202020',          
            )
        self.output_text_bg.place(x = 300, y = 740)

        self.output_text = tk.Text(
            self.output_text_bg,
            wrap=tk.WORD,
            height=11,
            width=104,
            background='#2d2d2d',
            borderwidth=0,
            relief='ridge',
            fg='white',
            state=tk.DISABLED,
            )
        self.output_text.place(x = 9, y = 9)

        self.video_source = 0  # Use the default webcam (change if needed)
        self.vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)
        
        # Set the desired resolution (e.g., 1280x720)
        desired_width = 1280
        desired_height = 720
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
        
        self.start_button_image = tk.PhotoImage(file='button_1.png')
        self.start_button = tk.Button(
            self.window,
            image=self.start_button_image, 
            command=self.start_face_recognition,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground='#202020',
            background='#202020'
            )
        self.start_button.place(
            x=30.0,
            y=850.0,
            width=204.0,
            height=59.0
            )
        
        self.stop_button_image = tk.PhotoImage(file='button_2.png')
        self.stop_button = tk.Button(
            self.window,
            image = self.stop_button_image,
            command=self.stop,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground='#202020',
            background='#202020'
            )       
        self.stop_button.place(
             x=30.0,
             y=770.0,
             width=204.0,
             height=59.0
             )
        
        self.is_running = True  # Camera is always on
        self.face_detection = False  # Face Detection is off initially
        self.face_recognition = False  # Face Recogntion is off initially

        # Load Face Detection Model
        self.face_detection_model = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')
        # Load Face Recognition Model
        self.face_recognition_model = load_model('MobileNetV2Model.h5')

        # Define Class Labels
        self.class_labels = {
                        0: 'Ronaldo',
                        1: 'Messi',
                        2: 'Mujtaba',
                        3: 'Neymar'
                        }
        
        self.update()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cursor.close()
            self.connection.close()
            self.window.destroy()
            
    
    def start_face_recognition(self):
        self.face_detection = True
        self.face_recognition = True
    
    def stop(self):
        self.face_detection = False
        self.face_recognition = False
    
    def update_output(self, output_text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, output_text + "\n\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def detect_faces(self, frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using the SSD model
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104, 117, 123))
        self.face_detection_model.setInput(blob)
        detections = self.face_detection_model.forward()
        
        # Iterate over the detected faces and draw rectangles
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Filter out weak detections
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (x, y, x1, y1) = box.astype("int")

                if self.face_recognition:
                    self.recognise_faces(frame, x, y, x1, y1)
                else:
                    cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        
        return frame
    
    def recognise_faces(self, frame, x, y, x1, y1):

        # Extract the detected face
        face = frame[y:y1, x:x1]

        # Preprocess the face for the face recognition model
        face = cv2.resize(face, (224, 224))
        face = np.array(face) / 255.0
        input_batch = np.expand_dims(face, axis=0)

        # Make predictions using the model
        predictions = self.face_recognition_model.predict(input_batch)
        class_indices = np.argmax(predictions, axis=1)
        predicted_class_label = self.class_labels[class_indices[0]]

        # Draw a rectangle and label the face
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        cv2.putText(frame, predicted_class_label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mark Face if it is new
        if class_indices == 2:
            self.markFace(int(class_indices[0]))

        output_text = (
            f"Class: {predicted_class_label}\n"
            f"Probability: {max(predictions[0]):.2f}\n"
            f"Location: x={x}, y={y}, width={x1-x}, height={y1-y}\n"
            "Detection: Face Detected"
            )

        self.update_output(output_text)


        return frame

    def update(self):
        ret, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        if ret and self.is_running:
            if self.face_detection:
                frame = self.detect_faces(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = cv2.resize(frame, (int(self.vid.get(3)), int(self.vid.get(4))))
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(photo))
            self.canvas.create_image(30, 29, image=photo, anchor=tk.NW)
            self.canvas.photo = photo
        if self.is_running:
            self.window.after(10, self.update)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def markFace(self, ID):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")
        today = date.today()

        self.cursor.execute("SELECT is_present FROM people WHERE student_id = %s", (ID,))
        currentStatus = self.cursor.fetchone()
        
        if currentStatus[0] == 0:
            self.cursor.execute("""UPDATE people
                              SET is_present = %s,
                                  attendance_date = %s,
                                  time_marked = %s
                              WHERE
                                  student_id = %s
                           """, (1, today, time, ID))
            self.connection.commit()

# MAIN CODE

login_root = tk.Tk()
login = LoginPage(login_root)
login_root.mainloop()

