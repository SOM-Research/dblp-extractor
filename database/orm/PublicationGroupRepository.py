from sqlalchemy import select
from database.orm import RepositoryBase
from model.Editor import Editor
from model.PublicationGroup import PublicationGroup

class PublicationGroupRepository(RepositoryBase):

    def insertPublicationGroup(self, uuid, title, publisher, year, isbn,  booktitle, serie, volume, number, ee, xmlKey, xmlMdate, xmlItem, researchers):
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
        if publication is not None:
            pGroup.publications.append(publication)
        self.session.commit()

        return pGroup

    def findByTitleAndVolume(self, title, volume):
        stmt = select(PublicationGroup).where(PublicationGroup.title == title).where(PublicationGroup.volume == volume)
        result = self.session.scalars(stmt)
        return result.first()

    def findByTitle(self, title):
        stmt = select(PublicationGroup).where(PublicationGroup.title == title)
        result = self.session.scalars(stmt)
        return result.first()

    def findByXmlKey(self, xmlKey):
        stmt = select(PublicationGroup).where(PublicationGroup.xml_key == xmlKey)
        result = self.session.scalars(stmt)
        return result.first()