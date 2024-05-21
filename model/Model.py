from typing import List

from sqlalchemy import Column, String, ForeignKey, UUID, DATE, Text, Table, Integer, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from model import ModelBase

affiliation = Table(
    "affiliations",
    ModelBase.metadata,
    Column("researcher_uuid", ForeignKey("researchers.uuid"), primary_key=True),
    Column("institution_uuid", ForeignKey("institutions.uuid"), primary_key=True),
)

editor = Table(
    "editors",
    ModelBase.metadata,
    Column("researcher_uuid", UUID, ForeignKey("researchers.uuid"), primary_key=True),
    Column("publication_group_uuid", UUID, ForeignKey("publication_groups.uuid"), primary_key=True),
    Column("position", Integer),
)

authorship = Table(
    "authorships",
    ModelBase.metadata,
    Column("researcher_uuid", UUID, ForeignKey("researchers.uuid"), primary_key=True),
    Column("publication_uuid", UUID, ForeignKey("publications.uuid"), primary_key=True),
    Column("position", Integer),
)

class Institution(ModelBase):
    __tablename__ = "institutions"

    uuid = Column(UUID, primary_key=True)
    name = Column(String, unique=True)
    version_names = Column(ARRAY(String))
    country = Column(String)

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
    publication_groups: Mapped[List["PublicationGroup"]] = relationship(secondary='editors', back_populates='model_editors')
    publications: Mapped[List["Publication"]] = relationship(secondary='authorships', back_populates='model_authors')

class PublicationGroup(ModelBase):
    __tablename__ = "publication_groups"

    uuid = Column(UUID, primary_key=True)
    title = Column(String)
    booktitle = Column(String)
    serie = Column(String)
    volume = Column(String)
    number = Column(String)
    publisher = Column(String)
    year = Column(Integer)
    doi = Column(String)
    isbn = Column(ARRAY(String))
    editors = Column(ARRAY(String))
    electronic_edition = Column(ARRAY(String))
    publication_venue = Column(UUID)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_tag = Column(Text)
    xml_item = Column(Text)
    crossref = Column(Text)
    model_editors: Mapped[List["Researcher"]] = relationship(secondary='editors', back_populates='publication_groups')
class Publication(ModelBase):
    __tablename__ = "publications"

    uuid = Column(UUID, primary_key=True)
    title = Column(String)
    pages = Column(String)
    type = Column(String)
    journal = Column(String)
    year = Column(Integer)
    num_pages = Column(Integer)
    doi = Column(String)
    authors = Column(ARRAY(String))
    electronic_edition = Column(ARRAY(String))
    is_corrigendum = Column(Boolean)
    corrigendum_of = Column(UUID)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_tag = Column(Text)
    xml_item = Column(Text)
    crossref = Column(Text)
    publication_group_uuid: Mapped[UUID] = mapped_column(ForeignKey("publication_groups.uuid"))
    publication_group: Mapped["PublicationGroup"] = relationship()
    model_authors: Mapped[List["Researcher"]] = relationship(secondary='authorships', back_populates='publications')
