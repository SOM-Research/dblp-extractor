
from database.orm.InstitutionRepository import InstitutionRepository
from database.orm.ResearcherRepository import ResearcherRepository
from database.DataBaseConnection import DataBaseConnection


connection = DataBaseConnection()
session = connection.alchemySession()
repoI = InstitutionRepository(session)
repoR = ResearcherRepository(session)


result = repoR.getCount()
print(result)
result = repoR.getOneById(uuid='64ef580f-3e58-4d76-91e0-35cb9df1ee91')
print(result.current_alias)
for affiliation in result.affiliations:
    print(affiliation.name)

