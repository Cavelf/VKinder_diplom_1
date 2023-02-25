from sqlalchemy.orm import sessionmaker
from models import *
from config import BD_CONNECT


class ORM:
    def __init__(self):
        self.DSN = BD_CONNECT
        self.engine = sq.create_engine(self.DSN)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        create_tables(self.engine)

    def drop_all_tables(self):
        drop_all_tables(self.engine)

    def add_user(self, user_id, user_looking):
        date = Users(vk_id=user_id, vk_id_user_looking=user_looking)
        self.session.add(date)
        self.session.commit()

    def search_id(self, looking_user_id, who_looking_user_id):
        id = self.session.query(Users).filter(
            Users.vk_id == looking_user_id and Users.vk_id_user_looking == who_looking_user_id).first()
        if id:
            return True
        else:
            None

    def search_id_in_db(self, ids):
        i = self.session.query(Users.vk_id).filter(Users.id == ids)
        return i.value(Users.vk_id)

    def count_id(self):
        count = self.session.query(Users.id).count()
        return count


if __name__ == "__main__":
    db = ORM()
