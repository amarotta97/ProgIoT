#!/usr/bin/python3

import sqlite3
from datetime import datetime
from sense_hat import SenseHat
import requests
import json
import os

dbname='/home/pi/ass1/ass1.db'
ACCESS_TOKEN="o.VIMZp8G8Fz93y1bT4RovYpE0WrYxtesI"

# Retrieves the current time, humidity and temperature using datetime and also sensehat
def getSenseHatData():
    sense = SenseHat()
    time = datetime.now()
    humid = sense.get_humidity()
    temp = sense.get_temperature()

    logData (time, temp, humid)
    return temp

# Commit the data into database
def logData (time, temp,  humid):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    sql = "INSERT INTO statistic (timestamp, temperature, humidity) VALUES (?, ?, ?)"
    curs.execute(sql, (time, temp, humid))
    conn.commit()
    conn.close()

# Return current results of the database
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM statistic;"):
        print (row)
    conn.close()

# Push notification to phone via PushBullet
def pushMessage(title, body):
    temp = getSenseHatData()
    data = {"type": "note", "title": title, "body": body}

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN,
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

# main function to run
def main():
    for i in range (0,1):
        getSenseHatData()
    displayData()

# function to push to phone only if temp is less than 20
def pushToPhone():
        temp = getSenseHatData()
        if ( 20 > temp ):
                pushMessage("Temp is: " + str(temp), "Bring a sweater")

# Executes the main and also push to phone
main()
pushToPhone()
