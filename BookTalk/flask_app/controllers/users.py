from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.controllers import books
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.controllers import magazines

@app.get('/')
def login_and_registration():
    return render_template('loginandregistration.html')


# Create Users Controller
@app.post('/process_registration')
def process_register():
    if not user.User.validate_info(request.form):
        return redirect('/')
    user.User.save(request.form)
    return redirect('/login')

@app.post('/process_login')
def process_login():
    if not user.User.validate_info(request.form):
        return redirect("/")
    session['email'] = request.form['email_login']
    return redirect('/login')

# Read Users Controller

@app.get('/login')
def login():
    account = user.User.get_by_email(session['email'])
    session['id'] = account.id
    session['first_name'] = account.first_name
    return redirect('/dashboard')
