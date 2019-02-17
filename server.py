from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key= "IAMGROOT"

@app.route('/users')
def index():
	# connect to databse
	# run query to select all the data we need to display on the template
	mysql=connectToMySQL("semi_resful_users")
	users= mysql.query_db("SELECT * FROM users;")
	return render_template("index.html", users=users)

# this renders the template for creating a new user
@app.route('/users/new')
def newUser():
	print("heyyyy YOU this iis new user")
	return render_template("newuser.html")

# this creates a new user
# concatenate the forms first name and last name to = full_name
@app.route('/users/create', methods=["POST"])
def create():
	print('heeeey')
	data= {
		"full_name": request.form['first_name'] + " " + request.form["last_name"],
		"email": request.form['email']
	}
	query="INSERT INTO users (full_name, email, created_at, updated_at) VALUES (%(full_name)s, %(email)s, NOW(), NOW());"
	mysql=connectToMySQL("semi_resful_users")
	mysql.query_db(query, data)
	return redirect('/users')

# make a route for the "show" a-tag in index.html
# displays all the user info
@app.route("/users/<int:user_id>")
def show(user_id):
	mysql=connectToMySQL("semi_resful_users")
	data={
		"user_id": user_id
	}
	query="SELECT * FROM users WHERE id = (%(user_id)s);"
	user= mysql.query_db(query, data)
	return render_template("show.html", user= user[0])

# make a route that takes you to the edit.html
@app.route("/users/<int:user_id>/edit")
def edit(user_id):
	data={
		"user_id": user_id
	}
	query="SELECT id, full_name, email FROM users WHERE id = (%(user_id)s);"
	mysql=connectToMySQL("semi_resful_users")
	user= mysql.query_db(query, data)
	return render_template("edit.html", user=user[0])

# make a route that updates a users info
@app.route('/update/<int:user_id>', methods=["POST"])
def update(user_id):
	data={
		"user_id" : user_id,
		"full_name": request.form['full_name'],
		"email": request.form['email']
	}
	query="UPDATE users SET full_name= %(full_name)s, email=%(email)s WHERE id=(%(user_id)s);"
	mysql=connectToMySQL("semi_resful_users")
	mysql.query_db(query, data)
	return redirect('/users')



# make a route that deletes a user based off of their id
@app.route("/delete/<int:user_id>")
def delete(user_id):
	data= {
		"user_id": user_id
	}
	query= "DELETE FROM users WHERE id = (%(user_id)s);"
	mysql=connectToMySQL("semi_resful_users")
	mysql.query_db(query, data)
	return redirect('/users')




if __name__ == "__main__":
    app.run(debug=True)