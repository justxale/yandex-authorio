import datetime

import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("authors.id"))
    author = orm.relationship('Author')


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("authors.id"))
    author = orm.relationship('Author')
