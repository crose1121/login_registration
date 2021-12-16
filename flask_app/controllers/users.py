from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register_user(): #HOW TO CATCH AN EMPTY PASSWORD FIELD!
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match tryu again")
        return redirect('/')
    
    data = {
        'temp': request.form['password'], #Is it acceptable to do this? So I can reference the value of the password they typed in rather than the value of the hashed pw. See line 54 in controller
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    if User.validate_user(data): #Should I be validating at the start of of register user? It seems like it'd make more sense
        User.register_user(data)
        return redirect('/user/success')
    else:
        return redirect('/')

@app.route('/user/success')
def user_success():
    return render_template('success.html')
    
@app.route('/user/login', methods=["POST"])
def user_login():
    data = { 
        "email" : request.form["email"] 
    }

    user_in_db = User.get_email(data)

    if not user_in_db:
        flash("INVALID EMAIL/PASSWORD")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

#How do i check for an empty password??
#This doesn't work
    # if bcrypt.check_password_hash("", request.form['password']):
    #     flash("Invalid Email/Password")
    #     return redirect('/')


    session['id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/user/dashboard')

@app.route('/user/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
