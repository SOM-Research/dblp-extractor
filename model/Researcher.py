from typing import List
import re
from sqlalchemy import Column, String, ForeignKey, UUID, DATE, Text, Table, Integer
from sqlalchemy.orm import relationship, Mapped
from model import ModelBase

affiliation = Table(
    "affiliations",
    ModelBase.metadata,
    Column("researcher_id", ForeignKey("researchers.id"), primary_key=True),
    Column("institution_id", ForeignKey("institutions.id"), primary_key=True),
)

class Researcher(ModelBase):
    __tablename__ = "researchers"

    id = Column(UUID, primary_key=True)
    current_alias = Column(String)
    last_year_current_alias = Column(Integer)
    orcid = Column(String)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    xml_cross_reference: Mapped[List["XmlKey"]] = relationship(back_populates="researcher")
    names: Mapped[List["ResearcherName"]] = relationship(back_populates="researcher")
    affiliations: Mapped[List["Institution"]] = relationship(secondary=affiliation)
    publications: Mapped[List["Authorship"]] = relationship(back_populates="researcher")
    publication_groups: Mapped[List["Editor"]] = relationship(back_populates="researcher")

    def orcidRegEx(self):
        """
        Regular Expression to identify an Orcid identifier
        :return: a regular expression class.
        """
        return re.compile('([0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9]([0-9]|X))')

    def orcidUrlRegEx(self):
        """
        Regular Expression to identify an Orcid URL
        :return: a regular expression class.
        """
        return re.compile('https://orcid\.org/.*')

    def addOrcid(self, orcid):
        """
        Add an Orcid, could be in an identifier or url format
        :param orcid: Orcid string as identifier or url
        :return: orcid identifier
        """
        if self.orcidRegEx().match(orcid):
            self.orcid = orcid
            return self.orcid
        if self.orcidUrlRegEx().match(orcid):
            self.orcid = re.search(self.orcidRegEx(), orcid).group(1)
            return self.orcid

    def updateCurrentAlias(self, currentAlias, year):
        """
        Updates the current Alias from last year saved.
        :param currentAlias: current Alias changed.
        :param year: Year from new current alias.
        """
        self.current_alias = currentAlias
        self.last_year_current_alias = year