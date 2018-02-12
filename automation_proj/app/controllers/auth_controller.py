from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms.auth_form import LoginForm
from .forms.registration_form import RegistrationForm
from .. import db
from ..models.user import User

@auth.route('/')
@login_required
def index():
	return render_template('dashboard.html')

@auth.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')

@auth.route('/suites')
@login_required
def suites():
	return render_template('suites.html')

@auth.route('/cases')
@login_required
def cases():
	return redirect(url_for('case.show_all'))

@auth.route('/case-settings')
@login_required
def urls():
	return render_template('case_settings.html')

@auth.route('/reports')
@login_required
def reports():
	return render_template('reports.html')

@auth.route('/charts')
@login_required
def charts():
	return render_template('charts.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
		    login_user(user, form.remember_me.data)
		    return redirect(request.args.get('next') or url_for('auth.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
	    user = User(email=form.email.data,
	                username=form.username.data,
	                password=form.password.data)
	    db.session.add(user)
	    db.session.commit()
	    token = user.generate_confirmation_token()
	    return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)