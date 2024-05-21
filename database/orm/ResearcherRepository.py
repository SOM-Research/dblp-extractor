from model.Model import Researcher
from sqlalchemy import select

class ResearcherRepository():
    def __init__(self, session):
        self.session = session

    def getOneById(self, uuid):
        stmt = select(Researcher).where(Researcher.uuid == uuid)
        result = self.session.scalars(stmt)
        return result.first()

    def getOneByXmlKey(self, xmlKey):
        stmt = select(Researcher).where(Researcher.xml_key == xmlKey)
        result = self.session.scalars(stmt)
        return result.first()

    def getCount(self):
        result = self.session.query(Researcher).count()
        return result