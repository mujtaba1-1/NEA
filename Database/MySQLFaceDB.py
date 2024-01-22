import mysql.connector

class People:

    def __init__(self, first, last, DoB, is_present, date, time):
        self.first = first
        self.last = last
        self.DoB = DoB
        self.is_present = is_present
        self.date = date
        self.time = time

try:    
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port = 3306,
        user="root",
        password="123Pass456",
        database="facialrecognition"
        )
        
    print("Connected!")

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE people(
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        date_of_birth DATE NOT NULL,
        is_present INT NOT NULL,
        attendance_date DATE,
        time_marked TIME)
        """)

    conn.commit()

    person_1 = People('Cristiano', 'Ronaldo', '1991-06-15', 0, None, None)
    person_2 = People('Lionel', 'Messi', '1994-09-25', 0, None, None)
    person_3 = People('Neymar', 'Jr', '1999-07-09', 0, None, None)
    person_4 = People('Mujtaba', 'Butt', '2006-04-01', 0, None, None)

    cur.execute("INSERT INTO people (first_name, last_name, date_of_birth, is_present, attendance_date, time_marked) VALUES (%s, %s, %s, %s, %s, %s)",
                (person_1.first, person_1.last, person_1.DoB, person_1.is_present, person_1.date, person_1.time))

    conn.commit()

    cur.execute("INSERT INTO people (first_name, last_name, date_of_birth, is_present, attendance_date, time_marked) VALUES (%s, %s, %s, %s, %s, %s)",
                (person_2.first, person_2.last, person_2.DoB, person_2.is_present, person_2.date, person_2.time))

    conn.commit()

    cur.execute("INSERT INTO people (first_name, last_name, date_of_birth, is_present, attendance_date, time_marked) VALUES (%s, %s, %s, %s, %s, %s)",
                (person_3.first, person_3.last, person_3.DoB, person_3.is_present, person_3.date, person_3.time))

    conn.commit()

    cur.execute("INSERT INTO people (first_name, last_name, date_of_birth, is_present, attendance_date, time_marked) VALUES (%s, %s, %s, %s, %s, %s)",
                (person_4.first, person_4.last, person_4.DoB, person_4.is_present, person_4.date, person_4.time))

    conn.commit()

    cur.close()
    conn.close()

except mysql.connector.Error as error:
    print(f"Error: {error}")
