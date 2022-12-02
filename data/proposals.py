import datetime
import sqlalchemy
import requests
import random
from sqlalchemy import null
from sqlalchemy_serializer import SerializerMixin
from db_session import SqlAlchemyBase


# Сама заявка (отредактировать поля)
class Proposal(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'calls'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    purpose_type = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    path_to_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    evaluation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    service = sqlalchemy.Column(sqlalchemy.String, nullable=True)
