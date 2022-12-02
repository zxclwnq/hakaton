from flask import jsonify
from flask_restful import Resource, reqparse, abort
from data import db_session
from .calls import Call

parser = reqparse.RequestParser()
parser.add_argument('message', required=True)
parser.add_argument('address', required=True)

def abort_if_call_not_found(id):
    session = db_session.create_session()
    call = session.query(Call).get(id)
    if not call:
        abort(404, message=f"Call {id} not found")


class CallResource(Resource):
    """
    API для вызовов
    """
    def get(self, id):
        """
        Возврашает вызов
        :param id: id вызова
        :return: json c информауией об одном вызове
        """
        abort_if_call_not_found(id)
        session = db_session.create_session()
        call = session.query(Call).get(id)
        return jsonify({'call': call.to_dict(
            only=('id', 'message', 'address', 'point', 'service', 'status', 'call_time', 'finish_time'))
        })


class CallListResource(Resource):
    """
    API для списка  вызовов
    """
    def get(self):
        """
        Возвращает список вызовов
        :return:  json c информауией о вызовах
        """
        session = db_session.create_session()
        calls = session.query(Call).all()
        return jsonify({'calls': [item.to_dict(
            only=('id', 'message', 'address', 'point', 'service', 'status', 'call_time', 'finish_time'))
            for item in calls]})

    def post(self):
        """
        Добавляет вызов
        :return:  номер вызова или информацию об ошибке
        """
        args = parser.parse_args()
        session = db_session.create_session()
        call = Call(
            message=args['message'],
            address=args['address']
        )
        try:
            call.recognize_call()
            session.add(call)
            session.commit()
            result = jsonify({'success': call.id})
        except:
            result = jsonify({'error': 'address not found'})
        return result


