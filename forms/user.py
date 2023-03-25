from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    otchestvo = StringField('Отчество', validators=[DataRequired()])
    # group = SelectField(u'', choices=(), validate_choice=False)
    img = FileField()
    submit = SubmitField()
