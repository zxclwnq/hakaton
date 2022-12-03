import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
from .db_session import SqlAlchemyBase
from tables import evaluation_table_video_default, evaluation_table_text_default, lowering_criteria_default


class Proposal(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'proposal'
    max_rates = 3

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    evaluation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lowering_criteria = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_data = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    experts_rates = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    @property
    def annotation(self):
        """Возвращает тему работы"""
        return self.user_data_dict.get("annotation")
    @property
    def theme(self):
        """Возвращает тему работы"""
        return self.user_data_dict.get("theme")
    @property
    def evaluation_dict(self):
        """Возвращает словарь параметров оценивания"""
        return json.loads(self.evaluation)

    @property
    def user_data_dict(self):
        """Возвращает личные данные пользователя"""
        return json.loads(self.user_data)

    @property
    def experts_list(self):
        """Возвращает список id экспертов проверявших эту работу"""
        return json.loads(self.experts_rates)
    @property
    def lowering_criteria_dict(self):
        """Возвращает словарь параметров понижения оценки"""
        return json.loads(self.lowering_criteria)

    def can_be_rated(self, expert_id):
        return self.status == "waiting_verification" and expert_id not in self.experts_list['expert_ids']

    @property
    def average_score(self):
        """Возвращает среднюю оценку заявки
        (Средняя оценка по критериям минус средняя оценка по понижающим критериям)
        """
        sum = 0
        for score in self.merge_ratings:
            sum += score[3]
        return round(sum / len(self.merge_ratings),2)
    @property
    def merge_ratings(self):
        """Возвращает комбинированные оценки для заявки
        """
        ratings = self.evaluation_dict["ratings"]
        lowering_ratings = self.lowering_criteria_dict["ratings"]
        merged_ratings = []
        for index in range(len(ratings)):
            merged_ratings.append((ratings[index],lowering_ratings[index],ratings[index]["expert"],
                                   sum(list(ratings[index].values())[:-1]) \
                                   - sum(list(lowering_ratings[index].values())[:-1])))
        return merged_ratings
    def verify_proposal(
            self,
            new_evaluation: dict,
            new_lowering_criteria: dict,
            expert_id: int):
        """
        Закрывает оценивание заявки
        :param new_evaluation: новые оценки заявки
        + указаны имя и фамилия эксперта
        :param new_lowering_criteria: новые понижающие оценки заявки
        + указаны имя и фамилия эксперта
        :param new_status: новый статус заявки
        """
        self.change_evaluation(new_evaluation)
        self.change_lowering_criteria(new_lowering_criteria)
        self.add_expert(expert_id)

    def add_expert(self, expert_id):
        """
        Изменяет добавляет id эксперта в список
        :param expert_id: id эксперта
        """

        experts_list = self.experts_list["expert_ids"]
        experts_list.append(expert_id)
        if len(experts_list) == self.max_rates:
            self.change_status('verified')
        self.experts_rates = json.dumps({"expert_ids" :experts_list})
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
        self.file = file
        if type == 'text':
            self.evaluation = json.dumps({"ratings": []})
        else:
            self.evaluation = json.dumps({"ratings": []})
        self.lowering_criteria = json.dumps({"ratings": []})
        self.status = "waiting_verification"
        self.likes = 0
        self.user_data = json.dumps(user_data)
        self.experts_rates = json.dumps({"expert_ids": []})

    def change_evaluation(self, new_evaluation: dict):
        """
        Изменяет оценки заявке
        :param new_evaluation: новые оценки заявки
        + указаны имя и фамилия эксперта
        """
        new_ratings = self.evaluation_dict["ratings"]
        new_ratings.append(new_evaluation)
        self.evaluation = json.dumps({"ratings":new_ratings})

    def change_lowering_criteria(self, new_lowering_criteria: dict):
        """
        Изменяет понижающие оценки заявки
        :param new_lowering_criteria: новые понижающие оценки заявки
        + указаны имя и фамилия эксперта
        """

        new_ratings = self.lowering_criteria_dict["ratings"]
        new_ratings.append(new_lowering_criteria)
        self.lowering_criteria = json.dumps({"ratings":new_ratings})

    def change_status(self, new_status):
        """
        Изменяет статус заявки
        :param new_status: новый статус заявки
        """
        self.status = new_status
