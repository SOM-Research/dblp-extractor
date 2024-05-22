from sqlalchemy import select, func

from model.Model import Publication


class PublicationRepository:
    def __init__(self, alchemy_session):
        self.session = alchemy_session

    def getOneByTitle(self, title):
        stmt = select(Publication).where(Publication.title == title)
        result = self.session.scalars(stmt)
        return result.first()

    def getCount(self):
        result = self.session.query(Publication).count()
        return result

    def getOneByUuid(self, uuid):
        stmt = select(Publication).where(Publication.uuid == uuid)
        result = self.session.scalars(stmt)
        return result.first()

    def getNumPublicationsByYear(self):
        result = self.session.query(Publication.year,
                      func.count(Publication.year)).group_by(Publication.year)
        return result.all()

    def getNumPublicationsByYearFromYear(self, year):
        result = (self.session.query(Publication.year, func.count(Publication.year))
                  .where(Publication.year >= year)
                  .where(Publication.year is not None)
                  .group_by(Publication.year)
                  )
        return result.all()
