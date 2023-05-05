from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from todo.auth.forms import LoginForm, RegisterForm
from todo.models import User, db


def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user_name.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('main.index')
            return redirect(next_url)
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.user_name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Now yor can login.')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)
