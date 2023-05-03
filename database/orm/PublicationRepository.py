from database.orm import RepositoryBase
from model.Authorship import Authorship
from model.Publication import Publication

class PublicationRepository(RepositoryBase):

    def insertPublication(self, uuid, title, year, pages, type, xmlKey, xmlMdate, xmlItem, electronicEditions):
        """
        Insert a Publication
        :param uuid: Publication uuid
        :param title: Publication title
        :param year: Publication year of publication
        :param pages: Publication pages, need to calculate the number of pages
        :param type: PublicationType
        :param xmlKey: Publication xml key
        :param xmlMdate: Publication xml modification date
        :param xmlItem: Publication xml item
        :param electronicEditions: Publication electronic editions, mostly is the doi link
        :return: Publication
        """
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
        """
        Add an Author as Authorship
        :param publication: Publication
        :param author: Author to add as authorship
        :param position: position has the Author as an Authorship
        """
        authorship = Authorship(researcher_id=author.id, researcher=author, publication_id=publication.id, publication=publication, position=position)
        if authorship not in publication.authors:
            publication.authors.append(authorship)
        self.session.commit()