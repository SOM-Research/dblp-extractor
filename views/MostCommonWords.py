from database.orm.PublicationRepository import PublicationRepository
from database.DataBaseConnection import DataBaseConnection
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from functools import reduce
import nltk
import matplotlib.pyplot as plt
from collections import Counter


nltk.download('punkt')

connection = DataBaseConnection()
session = connection.alchemySession()
repoP = PublicationRepository(session)



example_sent = """This is a sample sentence,
                  showing off the stop words filtration."""

stop_words = set(stopwords.words('english'))

# converts the words in word_tokens to lower case and then checks whether
# they are present in stop_words or not
# with no lower case conversion

to_add_as_a_stop_word = ['.', ':', '-', ',', '(', ')', '?', '\'s', '\'', '[', ']', 'using', 'approach', 'development',
                         'design', 'process', 'study', 'search', 'service', 'method', 'code', 'case', 'formal',
                         'based', 'learning', 'applications', 'system', 'program', 'use', 'towards', 'section', 'part',
                         'introduction', 'guest', 'issue', 'source', 'review', 'systematic', 'workshop',
                         'analysis', 'editorial']
for word in to_add_as_a_stop_word:
    stop_words.add(word)


def most_frequent_word_by_group(title_list, stop_words_custom):
    cleaned_titles = []
    for title in title_list:
        word_tokens = word_tokenize(title.lower())
        filtered_sentence = [w for w in word_tokens if not w in stop_words_custom]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        cleaned_titles.append(' '.join(filtered_sentence))
    all_words = reduce(lambda a, b: a + b, [sub.split() for sub in cleaned_titles])
    word_counts = Counter(all_words)
    return cleaned_titles, word_counts.most_common(5)

def most_frequent_word_all_together(title_list):
    all_words = reduce(lambda a, b: a + b, [sub.split() for sub in title_list])
    word_counts = Counter(all_words)
    return word_counts.most_common(5)


# International Conference on Software Language Engineering (SLE)
sle_titles = repoP.getTitlesFromNamedConference('SLE')
stop_words_sle = stop_words
to_add_as_a_stop_word_in_sle = ['software', 'language', 'engineering', 'languages']
for word in to_add_as_a_stop_word_in_sle:
    stop_words_sle.add(word)
print('sle_titles')
all_sle_titles, most_frequent_sle = most_frequent_word_by_group(sle_titles, stop_words_sle)
print(most_frequent_sle)

# International Conference on Software Engineering (ICSE)
icse_titles = repoP.getTitlesFromNamedConference('ICSE')
stop_words_icse = stop_words
to_add_as_a_stop_word_in_icse = ['software', 'engineering']
for word in to_add_as_a_stop_word_in_icse:
    stop_words_icse.add(word)
print('icse_titles')
all_icse_titles, most_frequent_icse = most_frequent_word_by_group(icse_titles, stop_words_icse)
print(most_frequent_icse)

# International Conference on Advanced Information Systems Engineering (CAiSE)
caise_titles = repoP.getTitlesFromNamedConference('CAiSE')
stop_words_caise = stop_words
to_add_as_a_stop_word_in_caise = ['advanced', 'information', 'systems',  'engineering']
for word in to_add_as_a_stop_word_in_caise:
    stop_words_caise.add(word)
print('caise_titles')
all_caise_titles, most_frequent_caise = most_frequent_word_by_group(caise_titles, stop_words_caise)
print(most_frequent_caise)

# International Conference on Model Driven Engineering Languages and Systems (MoDELS)
models_titles = repoP.getTitlesFromNamedConference('MoDELS')
stop_words_models = stop_words
to_add_as_a_stop_word_in_models = ['model', 'models', 'modeling']
for word in to_add_as_a_stop_word_in_models:
    stop_words_models.add(word)
print('models_titles')
all_models_titles, most_frequent_models = most_frequent_word_by_group(models_titles, stop_words_models)
print(most_frequent_models)

