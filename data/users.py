import datetime
import json
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

#Эксперт или Админ, вроде бы всё хорошо
class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    proposals = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    @property
    def proposals_list(self):
        return json.loads(proposals)['proposals']

    def make_new(self,name,surname,email,password):
        self.name = name
        self.surname = surname
        self.set_password(password)
        self.email = email
        self.position = "user"
        self.proposals = json.dumps({"proposals":[]})

    @property
    def access_level(self):
        level = {
            "admin":3,
            "expert":2,
            "moderator":1,
            "user":0
        }
        return level[self.position]

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return self.password == password or check_password_hash(self.password, password)
        #return check_password_hash(self.hashed_password, password)
