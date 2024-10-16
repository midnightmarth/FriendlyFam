from flask import Flask, render_template, request, redirect, session
# import mysql.connector
import sqlalchemy
import sqlite3

dbConn = sqlite3.connect("FriendlyFamDB") 

app = Flask(__name__)
app.secret_key = "Super Secret"
# my_db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="your workbench password",
#     database="your workbench database name"
# )
mycursor = dbConn.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS events (id INT AUTO_INCREMENT PRIMARY KEY,host VARCHAR(255),description VARCHAR(255),day VARCHAR(255), time VARCHAR(255),status VARCHAR(255) )")
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255),password VARCHAR(255))")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/login')
def loginRedir():
    return redirect("/")

@app.route('/home')
def home():
    return render_template("home.html")




if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)