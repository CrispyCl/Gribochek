from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField, SelectField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=30)])
    otchestvo = StringField('Отчество', validators=[Length(min=0, max=30)])
    groups = SelectField(u'', choices=())
    img = FileField()
    submit = SubmitField()
