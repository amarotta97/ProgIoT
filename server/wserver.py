#!/usr/bin/env python3
from flask import Flask, render_template, request
app = Flask(__name__)
import os
import sqlite3 as sql

# Retrieve data from database
def getData():
        conn=sqlite3.connect('/home/pi/ass1/ass1.db')
        curs=conn.cursor()

        for row in curs.execute("SELECT * FROM statistic;"):
                time = str(row[1])
                temp = row[2]
        conn.close()
        return time, temp

# main route

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

