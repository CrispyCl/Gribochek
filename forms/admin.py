from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class RegisterAdminForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField()
