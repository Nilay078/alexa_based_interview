from dao.login_dao import LoginDAO
from vo.login_vo import LoginVO


def validate_login(login_username, login_password):
    login_vo = LoginVO()
    login_dao = LoginDAO()
    login_vo.login_username = (login_username.lower())
    login_vo.login_password = login_password
    print("<<<<<<<>>>>>>>>", login_vo.login_username)
    print("<<<<<<<>>>>>>>>", login_vo.login_password)
    login_vo_list = login_dao.validate_login(login_vo)
    print("login_vo_list:",login_vo_list)
    login_dict_list = [i.as_dict() for i in login_vo_list]
    print(">>>>>>>>>>",login_dict_list)
    return login_dict_list
