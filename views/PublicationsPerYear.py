from database.orm.PublicationRepository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)

result = repoP.getNumPublicationsByYear()


years = []
num_publications_per_year = []
for pair in result:
    years.append(pair[0])
    num_publications_per_year.append(pair[1])


fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year')

ax.plot(years, num_publications_per_year, linewidth=2.0)
plt.savefig('../data/plots/PublicationPerYear/linear-totals.png')
plt.show()

#with symlog
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year (log)')
ax.plot(years, num_publications_per_year, linewidth=2.0)
plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.savefig('../data/plots/PublicationPerYear/linear-symlog-totals.png')
plt.show()

# plt.yscale('symlog')
# ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
# plt.savefig('../data/plots/PublicationPerYear/symlog-totals.png')
# plt.savefig('../data/plots/folder/symlog-totals.png')




fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year')
stats = cbook.boxplot_stats(num_publications_per_year)
bplot = ax.boxplot(num_publications_per_year, patch_artist=True)

plt.savefig('../data/plots/PublicationPerYear/boxplot-totals.png')
plt.show()
print(stats)
print(len(stats[0]['fliers']))
## 15 fliers

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year')

bplot = ax.boxplot(num_publications_per_year, patch_artist=True, showfliers=False)

plt.savefig('../data/plots/PublicationPerYear/no-outliers-totals.png')
plt.show()

result = repoP.getNumPublicationsByYearFromYear(2000)
print(result)

num_publications_from_2000 = []
years = []
for pair in result:
    years.append(pair[0])
    num_publications_from_2000.append(pair[1])

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year since 2000')
ax.plot(years, num_publications_from_2000, linewidth=2.0)
plt.show()
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year since 2000 (log)')
ax.plot(years, num_publications_from_2000, linewidth=2.0)

plt.yscale('symlog')
ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year since 2000')

bplot = ax.boxplot(num_publications_from_2000, patch_artist=True)

plt.show()
fig, ax = plt.subplots()

ax.set_ylabel('number of papers per year since 2000')

bplot = ax.boxplot(num_publications_from_2000, patch_artist=True)

plt.show()


# plt.yscale('symlog')
# ax.yaxis.set_major_formatter(lambda x, p: f'{int(x):,}')
# plt.savefig('../data/plots/folder/symlog-totals.png')