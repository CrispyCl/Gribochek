from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, StringField, SelectField
from wtforms.validators import DataRequired


class MerCreateFORM(FlaskForm):
    date = DateField('Нужная дата', validators=[DataRequired()])
    name = StringField("Название мероприятия", validators=[DataRequired()])
    time = SelectField('Выберите время мероприятия', choices=())
    submit = SubmitField("Создать")
