from sqlalchemy import select

from database.orm import RepositoryBase
from model.Institution import Institution

class InstitutionRepository(RepositoryBase):

    def insertInstitution(self, uuid, name):
        """
        Insert an Institution
        :param uuid: identifier of the Institution
        :param name: name of the Institution
        :return: Institution
        """
        institution = Institution(id=uuid, name=name)
        self.session.add(institution)
        self.session.commit()
        return institution

    def getOneByName(self, name):
        """
        Find one Institution by their name.
        :param name: name of the Institution to find
        :return: Institution or None
        """
        stmt = select(Institution).where(Institution.name == name)
        result = self.session.scalars(stmt)
        return result.first()