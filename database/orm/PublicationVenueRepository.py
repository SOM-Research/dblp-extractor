from sqlalchemy import select
from database.orm import RepositoryBase
from model.PublicationVenue import PublicationVenue


class PublicationVenueRepository(RepositoryBase):
    def findByName(self, name):
        stmt = select(PublicationVenue).where(PublicationVenue.name == name)
        result = self.session.scalars(stmt)
        return result.first()

    def insertPublicationVenue(self, uuid, name, type, pGroup):
        pVenue = PublicationVenue(id=uuid, name=name, type=type)
        if pGroup is not None:
            pVenue.publication_groups.append(pGroup)
        self.session.add(pVenue)
        self.session.commit()

        return pVenue

    def addPublicationGroupInVenue(self, pVenue, pGroup):
        pVenue.publication_groups.append(pGroup)
        self.session.commit()