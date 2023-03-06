from database.orm import RepositoryBase
from model.Publication import Publication

class PublicationRepository(RepositoryBase):

    def insertPublication(self, uuid, type, title, year, doi, pages, xmlKey, xmlMdate, xmlItem, electronicEditions):
        publication = Publication(id=uuid, type=type, title=title, year=year, doi=doi, pages=pages, xml_key=xmlKey,
                                xml_mdate=xmlMdate, xml_item=xmlItem)
        publication.calculatePages()
        publication.addElectronicEditions(electronicEditions)

        self.session.add(publication)
        self.session.commit()

        return publication