import datetime
import sqlalchemy
import requests
import random
from sqlalchemy import null
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from tables import *


def predict_service(text):
    """
    функция определяет какую службу вызвать по сообщению о ЧС
    :param text: сообщение о ЧС
    :return: название службы "ambulance", "fire" или "police"
    """
    from main import theme_clf
    from alice2 import translateTheme
    if text.strip() != "":
        rez = theme_clf.predict([text])[0]
        #rez = random.choice(themes)
        return translateTheme(rez)


class Call(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'calls'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    point = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    service = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    call_time = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.utcnow())
    finish_time = sqlalchemy.Column(sqlalchemy.DateTime,
                                    nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def recognize_call(self):
        """
        Заполняет поля address, point, service для нового вызова на основе сообщения и адреса
        """
        # определяем какую службу вызвать
        self.service = predict_service(self.message)
        self.change_address(self.address)
        self.change_status("received")

    def change_status(self, new_status):
        """
        Изменяет статус вызова received -> serviced -> finished
        :param new_status: новый статус
        """
        if new_status == "received":
            self.call_time = datetime.datetime.utcnow()
        elif new_status == "finished":
            self.finish_time = datetime.datetime.utcnow()
        self.status = new_status

    def change_address(self, new_address):
        """
        Изменяет адрес, обновляет координаты вызова
        :param new_address: новый адрес
        """
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": new_address.strip(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            raise ConnectionError("Не могу проверить адрес")

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем количество топонимов
        count = int(json_response["response"]["GeoObjectCollection"][
                        "metaDataProperty"]["GeocoderResponseMetaData"]["found"])
        if count == 0:
            raise LookupError("Не существует адрес")

        # Получаем топоним
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        self.point = toponym["Point"]["pos"]
        self.address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
