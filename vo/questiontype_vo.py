from dao import engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class QuestiontypeVO(Base):
    __tablename__ = 'questiontype_table'
    questiontype_id = Column(Integer, primary_key=True, autoincrement=True)
    questiontype_name = Column(String(100), nullable=False)
    questiontype_description = Column(String(100), nullable=False)

    def as_dict(self):
        return {'questiontype_id': self.questiontype_id,
                'questiontype_name': self.questiontype_name,
                'questiontype_description': self.questiontype_description, }


Base.metadata.create_all(engine)
