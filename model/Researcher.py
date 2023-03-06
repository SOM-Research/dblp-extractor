from typing import List
from sqlalchemy import Column, String, ForeignKey, UUID, DATE, Text, Table, Integer
from sqlalchemy.orm import relationship, Mapped
from model import ModelBase
from model.Authorship import Authorship

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
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    xml_cross_reference: Mapped[List["XmlKey"]] = relationship(back_populates="researcher")
    names: Mapped[List["ResearcherName"]] = relationship(back_populates="researcher")
    affiliations: Mapped[List["Institution"]] = relationship(secondary=affiliation)
    publications: Mapped[List["Authorship"]] = relationship(back_populates="researcher")