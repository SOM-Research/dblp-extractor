from model import ModelBase
from typing import List
from sqlalchemy import Column, String, UUID, DATE, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import re

from model.PublicationGroupElectronicEdition import PublicationGroupElectronicEdition


class PublicationGroup(ModelBase):
    __tablename__ = "publication_groups"
    id = Column(UUID, primary_key=True)
    title = Column(String)
    publication_venue = mapped_column(ForeignKey("publication_venues.id"))
    venue: Mapped["PublicationVenue"] = relationship(back_populates="publication_groups")
    publisher = Column(String)
    year = Column(Integer)
    isbn = Column(String)
    doi = Column(String)
    booktitle = Column(String)
    serie = Column(String)
    volume = Column(String)
    number = Column(String)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    editors: Mapped[List["Editor"]] = relationship(back_populates="publication_group")
    electronic_editions: Mapped[List["PublicationGroupElectronicEdition"]] = relationship(back_populates="publication_group")
    publications: Mapped[List["Publication"]] = relationship(back_populates="publication_group")


    def addElectronicEditions(self, electronicEditions):
        r = re.compile('https://doi\.org/.*')
        for ee in electronicEditions:
            eeItem = PublicationGroupElectronicEdition(publication_group_id=self.id, publication_group=self, electronic_edition=ee)
            if r.match(ee):
                self.doi = ee
            if eeItem not in self.electronic_editions:
                self.electronic_editions.append(eeItem)