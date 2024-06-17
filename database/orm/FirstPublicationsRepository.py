from model.Model import FirstPublications, Publication, PublicationGroup, PublicationsFiltered
from sqlalchemy import select, text, or_


class FirstPublicationsRepository():
    def __init__(self, session):
        self.session = session

    def getAll(self):
        stmt = select(FirstPublications)
        result = self.session.scalars(stmt)
        return result.all()


    def getResearchers(self,  all, has_publication_before):
        if all:
            stmt = select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
            result = self.session.execute(stmt)
            return result.all()

        stmt = (select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
                .where(FirstPublications.has_publications_before == has_publication_before)
                .where(FirstPublications.num_publications > 3)
                .distinct()).order_by(FirstPublications.researcher_uuid)
        result = (self.session.execute(stmt))
        return result.all()
    def getAllWithCondition(self, condition, types):
        stmt = (
            select(FirstPublications)
            .where(FirstPublications.has_publications_before == condition)
            .where(FirstPublications.type.in_(types))
            .where(FirstPublications.num_publications > 3)
            .order_by(FirstPublications.researcher_uuid, FirstPublications.year_publication)
        )
        result = self.session.execute(stmt)
        return result.all()


    def getResearchersBetween(self,  all, condition, year_from, year_to):
        if all:
            stmt = select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
            result = self.session.execute(stmt)
            return result.all()

        stmt = (select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
                .where(FirstPublications.has_publications_before == condition)
                .where(FirstPublications.num_publications > 3)
                .where(FirstPublications.year_frist_publication >= year_from)
                .where(FirstPublications.year_frist_publication < year_to)
                .distinct()).order_by(FirstPublications.researcher_uuid)
        result = (self.session.execute(stmt))
        return result.all()

    def getAllWithConditionBetween(self, condition, types, year_from, year_to):
        stmt = (
            select(FirstPublications)
            .where(FirstPublications.has_publications_before == condition)
            .where(FirstPublications.type.in_(types))
            .where(FirstPublications.num_publications > 3)
            .where(FirstPublications.year_frist_publication >= year_from)
            .where(FirstPublications.year_frist_publication < year_to)
            .order_by(FirstPublications.researcher_uuid, FirstPublications.year_publication)
        )
        result = self.session.execute(stmt)
        return result.all()


    def getResearchersInConferencesAndJournals(self, all, condition):
        if all:
            stmt = (select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
                    .join(PublicationsFiltered, FirstPublications.publication_uuid == PublicationsFiltered.uuid))
            result = self.session.execute(stmt)
            return result.all()

        stmt = (select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
                .join(PublicationsFiltered, FirstPublications.publication_uuid == PublicationsFiltered.uuid)
                .where(FirstPublications.has_publications_before == condition)
                .where(FirstPublications.num_publications > 3)
                .distinct()).order_by(FirstPublications.researcher_uuid)
        result = (self.session.execute(stmt))
        return result.all()


    def getAllWithConditionInConferencesAndJournals(self, condition, types):
        stmt = (
            select(FirstPublications)
            .join(PublicationsFiltered, FirstPublications.publication_uuid == PublicationsFiltered.uuid)
            .where(FirstPublications.has_publications_before == condition)
            .where(FirstPublications.type.in_(types))
            .where(FirstPublications.num_publications > 3)
            .order_by(FirstPublications.researcher_uuid, FirstPublications.year_publication)
        )
        result = self.session.execute(stmt)
        return result.all()

    def getResearchersBetweenInConferencesAndJournals(self,  all, condition, year_from, year_to):
        if all:
            stmt = select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
            result = self.session.execute(stmt)
            return result.all()

        stmt = (select(FirstPublications.researcher_uuid, FirstPublications.researcher_name)
            .join(PublicationsFiltered, FirstPublications.publication_uuid == PublicationsFiltered.uuid)
                .where(FirstPublications.has_publications_before == condition)
                .where(FirstPublications.num_publications > 3)
                .where(FirstPublications.year_frist_publication >= year_from)
                .where(FirstPublications.year_frist_publication < year_to)
                .distinct()).order_by(FirstPublications.researcher_uuid)
        result = (self.session.execute(stmt))
        return result.all()

    def getAllWithConditionBetweenInConferencesAndJournals(self, condition, types, year_from, year_to):
        stmt = (
            select(FirstPublications)
            .join(PublicationsFiltered, FirstPublications.publication_uuid == PublicationsFiltered.uuid)
            .where(FirstPublications.has_publications_before == condition)
            .where(FirstPublications.type.in_(types))
            .where(FirstPublications.num_publications > 3)
            .where(FirstPublications.year_frist_publication >= year_from)
            .where(FirstPublications.year_frist_publication < year_to)
            .order_by(FirstPublications.researcher_uuid, FirstPublications.year_publication)
        )
        result = self.session.execute(stmt)
        return result.all()