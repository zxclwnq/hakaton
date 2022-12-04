import os
from datetime import datetime
import random
from multiprocessing import Process
from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from classes.stage import Stage
from data import db_session
from data.proposals import Proposal
from data.users import User
from data.voting import Vote
from forms.addexpertform import AddExpertForm
from forms.addproposalform import AddProposalForm
from forms.editcallform import EditCallForm
from forms.textratingform import TextRatingForm
from forms.videoratingform import VideoRatingForm
from forms.loginform import LoginForm
from forms.registerform import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)
competition_stage = Stage()




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

@app.route('/add_expert', methods=['GET', 'POST'])
@login_required
def add_expert():
    if current_user.access_level == 3:
        form = AddExpertForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация эксперта',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация эксперта',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User()
            user.make_new(form.name.data,form.surname.data,form.email.data,form.password.data,"expert")
            db_sess.add(user)
            db_sess.commit()
            return render_template('locked.html', title="Аккаунт эксперта успешно создан")

        return render_template('register.html', title='Регистрация эксперта', form=form)
    return  render_template('locked.html', title="Недостаточно прав")
@app.route('/')
def index():
    """Запуск основой страцицы"""
    db_sess = db_session.create_session()
    total_proposals = db_sess.query(Proposal).all()
    db_sess.commit()
    verified_proposes = db_sess.query(Proposal).filter(Proposal.status == "verified").all()
    return render_template('news.html',stage=competition_stage,
                           total_proposals=len(total_proposals),
                           verified_proposes=len(verified_proposes))
@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    db_sess = db_session.create_session()
    my_proposals_ids = current_user.proposals_list
    my_proposals = []
    for proposal_id in my_proposals_ids:
        my_proposals.append(db_sess.query(Proposal).filter(Proposal.id == proposal_id).first())
    return render_template('cabinet.html',
                           stage=competition_stage,
                           proposals=my_proposals,
                           is_empty=len(my_proposals)==0)


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
        user = User()
        user.make_new(form.name.data,form.surname.data,form.email.data,form.password.data,"user")
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_proposal', methods=['GET', 'POST'])
@login_required
def add_proposal():  # new proposal
    """Добавление заявки в БД"""
    global competition_stage

    if competition_stage.can_make_proposes:
        if current_user.access_level !=0:
            return render_template('locked.html', title='Вы не можете создавать заявки',
                                   message='Пользователи отвечающие за проверку и администрацию сайта не могут '
                                           'создавать заявки')
        form = AddProposalForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            new_proposal = Proposal()

            # заполнение пустой заявки данными из формы
            new_proposal.make_proposal(form.type.data, form.file.data, form.user_data)
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            # добавление заявки в БД
            db_sess.add(new_proposal)
            db_sess.commit()
            # прикрепление заявки к пользователю
            user.add_proposal(new_proposal.id)
            db_sess.commit()


            return redirect("/cabinet")
        return render_template('add_proposal.html',form=form)

    return render_template('locked.html', title='Страница не доступна в данный момент')

@app.route('/set_stage/<int:stage_id>', methods=['GET', 'POST'])
@login_required
def set_stage(stage_id):
    global competition_stage
    competition_stage.set_stage(stage_id)
    return redirect('/')

""" Оценка заявок экспертами """
@app.route('/proposals/rate/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
def eval_proposal(proposal_id): # Оценивание заявок экспертами
    db_sess = db_session.create_session()
    current_proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    form = TextRatingForm() if current_proposal.type == "text" else VideoRatingForm()


    if form.validate_on_submit():
        ratings = form.get_text_rating if current_proposal.type == 'text' else form.get_video_rating
        lowering_ratings = form.get_lowering_rating
        ratings["expert"] = f"{current_user.surname} {current_user.name}"
        lowering_ratings["expert"] = f"{current_user.surname} {current_user.name}"
        current_proposal.verify_proposal(ratings,lowering_ratings,current_user.id)
        db_sess.commit()
        return render_template('locked.html', title=f'Заявка № {current_proposal.id} успешно оценена',
                               message="")
    return render_template("evaluate_proposal.html",proposal=current_proposal,form=form)

@app.route('/proposals/view/<int:proposal_id>', methods=['GET', 'POST'])
def view_proposal(proposal_id):
    proposal = get_proposal(proposal_id)
    return render_template('view_proposal.html',proposal=proposal)



@app.route('/proposals')
def proposals():
    if competition_stage.result_table_state == 0:
        return render_template('locked.html', title='Страница не доступна в данный момент',
                               message="")
    elif competition_stage.result_table_state == 1:
        db_sess = db_session.create_session()
        proposals = db_sess.query(Proposal).order_by(Proposal.likes.desc()).all()
        db_sess.commit()
        return render_template('proposals_voting.html', proposals=proposals)
    elif competition_stage.result_table_state == 2:
        db_sess = db_session.create_session()
        proposals = db_sess.query(Proposal).order_by(Proposal.likes.desc()).all()
        db_sess.commit()
        return render_template('proposals.html', proposals=proposals)
    return render_template('locked.html', title='Произошла ошибка во время работы')

@app.route('/proposals/vote/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
def vote_proposal(proposal_id):
    if current_user.access_level != 0:
        return render_template('locked.html', title="Вы не можете принимать участие в голосовании")
    if proposal_id in current_user.proposals_list:
        return render_template('locked.html', title="Вы не можете проголосовать за свою работу")
    db_sess = db_session.create_session()
    votes = db_sess.query(Vote).filter(Vote.proposal_id == proposal_id).all()
    if current_user.id in [votes[i].user_id for i in range(len(votes))]:
        return render_template('locked.html', title="Вы уже голосовали за эту работу")
    new_vote = Vote(user_id=current_user.id,
                    proposal_id=proposal_id)
    db_sess.add(new_vote)
    proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    proposal.inc_likes()
    db_sess.commit()
    return render_template('locked.html', title="Ваш голос зачтен")




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
