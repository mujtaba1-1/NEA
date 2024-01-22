import mysql.connector
from datetime import datetime, date

time = datetime.now()
formatted_time = time.strftime("%H:%M:%S")
today = date.today()
formatted_today = today.strftime("%Y-%m-%d")

print(formatted_time)
print(today)

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

    for i in range(1, 5):
        cur.execute("SELECT * FROM people WHERE student_id = %s", (i,))
        person = cur.fetchone()
        print(person)

    idNum = int(input("ID: "))
    marked = 1

    cur.execute("""UPDATE people
                  SET is_present = %s,
                      attendance_date = %s,
                      time_marked = %s
                  WHERE
                      student_id = %s
                """, (marked, today, time, idNum))

    conn.commit()

    cur.execute("SELECT * FROM people WHERE student_id = %s", (idNum,))
    person = cur.fetchone()
    print(person)

    cur.close()
    conn.close()
    
except mysql.connector.Error as error:
    print(f"Error: {error}")





