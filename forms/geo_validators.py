import requests
from wtforms import ValidationError


class AddressRequired:
    def __init__(self, message=None, unique=False):
        '''
        инициализация валидатора адреса
        :param message: сообщение об ошибке
        :param many_variants: допустимо ли много вариантов адреса
        '''
        if not message:
            message = 'Должен быть указан существующий адрес'
        self.message = message
        self.unique=unique

    def __call__(self, form, field):
        """
        Проверяет адрес
        :param form: Форма
        :param field: Поле
        :return: Бросает исключение, если адрес неверный
        """
        if len(field.data.strip()) == 0:
            raise ValidationError(self.message)

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": field.data.strip(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            raise ValidationError("Не могу проверить адрес")

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем количество топонимов
        count = int(json_response["response"]["GeoObjectCollection"][
            "metaDataProperty"]["GeocoderResponseMetaData"]["found"])
        if count == 0 or self.unique and count > 1:
            raise ValidationError(self.message)

