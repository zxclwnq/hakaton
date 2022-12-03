import os
import datetime
import random

from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc

from data import db_session, call_resource
from data.proposals import Proposal
from data.users import User
from forms.addproposalform import AddProposalForm
from forms.editcallform import EditCallForm
from forms.textratingform import TextRatingForm
from forms.videoratingform import VideoRatingForm
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






def get_proposal(proposal_id):
    db_sess = db_session.create_session()
    curr_proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    #db_sess.expunge_all()
    return curr_proposal

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
def index():
    """Запуск основой страцицы"""
    return render_template('main.html')


@app.route('/add_proposal', methods=['GET', 'POST'])
def add_proposal():  # new proposal
    """Добавление заявки в БД"""
    form = AddProposalForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_proposal = Proposal()

        proposal_id = random.randint(100,1000)# создание рандомного id
        # заполнение пустой заявки данными из формы
        new_proposal.make_proposal(proposal_id ,form.type.data, form.file.data, form.user_data)

        # добавление заявки в БД
        db_sess.add(new_proposal)
        db_sess.commit()
        return redirect("/proposals")
    return render_template('add_proposal.html',form=form)



""" Оценка заявок экспертами """
@app.route('/proposals/rate/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
def eval_proposal(proposal_id): # Оценивание заявок экспертами
    db_sess = db_session.create_session()
    current_proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    if current_proposal.type == "text":
        form = TextRatingForm()
    else:
        form = VideoRatingForm()

    if form.validate_on_submit():
        ratings = form.get_text_rating if current_proposal.type == 'text' else form.get_video_rating
        lowering_ratings = form.get_lowering_rating
        current_proposal.verify_proposal(ratings,lowering_ratings,'verified')
        db_sess.commit()
        return redirect("/proposals")
    return render_template("evaluate_proposal.html",type=current_proposal.type,form=form)

@app.route('/proposals/view/<int:proposal_id>', methods=['GET', 'POST'])
def view_proposal(proposal_id):
    proposal = get_proposal(proposal_id)
    return render_template('view_proposal.html',proposal=proposal)



@app.route('/proposals')
def proposals():
    db_sess = db_session.create_session()
    proposals = db_sess.query(Proposal).all()#.filter(Proposal.status == 'verified').all()
    db_sess.commit()
    return render_template('proposals.html', proposals=proposals)


@app.route('/delete_proposal/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
def delete_proposal(proposal_id):
    """Удаление заявки из БД
        Только для админов"""
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    if proposal:
        db_sess.delete(proposal)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/proposals')



def main():  # run program
    db_session.global_init("main.db")
    port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(port=port, debug=True)


if __name__ == '__main__':
    main()
