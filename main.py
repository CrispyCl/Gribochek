from flask import Flask, redirect, render_template, request, abort, url_for, session
from PIL import Image
from flask_login import LoginManager, current_user, login_required, logout_user, login_user

from data import db_session
from data.audiences import Audience
from data.users import User
from forms.admin import RegisterAdminForm
from forms.audience import AudienceForm
from forms.edit_user import EditUserForm
from forms.user import RegisterForm
from static.python.functions import create_main_admin, ST_message
from copy import copy
from json import dumps, loads

current_user.is_authenticated: bool

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('message'):
        session['message'] = dumps(ST_message)
    smessage = session['message']
    if request.method == 'POST':
        db_sess = db_session.create_session()
        password = request.form['password']
        email = request.form['email']
        remember = bool(request.form.getlist('remember'))
        print(remember)
        user = db_sess.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect('/')
        message = {'status': 0, 'text': 'Неверный логин или пароль'}
        return render_template('index.html',
                               title='Главная страница', message=dumps(message))
    session['message'] = dumps(ST_message)
    return render_template('index.html', title='Главная страница', message=smessage)


@app.route('/profile/<int:user_id>', methods=["GET", "POST"])
def profile(user_id):
    db_sess = db_session.create_session()
    db_sess.query(User).get(user_id)
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404)
    if user.role == 4:
        abort(404)
    if user.role == 3 and current_user.role != 4:
        abort(404)
    if current_user.role == 1 and current_user.id != user_id:
        abort(404)
    smessage = session['message']
    session['message'] = dumps(ST_message)
    return render_template('profile.html', title='Профиль', message=smessage, user=user)


@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if not current_user.is_authenticated:
        abort(404)
    if not current_user.role == 4:
        abort(404)
    form = RegisterAdminForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    last_id = users[-1].id + 1

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            message = {'status': 0, 'text': 'Пароли не совпадают'}
            return render_template('register_admin.html', title='Регистрация админа',
                                   form=form,
                                   message=dumps(message))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            message = {'status': 0, 'text': 'Такой пользователь уже есть'}
            return render_template('register_admin.html', title='Регистрация админа',
                                   form=form,
                                   message=dumps(message))
        user = User(
            id=last_id,
            email=form.email.data,
            role=3,
            img=f'img/users/{last_id}.jpg',
        )
        Image.open(
            'static/img/admin.jpg').save(f'static/img/users/{last_id}.jpg')
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        message = dumps({'status': 1, 'text': 'Администратор зарегистрирован'})
        session['message'] = message
        return redirect('/')
    return render_template('register_admin.html', title='Регистрация админа', form=form, message=dumps(ST_message))


@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if not current_user.is_authenticated:
        abort(404)
    if current_user.role not in (3, 4):
        abort(404)
    form = RegisterForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    last_id = users[-1].id + 1

    if form.validate_on_submit():
        print(0)
        if form.password.data != form.password_again.data:
            message = {'status': 0, 'text': 'Пароли не совпадают'}
            return render_template('register_teacher.html', title='Регистрация преподавателя',
                                   form=form,
                                   message=dumps(message))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            message = {'status': 0, 'text': 'Такой пользователь уже есть'}
            return render_template('register_teacher.html', title='Регистрация преподавателя',
                                   form=form,
                                   message=dumps(message))
        user = User(
            id=last_id,
            name=form.name.data,
            surname=form.surname.data,
            otchestvo=form.otchestvo.data,
            email=form.email.data,
            role=2,
        )
        print(1)
        if form.img.data:
            form.img.data.save(f"static/img/users/{last_id}.jpg")
        else:
            Image.open(
                f'static/img/teachers/no-img.jpg').save(f"static/img/users/{last_id}.jpg")
        user.img = f'img/users/{last_id}.jpg'
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        message = dumps({'status': 1, 'text': 'Учитель зарегистрирован'})
        session['message'] = message
        return redirect('/')
    return render_template('register_teacher.html', title='Регистрация преподавателя', form=form, message=dumps(ST_message))


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if not current_user.is_authenticated:
        abort(404)
    if current_user.role not in (3, 4):
        abort(404)
    form = RegisterForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    last_id = 1 if not users else users[-1].id + 1

    if request.method == 'GET':
        pass
        # groups = db_sess.query(Group.name).all()
        # groups = [(1, 'Первая группа'), (2, 'Вторая группа')]
        # form.group.choices = groups

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            message = {'status': 0, 'text': 'Пароли не совпадают'}
            return render_template('register_student.html', title='Регистрация студента',
                                   form=form,
                                   message=dumps(message))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            message = {'status': 0, 'text': 'Такой пользователь уже есть'}
            return render_template('register_student.html', title='Регистрация студента',
                                   form=form,
                                   message=dumps(message))
        user = User(
            id=last_id,
            name=form.name.data,
            surname=form.surname.data,
            otchestvo=form.otchestvo.data,
            email=form.email.data,
            role=1,
        )
        if form.img.data:
            img1 = form.img.data
            img1.save(f"static/img/users/{last_id}.jpg")
        else:
            Image.open(
                f'static/img/users/no-img.jpg').save(f"static/img/users/{last_id}.jpg")
        user.img = f'img/users/{last_id}.jpg'
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        message = dumps({'status': 1, 'text': 'Ученик зарегистрирован'})
        session['message'] = message
        return redirect('/')
    return render_template('register_student.html', title='Регистрация студента', form=form, message=dumps(ST_message))


