from database.orm import RepositoryBase
from model.Authorship import Authorship
from model.Publication import Publication

class PublicationRepository(RepositoryBase):

    def insertPublication(self, uuid, title, year, pages, type, xmlKey, xmlMdate, xmlItem, electronicEditions):
        pages = pages.strip() if pages is not None else None
        publication = Publication(id=uuid, title=title, year=year, pages=pages, xml_key=xmlKey,
                                xml_mdate=xmlMdate, xml_item=xmlItem)

        publication.setType(type)
        publication.calculatePages()
        publication.addElectronicEditions(electronicEditions)

        self.session.add(publication)
        self.session.commit()

        return publication

    def addAuthorship(self, publication, author, position):
        authorship = Authorship(researcher_id=author.id, researcher=author, publication_id=publication.id, publication=publication, position=position)
        if authorship not in publication.authors:
            publication.authors.append(authorship)
        self.session.commit()