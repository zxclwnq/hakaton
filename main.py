import os
import datetime
from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from data import db_session, call_resource
from data.proposals import Proposal
from data.users import User
from forms.addcallform import AddCallForm
from forms.editcallform import EditCallForm

from forms.loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # find user in database
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# add proposal
# delete proposal
def add_proposal(proposal:Proposal):
    """Добавление заявки в БД"""
    db_sess = db_session.create_session()
    return db_sess.add(User)

@app.errorhandler(404)
def not_found(error):  # Error 404
    return render_template('404.html', title='Страница не найдена'), 404


@app.errorhandler(401)
def unauthorized_access(error):  # Access error
    return redirect('/login')






@app.route('/login', methods=['GET', 'POST'])
def login():  # Auth of experts and administrator
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
def logout():  # exit
    logout_user()
    return redirect("/")


@app.route('/')
def index():  # main page
    db_sess = db_session.create_session()
    calls = db_sess.query(Proposal).filter(Proposal.status != 'finished').all()
    db_sess.commit()
    return render_template('main.html')


@app.route('/add_proposal', methods=['GET', 'POST'])
@login_required
def add_proposal():  # new proposal
    form = None  # Витина форма (Не работает)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        proposal = Proposal()
        proposal.message = form.message.data
        proposal.address = form.address.data
        proposal.recognize_call()
        db_sess.add(proposal)
        db_sess.commit()
        return redirect('/proposals')
    return render_template('add_proposal.html', title='Новый вызов',
                           form=form)

"""ПОЛНОСТЬЮ Переделать"""
@app.route('/proposals/<int:call_id>', methods=['GET', 'POST'])
@login_required
def edit_proposal(call_id):  # edit existing proposal (i.e., edit grading)
    form = EditCallForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        proposal = db_sess.query(Proposal).filter(Proposal.id == call_id).first()
        if proposal:
            form.message.data = proposal.message
            form.address.data = proposal.address
            form.service.data = proposal.service
            form.status.data = proposal.status
            form.answer.data = proposal.answer
            form.call_id.data = proposal.id
            form.call_time.data = proposal.call_time
            form.finish_time.data = proposal.finish_time
            if proposal.point:
                x, y = proposal.point.split()
                form.point.data = f"{x},{y}"
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        proposal = db_sess.query(Proposal).filter(Proposal.id == call_id).first()
        if proposal:
            proposal.message = form.message.data
            proposal.service = form.service.data
            proposal.answer = form.answer.data
            proposal.change_address(form.address.data)
            proposal.change_status(form.status.data)
            db_sess.commit()
            return redirect('/calls')
        else:
            abort(404)
    return render_template('edit_proposal.html',
                           title='Редактирование вызова',
                           form=form)


@app.route('/proposals')
@login_required
def proposals():
    db_sess = db_session.create_session()
    calls = db_sess.query(Proposal).order_by(desc(Proposal.call_time)).all() # call time нет !!!
    db_sess.commit()
    return render_template('proposals.html', calls=calls, time_now=datetime.datetime.today())


@app.route('/delete_proposal/<int:call_id>', methods=['GET', 'POST'])
@login_required
def delete_proposal(call_id):  # delete proposal (e.g. copy of someone's work)
    db_sess = db_session.create_session()
    call = db_sess.query(Proposal).filter(Proposal.id == call_id).first()
    if call:
        db_sess.delete(call)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/calls')



"""Сейчас не заработает из-за ошибок в полях с адресом"""

def main():  # run program
    db_session.global_init("main.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=port, debug=True)

if __name__ == '__main__':
    main()
