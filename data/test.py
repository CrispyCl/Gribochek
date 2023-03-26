import datetime

from data import db_session
from data.audiences import Audience
from data.days import Day
from data.weeks import Week


db_session.global_init("../db/GriBD.db")
db_sess = db_session.create_session()
audience1 = Audience(
    id=0,
    name='',
    image='',
    is_eventable=False,
)
db_sess.add(audience1)
db_sess.commit()
week1 = Week(
    id=0,
    week_start_date=datetime.date.today(),
    week_end_date=datetime.date.today(),
    audience_id=0,
)

db_sess.add(week1)
db_sess.commit()

# day1 = Day(
#     id=0,
#     date=datetime.date.today(),
# )
# day2 = Day(
#     id=1,
#     date=datetime.date.today(),
# )
# day3 = Day(
#     id=2,
#     date=datetime.date.today(),
# )
# week1.days.append(day1)
# week1.days.append(day2)
# week2.days.append(day3)
# print(week2.days)
# print(week1.days)
# db_sess.commit()

res = db_sess.query(Week).all()
print(res)
for r in res:
    print(r.days)
