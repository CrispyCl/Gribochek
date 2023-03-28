from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class AddParForm(FlaskForm):
    group_id = SelectField('Выберите группу', choices=())
    submit = SubmitField()
