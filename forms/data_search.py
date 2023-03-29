from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class DataSearchForm(FlaskForm):
    need_date = DateField('Нужная дата', validators=[DataRequired()])
    submit = SubmitField("Найти")