@app.route('/create_audience', methods=['GET', 'POST'])
def create_audience():
    if not current_user.is_authenticated:
        abort(404)
    if current_user.role not in (3, 4):
        abort(404)
    form = AudienceForm()
    smessage = session['message']
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Audience).filter(Audience.name == form.name.data).first():
            message = {'status': 0, 'text': 'Такая аудитория уже есть'}
            return render_template('create_audience.html', title='Создание аудитории',
                                   form=form,
                                   message=dumps(message))
        audiences = db_sess.query(Audience).all()
        last_id = audiences[-1].id + 1 if audiences else 0
        audience = Audience(
            id=last_id,
            name=form.name.data
        )
        if form.is_eventable.data:
            audience.is_eventable = form.is_eventable.data
        # le = 0
        # auditories_path = []
        # if form.img.data:
        #     i = last_id
        #     for file in form.img.data:
        #         auditories_path.append(f'img/audiences/au{last_id}im{i}.jpg')
        #         file.save(f"static/" + auditories_path[-1])
        #         i += 1
        #         le += 1
        # auditory.image_count = le
        # auditory.images = '✡'.join(auditories_path)
        if form.img.data:
            form.img.data.save(f'static/img/audiences/au{last_id}im.jpg')
        else:
            Image.open(
                'static/img/standarts/audience.jpg').save(f'static/img/audiences/au{last_id}im.jpg')
        audience.image = f'img/audiences/au{last_id}im.jpg'

        db_sess.add(audience)
        db_sess.commit()
        message = dumps({'status': 1, 'text': 'Аудитория создана'})
        session['message'] = message
        return redirect('/')
    session['message'] = dumps(ST_message)
    return render_template('create_audience.html', title='Создание аудитории', form=form,
                           message=smessage)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if not current_user.is_authenticated:
        abort(404)
    if current_user.role in (1, 2) and current_user.id != user_id:
        abort(404)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404)
    if user.role == 4:
        abort(404)
    if current_user.role == user.role and current_user.id != user.id:
        abort(404)
    form = EditUserForm()
    smessage = session['message']
    if request.method == 'GET':
        if current_user.id == user.id or user.role == 3:
            form.email.data = user.email
        else:
            form.name.data = user.name
            form.surname.data = user.surname
            form.otchestvo.data = user.otchestvo
    if form.validate_on_submit():
        if form.new_password.data != form.password_again.data:
            message = {'status': 0, 'text': 'Пароли не совпадают'}
            return render_template('edit_user.html', title='Изменение профиля',
                                   form=form, user=user,
                                   message=dumps(message))
        if current_user.id == user.id:
            if db_sess.query(User).filter(User.email == form.email.data).first() and form.email.data != user.email:
                message = {'status': 0, 'text': 'Такой пользователь уже есть'}
                return render_template('edit_user.html', title='Изменение профиля', user=user,
                                       form=form, message=dumps(message))
            if not user.check_password(form.password.data):
                message = {'status': 0,
                           'text': 'Введён неверный старый пароль'}
                return render_template('edit_user.html', title='Изменение профиля',
                                       form=form, user=user,
                                       message=dumps(message))
            user.email = form.email.data
            if form.img.data:
                form.img.data.save(f'static/img/users/{user.id}.jpg')
            if form.new_password.data:
                user.set_password(form.new_password.data)
            db_sess.merge(user)
            db_sess.commit()
            message = dumps({'status': 1, 'text': 'Профиль изменён'})
            session['message'] = message
            return redirect('/')
        else:
            if user.role == 3:
                if db_sess.query(User).filter(User.email == form.email.data).first() and form.email.data != user.email:
                    message = {'status': 0,
                               'text': 'Такой пользователь уже есть'}
                    return render_template('edit_user.html', title='Изменение профиля', user=user,
                                           form=form, message=dumps(message))
                user.email = form.email.data
                if form.new_password.data:
                    user.set_password(form.new_password.data)
                db_sess.merge(user)
                db_sess.commit()
                message = dumps({'status': 1, 'text': 'Профиль изменён'})
                session['message'] = message
                return redirect('/')
            else:
                if form.new_password.data:
                    user.set_password(form.new_password.data)
                user.name = form.name.data
                user.surname = form.surname.data
                user.otchestvo = form.otchestvo.data
                db_sess.merge(user)
                db_sess.commit()
                message = dumps({'status': 1, 'text': 'Профиль изменён'})
                session['message'] = message
                return redirect('/')
    session['message'] = dumps(ST_message)
    return render_template('edit_user.html', title='Изменение профиля', form=form, message=smessage,
                           user=user)


@app.route('/teachers')
def teachers():
    return render_template('teachers.html', message=dumps(ST_message))


@app.route('/users')
def users():
    return render_template('users.html', message=dumps(ST_message))


@app.route('/group/1')
def group():
    return render_template('group.html', message=dumps(ST_message))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/audience_list')
def audience_list():
    if not current_user.is_authenticated:
        abort(404)
    smessage = session['message']
    db_sess = db_session.create_session()
    audiences = db_sess.query(Audience).all()
    return render_template('audience_list.html', audiences=audiences, title='Список аудиторий', message=smessage, curuser=current_user)


@app.route('/audience/<int:aud_id>', methods=["GET", "POST"])
def audience(aud_id):
    db_sess = db_session.create_session()
    db_sess.query(Audience).get(aud_id)
    audience = db_sess.query(Audience).filter(Audience.id == aud_id).first()
    session['message'] = dumps(ST_message)
    smessage = session['message']
    if request.method == 'GET':
        return render_template('audience.html', title=f'{audience.name}', message=smessage, audience=audience)
    else:
        return redirect(f'/audience/{aud_id}')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    # db_session.global_init("db/structure.db")
    db_session.global_init("db/GriBD.db")
    create_main_admin(db_session.create_session())
    app.run(port=8081, host='127.0.0.1')
