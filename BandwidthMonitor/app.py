from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import psutil
import threading

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOUST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bandwidth_monitor'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)

# Index
start_bytes_sent = 0
start_bytes_recv = 0
start_packets_sent = 0
start_packets_recv = 0
@app.route('/')
def index():
    bytes_sent = psutil.net_io_counters()[0] - start_bytes_sent
    bytes_recv = psutil.net_io_counters()[1] - start_bytes_recv
    packets_sent = psutil.net_io_counters()[2] - start_packets_sent
    packets_recv = psutil.net_io_counters()[3] - start_packets_recv
    return render_template('index.html', bytes_sent=bytes_sent, bytes_recv=bytes_recv,
                           packets_sent=packets_sent, packets_recv=packets_recv)

@app.route('/monitoring/')
def monitoring():
    global start_bytes_sent
    global start_bytes_recv
    global start_packets_sent
    global start_packets_recv
    start_bytes_sent = psutil.net_io_counters()[0]
    start_bytes_recv = psutil.net_io_counters()[1]
    start_packets_sent = psutil.net_io_counters()[2]
    start_packets_recv = psutil.net_io_counters()[3]
    running = True
    # Modify this so it increases
    bytes_sent = 0
    bytes_recv = 0
    packets_sent = 0
    packets_recv = 0
    return render_template('index.html', bytes_sent=bytes_sent, bytes_recv=bytes_recv,
                           packets_sent=packets_sent, packets_recv=packets_recv, running=running)

@app.route('/about')
def about():
    return render_template('about.html')

def get_bytes_rec():
    #threading.Timer(2.0, get_bytes_rec).start()
    return psutil.net_io_counters()[0]

if __name__ == '__main__':
    app.run(debug=True)