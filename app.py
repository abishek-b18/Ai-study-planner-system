from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "studyplanner"

DATABASE = "users.db"

# Database setup
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            hours INTEGER,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username,password)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():

    username=request.form['username']
    password=request.form['password']

    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user=cursor.fetchone()

    if user:
        session['username']=username
        return redirect('/dashboard')

    return "Invalid Login"


@app.route('/dashboard')
def dashboard():

    conn=sqlite3.connect(DATABASE)
    df=pd.read_sql_query("SELECT * FROM tasks",conn)

    total_hours=df["hours"].sum() if not df.empty else 0

    return render_template(
        "dashboard.html",
        total_hours=total_hours
    )


@app.route('/planner')
def planner():
    return render_template("planner.html")


@app.route('/add_task',methods=['POST'])
def add_task():

    subject=request.form['subject']
    hours=request.form['hours']

    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(username,subject,hours,status) VALUES(?,?,?,?)",
        (
            session['username'],
            subject,
            hours,
            "Pending"
        )
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')


@app.route('/analytics')
def analytics():

    conn=sqlite3.connect(DATABASE)
    df=pd.read_sql_query("SELECT * FROM tasks",conn)

    subjects=df["subject"].tolist()
    hours=df["hours"].tolist()

    return render_template(
        "analytics.html",
        subjects=subjects,
        hours=hours
    )


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)