from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired


"""Разобраться с полями"""
class AddProposalForm(FlaskForm):

    #В словарь
    fullname = StringField('Введите ФИО', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    number = StringField('Введите ваш телефон', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    post = StringField('Введите вашу должность', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    place_of_work = StringField('Введите место работы', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    theme = StringField('Введите тему работы', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    title = StringField('Введите заголовок работы', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])
    annotation = StringField('Введите аннотацию по конкурсной работе', validators=[DataRequired(message="Поле 'адрес' не может быть пустым")])

    #Передаю в базу
    type = RadioField('Выберите тип заявки', choices=[('text','Печатное издание'),('video','Видеоматериал')])
    file = StringField('Введите ссылку на файл в облачном хранилище', validators=[DataRequired(message="Поле 'адрес' "
                                                                                                       "не может быть пустым")])
    @property
    def user_data(self):
        return {
            "fullname": str(self.fullname.data),
            "number": str(self.number.data),
            "post": str(self.post.data),
            "place of work": str(self.place_of_work.data),
            "theme": str(self.theme.data),
            "title": str(self.title.data),
            "annotation": str(self.annotation.data)
        }

    submit = SubmitField('Отправить заявку')
