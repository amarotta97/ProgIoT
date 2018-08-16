# ProgIoT Semester 2 2018
s3602839 Assignment 1 for Programming Internet of Things
	
<br />
<br />
**File Details:**

- ass1.db: Was created using sqlite3 commands, storing output from ass1.py

- ass1.py: Contains section i & ii. 
    - currently successful section i) Apart from webserver (not complete, coding in seperate file [/server/webserver.py]) Currently logs data to 		my sqlite3 database, also prints the current data in the database
    - currently successful section ii) Pushbullet API works 100%, sends Notification to my mobile with temp as title, and "Bring 
		a sweater" as body when temp recorded is less than 20 Celsius
    
- bt.py: Contains section iii, currently successful, locates bluetooth device and displays temperature on Pi

- webserver.py: Currently in progress
<br />
<br />
**Other tasks completed:** <br />
<br />
Cron job was completed using:<br />
sudo crontab -e <br />
and then within that file: * * * * * sudo python3 /home/pi/ass1/ass1.py <br />
<br />
Database was created using sqlite3 commands: <br />
sqlite3 ass1.db <br /><br />
    
schema:<br />
CREATE TABLE statistic(id INTEGER PRIMARY KEY autoincrement, timestamp DATETIME NOT NULL, temperature NUMERIC NOT NULL, humidity NUMERIC NOT NULL);
<br /><br />
    sqlite> PRAGMA table_info(statistic);<br />
    0|id|INTEGER|0||1<br />
    1|timestamp|DATETIME|1||0<br />
    2|temperature|NUMERIC|1||0<br />
    3|humidity|NUMERIC|1||0<br />

    
