from model import ModelBase
import re
from typing import List
from sqlalchemy import Column, String, UUID, DATE, Text, Integer, Enum
from sqlalchemy.orm import relationship, Mapped
from model.PublicationElectronicEdition import PublicationElectronicEdition
from model.PublicationType import PublicationType

class Publication(ModelBase):
    __tablename__ = "publications"

    id = Column(UUID, primary_key=True)
    type = Column(Enum(PublicationType))
    title = Column(String)
    year = Column(Integer)
    doi = Column(String)
    pages = Column(String)
    num_pages = Column(Integer)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    electronic_editions: Mapped[List["PublicationElectronicEdition"]] = relationship(back_populates="publication")
    authors: Mapped[List["Authorship"]] = relationship(back_populates="publication")

    def setType(self):
        word = self.xml_key.split('/')[0]
        if 'journals' == word:
            self.type = PublicationType.journal
        if 'conf' == word:
            self.type = PublicationType.conference
        if 'phd' == word:
            self.type = PublicationType.thesis
        return self.type

    def calculatePages(self):
        if self.pages.isnumeric():
            self.num_pages = int(self.pages)
        else:
            r = re.compile('[0-9]+-[0-9]+')
            if r.match(self.pages):
                self.num_pages = int(self.pages.split('-')[1]) - int(self.pages.split('-')[0])
            else:
                print("Pages not numeric nor calculable: ", self.pages)

    def addElectronicEditions(self, electronicEditions):
        r = re.compile('https://doi\.org/.*')
        for ee in electronicEditions:
            if r.match(ee):
                self.doi = ee
            if ee not in self.electronic_editions:
                self.electronic_editions.append(
                    PublicationElectronicEdition(publication_id=self.id, publication=self, electronic_edition=ee)
                )