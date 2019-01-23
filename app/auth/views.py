from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import db, User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('main.index')
			return redirect(next)
		flash('Invalid username or password')	
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		
		flash(token)
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.add(current_user)
		db.session.commit()
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
			and request.blueprint != 'auth' \
			and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	#send_email(current_user.email, 'Reconfirm your account', 'auth/email/confirm', user=current_user, token=token)
	flash(token)
	return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.new_password.data
			db.session.add(current_user)
			db.session.commit()
			logout_user()
			flash('Passwords have changed, Please Log in again')
			return redirect(url_for('auth.login'))
		flash('Old passwords do not match')
	flash('妈卖批')
	return render_template('auth/change_password.html', form=form)

@auth.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token=user.generate_reset_token()
			flash('password reset email has been send')
			flash(token)
			return redirect(url_for('main.index'))
		flash('user is not existed')
	return render_template('auth/password_reset_request.html', form=form)

@auth.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	form = PasswordResetForm()
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('Password have been reset, please log in')
			return redirect(url_for('auth.login'))
		flash('The confirmation link is invalid or has expired')
		return redirect(url_for('auth.password_reset_request'))
	return render_template('auth/password_reset.html', form=form)
	
@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			token = current_user.generate_email_change_token(form.email.data)
			flash(url_for('.change_email_request')+'/'+token)
			return redirect(url_for('main.index'))
		flash('Invalid email or Wrong password')
	return render_template('auth/change_email_request.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		db.session.commit()
		flash('Email has been changed')
	else:
		flash('Invalid token or expired')
	return redirect(url_for('main.index'))

		



# @auth.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
# 	form = ResetPasswordForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(email=form.email.data).first()
# 		if user:
# 			token = user.generate_confirmation_token()
# 			flash('email sent, please check')
# 			flash(token)
# 			return redirect(url_for('main.index'))
# 		else:
# 			flash('wrong email')
# 	return render_template('auth/reset_password.html', form=form)

# @auth.route('reset_confirm/<token>', methods=['GET', 'POST'])
# def reset_confirm(token):
# 	form = ResetConfirmForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(email=form.email.data).first()
# 		if user:
# 			if user.confirm(token):
# 				user.password = form.password.data
# 				db.session.add(user)
# 				db.session.commit()
# 				flash('Your password has benn reset, please log in now')
# 				return redirect(url_for('auth.login'))
# 			flash('The confirmation link is invalid or has expired')
# 			return redirect(url_for('auth.reset_password'))db.session.add(self)
# 		flash('THe email does not exist')
# 	return render_template('auth/reset_confirm.html', form=form)