# International Conference on Conceptual Modeling (ER)
er_titles = repoP.getTitlesFromNamedConference("ER' AND pg.title like 'Conceptual Modeling%")
stop_words_er = stop_words
to_add_as_a_stop_word_in_er = ['conceptual', 'modeling']
for word in to_add_as_a_stop_word_in_er:
    stop_words_er.add(word)
print('er_titles')
all_er_titles, most_frequent_er = most_frequent_word_by_group(er_titles, stop_words_er)
print(most_frequent_er)

# International Conference on Web Engineering (ICWE)
icwe_titles = repoP.getTitlesFromNamedConference("ICWE")
stop_words_icwe = stop_words
to_add_as_a_stop_word_in_icwe = ['web', 'engineering']
for word in to_add_as_a_stop_word_in_icwe:
    stop_words_icwe.add(word)
print('icwe_titles')
all_icwe_titles, most_frequent_icwe = most_frequent_word_by_group(icwe_titles, stop_words_icwe)
print(most_frequent_icwe)

# The Web Conference (WWW)
www_titles = repoP.getTitlesFromNamedConference("WWW")
stop_words_www = stop_words
to_add_as_a_stop_word_in_www = ['web']
for word in to_add_as_a_stop_word_in_www:
    stop_words_www.add(word)
print('www_titles')
all_www_titles, most_frequent_www = most_frequent_word_by_group(www_titles, stop_words_www)
print(most_frequent_www)

# International Conference on Model Transformation (ICMT)
icmt_titles = repoP.getTitlesFromNamedConference("ICMT")
stop_words_icmt = stop_words
to_add_as_a_stop_word_in_icmt = ['model', 'transformation', 'transformations']
for word in to_add_as_a_stop_word_in_icmt:
    stop_words_icmt.add(word)
print('icmt_titles')
all_icmt_titles, most_frequent_icmt = most_frequent_word_by_group(icmt_titles, stop_words_icmt)
print(most_frequent_icmt)

# International Working Conference on Exploring Modeling Methods for Systems Analysis and Development (EMMSAD)
emmsad_titles = repoP.getTitlesFromNamedConference("EMMSAD")
stop_words_emmsad = stop_words
to_add_as_a_stop_word_in_emmsad = ['exploring', 'modeling', 'methods', 'systems', 'analysis', 'development']
for word in to_add_as_a_stop_word_in_emmsad:
    stop_words_emmsad.add(word)
print('emmsad_titles')
all_emmsad_titles, most_frequent_emmsad = most_frequent_word_by_group(emmsad_titles, stop_words_emmsad)
print(most_frequent_emmsad)

# International Conference on Software Analysis, Evolution and Reengineering (SANER)
saner_titles = repoP.getTitlesFromNamedConference("SANER")
stop_words_saner = stop_words
to_add_as_a_stop_word_in_saner = ['software', 'analysis', 'evolution', 'reengineering', 'engineering']
for word in to_add_as_a_stop_word_in_saner:
    stop_words_saner.add(word)
print('saner_titles')
all_saner_titles, most_frequent_saner = most_frequent_word_by_group(saner_titles, stop_words_saner)
print(most_frequent_saner)

# Research Challenges in Information Science (RCIS)
rcis_titles = repoP.getTitlesFromNamedConference("RCIS")
stop_words_rcis = stop_words
to_add_as_a_stop_word_in_rcis = ['research', 'challenges', 'information', 'science']
for word in to_add_as_a_stop_word_in_rcis:
    stop_words_rcis.add(word)
print('rcis_titles')
all_rcis_titles, most_frequent_rcis = most_frequent_word_by_group(rcis_titles, stop_words_rcis)
print(most_frequent_rcis)

# International Conference on Mining Software Repositories (MSR)
msr_titles = repoP.getTitlesFromNamedConference("MSR")
stop_words_msr = stop_words
to_add_as_a_stop_word_in_msr = ['mining', 'software', 'repositories']
for word in to_add_as_a_stop_word_in_msr:
    stop_words_msr.add(word)
