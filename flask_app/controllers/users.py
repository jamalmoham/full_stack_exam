from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.models.arbotrary import Arbotrary
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    logged_in_user = user.User.user_by_id(data)

    arbotraries = Arbotrary.arbotrary_and_planter()
    
    return render_template('dashboard.html', user = logged_in_user, arbotraries = arbotraries)

@app.route('/register', methods = ['POST'])
def register():
    if not user.User.user_validation(request.form):
        return redirect('/')
    else:
        pw = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'firstname' : request.form['firstname'],
            'lastname' : request.form['lastname'], 
            'email' : request.form['email'],
            'password' : pw
        }
        user.User.save(data)
        
        dt = {
            'email' : request.form['email']
        }        
        userId = user.User.user_by_email(dt)
        session['user_id'] = userId.id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = user.User.user_by_email(data)
    if not user_in_db:
        flash('Invalid email/password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


