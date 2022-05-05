from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from todo.models import User


class LoginForm(FlaskForm):
    user_name = StringField('User', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    user_name = StringField('User', validators=[DataRequired(),
                                                Regexp('^[A-Za-z0-9]*$', 0,
                                                       'User name must have only letters and numbers'),
                                                Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password',
                                                                             message='Passwords must match'),
                                                     Length(8, 20)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(8, 20)])
    submit = SubmitField('Register')

    def validate_user_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('User name already exist.')
