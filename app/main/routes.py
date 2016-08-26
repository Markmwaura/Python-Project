from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from ..models import User
from . import main
from app import db

from .forms import LoginForm, RegistrationForm


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.email.data,
        #            form.password.data)

        # db.session.add(user)
        # db.session.commit()

        User.register(form.username.data,form.password.data)
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)



@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/protected')
@login_required
def protected():
    return render_template('protected.html')
