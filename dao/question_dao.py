from dao import engine
from sqlalchemy.orm import sessionmaker
from vo.question_vo import QuestionVO

Session = sessionmaker(bind=engine)
session = Session()


class QuestionDAO:
    def view_question_by_questiontype_id(self, question_vo):
        print("start view function.")
        question_vo_list = session.query(QuestionVO).filter_by(question_questiontype_id=question_vo.question_questiontype_id,question_description=question_vo.question_description)
        print("question_vo_list:",question_vo_list)
        return question_vo_list

    def question_count(self):
        total_question = session.query(QuestionVO).count()
        return total_question

    def view_question_decription(self):
        question_vo_list = session.query(QuestionVO).all()
        return question_vo_list
