from dao.questiontype_dao import QuestiontypeDAO
from vo.questiontype_vo import QuestiontypeVO


def view_questiontype():
    questiontype_dao = QuestiontypeDAO()
    questiontype_vo_list = questiontype_dao.view_questiontype()
    questiontype_dict_list = [i.as_dict() for i in questiontype_vo_list]
    return questiontype_dict_list


def get_questiontype_id(request_questiontype_name):
    questiontype_dao = QuestiontypeDAO()
    questiontype_vo = QuestiontypeVO()
    questiontype_vo.questiontype_name = request_questiontype_name
    questiontype_id = questiontype_dao.find_questiontype_id(questiontype_vo)
    print("questiontype_id>>>>>", questiontype_id)
    return questiontype_id
