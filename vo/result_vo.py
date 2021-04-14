from dao import engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from vo.login_vo import LoginVO

Base = declarative_base()


class ResultVO(Base):
    __tablename__ = 'result_table'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    result_language=Column(String(255), nullable=False)
    result_grade = Column(String(255), nullable=False)
    result_status = Column(String(255), nullable=False)
    result_datetime = Column(DateTime, nullable=False)
    result_login_id = Column(ForeignKey(LoginVO.login_id), nullable=False)

    def as_dict(self):
        return {'result_id': self.result_id,
                'result_language': self.result_language,
                'result_grade': self.result_grade,
                'result_status': self.result_status,
                'result_datetime': self.result_datetime,
                'result_login_id': self.result_login_id
                }


Base.metadata.create_all(engine)
