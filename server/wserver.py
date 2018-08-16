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

def getHistData (numSamples):
        curs.execute("SELECT * FROM statistic ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
        timestamp = []
        temperature = []
        for row in reversed(data):
                timestamp.append(row[1])
                temperature.append(row[2])
        return timestamp, temperature

def maxRowsTable():
        for row in curs.execute("SELECT COUNT(temperature) from statistic"):
                maxNumberRows=row[0]
        return maxNumberRows

# Define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 1001):
        numSamples = 1000

@app.route('/temp')
def plot_temp():
        timestamp, temperature  = getHistData(numSamples)
        ys = temperature
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("Temperature [°C]")
        axis.set_xlabel("Samples")
        axis.grid(True)
        xs = range(numSamples)
        axis.plot(xs, ys)
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = 'image/png'
        return response

@app.route("/")
def home():
        return render_template("index.html")

@app.route("/list")
def list():
        con = sql.connect('/home/pi/ass1/ass1.db')
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from statistic;")

        rows = cur.fetchall();
        return render_template("list.html",rows = rows)

if __name__ == "__main__":
        host = os.popen('hostname -I').read()
        app.run(host=host, port=80, debug=False)
