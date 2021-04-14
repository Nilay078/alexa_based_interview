from dao import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class ResultDAO:
    def insert_result(self, result_vo):
        session.add(result_vo)
        session.commit()
