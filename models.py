
from sqlalchemy.exc import IntegrityError
import db
from sqlalchemy import Column, Integer, String

class Keyword(db.Base):
    __tablename__ ='keywords'
    id = Column(Integer,primary_key=True)
    keywords = Column(String,nullable =False, unique =True)
    #importante unique =True

    posicion = Column(Integer,nullable=True)

    def __init__(self,keywords,posicion =None):
        self.keywords = keywords
        self.posicion = posicion
    def __repr__(self):
        return f'Ranking({self.keywords}),{self.posicion}'

    def __str__(self):
        return f'a palabra clave {self.keywords} rankea en a posicion {self.posicion}'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            #si las palabras clave ya existen, se hace un rollback
            #de la base de datos
            db.session.rollback()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_all():
        return db.session.query(Keyword).all()
