import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)   # id найденной страницы
    vk_id_user_looking = sq.Column(sq.Integer)   # id пользователя который осуществлял поиск




def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_all_tables(engine):
    Base.metadata.drop_all(engine)

