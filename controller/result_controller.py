import datetime
import math

import pytz
from dao.result_dao import ResultDAO
from vo.result_vo import ResultVO


def result_calculation(correct_answer_count, incorrect_answer_count, total_question_counter, session_login_id,
                       language_type):
    result_dict = {
        "correct_answer_count": correct_answer_count,
        "incorrect_answer_count": incorrect_answer_count,
        "total_question_counter": total_question_counter
    }

    percentage = (correct_answer_count / total_question_counter) * 100
    percentage = math.ceil(percentage)

    result_grade = None
    result_status = None

    if percentage in range(90, 101):
        result_grade = 'A'
        result_status = "Qualified"
    elif percentage in range(80, 91):
        result_grade = 'B'
        result_status = "Qualified"
    elif percentage in range(70, 81):
        result_grade = 'C'
        result_status = "Qualified"
    elif percentage in range(60, 71):
        result_grade = 'D'
        result_status = "Qualified"
    else:
        result_grade = 'F'
        result_status = "Not Qualified"

    result_vo = ResultVO()
    result_dao = ResultDAO()

    IST = pytz.timezone('Asia/Kolkata')
    result_datetime = datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

    result_vo.result_status = result_status
    result_vo.result_language = language_type
    result_vo.result_grade = result_grade
    result_vo.result_datetime = result_datetime
    result_vo.result_login_id = session_login_id

    result_dao.insert_result(result_vo)
    return result_dict
