ST_message = {'status': 404, 'text': ''}
DAYS = {1: 'Пн', 2: "Вт", 3: "Ср", 4: "Чт", 5: "Пт", 6: "Сб"}
PARS_TIMES = {1: '8:30-10:00', 2: '11:40-13:10', 3: '13:20-14:50', 4: '15:00-16:30', 5: '16:40-18:10', 6: '18:15-19:45'}


class vAudience:
    def __init__(self, auditory_id, name, image, is_eventable):
        self.id = auditory_id
        self.name = name
        self.image = image
        self.is_eventable = is_eventable

    def __str__(self):
        return f"id: {self.id},\n" \
               f"name:{self.name},\n" \
               f"image{self.image},\n" \
               f"is_eventable{self.is_eventable}"


class vUser:
    def __init__(self, user_id, name, surname, otchestvo, email, hashed_password, img, role):
        self.id = user_id
        self.name = name
        self.surname = surname
        self.otchestvo = otchestvo
        self.email = email
        self.hashed_password = hashed_password
        self.img = img
        self.role = role


class vGroup:
    def __init__(self, group_id, subject, teacher: vUser, audience: vAudience, week_day0, week_day1, course_start_date,
                 course_end_date):
        self.id = group_id
        self.subject = subject
        self.teacher = teacher
        self.audience = audience
        self.week_day0 = week_day0
        self.week_day1 = week_day1
        self.course_start_date = course_start_date
        self.course_end_date = course_end_date


class vDay:
    def __init__(self, day_id, para_groups: list[vGroup], week, date, is_holiday):
        self.id = day_id
        self.pars = para_groups
        self.week = week
        self.date = date
        self.is_holiday = is_holiday


class vWeek:
    def __init__(self, week_id, week_start_date, week_end_date, audience, days: list[vDay]):
        self.id = week_id
        self.week_end_date = week_end_date
        self.week_start_date = week_start_date
        self.audience = audience
        self.days = days

    def __str__(self):
        return f"id: {self.id},\n" \
               f"week_end_date:{self.week_end_date},\n" \
               f"week_start_date{self.week_start_date},\n" \
               f"audience{self.audience},\n" \
               f"days{self.days}"
