from sqlalchemy import select

from model.Model import PublicationGroup


class PublicationGroupRepository:
    def __init__(self, alchemy_session):
        self.session = alchemy_session

    def getOneByTitle(self, title):
        stmt = select(PublicationGroup).where(PublicationGroup.title == title)
        result = self.session.scalars(stmt)
        return result.first()

    def getCount(self):
        result = self.session.query(PublicationGroup).count()
        return result

    def getOneByUuid(self, uuid):
        stmt = select(PublicationGroup).where(PublicationGroup.uuid == uuid)
        result = self.session.scalars(stmt)
        return result.first()
