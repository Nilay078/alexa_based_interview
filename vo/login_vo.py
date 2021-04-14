from dao import engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LoginVO(Base):
    print('in LoginVOClass')
    __tablename__ = 'login_table'

    login_id = Column(Integer, primary_key=True, autoincrement=True)
    login_username = Column(String(100), nullable=False)
    login_password = Column(String(100), nullable=False)
    login_role = Column(String(100), nullable=False)
    login_status = Column(String(100), nullable=False)
    login_secretkey = Column(String(100), nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'login_status': self.login_status,
            'login_secretkey': self.login_secretkey
        }


Base.metadata.create_all(engine)
