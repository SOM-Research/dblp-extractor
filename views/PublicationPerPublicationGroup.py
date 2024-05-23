from database.orm.PublicationRepository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt



connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)

result = repoP.getNumPublicationsPerPublicationGroup()


fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')

bplot = ax.boxplot(result, patch_artist=True)

plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')

bplot = ax.boxplot(result, patch_artist=True, showfliers=False)
plt.show()


# The first one is in 1951
result50 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(1950, 1960)
result60 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(1960, 1970)
result70 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(1970, 1980)
result80 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(1980, 1990)
result90 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(1990, 2000)

results_50_to_2000 = [result50, result60, result70, result80, result90]
labels = ["50's-60's", "60's-70's", "70's-80's", "80's-90's", "90's-2000"]
#publications between 50s and 60s
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(results_50_to_2000,
                   patch_artist=True,
                   tick_labels=labels)

plt.show()


result2000 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(2000, 2005)
result2005 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(2005, 2010)
result2010 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(2010, 2015)
result2015 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(2015, 2020)
result2020 = repoP.getNumPublicationsLessThan125PerPublicationGroupPeriodsBetween(2020, 2024)


results_2000_to_2024 = [result2000, result2005, result2010, result2015, result2020]
labels = ["2000-2005", "2005-2010", "2010-2015", "2015-2020", "2020-2024"]
#publications between 50s and 60s
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(results_2000_to_2024,
                   patch_artist=True,
                   tick_labels=labels)

plt.show()
print(results_2000_to_2024)

result2000m = repoP.getNumPublicationsMoreThan124PerPublicationGroupPeriodsBetween(2000, 2005)

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(result2000m, patch_artist=True,)

plt.show()
result = repoP.getNumPublicationsPerPublicationGroupWithHavingCondition(" <125  ")


fig, ax = plt.subplots()
ax.set_ylabel('number of papers per publication group')
bplot = ax.boxplot(result, patch_artist=True,)

plt.show()