print('msr_titles')
all_msr_titles, most_frequent_msr = most_frequent_word_by_group(msr_titles, stop_words_msr)
print(most_frequent_msr)

# International Symposium on Empirical Software Engineering and Measurement (ESEM)
esem_titles = repoP.getTitlesFromNamedConference("ESEM")
stop_words_esem = stop_words
to_add_as_a_stop_word_in_esem = ['empirical', 'software', 'engineering', 'measurement']
for word in to_add_as_a_stop_word_in_esem:
    stop_words_esem.add(word)
print('esem_titles')
all_esem_titles, most_frequent_esem = most_frequent_word_by_group(esem_titles, stop_words_esem)
print(most_frequent_esem)

# Fundamental Approaches to Software Engineering (FASE)
fase_titles = repoP.getTitlesFromNamedConference("FASE")
stop_words_fase = stop_words
to_add_as_a_stop_word_in_fase = ['approaches', 'software', 'engineering']
for word in to_add_as_a_stop_word_in_fase:
    stop_words_fase.add(word)
print('fase_titles')
all_fase_titles, most_frequent_fase = most_frequent_word_by_group(fase_titles, stop_words_fase)
print(most_frequent_fase)

# ISymposium on Applied Computing (SAC)
sac_titles = repoP.getTitlesFromNamedConference("SAC")
stop_words_sac = stop_words
to_add_as_a_stop_word_in_sac = ['applied', 'computing']
for word in to_add_as_a_stop_word_in_sac:
    stop_words_sac.add(word)
print('sac_titles')
all_sac_titles, most_frequent_sac = most_frequent_word_by_group(sac_titles, stop_words_sac)
print(most_frequent_sac)





###       JOURNALS      #####
# Software and Systems Modeling (Softw. Syst. Model.)
ssm_titles = repoP.getTitlesFromJournal("Softw. Syst. Model.")
stop_words_ssm = stop_words
to_add_as_a_stop_word_in_ssm = ['systems', 'modeling']
for word in to_add_as_a_stop_word_in_ssm:
    stop_words_ssm.add(word)
print('ssm_titles')
all_ssm_titles, most_frequent_ssm = most_frequent_word_by_group(ssm_titles, stop_words_ssm)
print(most_frequent_ssm)

# IEEE Transactions on Software Engineering (TSE) (IEEE Trans. Software Eng.)
tse_titles = repoP.getTitlesFromJournal("IEEE Trans. Software Eng.")
stop_words_tse = stop_words
to_add_as_a_stop_word_in_tse = ['transactions', 'distributed']
for word in to_add_as_a_stop_word_in_tse:
    stop_words_tse.add(word)
print('tse_titles')
all_tse_titles, most_frequent_tse = most_frequent_word_by_group(tse_titles, stop_words_tse)
print(most_frequent_tse)

# ACM Transactions on Software Engineering and Methodology (TOSEM) (ACM Trans. Softw. Eng. Methodol.)
tosem_titles = repoP.getTitlesFromJournal("ACM Trans. Softw. Eng. Methodol.")
stop_words_tosem = stop_words
to_add_as_a_stop_word_in_tosem = ['transactions', 'software', 'engineering', 'methodology']
for word in to_add_as_a_stop_word_in_tosem:
    stop_words_tosem.add(word)
print('tosem_titles')
all_tosem_titles, most_frequent_tosem = most_frequent_word_by_group(tosem_titles, stop_words_tosem)
print(most_frequent_tosem)

# IEEE Software  (IEEE Softw.)
ieees_titles = repoP.getTitlesFromJournal("IEEE Softw.")
stop_words_ieees = stop_words
to_add_as_a_stop_word_in_ieees = ['software']
for word in to_add_as_a_stop_word_in_ieees:
    stop_words_ieees.add(word)
print('ieees_titles')
all_ieees_titles, most_frequent_ieees = most_frequent_word_by_group(ieees_titles, stop_words_ieees)
print(most_frequent_ieees)

