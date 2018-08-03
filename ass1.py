#!/usr/bin/python3

from sense_hat import SenseHat
from datetime import datetime
from time import sleep, strftime, time
import sqlite3

sense = SenseHat()
currtime = datetime.now()

temp = sense.get_temperature()
humid = sense.get_humidity()

sqlite_file = '/home/pi/ass1/db_files/ass1.db'
#Open database connection.
db = sqlite3.connect(sqlite_file)

try:
	#Prepare a cursor object using cursor() method.
	cursor = db.cursor()

	sql = "INSERT INTO statistic (timestamp, temperature, humidity) VALUES (?, ?, ?)"
	cursor.execute(sql, (currtime, temp, humid))
	db.commit()
except Exception as e:
	db.rollback()
	raise e
finally:
        with open("/home/pi/ass1/temp_record.csv", "w", newline='') as csv_file:
                cursor.execute("SELECT * FROM statistic;")
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(cursor)
		db.close()
