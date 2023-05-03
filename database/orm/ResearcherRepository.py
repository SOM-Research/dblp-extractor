from database.orm import RepositoryBase
from model.Researcher import Researcher
from model.ResearcherName import ResearcherName
from model.XmlKey import XmlKey
from sqlalchemy import select

class ResearcherRepository(RepositoryBase):

    def insertResearcher(self, uuid, currentAlias, currentAliasYear, urls, xmlKey, xmlMdate, xmlItem, names, affiliations):
        """
        Insert a Researcher
        :param uuid: Researcher uuid
        :param currentAlias: Researcher current Alias
        :param currentAliasYear: Researcher year of the last publication to know the current Alias
        :param urls: Researcher urls attached to the Researcher, orcid could be one
        :param xmlKey: Researcher xml key
        :param xmlMdate: Researcher xml modification date
        :param xmlItem: Researcher xml item
        :param names: Researcher array of names could be found by this researcher
        :param affiliations: Researcher affiliations
        :return: Researcher
        """
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

    def updateResearcher(self, researcher):
        """
        Update a Researcher
        :param researcher: Researcher
        """
        self.session.commit()

    def getOneByXmlKey(self, xmlKey):
        """
        Find one Researcher by xml key
        :param xmlKey: Researcher xml key
        :return: Researcher or None
        """
        stmt = select(Researcher).where(Researcher.xml_key == xmlKey)
        result = self.session.scalars(stmt)
        return result.first()

    def getOneByName(self, name):
        """
        Find one by name
        :param name: Name to be find
        :return: Researcher or None
        """
        return self.session.query(Researcher).join(ResearcherName).filter(ResearcherName.name == name).first()