from sqlalchemy import select

from model.Model import Institution

class InstitutionRepository():
    def __init__(self, alchemySession):
        self.session = alchemySession

    def getOneByName(self, name):
        stmt = select(Institution).where(Institution.name == name)
        result = self.session.scalars(stmt)
        return result.first()

    def getCount(self):
        result = self.session.query(Institution).count()
        return result