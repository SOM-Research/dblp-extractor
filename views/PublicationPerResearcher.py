from database.orm.AuthorshipsRepository import AuthorshipsRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt

connection = DataBaseConnection()
session = connection.alchemySession()
repoA = AuthorshipsRepository(session)

numPubPerResearcher = []
labels = ['total', 'journals', 'conferences', 'workshops']
numPubPerResearcher.append(repoA.getPublicationsPerResearcher())
numPubPerResearcher.append(repoA.getJournalsPerResearcher())
numPubPerResearcher.append(repoA.getConferencesPerResearcher())
numPubPerResearcher.append(repoA.getWorkshopsPerResearcher())


fig, ax = plt.subplots()
ax.set_ylabel('number of papers per researchers')

bplot = ax.boxplot(numPubPerResearcher, patch_artist=True, tick_labels=labels)

plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per researchers')

bplot = ax.boxplot(numPubPerResearcher, patch_artist=True, showfliers=False, tick_labels=labels)
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of workshops per researchers')

bplot = ax.boxplot(numPubPerResearcher[3], patch_artist=True)
plt.show()





result = repoA.getWorkshopsPerResearcherMoreThan(1)
fig, ax = plt.subplots()
ax.set_ylabel('number of workshops (more than 1) per researchers')

bplot = ax.boxplot(result, patch_artist=True)
plt.show()
