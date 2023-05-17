from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import sqlalchemy as db
import mysql.connector
import re

import mysql.connector

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Elsk@012"
)

# Create a new database
# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE DataBase1")

# Connect to the new database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Elsk@012",
  database="python1"
)

# Create a new table
# mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), email VARCHAR(255))")

# Insert some data into the table
mycursor = mydb.cursor()
# sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
# val = ("john", "password123")
# mycursor.execute(sql, val)
# mydb.commit()

# print("Data inserted successfully.")




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)



class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
	db.create_all()


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Perform necessary validations
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Check if email already exists
            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                msg = 'Email already exists!'
            else:
                # Insert the user into the database
                sql = 'INSERT INTO user (username, password, email) VALUES (%s, %s, %s)'
                val = (username, password, email)
                cursor.execute(sql, val)
                mydb.commit()
                msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('sign_up.html', msg=msg)




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the username and password match a user in the database
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for("signin_successful"))
        else:
            return render_template("login.html", msg="Invalid email or password")

    return render_template("login.html")


@app.route('/signin_successful')
def signin_successful():
    msg = request.args.get('msg')
    return render_template('signin_successful.html', msg=msg)

@app.route("/")
def home():
	return render_template("home.html")


if __name__ == "__main__":
	app.run()
