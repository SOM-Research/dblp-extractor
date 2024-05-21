
from database.orm.PublicationRespository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection


connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)

result = repoP.getCount()
print(result)
result = repoP.getOneByTitle(title='Automatic Detection of Verbal Deception')
print(result.uuid)
result = repoP.getOneByUuid(uuid='93127ee1-1497-408a-a1e5-f055428369d2')
print(result.title)
for editor in result.model_authors:
    print(editor.current_alias)
    print(editor.uuid)