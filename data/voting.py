import datetime
import json
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

class Voting(SqlAlchemyBase):
    __tablename__ = 'voting'

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    proposal_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)

