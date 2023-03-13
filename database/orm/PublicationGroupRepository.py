from sqlalchemy import select
from database.orm import RepositoryBase
from model.PublicationGroup import PublicationGroup

class PublicationGroupRepository(RepositoryBase):

    def insertPublicationGroup(self, uuid, title, publisher, year, isbn,  booktitle, serie, volume, number, xmlKey, xmlMdate, xmlItem):
        pGroup = PublicationGroup(id=uuid, title=title, publisher=publisher, year=year, isbn=isbn, booktitle=booktitle, serie=serie,
                                  volume=volume, number=number, xml_key=xmlKey, xml_mdate=xmlMdate, xml_item=xmlItem)

        self.session.add(pGroup)
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