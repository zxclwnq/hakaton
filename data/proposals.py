import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
from .db_session import SqlAlchemyBase
from tables import evaluation_table_video_default, evaluation_table_text_default, lowering_criteria_default


class Proposal(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'proposal'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    evaluation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lowering_criteria = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_data = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    @property
    def evaluation_dict(self):
        """Возвращает словарь параметров оценивания"""
        return json.loads(self.evaluation)

    @property
    def user_data_dict(self):
        """Возвращает личные данные пользователя"""
        return json.loads(self.user_data)

    @property
    def lowering_criteria_dict(self):
        """Возвращает словарь параметров понижения оценки"""
        return json.loads(self.lowering_criteria)

    def verify_proposal(
            self,
            new_evaluation: dict,
            new_lowering_criteria: dict,
            new_status: str):
        """
        Закрывает оценивание заявки
        :param new_evaluation: новые оценки заявки
        :param new_lowering_criteria: новые понижающие оценки заявки
        :param new_status: новый статус заявки
        """
        self.change_evaluation(new_evaluation)
        self.change_lowering_criteria(new_lowering_criteria)
        self.change_status(new_status)

    def make_proposal(
            self,
            id: int,
            type: str,
            file: str,
            user_data: dict):
        """
        Заполняет новую заявку дефолтными значениями
        :param id Id заявки
        :param type тип заявки (text or video)
        :param file прикрепленный файл заявки
        :param user_data личные данные пользователя
        """
        self.id = id
        self.type = type
        self.path = f"static/purposes/{id}"
        if type == 'text':
            self.evaluation = json.dumps(evaluation_table_text_default)
        else:
            self.evaluation = json.dumps(evaluation_table_video_default)
        self.lowering_criteria = json.dumps(lowering_criteria_default)
        self.status = "waiting_verification"
        self.likes = 0
        self.user_data = json.dumps(user_data)

    def change_evaluation(self, new_evaluation: dict):
        """
        Изменяет оценки заявке
        :param new_evaluation: новые оценки заявки
        """
        self.evaluation = json.dumps(new_evaluation)

    def change_lowering_criteria(self, new_lowering_criteria: dict):
        """
        Изменяет понижающие оценки заявки
        :param new_lowering_criteria: новые понижающие оценки заявки
        """
        self.lowering_criteria = json.dumps(new_lowering_criteria)

    def change_status(self, new_status):
        """
        Изменяет статус заявки
        :param new_status: новый статус заявки
        """
        self.status = new_status
