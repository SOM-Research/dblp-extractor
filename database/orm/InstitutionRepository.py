from sqlalchemy import select
from sqlalchemy import func

from model.Institution import Institution

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