# Communications of the ACM (Commun. ACM)
cacm_titles = repoP.getTitlesFromJournal("Commun. ACM")
stop_words_cacm = stop_words
to_add_as_a_stop_word_in_cacm = ['communications', 'acm']
for word in to_add_as_a_stop_word_in_cacm:
    stop_words_cacm.add(word)
print('cacm_titles')
all_cacm_titles, most_frequent_cacm = most_frequent_word_by_group(cacm_titles, stop_words_cacm)
print(most_frequent_cacm)

# Information & Software Technology (Inf. Softw. Technol.)
ist_titles = repoP.getTitlesFromJournal("Inf. Softw. Technol.")
stop_words_ist = stop_words
to_add_as_a_stop_word_in_ist = ['information', 'software', 'technology']
for word in to_add_as_a_stop_word_in_ist:
    stop_words_ist.add(word)
print('ist_titles')
all_ist_titles, most_frequent_ist = most_frequent_word_by_group(ist_titles, stop_words_ist)
print(most_frequent_ist)

# Empirical Software Engineering (Empir. Softw. Eng.)
ese_titles = repoP.getTitlesFromJournal("Empir. Softw. Eng.")
stop_words_ese = stop_words
to_add_as_a_stop_word_in_ese = ['empirical', 'software', 'engineering']
for word in to_add_as_a_stop_word_in_ese:
    stop_words_ese.add(word)
print('ese_titles')
all_ese_titles, most_frequent_ese = most_frequent_word_by_group(ese_titles, stop_words_ese)
print(most_frequent_ese)

# Journal of Object Technology  (J. Object Technol.)
jot_titles = repoP.getTitlesFromJournal("J. Object Technol.")
stop_words_jot = stop_words
to_add_as_a_stop_word_in_jot = ['object', 'technology']
for word in to_add_as_a_stop_word_in_jot:
    stop_words_jot.add(word)
print('jot_titles')
all_jot_titles, most_frequent_jot = most_frequent_word_by_group(jot_titles, stop_words_jot)
print(most_frequent_jot)

# Journal of Systems and Software (JSS)(J. Syst. Softw.)
jss_titles = repoP.getTitlesFromJournal("J. Syst. Softw.")
stop_words_jss = stop_words
to_add_as_a_stop_word_in_jss = ['systems', 'software']
for word in to_add_as_a_stop_word_in_jss:
    stop_words_jss.add(word)
print('jss_titles')
all_jss_titles, most_frequent_jss = most_frequent_word_by_group(jss_titles, stop_words_jss)
print(most_frequent_jss)


# All conferences

conferences_titles = (all_sle_titles + all_icse_titles + all_caise_titles + all_models_titles + all_er_titles +
                      all_icwe_titles + all_www_titles + all_icmt_titles + all_emmsad_titles + all_saner_titles +
                      all_rcis_titles + all_msr_titles + all_esem_titles + all_fase_titles + all_sac_titles)
most_frequent_words_all_c = most_frequent_word_all_together(conferences_titles)
print('Most frequent all titles CONFERENCES:')
print(most_frequent_words_all_c)

# All journals

journals_titles = (all_ssm_titles + all_tse_titles + all_tosem_titles + all_ieees_titles + all_cacm_titles +
                   all_ist_titles + all_ese_titles + all_jot_titles + all_jss_titles)
most_frequent_words_all_j = most_frequent_word_all_together(journals_titles)
print('Most frequent all titles JOURNALS:')
print(most_frequent_words_all_j)

all_titles = journals_titles + conferences_titles
most_frequent_words_all = most_frequent_word_all_together(all_titles)
print('Most frequent all titles TOTAL:')
print(most_frequent_words_all)


print('CONFERENCES: ', len(conferences_titles))
print('JOURNALS: ', len(journals_titles))
print('TOTAL: ', len(all_titles))

