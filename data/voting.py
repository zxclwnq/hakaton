import datetime
import json
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

class Vote(SqlAlchemyBase):
    __tablename__ = 'voting'

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    proposal_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

