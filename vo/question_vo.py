from dao import engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from vo.questiontype_vo import QuestiontypeVO

Base = declarative_base()


class QuestionVO(Base):
    __tablename__ = 'question_table'
    question_id = Column('question_id', Integer, primary_key=True, autoincrement=True)
    question_name = Column('question_name', String(100), nullable=False)
    question_description = Column('question_description',String(100),nullable=False)
    question_answer = Column('question_answer', String(100), nullable=False)
    question_answerpoint = Column('question_answerpoint', String(100), nullable=False)
    question_questiontype_id = Column('question_questiontype_id', Integer, ForeignKey(QuestiontypeVO.questiontype_id))

    def as_dict(self):
        return {'question_id': self.question_id,
                'question_name': self.question_name,
                'question_description': self.question_description,
                'question_answer': self.question_answer,
                'question_answerpoint': self.question_answerpoint,
                'question_questiontype_id': self.question_questiontype_id}


Base.metadata.create_all(engine)
