from model.Researcher import Researcher
from model.ResearcherName import ResearcherName
from model.XmlKey import XmlKey
from sqlalchemy import select

class ResearcherRepository():
    def __init__(self, session):
        self.session = session

    def insertResearcher(self, uuid, currentAlias, xmlKey, xmlMdate, xmlItem, names, affiliations):
        # I should put a uuid5 because when I cascade all data, a uuid i duplicated
        researcher = Researcher(id=uuid, current_alias=currentAlias, xml_key=xmlKey, xml_mdate=xmlMdate, xml_item=xmlItem)

        for name in names:
            researcherName = ResearcherName(researcher_id=researcher.id, name=name)
            researcher.names.append(researcherName)
            self.session.add(researcherName)

        researcher.xml_cross_reference.append(XmlKey(researcher_id=researcher.id, xml_key=xmlKey))

        for affiliation in affiliations:
            researcher.affiliations.append(affiliation)


        self.session.add(researcher)
        self.session.commit()

        return researcher

    def getOneById(self, uuid):
        stmt = select(Researcher).where(Researcher.id == uuid)
        result = self.session.scalars(stmt)
        return result.first()

    def updateResearcher(self, researcher):
        self.session.commit()

    def getOneByXmlKey(self, xmlKey):
        stmt = select(Researcher).where(Researcher.xml_key == xmlKey)
        result = self.session.scalars(stmt)
        return result.first()
