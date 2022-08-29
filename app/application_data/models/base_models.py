from sqlalchemy import (
    Table, Column,
    DateTime, ForeignKey, Integer,
    String, func, Float
)
from sqlalchemy.orm import (
    relationship, declarative_mixin,
    declared_attr
)
from application_data import db


@declarative_mixin
class StandartModelMixin:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def update_or_create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        self.id = None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)
