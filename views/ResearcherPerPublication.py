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
plt.savefig('../data/plots/ResearcherPerPublication/plain-totals.png')
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of researchers per papers')

bplot = ax.boxplot(numResearchersPerPublication, patch_artist=True, tick_labels=labels)
plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.savefig('../data/plots/ResearcherPerPublication/symlog-totals.png')
plt.show()


fig, ax = plt.subplots()
ax.set_ylabel('number of researchers per papers without outliers')

bplot = ax.boxplot(numResearchersPerPublication, patch_artist=True, showfliers=False, tick_labels=labels)
plt.savefig('../data/plots/ResearcherPerPublication/no-outliers-totals.png')
plt.show()



# Total outliers: 287367 from 7237410 publications
# Journals outliers: 156792 from 3517063 journals
# Conferences outliers: 128656 from 3490871 conferences
# Workshops outliers: 80 from 5083 workshops