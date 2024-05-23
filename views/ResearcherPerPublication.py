from database.orm.AuthorshipsRepository import AuthorshipsRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt

connection = DataBaseConnection()
session = connection.alchemySession()
repoA = AuthorshipsRepository(session)

numResearchersPerPublication = []
labels = ['total', 'journals', 'conferences', 'workshops']
numResearchersPerPublication.append(repoA.getResearcherPerPublications())
numResearchersPerPublication.append(repoA.getResearcherPerJournals())
numResearchersPerPublication.append(repoA.getResearcherPerConferences())
numResearchersPerPublication.append(repoA.getResearcherPerWorkshops())


fig, ax = plt.subplots()
ax.set_ylabel('number of researchers per papers')

bplot = ax.boxplot(numResearchersPerPublication, patch_artist=True, tick_labels=labels)

plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of researchers per papers')

bplot = ax.boxplot(numResearchersPerPublication, patch_artist=True, showfliers=False, tick_labels=labels)
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of researchers per workshops')

bplot = ax.boxplot(numResearchersPerPublication[3], patch_artist=True)
plt.show()
