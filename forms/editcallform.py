from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired
from forms.geo_validators import AddressRequired
from tables import translateT

class EditCallForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired(message="Поле 'сообщение' не может быть пустым")])
    address = StringField('Адрес', validators=[DataRequired(message="Поле 'адрес' не может быть пустым"),
                                                            AddressRequired(unique=True)])
    service = SelectField(u'Тема',
                          choices=
                          [(x, x) for x in translateT.values()])
    status = RadioField('Статус',
                        choices=[('received', 'Принят'), ('serviced', 'Выполняется'), ('finished', 'Завершен')])
    answer = StringField('Ответ')
    call_time = DateTimeField('Время вызова')
    finish_time = DateTimeField('Время завершения')
    call_id = IntegerField('ID')
    point = StringField('Point')
    submit = SubmitField('Cохранить изменения')
