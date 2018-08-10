#!/usr/bin python3

#from flask import Flask, render_template, request
import sqlite3 as sql
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
#app = Flask(__name__)

#@app.route('/')
#def list():
#    con = sql.connect('/home/pi/ass1/ass1.db')
#    con.row_factory = sql.Row

#    cur = con.cursor()
#    cur.execute("select * from statistic;")

#    rows = cur.fetchall();
#    return render_template("list.html",rows = rows)

def graph_data():
    sqlite_file = '/home/pi/ass1/ass1.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    style.use('fivethirtyeight')

    c.execute('SELECT timestamp, temperature FROM statistic;')
    data = c.fetchall()

    timestamp = []
    temperature = []

    for row in data:
        temperature.append(row[2])
        timestamp.append(parser.parse(row[1]))

    plt.plot_date(timestamp,temperature,'-')
    plt.show()

    c.close()
    conn.close()

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')

graph_data()

