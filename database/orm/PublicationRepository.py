from database.orm import RepositoryBase
from model.Publication import Publication

class PublicationRepository(RepositoryBase):

    def insertPublication(self, uuid, title, year, pages, xmlKey, xmlMdate, xmlItem, electronicEditions):
        publication = Publication(id=uuid, title=title, year=year, pages=pages, xml_key=xmlKey,
                                xml_mdate=xmlMdate, xml_item=xmlItem)
        publication.setType()
        publication.calculatePages()
        publication.addElectronicEditions(electronicEditions)

        self.session.add(publication)
        self.session.commit()

        return publication