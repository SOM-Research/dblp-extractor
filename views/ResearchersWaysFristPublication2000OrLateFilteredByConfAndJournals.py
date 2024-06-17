from uuid import UUID

from database.orm.FirstPublicationsRepository import FirstPublicationsRepository
from database.DataBaseConnection import DataBaseConnection
import collections
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
from sankeyflow import Sankey


def count_array(count_raw):
    count = {'j-j': 0, 'c-j': 0, 'j-c': 0, 'c-c': 0,}
    provisional_count = {i: count_raw.count(i) for i in count_raw}
    for key in provisional_count.keys():
        count[key] = provisional_count[key]
    return count
def count_3_levels(researcher_list):
    counts_3_raw = []
    counts_2_raw = []
    counts_1_raw = []
    for r in researcher_list:
        if len(r.publications) >= 4:
            counts_3_raw.append('-'.join([r.publications[2].type[0], r.publications[3].type[0]]))
            counts_2_raw.append('-'.join([r.publications[1].type[0], r.publications[2].type[0]]))
            counts_1_raw.append('-'.join([r.publications[0].type[0], r.publications[1].type[0]]))

    counts_1 = count_array(counts_1_raw)
    print(counts_1)
    counts_2 = count_array(counts_2_raw)
    print(counts_2)
    counts_3 = count_array(counts_3_raw)
    print(counts_3)
    return counts_1, counts_2, counts_3

def create_researcher_list_from_query_result(researchers_uuids, first_publications):
    researcher_list = list()
    uuid_list = list()
    for fp_researcher in researchers_uuids:
        uuid_list.append(fp_researcher[0])
        researcher_list.append(researcher(uuid=fp_researcher[0], name=fp_researcher[1], publications=[]))
    for f_pub in first_publications:
        i = uuid_list.index(f_pub[0].researcher_uuid)
        if len(researcher_list[i].publications) < 4:
            researcher_list[i].publications.append(
                publication(uuid=f_pub[0].publication_uuid, year=f_pub[0].year_publication, type=f_pub[0].type))
    return researcher_list

def get_flows(list_1, list_2, list_3, total):
    return [
        ('Journal1', 'Journal2', list_1['j-j']/ total * 100000, {'color': 'plum'}),
        ('Conference1', 'Journal2', list_1['c-j']/ total * 100000, {'color': 'paleturquoise'}),
        ('Journal1', 'Conference2', list_1['j-c']/ total * 100000, {'color': 'plum'}),
        ('Conference1', 'Conference2', list_1['c-c']/ total * 100000, {'color': 'paleturquoise'}),
        ('Journal2', 'Journal3', list_2['j-j']/ total * 100000, {'color': 'plum'}),
        ('Conference2', 'Journal3', list_2['c-j']/ total * 100000, {'color': 'paleturquoise'}),
        ('Journal2', 'Conference3', list_2['j-c']/ total * 100000, {'color': 'plum'}),
        ('Conference2', 'Conference3', list_2['c-c']/ total * 100000, {'color': 'paleturquoise'}),
        ('Journal3', 'Journal4', list_3['j-j']/ total * 100000, {'color': 'plum'}),
        ('Conference3', 'Journal4', list_3['c-j']/ total * 100000, {'color': 'paleturquoise'}),
        ('Journal3', 'Conference4', list_3['j-c']/ total * 100000, {'color': 'plum'}),
        ('Conference3', 'Conference4', list_3['c-c']/ total * 100000, {'color': 'paleturquoise'}),
    ]

