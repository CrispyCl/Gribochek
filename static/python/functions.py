from PIL import Image

from data.users import User

ST_message = {'status': 404, 'text': ''}


def create_main_admin(db_sess):
    res = db_sess.query(User).all()
    if res:
        return
    user = User(
        id=1,
        email='main_admin@mail.ru',
        role=4,
        img='img/users/1.jpg'
    )
    Image.open('static/img/admin.jpg').save('static/img/users/1.jpg')
    user.set_password('111')
    db_sess.add(user)
    db_sess.commit()
