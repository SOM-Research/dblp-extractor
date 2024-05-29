from database.orm.PublicationRepository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection
import numpy as np
import matplotlib.cbook as cbook

import matplotlib.pyplot as plt



connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)

result = repoP.getNumPublicationsPerPublicationGroup()




fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')

bplot = ax.boxplot(result, patch_artist=True)

plt.savefig('../data/plots/PublicationPerPubGroup/plain-totals.png')
plt.show()

stats = cbook.boxplot_stats(result)
print(stats)
print(len(stats[0]['fliers']))
#  outliers  'q1': 16.0, 'med': 31.0, 'q3': 58.0

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group (log)')
plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
bplot = ax.boxplot(result, patch_artist=True)

plt.savefig('../data/plots/PublicationPerPubGroup/symlog-totals.png')
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group without outliers')

bplot = ax.boxplot(result, patch_artist=True, showfliers=False)
plt.savefig('../data/plots/PublicationPerPubGroup/no-outliers-totals.png')
plt.show()


# The first one is in 1951
result50 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(1950, 1960)
result50 = np.array(result50)
result60 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(1960, 1970)
result60 = np.array(result60)
result70 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(1970, 1980)
result70 = np.array(result70)
result80 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(1980, 1990)
result80 = np.array(result80)
result90 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(1990, 2000)
result90 = np.array(result90)

results_50_to_2000 = [result50[:,0], result60[:,0], result70[:,0], result80[:,0], result90[:,0]]
labels = ["50's-60's", "60's-70's", "70's-80's", "80's-90's", "90's-2000"]
#publications between 50s and 60s
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(results_50_to_2000,
                   patch_artist=True,
                   tick_labels=labels)

plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.show()


result2000 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(2000, 2005)
result2000 = np.array(result2000)
result2005 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(2005, 2010)
result2005 = np.array(result2005)
result2010 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(2010, 2015)
result2010 = np.array(result2010)
result2015 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(2015, 2020)
result2015 = np.array(result2015)
result2020 = repoP.getNumPublicationsAndYearPerPublicationGroupPeriodsBetween(2020, 2024)
result2020 = np.array(result2020)

results_2000_to_2024 = [result2000[:,0], result2005[:,0], result2010[:,0], result2015[:,0], result2020[:,0]]
labels = ["2000-2005", "2005-2010", "2010-2015", "2015-2020", "2020-2024"]
#publications between 50s and 60s
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(results_2000_to_2024,
                   patch_artist=True,
                   tick_labels=labels)

plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.show()
