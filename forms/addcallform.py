from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

"""Разобраться с полями"""
class AddCallForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired(message="Поле 'сообщение' не может быть пустым")])
    address = StringField('Адрес происшествия', validators=[DataRequired(message="Поле 'адрес' не может быть пустым"),
                                                            ]) #тут был адрес
    submit = SubmitField('Добавить сообщение')
