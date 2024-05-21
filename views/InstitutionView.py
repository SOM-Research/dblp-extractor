
from database.orm.InstitutionRepository import InstitutionRepository
from database.DataBaseConnection import DataBaseConnection


connection = DataBaseConnection()
repoI = InstitutionRepository(connection.alchemySession())

result = repoI.getOneByName(name='University  of California at Santa Barbara, CA, USA')


print(result.name)