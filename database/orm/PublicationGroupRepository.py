from sqlalchemy import select
from database.orm import RepositoryBase
from model.Editor import Editor
from model.PublicationGroup import PublicationGroup

class PublicationGroupRepository(RepositoryBase):

    def insertPublicationGroup(self, uuid, title, publisher, year, isbn,  booktitle, serie, volume, number, ee, xmlKey, xmlMdate, xmlItem, researchers):
        """
        Insert PublicationGroup object
        :param uuid: PublicationGroup uuid
        :param title: PublicationGroup title
        :param publisher: PublicationGroup publisher
        :param year: PublicationGroup year of publication
        :param isbn: PublicationGroup isbn
        :param booktitle: PublicationGroup booktitle
        :param serie: PublicationGroup serie
        :param volume: PublicationGroup volume
        :param number: PublicationGroup number
        :param ee: PublicationGroup array of electronic editions
        :param xmlKey: PublicationGroup xml key; only for instances entire comes from xml
        :param xmlMdate: PublicationGroup xml modification date; only for instances entire comes from xml
        :param xmlItem: PublicationGroup xml item; only for instances entire comes from xml
        :param researchers: array of Researchers who were Editors in the instances
        :return: PublicationGroup
        """
        pGroup = PublicationGroup(id=uuid, title=title, publisher=publisher, year=year, isbn=isbn, booktitle=booktitle, serie=serie,
                                  volume=volume, number=number, xml_key=xmlKey, xml_mdate=xmlMdate, xml_item=xmlItem)

        if ee is not None:
            pGroup.addElectronicEditions(ee)

        if researchers is not None:
            position = 0
            for researcher in researchers:
                editor = Editor(researcher_id=researcher.id, researcher=researcher, publication_group_id=pGroup.id, publication_group=pGroup, position=position)
                if editor not in pGroup.editors:
                    pGroup.editors.append(editor)
                    position += 1

        self.session.add(pGroup)
        self.session.commit()

        return pGroup

    def addPublicationIntoPublicationGroup(self, pGroup, publication):
        """
        Add a Publication into PublicationGroup
        :param pGroup: PublicationGroup
        :param publication: Publication to add
        :return: PublicationGroup
        """
        if publication is not None:
            pGroup.publications.append(publication)
        self.session.commit()

        return pGroup

    def findByTitleAndVolume(self, title, volume):
        """
        Find a PublicationGroup by Title and Volume
        :param title: PublicationGroup Title
        :param volume: PublicationGroup Volume
        :return: PublicationGroup or None
        """
        stmt = select(PublicationGroup).where(PublicationGroup.title == title).where(PublicationGroup.volume == volume)
        result = self.session.scalars(stmt)
        return result.first()

    def findByTitle(self, title):
        """
        Find a PublicationGroup by Title
        :param title: PublicationGroup Title
        :return: PublicationGroup or None
        """
        stmt = select(PublicationGroup).where(PublicationGroup.title == title)
        result = self.session.scalars(stmt)
        return result.first()

    def findByXmlKey(self, xmlKey):
        """
        Find a PublicationGroup by xml key
        :param xmlKey: PublicationGroup xml key
        :return: PublicationGroup or None
        """
        stmt = select(PublicationGroup).where(PublicationGroup.xml_key == xmlKey)
        result = self.session.scalars(stmt)
        return result.first()