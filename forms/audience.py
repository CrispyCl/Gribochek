from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired


class AudienceForm(FlaskForm):
    name = StringField('Название аудитории', validators=[DataRequired()])
    # about = TextAreaField('Описание', validators=[DataRequired()])
    # img = MultipleFileField('Фото аудитории')
    img = FileField('Фото аудитории')
    is_eventable = BooleanField('Место для мероприятий')
    submit = SubmitField()
