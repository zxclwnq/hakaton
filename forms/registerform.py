from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
"""Тут не надо (сразу запихать в базу)"""
class RegisterForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(message="Поле 'почта' не может быть пустым")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    name = StringField('Имя оператора', validators=[DataRequired(message="Поле 'имя' не может быть пустым")])
    surname = StringField('Фамилия оператора', validators=[DataRequired(message="Поле 'фамилия' не может быть пустым")])
    submit = SubmitField('Зарегистрироваться')