print('all_sle_titles: ', len(all_sle_titles))
print('all_icse_titles: ', len(all_icse_titles))
print('all_caise_titles: ', len(all_caise_titles))
print('all_models_titles: ', len(all_models_titles))
print('all_er_titles: ', len(all_er_titles))
print('all_icwe_titles: ', len(all_icwe_titles))
print('all_www_titles: ', len(all_www_titles))
print('all_icmt_titles: ', len(all_icmt_titles))
print('all_emmsad_titles: ', len(all_emmsad_titles))
print('all_saner_titles: ', len(all_saner_titles))
print('all_rcis_titles: ', len(all_rcis_titles))
print('all_msr_titles: ', len(all_msr_titles))
print('all_esem_titles: ', len(all_esem_titles))
print('all_fase_titles: ', len(all_fase_titles))
print('all_sac_titles: ', len(all_sac_titles))
print('all_ssm_titles: ', len(all_ssm_titles))
print('all_tse_titles: ', len(all_tse_titles))
print('all_tosem_titles: ', len(all_tosem_titles))
print('all_ieees_titles: ', len(all_ieees_titles))
print('all_cacm_titles: ', len(all_cacm_titles))
print('all_ist_titles: ', len(all_ist_titles))
print('all_ese_titles: ', len(all_ese_titles))
print('all_jot_titles: ', len(all_jot_titles))
print('all_jss_titles: ', len(all_jss_titles))


frequent_words = []
frequent_words_counting = []

## BAR PLOT ALL WORDS ##
for couple_word_freq in most_frequent_words_all:
    frequent_words.append(couple_word_freq[0])
    frequent_words_counting.append(couple_word_freq[1])

fig, ax = plt.subplots()
bar_container = ax.bar(frequent_words, frequent_words_counting)
ax.set(ylabel='occurrences', title='Most frequent words in titles (All Conferences and Journals)', ylim=(0, 3400))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.savefig('../data/plots/MostCommonWord/all-barplot.png')
plt.show()


## BAR PLOT CONFERENCES WORDS ## folder: MostCommonWord

frequent_words = []
frequent_words_counting = []
for couple_word_freq in most_frequent_words_all_c:
    frequent_words.append(couple_word_freq[0])
    frequent_words_counting.append(couple_word_freq[1])

fig, ax = plt.subplots()
bar_container = ax.bar(frequent_words, frequent_words_counting)
ax.set(ylabel='occurrences', title='Most frequent words in titles (Conferences) ', ylim=(0, 2000))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.savefig('../data/plots/MostCommonWord/conferences-barplot.png')
plt.show()

## BAR PLOT JOURNAL WORDS ##

frequent_words = []
frequent_words_counting = []
for couple_word_freq in most_frequent_words_all_j:
    frequent_words.append(couple_word_freq[0])
    frequent_words_counting.append(couple_word_freq[1])

fig, ax = plt.subplots()
bar_container = ax.bar(frequent_words, frequent_words_counting)
ax.set(ylabel='occurrences', title='Most frequent words in titles (Journals)', ylim=(0, 1500))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.savefig('../data/plots/MostCommonWord/journals-barplot.png')
plt.show()

## BAR PLOT SAC Conference WORDS ##

frequent_words = []
frequent_words_counting = []
for couple_word_freq in most_frequent_sac:
    frequent_words.append(couple_word_freq[0])
    frequent_words_counting.append(couple_word_freq[1])

fig, ax = plt.subplots()
bar_container = ax.bar(frequent_words, frequent_words_counting)
ax.set(ylabel='occurrences', title='Most frequent words in titles (ISymposium on Applied Computing)', ylim=(0, 800))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.savefig('../data/plots/MostCommonWord/sac-barplot.png')
plt.show()

## BAR PLOT CACM Journal WORDS ##

frequent_words = []
frequent_words_counting = []
for couple_word_freq in most_frequent_cacm:
    frequent_words.append(couple_word_freq[0])
    frequent_words_counting.append(couple_word_freq[1])

fig, ax = plt.subplots()
bar_container = ax.bar(frequent_words, frequent_words_counting)
ax.set(ylabel='occurrences', title='Most frequent words in titles (Communications of the ACM)', ylim=(0, 1200))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.savefig('../data/plots/MostCommonWord/cacm-barplot.png')
plt.show()