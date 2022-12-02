import os
import datetime
import joblib
from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_moment import Moment
from flask_restful import Api
from sqlalchemy import desc

from alice2 import call_process
from data import db_session, call_resource
from data.calls import Call
from data.users import User
from forms.addcallform import AddCallForm
from forms.editcallform import EditCallForm
from forms.edituserform import EditUserForm
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from tables import *

app = Flask(__name__)
api = Api(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)
theme_clf = joblib.load('themes_clf')
cat_clf = joblib.load('cat_clf')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'url not found'}), 404
    else:
        return render_template('404.html', title='Страница не найдена'), 404


@app.errorhandler(401)
def unauthorized_access(error):
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            position=form.position.data,
            locality=form.locality.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = EditUserForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.email.data = user.email
            form.name.data = user.name
            form.surname.data = user.surname
            form.locality.data = user.locality
            form.position.data = user.position
        else:
            abort(404)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit_user.html', title='Профиль оператора',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data, User.id != id).first():
            return render_template('edit_user.html', title='Профиль оператора',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            user.email = form.email.data
            user.name = form.name.data
            user.surname = form.surname.data
            user.locality = form.locality.data
            user.position = form.position.data
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/login')
        else:
            abort(404)
    return render_template('edit_user.html', title='Профиль оператора', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/map')
@app.route('/')
def index():
    db_sess = db_session.create_session()
    calls = db_sess.query(Call).filter(Call.status != 'finished').all()
    db_sess.commit()
    calls_for_js = []
    for call in calls:
        if call.point:
            coord = [float(x) for x in call.point.split()]
            coord[1], coord[0] = coord[0], coord[1]
            theme_number = [k for k, v in translateT.items() if v == call.service][0]
            calls_for_js.append([coord, themeToCat[theme_number], call.id if current_user.is_authenticated else 0])

    return render_template('map.html', calls=calls_for_js)


@app.route('/add_call', methods=['GET', 'POST'])
@login_required
def add_call():
    form = AddCallForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        call = Call()
        call.message = form.message.data
        call.address = form.address.data
        call.recognize_call()
        db_sess.add(call)
        db_sess.commit()
        return redirect('/calls')
    return render_template('add_call.html', title='Новый вызов',
                           form=form)


@app.route('/calls/<int:call_id>', methods=['GET', 'POST'])
@login_required
def edit_call(call_id):
    form = EditCallForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        call = db_sess.query(Call).filter(Call.id == call_id).first()
        if call:
            form.message.data = call.message
            form.address.data = call.address
            form.service.data = call.service
            form.status.data = call.status
            form.answer.data = call.answer
            form.call_id.data = call.id
            form.call_time.data = call.call_time
            form.finish_time.data = call.finish_time
            if call.point:
                x, y = call.point.split()
                form.point.data = f"{x},{y}"
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        call = db_sess.query(Call).filter(Call.id == call_id).first()
        if call:
            call.message = form.message.data
            call.service = form.service.data
            call.answer = form.answer.data
            call.change_address(form.address.data)
            call.change_status(form.status.data)
            db_sess.commit()
            return redirect('/calls')
        else:
            abort(404)
    return render_template('edit_call.html',
                           title='Редактирование вызова',
                           form=form
                           )


@app.route('/calls')
@login_required
def calls():
    db_sess = db_session.create_session()
    calls = db_sess.query(Call).order_by(desc(Call.call_time)).all()
    db_sess.commit()
    return render_template('calls.html', calls=calls, time_now=datetime.datetime.today())


@app.route('/delete_call/<int:call_id>', methods=['GET', 'POST'])
@login_required
def delete_call(call_id):
    db_sess = db_session.create_session()
    call = db_sess.query(Call).filter(Call.id == call_id).first()
    if call:
        db_sess.delete(call)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/calls')


@app.route('/calls/post', methods=['POST'])
def alice_add_call():
    return call_process()


def main():
    db_session.global_init("emergency.db")
    api.add_resource(call_resource.CallListResource, '/api/calls')
    api.add_resource(call_resource.CallResource, '/api/calls/<int:id>')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(port=port, debug=True)


if __name__ == '__main__':
    main()
