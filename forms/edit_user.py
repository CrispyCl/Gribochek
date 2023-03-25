from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField, SelectMultipleField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    # For self edit
    email = EmailField('Почта')
    img = FileField()
    password = PasswordField('Введите предыдущий пароль для изменений')

    # For other user edit
    name = StringField('Имя')
    surname = StringField('Фамилия')
    otchestvo = StringField('Отчество')
    # group = SelectMultipleField(u'', choices=(), validate_choice=False)

    # For all
    new_password = PasswordField('Новый пароль')
    password_again = PasswordField('Повторите пароль')

    submit = SubmitField()
