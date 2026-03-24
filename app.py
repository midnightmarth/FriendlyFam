from flask import Flask, render_template, request, redirect, session, jsonify
# from flask_wtf.csrf import CSRFProtect
# import mysql.connector
import sqlite3


app = Flask(__name__)
app.secret_key = "Super Secret"
# csrf = CSRFProtect(app)
wsgi_app = app.wsgi_app

# my_db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="your workbench password",
#     database="your workbench database name"
# )

with sqlite3.connect("FriendlyFamDB.db") as dbConn:
    mycursor = dbConn.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY,host VARCHAR(255),description VARCHAR(255),day VARCHAR(255), time VARCHAR(255),status VARCHAR(255) )")
    mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username VARCHAR(255),password VARCHAR(255))")

    dbConn.commit()

message = ""

@app.route('/')
def index():
    if "username" in session:
        return redirect("/home")
    
    return render_template("index.html", message=message)


@app.route('/signup', methods=["get", "post"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with sqlite3.connect("FriendlyFamDB.db") as conn:
            cursor = conn.cursor()
            
            userCheck = cursor.execute(f'''SELECT username FROM users WHERE username = "{username}"''').fetchall()
            if(len(userCheck) > 0):
                print(f"User already exists {username}")
                return redirect("/signup")
            
            smt = cursor.execute(f'''INSERT INTO users (username, password) VALUES ("{username}", "{password}")''').fetchall()
            conn.commit()
            
        return redirect("/")
    if request.method == "GET":
        return render_template("signup.html")


@app.route('/login', methods=["get", "post"])
def login():
    global message
    message = ""
    if "username" in session:
        return redirect("/home")
    
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with sqlite3.connect("FriendlyFamDB.db") as conn:
            cursor = conn.cursor()
            
            usr = cursor.execute(f'''SELECT username, password FROM users WHERE username = "{username}" AND password = "{password}"''').fetchone()
            if usr != "" and usr != None:
                print(f"username {usr[0]} is logging in with password: {usr[1]}")
                session["username"] = usr[0]
                return redirect("/home")
            message = f"Error! Username/password mismatch"
        return redirect('/')
            

    if request.method == "GET":
        return redirect("/")

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route('/home')
def home():
    
    if("username" in session ):
        with sqlite3.connect("FriendlyFamDB.db") as db:
            cursor = db.cursor()
            events = cursor.execute('''SELECT * FROM events''').fetchall()
            return render_template("home.html", user=session["username"], list=events)
    else:
        return redirect('/')

@app.route('/add', methods=["get", "post"])
def add():
    if request.method == "GET":
        return render_template("add.html", user=session["username"])
    if request.method == "POST":
        
        desc = request.form.get('description')
        day = request.form.get('day')
        time = request.form.get('time')
        
        with sqlite3.connect("FriendlyFamDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f'''INSERT INTO events (host, description, day, time, status) VALUES ("{session['username']}", "{desc}", "{day}", "{time}", "RUNNING")''')
            conn.commit()
        return redirect('/')
    
@app.route('/myevents')
def myevents():
    
    with sqlite3.connect("FriendlyFamDB.db") as conn:
        cursor = conn.cursor()
        events = cursor.execute(f'''SELECT * FROM events WHERE host = "{session["username"]}"''').fetchall()
        return render_template("myevents.html", list=events, user=session["username"])

@app.route('/update/<id>', methods=["GET", "POST"])
def updateEvent(id):
    if request.method == "GET":
        with sqlite3.connect("FriendlyFamDB.db") as conn:
            cursor = conn.cursor()
            event = cursor.execute(f'''SELECT * FROM events WHERE id={id}''').fetchone()
            return render_template("edit.html", event=event, user=session["username"])
        return redirect("/home")
    
    
    if request.method == "POST":
        
        desc = request.form.get("description")
        status = request.form.get("status")
        time = request.form.get("time")
        day = request.form.get("day")
        
        
        with sqlite3.connect("FriendlyFamDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f'''UPDATE events SET description="{desc}", status="{status}", day="{day}", time="{time}" WHERE id={id}''')

            conn.commit()
        # data = {"someData": "someData"}
        # return Flask.make_response(.jsonify(data), 200)
        
        # response = jsonify(success=True)
        # response.status_code = 200
        # return response
        return redirect('/myevents')
    
@app.route('/cancel/<id>')
def cancelEvent(id):
    
    # conn = getConn()
    with sqlite3.connect("FriendlyFamDB.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(f'''UPDATE events SET status="Canceled" WHERE host = "{session["username"]}"''')
        
        conn.commit()
    return redirect("/myevents")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)