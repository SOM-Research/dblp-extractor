from sqlalchemy import select, func, text

from model.Model import Publication, PublicationGroup


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

    def getNumPublicationsPerPublicationGroup(self):
        textual_sql = text(
            " select count(p.publication_group_uuid) "
            " from publications as p left join publication_groups as pg on (pg.uuid = p.publication_group_uuid) "
            " group by p.publication_group_uuid, pg.uuid, pg.title")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getNumPublicationsPerPublicationGroupWithHavingCondition(self, havingCount):
        textual_sql = text(
            " select count(p.publication_group_uuid) "
            " from publications as p left join publication_groups as pg on (pg.uuid = p.publication_group_uuid) "
            " group by p.publication_group_uuid, pg.uuid, pg.title"
            " having count(p.publication_group_uuid) " + havingCount )
        result = self.session.scalars(textual_sql)
        return result.all()

    def getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(self, since, until):
        textual_sql = text(
            " select count(p.publication_group_uuid) "
            " from publications as p left join publication_groups as pg on (pg.uuid = p.publication_group_uuid) "
            " where p.year BETWEEN " + str(since) + " AND " + str(until) +
            " group by p.publication_group_uuid, pg.uuid, pg.title"
            " having count(p.publication_group_uuid) < 125")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getNumPublicationsMoreThan124PerPublicationGroupPeriodsBetween(self, since, until):
        textual_sql = text(
            " select count(p.publication_group_uuid) "
            " from publications as p left join publication_groups as pg on (pg.uuid = p.publication_group_uuid) "
            " where p.year BETWEEN " + str(since) + " AND " + str(until) +
            " group by p.publication_group_uuid, pg.uuid, pg.title"
            " having count(p.publication_group_uuid) > 124")
        result = self.session.scalars(textual_sql)
        return result.all()