from database.orm import RepositoryBase
from model.Researcher import Researcher
from model.ResearcherName import ResearcherName
from model.XmlKey import XmlKey
from sqlalchemy import select

class ResearcherRepository(RepositoryBase):

    def insertResearcher(self, uuid, currentAlias, currentAliasYear, urls, xmlKey, xmlMdate, xmlItem, names, affiliations):
        researcher = Researcher(id=uuid, current_alias=currentAlias, last_year_current_alias=currentAliasYear, xml_key=xmlKey, xml_mdate=xmlMdate, xml_item=xmlItem)
        if len(urls) > 0:
            for url in urls:
                if researcher.orcidUrlRegEx().match(url):
                    researcher.addOrcid(url)

        for name in names:
            if name is None:
                name = xmlKey
            researcherName = ResearcherName(researcher_id=researcher.id, name=name)
            if researcherName not in researcher.names:
                researcher.names.append(researcherName)
                self.session.add(researcherName)

        researcher.xml_cross_reference.append(XmlKey(researcher_id=researcher.id, xml_key=xmlKey))

        for affiliation in affiliations:
            if affiliation not in researcher.affiliations:
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

    def getOneByName(self, name):
        return self.session.query(Researcher).join(ResearcherName).filter(ResearcherName.name == name).first()