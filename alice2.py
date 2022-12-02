# -*- coding: utf-8 -*-

import joblib  # to load models
import numpy as np  # operations with arrays
import json  # work with json requests and responses
from tables import *
from flask import request
from data import db_session
from data.calls import Call
import csv

# words of agreement
accept = ['да', 'конечно', 'точно', 'верно', 'согласен', 'естественно', 'правильно', 'ага', 'именно', 'правда']


# words of disagreemnt
decline = ['не', 'нет', 'неверно', 'не верно', 'неправильно', 'не правильно', 'не точно', 'неточно', 'несогласен',
           'не согласен', 'неа', 'не правда', 'неправда', 'несогласен', 'не согласен']

def check_address(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value'] and 'street' in entity['value'] and 'house_number' in entity['value']:
                return True
    return False


def getCatOfTheme(theme):
    ''' returns id of categorie of theme '''
    return themeToCat[themes[theme]]


def getThemesOfCat(categorie):
    ''' returns ids of themes of categorie '''
    return catToThemes[сategories[categorie]]


def translateTheme(n):
    ''' returns translation of theme from id '''
    return translateT[themes[n]]


def translateCategorie(n):
    ''' returns translation of categorie from id '''
    return translateC[сategories[n]]


def ask(txt):
    if any(x in txt[0].lower() for x in decline):
        return -1
    elif any(x in txt[0].lower() for x in accept):
        return 1
    else:
        return 0


def to_zeros(arr, cat):
    x = getThemesOfCat(cat)
    for i in range(len(arr[0])):
        if themes[i] not in x:
            arr[0][i] = 0


cat_model = joblib.load('cat_clf')  # load classificator of categories
themes_model = joblib.load('themes_clf')  # load classificator of themes

sessionStorage = {}


def call_process():
    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    dialog(request.json, response)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response, ensure_ascii=False, indent=2)


