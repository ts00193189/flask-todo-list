from flask import render_template
from todo.auth.forms import LoginForm


def login():
    form = LoginForm()
    return render_template('login.html', form=form)
