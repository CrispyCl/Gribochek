import sqlalchemy
from .db_session import SqlAlchemyBase


class MerParams(SqlAlchemyBase):
    __tablename__ = 'mer_params'

    mer_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("groups.id"),
                               primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    par = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DATE)
