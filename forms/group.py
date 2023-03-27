from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired


class CreateGroupForm(FlaskForm):
    subject = StringField('Название дисциплины', validators=[DataRequired(), Length(min=4, max=20)])
    teacher_id = SelectField(u'', choices=())
    audience_id = SelectField(u'', choices=())
    course_start_date = DateField('Дата начала', validators=[DataRequired()])
    course_end_date = DateField('Дата конца', validators=[DataRequired()])
    day0 = IntegerField('Пн', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    day1 = IntegerField('Вт', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    day2 = IntegerField('Ср', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    day3 = IntegerField('Чт', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    day4 = IntegerField('Пт', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    day5 = IntegerField('Сб', validators=[NumberRange(min=0, max=2, message='must be by 0 to 2')], default=0)
    submit = SubmitField()
