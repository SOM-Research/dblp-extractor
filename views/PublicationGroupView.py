
from database.orm.PublicationGroupRepository import PublicationGroupRepository
from database.DataBaseConnection import DataBaseConnection


connection = DataBaseConnection()
session = connection.alchemySession()
repoPG = PublicationGroupRepository(session)

result = repoPG.getCount()
print(result)
result = repoPG.getOneByTitle(title='Handbook of Genetic Programming Applications')
print(result.uuid)
result = repoPG.getOneByUuid(uuid='5769acad-6dda-4f92-b662-8bf6bdaec9b3')
print(result.title)
for editor in result.model_editors:
    print(editor.current_alias)
    print(editor.uuid)
print(len(result.publications))
print(result.publications[0].title)