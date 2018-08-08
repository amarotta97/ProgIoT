#!/usr/bin/python3

import sqlite3
from datetime import datetime
from sense_hat import SenseHat
import requests
import json
import os

dbname='/home/pi/ass1/ass1.db'
ACCESS_TOKEN="o.VIMZp8G8Fz93y1bT4RovYpE0WrYxtesI"

# get data from SenseHat sensor
def getSenseHatData():
    sense = SenseHat()
    time = datetime.now()
    humid = sense.get_humidity()
    temp = sense.get_temperature()

    logData (time, temp, humid)
    return temp
# log sensor data on database
def logData (time, temp,  humid):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    sql = "INSERT INTO statistic (timestamp, temperature, humidity) VALUES (?, ?, ?)"
    curs.execute(sql, (time, temp, humid))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM statistic;"):
        print (row)
    conn.close()

def pushMessage(title, body):
    temp = getSenseHatData()
    data = {
            'type':'note',
            'title':title,
            'body':body
           }
    resp = requests.post('https//api.pushbullet.com/v2/pushes', data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN,
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

# main function
def main():
    temp = getSenseHatData()
    for i in range (0,1):
        getSenseHatData()
    displayData()
    pushMessage(temp, "Bring a sweater")

# Execute program
main()
