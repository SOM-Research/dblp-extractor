from database.orm.PublicationRespository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection

import matplotlib.pyplot as plt
import numpy as np


connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)

result = repoP.getNumPublicationsByYear()
print(result)


years = []
num_publications_per_year = []
for pair in result:
    years.append(pair[0])
    num_publications_per_year.append(pair[1])


fig, ax = plt.subplots()
ax.plot(years, num_publications_per_year, linewidth=2.0)
plt.show()
fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year')

bplot = ax.boxplot(num_publications_per_year, patch_artist=True)

plt.show()


result = repoP.getNumPublicationsByYearFromYear(2000)
print(result)

num_publications_from_2000 = []
years = []
for pair in result:
    years.append(pair[0])
    num_publications_from_2000.append(pair[1])

fig, ax = plt.subplots()
ax.plot(years, num_publications_from_2000, linewidth=2.0)
plt.show()

fig, ax = plt.subplots()
ax.set_ylabel('number of papers per year since 2000')

bplot = ax.boxplot(num_publications_from_2000, patch_artist=True)

plt.show()