def ask1(req, res, user_id):
    print("First asks")
    sessionStorage[user_id]['cats'] += 1
    if sessionStorage[user_id]['cats']-1 == 0:
        sessionStorage[user_id]['themes'] = themes_model.predict_proba(sessionStorage[user_id]['message'])
        sessionStorage[user_id]['categories'] = cat_model.predict_proba(sessionStorage[user_id]['message'])
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response']['text'] = f'Вы подразумевали тему "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'

    elif sessionStorage[user_id]['cats']-1 == 1:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = 'Принято. Пожалуйста, уточните адрес.'
            sessionStorage[user_id]['askadress'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
            res['response'][
                'text'] = f'Вы подразумевали тему "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'
            sessionStorage[user_id]['askcat'] = True

    else:
        sessionStorage[user_id]["noask"] = True
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято. Пожалуйста, уточните адрес.'
            sessionStorage[user_id]['askadress'] = True
        else:
            print("Reask message")
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            res['response']['text'] = f'Пожалуйста, повторите сообщение, указав больше важной информации'
            sessionStorage[user_id]['cats'] += 1



def reask(req, res, user_id):
    print('Reasking...')
    sessionStorage[user_id]["reask_msg"] = False
    if sessionStorage[user_id]['cats'] == 0:
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response']['text'] = f'Вы подразумевали тему "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'
        sessionStorage[user_id]['cats'] += 1

    elif sessionStorage[user_id]['cats'] == 1:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято. Пожалуйста, уточните адрес.'
            sessionStorage[user_id]['askadress'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
            res['response'][
                'text'] = f'Вы подразумевали категорию "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'
            sessionStorage[user_id]['cats'] += 1
            sessionStorage[user_id]['askcat'] = True
            sessionStorage[user_id]['reask'] = False

    else:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято. Пожалуйста, уточните адрес.'
            sessionStorage[user_id]['askadress'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['cat_max'] = np.argmax(sessionStorage[user_id]['categories'], axis=1)[0]
            res['response'][
                'text'] = f'Вы подразумевали категорию "{translateCategorie(sessionStorage[user_id]["cat_max"])}"?'
            sessionStorage[user_id]['cats'] += 1000
            sessionStorage[user_id]['askcat'] = True
            sessionStorage[user_id]['reask'] = False


def askcat(req, res, user_id):
    print("Asking cat...")
    print(sessionStorage[user_id]["categories"][0])
    if ask(sessionStorage[user_id]['message']) == 1:
        sessionStorage[user_id]["categorie"] = sessionStorage[user_id]["cat_max"]
        to_zeros(sessionStorage[user_id]["themes"], sessionStorage[user_id]["categorie"])
        sessionStorage[user_id]["theme_max"] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response']['text'] = f'Принято\nВы подразумевали тему "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'
        sessionStorage[user_id]['askcat'] = False
        sessionStorage[user_id]['asktheme'] = True
        print(sessionStorage[user_id]["themes"])
    else:
        if not sessionStorage[user_id]['categories'].any():
            res['response']['text'] = 'К сожалению не удалось распознать категорию сообщения'
            sessionStorage[user_id]['askadress'] = True
            return
        sessionStorage[user_id]['categories'][0][sessionStorage[user_id]['cat_max']] = 0
        sessionStorage[user_id]['cat_max'] = np.argmax(sessionStorage[user_id]['categories'], axis=1)[0]
        print(sessionStorage[user_id])
        res['response'][
            'text'] = f'Возможно Вы подразумевали категорию "{translateCategorie(sessionStorage[user_id]["cat_max"])}"?'


def askTheme(req, res, user_id):
    print("Asking themes...")
    print(sessionStorage[user_id]["themes"])
    if sessionStorage[user_id]['new']:
        sessionStorage[user_id]["theme_max"] = np.argmax(sessionStorage[user_id]["themes"])
        sessionStorage[user_id]['new'] = False
    if ask(sessionStorage[user_id]['message']) == 1:
        sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
        sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
        res['response'][
            'text'] = f'Принято. Пожалуйста, уточните адрес.'
        res['response']['end_session'] = True
    else:
        if not sessionStorage[user_id]['themes'].any():
            res['response']['text'] = 'К сожалению не удалось распознать тему сообщения'
            sessionStorage[user_id]['askadress'] = True
            return
        sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response'][
            'text'] = f'В таком случае, Вы подразумевали тему "{translateTheme(sessionStorage[user_id]["theme_max"])}"?'


def dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[user_id] = {
            'theme_max': -1,
            'cat_max': -1,
            'noask': False,
            'message': '',
            'address': '',
            'theme': '',
            'categorie': '',
            'cats': 0,
            'reask': False,
            'themes': np.array([]),
            'categories': np.array([]),
            'askcat': False,
            'asktheme': False,
            'new': True,
            'askadress': False,
            'firstmsg': '',
            'savemsg': True
        }
        # Заполняем текст ответа
        print("New user")
        res['response']['text'] = 'Здравствуйте! Пожалуйста, расскажите о проблеме, с которой Вы столкнулись'
        return
    sessionStorage[user_id]['message'] = [req['request']['original_utterance']]
    if not sessionStorage[user_id]["askadress"]:
        if sessionStorage[user_id]["savemsg"]:
            sessionStorage[user_id]["firstmsg"] = sessionStorage[user_id]["message"]
            sessionStorage[user_id]["savemsg"] = False
        if not sessionStorage[user_id]["noask"]:
            ask1(req, res, user_id)

        elif sessionStorage[user_id]['reask']:
            reask(req, res, user_id)
            return

        elif sessionStorage[user_id]['askcat']:
            askcat(req, res, user_id)
            return

        elif sessionStorage[user_id]['asktheme']:
            askTheme(req, res, user_id)
            return

    elif sessionStorage[user_id]['askadress']:
        if check_address(req):
            sessionStorage[user_id]['address'] = req['request']['original_utterance']
            # создать вызов
            call = Call()
            call.message = sessionStorage[user_id]['firstmsg'][0]
            #call.address = sessionStorage[user_id]['address']
            call.service = translateTheme(sessionStorage[user_id]["theme"])
            call.change_status("received")
            try:
                call.change_address(sessionStorage[user_id]["address"])
            except:
                res['response']['text'] = f'Пожалуйста, уточните адрес. Возможно вы ошиблись или не указали полное ' \
                                         f'название населенного пункта '
            else:
                db_sess = db_session.create_session()
                db_sess.add(call)
                db_sess.commit()
                res['response']['text'] = f'Вызов принят. Адрес: {sessionStorage[user_id]["address"]}'
                res['response']['end_session'] = True
        else:
            res['response']['text'] = f'Пожалуйста, уточните адрес. Возможно вы ошиблись или не указали полное ' \
                                      f'название населенного пункта '
        return

    '''else:
        f_name = '/content/drive/MyDrive/Data/dataset.csv'
        with open(f_name, mode='a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # print([сategories[cat], translateCategorie(cat), themes[theme], translateTheme(theme), message])
        writer.writerow(
            [sessionStorage[user_id]['categorie'], translateCategorie(cat), themes[theme], translateTheme(theme),
             message])'''


