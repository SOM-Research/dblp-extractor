from model.Model import Researcher
from sqlalchemy import select, text

class AuthorshipsRepository():
    def __init__(self, session):
        self.session = session

    def getPublicationsPerResearcher(self):
        textual_sql = text(
            " select count(a.researcher_uuid) "
            " from authorships as a "
            " group by a.researcher_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getJournalsPerResearcher(self):
        textual_sql = text(
            " select count(a.researcher_uuid) "
            " from authorships as a left join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'journal' "
            " group by a.researcher_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getConferencesPerResearcher(self):
        textual_sql = text(
            " select count(a.researcher_uuid) "
            " from authorships as a left join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'conference' "
            " group by a.researcher_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getWorkshopsPerResearcher(self):
        textual_sql = text(
            " select count(a.researcher_uuid) "
            " from authorships as a left join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'workshop' "
            " group by a.researcher_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getWorkshopsPerResearcherMoreThan(self, num):
        textual_sql = text(
            " select count(a.researcher_uuid) "
            " from authorships as a left join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'workshop' "
            " group by a.researcher_uuid"
            " having count(a.researcher_uuid) > " + str(num))
        result = self.session.scalars(textual_sql)
        return result.all()

    def getResearcherPerPublications(self):
        textual_sql = text(
            " select count(a.publication_uuid) "
            " from authorships as a "
            " group by a.publication_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()
    def getResearcherPerJournals(self):
        textual_sql = text(
            " select count(a.publication_uuid) "
            " from authorships as a right join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'journal' "
            " group by a.publication_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getResearcherPerConferences(self):
        textual_sql = text(
            " select count(a.publication_uuid) "
            " from authorships as a right join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'conference' "
            " group by a.publication_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()

    def getResearcherPerWorkshops(self):
        textual_sql = text(
            " select count(a.publication_uuid) "
            " from authorships as a right join publications as p ON (a.publication_uuid = p.uuid)"
            " where p.type = 'workshop' "
            " group by a.publication_uuid")
        result = self.session.scalars(textual_sql)
        return result.all()





