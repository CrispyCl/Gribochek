from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length


class EditAudienceForm(FlaskForm):
    name = StringField('Название аудитории', validators=[DataRequired(), Length(min=5, max=40)])
    # about = TextAreaField('Описание', validators=[DataRequired()])
    # img = MultipleFileField('Фото аудитории')
    img = FileField('Фото аудитории')
    is_eventable = BooleanField('Место для мероприятий')
    submit = SubmitField()