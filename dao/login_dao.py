from dao import engine
from sqlalchemy.orm import sessionmaker
from vo.login_vo import LoginVO

Session = sessionmaker(bind=engine)
session = Session()


class LoginDAO:
    def validate_login(self, loginVO):
        login_vo_list = session.query(LoginVO).filter_by(login_username=loginVO.login_username,
                                                     login_password=loginVO.login_password)

        return login_vo_list