def sankey_plot_between_date(year_from, year_to):
    print(year_from, year_to)
    first_publications_researchers_uuids = repoFP.getResearchersBetweenInConferencesAndJournals(all=False, condition=False, year_from=year_from,
                                                                        year_to=year_to)
    first_publications = repoFP.getAllWithConditionBetweenInConferencesAndJournals(
        condition=False,
        types=['journal', 'conference'],
        year_from=year_from,
        year_to=year_to
    )
    print(len(first_publications))

    researcher_list = create_researcher_list_from_query_result(first_publications_researchers_uuids, first_publications)
    counts_1, counts_2, counts_3 = count_3_levels(researcher_list)
    total = (counts_1['j-j']+counts_1['j-c']+counts_1['c-j']+counts_1['c-c'])
    flows = get_flows(counts_1, counts_2, counts_3, total)

    print(flows)
    nodes = [
        [('Journal1', (counts_1['j-j'] + counts_1['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference1', (counts_1['c-j'] + counts_1['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal2', (counts_2['j-j'] + counts_2['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference2', (counts_2['c-j'] + counts_2['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal3', (counts_3['j-j'] + counts_3['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference3', (counts_3['c-j'] + counts_3['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal4', (counts_3['j-j'] + counts_3['c-j']) / total * 100000, {'color': 'orchid'}),
         ('Conference4', (counts_3['j-c'] + counts_3['c-c']) / total * 100000, {'color': 'darkturquoise'})],
    ]
    plt.figure(figsize=(8, 4))
    s = Sankey(
        flows=flows,
        nodes=nodes
    )
    s.draw()
    plt.title('Selected Journal-Conferences Sankey from ' + str(year_from) + ' to ' + str(year_to) + '.%')
    plt.savefig('../data/plots/sankey-filtered/per-years-from' + str(year_from) + '-to-' + str(year_to) + '.png')
    plt.savefig('../data/plots/sankey-filtered/per-years-from' + str(year_from) + '-to-' + str(year_to) + '.pdf')
    plt.savefig('../data/plots/sankey-filtered/per-years-from' + str(year_from) + '-to-' + str(year_to) + '.svg')
    plt.show()

connection = DataBaseConnection()
session = connection.alchemySession()
repoFP = FirstPublicationsRepository(session)

publication = collections.namedtuple('Publication', 'uuid, year, type')
researcher = collections.namedtuple('Researcher', 'uuid name publications')


first_publications_researchers_uuids = repoFP.getResearchersInConferencesAndJournals(all = False, condition = False)
first_publications = repoFP.getAllWithConditionInConferencesAndJournals(condition = False, types=['journal', 'conference',])
print(len(first_publications))

researcher_list = create_researcher_list_from_query_result(first_publications_researchers_uuids, first_publications)
counts_1, counts_2, counts_3 = count_3_levels(researcher_list)
total = (counts_1['j-j']+counts_1['j-c']+counts_1['c-j']+counts_1['c-c'])
flows = get_flows(counts_1, counts_2, counts_3, total)

print(flows)

nodes = [
        [('Journal1', (counts_1['j-j'] + counts_1['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference1', (counts_1['c-j'] + counts_1['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal2', (counts_2['j-j'] + counts_2['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference2', (counts_2['c-j'] + counts_2['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal3', (counts_3['j-j'] + counts_3['j-c']) / total * 100000, {'color': 'orchid'}),
         ('Conference3', (counts_3['c-j'] + counts_3['c-c']) / total * 100000, {'color': 'darkturquoise'})],
        [('Journal4', (counts_3['j-j'] + counts_3['c-j']) / total * 100000, {'color': 'orchid'}),
         ('Conference4', (counts_3['j-c'] + counts_3['c-c']) / total * 100000, {'color': 'darkturquoise'})],
]
plt.figure(figsize=(8, 4))
s = Sankey(flows=flows, nodes=nodes)
s.draw()
plt.title('Journal-Conferences Sankey from a selected journals and conferences.%')
plt.savefig('../data/plots/sankey-filtered/overall.png')
plt.savefig('../data/plots/sankey-filtered/overall.pdf')
plt.savefig('../data/plots/sankey-filtered/overall.svg')
plt.show()



years = [ [2000, 2005], [2005, 2010], [2010, 2015], [2015, 2020], [2020, 2025], ]
for couple_year in years:
    sankey_plot_between_date(couple_year[0], couple_year[1])
