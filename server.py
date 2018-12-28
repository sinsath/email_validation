from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)

SCHEMA = 'email_validation' 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"


@app.route('/')
def index():  
    return render_template('index.html')

@app.route("/create", methods=['POST'])
def add_email():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    else:      
        mysql = connectToMySQL(SCHEMA)
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        data = {
         'email': request.form['email'],           
        }
        mysql.query_db(query, data)    
        mysql = connectToMySQL(SCHEMA)
        all_emails = mysql.query_db("SELECT * from emails")
        return render_template("success.html",emails = all_emails)

if __name__=="__main__":
    app.run(debug=True) 