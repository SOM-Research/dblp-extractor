from database.orm.AuthorshipsRepository import AuthorshipsRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt

connection = DataBaseConnection()
session = connection.alchemySession()
repoA = AuthorshipsRepository(session)

print(repoA.researchersFirstPublicationsAfter1999())