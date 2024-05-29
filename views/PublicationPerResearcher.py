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
plt.savefig('../data/plots/PublicationPerResearcher/plain-totals.png')
plt.show()


fig, ax = plt.subplots()
ax.set_ylabel('number of publications per researchers')

bplot = ax.boxplot(numPubPerResearcher, patch_artist=True, tick_labels=labels)
plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.savefig('../data/plots/PublicationPerResearcher/symlog-totals.png')
plt.show()


# total 515847 outliers from a total of 3516713
# journals 278923 from a total of 2355516
# conferences 273758 from a total of 2243536
# workshops 87 from a total of 12384

fig, ax = plt.subplots()
ax.set_ylabel('number of publications per researchers without outliers')

bplot = ax.boxplot(numPubPerResearcher, patch_artist=True, showfliers=False, tick_labels=labels)
plt.savefig('../data/plots/PublicationPerResearcher/no-outliers-totals.png')
plt.show()
