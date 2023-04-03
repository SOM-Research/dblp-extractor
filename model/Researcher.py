from typing import List
import re
from sqlalchemy import Column, String, ForeignKey, UUID, DATE, Text, Table
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
    orcid = Column(String)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    xml_cross_reference: Mapped[List["XmlKey"]] = relationship(back_populates="researcher")
    names: Mapped[List["ResearcherName"]] = relationship(back_populates="researcher")
    affiliations: Mapped[List["Institution"]] = relationship(secondary=affiliation)
    publications: Mapped[List["Authorship"]] = relationship(back_populates="researcher")
    publication_groups: Mapped[List["Editor"]] = relationship(back_populates="researcher")

    def addOrcid(self, orcid):
        orcidRegEx = re.compile('([0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9]([0-9]|X))')
        orcidPath = re.compile('https://orcid\.org/.*')
        if orcidRegEx.match(orcid):
            self.orcid = orcid
            return orcid
        if orcidPath.match(orcid):
            self.orcid = re.search(orcidRegEx, orcid).group(1)
            return self.orcid