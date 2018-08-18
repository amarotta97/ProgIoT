#!/usr/bin/env python3

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import os

import sqlite3 as sql
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

# Retrieve data from database
conn=sqlite3.connect('/home/pi/ass1/ass1.db')
curs=conn.cursor()

# Function that will retrieve data in desecending order of timestamp
def getData():
        for row in curs.execute("SELECT * FROM statistic ORDER BY timestamp DESC LIMIT 1"):
                timestamp = str(row[1])
                temperature = row[2]
                humidity = row[3]
        return timestamp, temperature, humidity

# Function to retrieve data for histogram
def getHistData (sampleAmount):
        curs.execute("SELECT * FROM statistic ORDER BY timestamp DESC LIMIT "+str(sampleAmount))
        data = curs.fetchall()
        timestamp = []
        temperature = []
        humidity = []
        for row in reversed(data):
                timestamp.append(row[1])
                temperature.append(row[2])
                humidity.append(row[3])
        return timestamp, temperature, humidity

# Function to define the number of rows to use
def numOfRows():
        for row in curs.execute("SELECT COUNT(temperature) from statistic"):
                numOfRows=row[0]
        return numOfRows

# Define and initialize global variables
global sampleAmount
sampleAmount = numOfRows()
if (sampleAmount > 101):
        sampleAmount = 100

# main route
@app.route("/")
def index():
        timestamp, temperature, humidity = getData()
        templateData = {
                'timestamp'             : timestamp,
                'temperature'           : temperature,
                'humidity'              : humidity,
                'sampleAmount'  : sampleAmount
        }
        return render_template('index.html', **templateData)

# Main route to recieve number of posts
@app.route('/', methods=['POST'])
def form():
        global sampleAmount
        sampleAmount = int (request.form['sampleAmount'])
        sampleMaximum = numOfRows()
        if (sampleAmount > sampleMaximum):
                sampleAmount = (sampleMaximum-1)

        timestamp, temperature, humidity  = getData()

        templateData = {
                'timestamp'             : timestamp,
                'temperature'           : temperature,
                'humidity'              : humidity,
                'sampleAmount'  : sampleAmount
        }
        return render_template('index.html', **templateData)

# Route to the plot image of temperature and the function to graph temperature results
@app.route('/plot/temperature')
def plot_temp():
        timestamp, temperature, humidity  = getHistData(sampleAmount)
        ys = temperature
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("Temperature [°C]")
        axis.set_xlabel("Result ")
        axis.grid(True)
        xs = range(sampleAmount)
        axis.plot(xs, ys)
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = 'image/png'
        return response

# Route to plot image of humidity and the function to graph humidity results
@app.route('/plot/humidity')
def plot_hum():
        timestamp, temperature, humidity = getHistData(sampleAmount)
        ys = humidity
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("Humidity [%]")
        axis.set_xlabel("Result ")
        axis.grid(True)
        xs = range(sampleAmount)
        axis.plot(xs, ys)
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = 'image/png'
        return response

# Route and function to list the entire database contents with all fields
@app.route("/list")
def list():
        con = sql.connect('/home/pi/ass1/ass1.db')
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from statistic;")

        rows = cur.fetchall();
        return render_template("list.html",rows = rows)

# Main
if __name__ == "__main__":
        host = os.popen('hostname -I').read()
        app.run(host=host, port=80, debug=False)
