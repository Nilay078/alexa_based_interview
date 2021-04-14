from dao import engine
from sqlalchemy.orm import sessionmaker
from vo.questiontype_vo import QuestiontypeVO

Session = sessionmaker(bind=engine)
session = Session()


class QuestiontypeDAO:
    def view_questiontype(self):
        questiontype_vo_list = session.query(QuestiontypeVO).all()
        return questiontype_vo_list

    def find_questiontype_id(self, questiontype_vo):
        print(">>>>>>>>>>>>",questiontype_vo.questiontype_name)
        questiontype_id = session.query(QuestiontypeVO.questiontype_id).filter_by(questiontype_name=questiontype_vo.questiontype_name).all()

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("questiontype_id=>>>>>>",questiontype_id)
        print("questiontype_id=>>>>>>", questiontype_id[0][0])
        return questiontype_id[0][0]
