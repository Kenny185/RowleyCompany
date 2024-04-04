from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user 

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', active_page='login')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if not email or not password:
        flash('Invalid credentials')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  
    # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    session['user_id'] = user.id
    login_user(user, remember=remember)
    if user.role == 'agent':
        return redirect(url_for('main.agentDashboard'))
    else :
        return redirect(url_for('main.clientDashboard'))        

@auth.route('/signup')
def signup():
    return render_template('signup.html', active_page='signup')

@auth.route('/signup', methods=['POST'])
def signup_post():
    surname = request.form.get('surname')
    first_name = request.form.get('first_name')
    second_name = request.form.get('second_name')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    gender = request.form.get('gender')
    role = request.form.get('role')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() 
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(surname=surname, first_name=first_name, second_name=second_name,
                    email=email, telephone=telephone, gender=gender, role=role, 
                    password=generate_password_hash(password, method='pbkdf2:sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))
        

@auth.route('/agent_login')
def agentLogin():
    return render_template('agentLogin.html', active_page='agentLogin')

@auth.route('/agent_login', methods=['POST'])
def agentLogin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
        
    user = User.query.filter_by(email=email).first()
   
    if not user or not check_password_hash(user.password, password)or user.role != 'agent':
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.agentLogin'))    
  
    login_user(user, remember=remember)
    return redirect(url_for('main.agentDashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('main.index'))