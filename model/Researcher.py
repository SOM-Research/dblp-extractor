from typing import List

from sqlalchemy import Column, String, ForeignKey, UUID, DATE, Text, Table, Integer
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ARRAY

from model import ModelBase

affiliation = Table(
    "affiliations",
    ModelBase.metadata,
    Column("researcher_uuid", ForeignKey("researchers.uuid"), primary_key=True),
    Column("institution_uuid", ForeignKey("institutions.uuid"), primary_key=True),
)


# an example mapping using the base
class Researcher(ModelBase):
    __tablename__ = "researchers"

    uuid = Column(UUID, primary_key=True)
    current_alias = Column(String)
    last_year_current_alias = Column(Integer)
    orcid = Column(String)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_tag = Column(Text)
    xml_item = Column(Text)
    crossref =  Column(Text)
    names = Column(ARRAY(String))
    affiliations: Mapped[List["Institution"]] = relationship(secondary=affiliation)
