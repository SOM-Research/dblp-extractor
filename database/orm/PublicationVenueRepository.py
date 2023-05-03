from sqlalchemy import select
from database.orm import RepositoryBase
from model.PublicationVenue import PublicationVenue


class PublicationVenueRepository(RepositoryBase):
    def findByName(self, name):
        """
        Find PublicationVenue by name
        :param name: name of the PublicationVenue
        :return: PublicationVenue or None
        """
        stmt = select(PublicationVenue).where(PublicationVenue.name == name)
        result = self.session.scalars(stmt)
        return result.first()

    def insertPublicationVenue(self, uuid, name, type, pGroup):
        """
        insert a PublicationVenue
        :param uuid: PublicationVenue uuid
        :param name: PublicationVenue name
        :param type: PublicationVenue type
        :param pGroup: PublicationVenue publicationGroups from the Venue
        :return: PublicationVenue
        """
        pVenue = PublicationVenue(id=uuid, name=name, type=type)
        if pGroup is not None:
            pVenue.publication_groups.append(pGroup)
        self.session.add(pVenue)
        self.session.commit()

        return pVenue

    def addPublicationGroupInVenue(self, pVenue, pGroup):
        """
        Add a PublicationGroup in a PublicationVenue
        :param pVenue: PublicationVenue
        :param pGroup: PublicationGroup
        """
        pVenue.publication_groups.append(pGroup)
        self.session.commit()