from dao.question_dao import QuestionDAO
from vo.question_vo import QuestionVO


def view_question(question_questiontype_id, language_type):
    question_vo = QuestionVO()
    question_dao = QuestionDAO()
    question_vo.question_questiontype_id = question_questiontype_id
    question_vo.question_description = language_type
    print("question_vo.question_description:",question_vo.question_description)
    question_vo_list = question_dao.view_question_by_questiontype_id(question_vo)
    print("question_vo_list:",question_vo_list)
    # print(question_vo_list['question_name'])
    # for i in question_vo_list:
    #     print("i:",i)
        # print(i['question_name'])
    question_dict_list = [i.as_dict() for i in question_vo_list]
    print("question_dict_list=", question_dict_list)
    return question_dict_list


def count_total_question():
    question_dao = QuestionDAO()
    total_question = question_dao.question_count()
    return total_question


def view_languagetype():
    question_dao = QuestionDAO()
    language_list = []
    question_vo_list = question_dao.view_question_decription()
    print("question_vo_list:", question_vo_list)
    language_dict_list = [i.as_dict() for i in question_vo_list]
    for i in language_dict_list:
        if i['question_description'] not in language_list:
            language_list.append(i['question_description'])
    print("language_list:", language_list)
    return language_list
