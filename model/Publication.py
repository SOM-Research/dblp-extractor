import roman

from model import ModelBase
import re
from typing import List
from sqlalchemy import Column, String, UUID, DATE, Text, Integer, Enum, ForeignKey
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
    publication_group_id = Column(UUID, ForeignKey("publication_groups.id"))
    publication_group: Mapped["PublicationGroup"] = relationship(back_populates="publications")

    def setType(self, type):
        """
        Set publication type
        :param type: Publication type
        :return: PublicationType
        todo: refactor first if to get a better control.
        """
        if type is not None:
            self.type = PublicationType.book
            return self.type
        word = self.xml_key.split('/')[0]
        if 'journals' == word:
            self.type = PublicationType.journal
        if 'conf' == word:
            self.type = PublicationType.conference
        if 'phd' == word or 'ms' == word:
            self.type = PublicationType.thesis
        return self.type

    def calculatePages(self):
        """
        Calculate number of pages from pages.
        :return: int - number of pages
        """
        try:
            if self.pages is None:
                return None
            # Maximum size of an int in MariaDB is 2147483647
            if self.pages.isnumeric() and int(self.pages) < 2147483647:
                self.num_pages = int(self.pages)
            else:
                self.pages = self.pages.upper()
                r1 = re.compile('[0-9]+-[0-9]+')
                r2 = re.compile('[0-9]+:[0-9]+-[0-9]+:[0-9]+')
                r3 = re.compile('[MDCLXVI]+-[MDCLXVI]+')
                r4 = re.compile('[0-9]+:[MDCLXVI]+-[0-9]+:[MDCLXVI]+')
                rBook = re.compile('[MDCLXVI]+-[MDCLXVI]+, [0-9]+-[0-9]+')
                if self.type == PublicationType.book and rBook.match(self.pages):
                    splitPages = self.pages.split('-')
                    self.num_pages = int(splitPages[(len(splitPages) - 1)])
                elif r1.match(self.pages):
                    self.num_pages = int(self.pages.split('-')[1]) - int(self.pages.split('-')[0])
                elif r2.match(self.pages):
                    self.num_pages = int(self.pages.split('-')[1].split(':')[1]) - int(
                        self.pages.split('-')[0].split(':')[1])
                elif r3.match(self.pages):
                    self.num_pages = int(roman.fromRoman(self.pages.split('-')[1])) - int(
                        roman.fromRoman(self.pages.split('-')[0]))
                elif r4.match(self.pages):
                    self.num_pages = int(roman.fromRoman(self.pages.split('-')[1].split(':')[1])) - int(
                        roman.fromRoman(self.pages.split('-')[0].split(':')[1]))
                else:
                    # print("Pages not numeric nor calculable: ", self.pages)
                    self.num_pages = None
        except:
            # print('exception occurred in calculated pages:', self.pages)
            self.num_pages = None

    def addElectronicEditions(self, electronicEditions):
        """
        Add an array of Electronic Editions in electronic editions array
        :param electronicEditions: electronicEditions
        """
        r = re.compile('https://doi\.org/.*')
        for ee in electronicEditions:
            if r.match(ee):
                self.doi = ee
            if self.isInElectronicEditions(ee) is False:
                self.electronic_editions.append(PublicationElectronicEdition(
                    publication_id=self.id,
                    publication=self,
                    electronic_edition=ee.lower()
                ))

    def isInElectronicEditions(self, electronicEdition):
        """
        Check if an electronic edition is in array ignoring the string case.
        :param electronicEdition: electronic edition to check
        :return: Boolean - True if exists this electronic edition in the array otherwise False.
        """
        for ee in self.electronic_editions:
            if ee.electronic_edition.lower() == electronicEdition.lower():
                return True
        return False
