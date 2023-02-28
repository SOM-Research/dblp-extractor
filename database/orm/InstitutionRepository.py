from sqlalchemy import select

from model.Institution import Institution

class InstitutionRepository():
    def __init__(self, alchemySession):
        self.session = alchemySession

    def updateSession(self, session):
        self.session = session

    def insertInstitution(self, uuid, name):
        institution = Institution(id=uuid, name=name)
        self.session.add(institution)
        self.session.commit()
        return institution

    def getOneByName(self, name):
        stmt = select(Institution).where(Institution.name == name)
        result = self.session.scalars(stmt)
        return result.first()