from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from todo.auth.forms import LoginForm
from todo.models import User


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
