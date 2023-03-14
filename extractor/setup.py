import argparse
import xml.etree.ElementTree as ET
import Parser
import time
from database.DataBaseConnection import DataBaseConnection
from database.orm.InstitutionRepository import InstitutionRepository
from database.orm.PublicationRepository import PublicationRepository
from database.orm.ResearcherRepository import ResearcherRepository
from database.orm.PublicationGroupRepository import PublicationGroupRepository
from extractor.DataBaseInserts import DataBaseInserts
from extractor.ErrorLogger import ErrorLogger


def rawData(file):
    xml = open(file)
    tree = ET.parse(xml, Parser.parser())
    xml.close()
    return tree

def iterParseData(file, repoR, repoI, errorLog):
    rCrossRef = {}
    xml = open(file)
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'start':
            if item.tag == "www":
                result = dbInserts.insertResearcher(item, repoR, repoI)
                if "r_cross_ref" in result:
                    rCrossRef[result["r_cross_ref"]] = {'crossref': result["r_key"], 'item': ET.tostring(item)}
            item.clear()

    print("Totals:")
    errorLog.startObjectList('crossref')
    for key in rCrossRef:
        dbInserts.insertKeyFromCrossRef(key, rCrossRef[key]['crossref'], rCrossRef[key]['item'], repoR, errorLog)
    errorLog.endObjectList('crossref')

def splitXml(tree):
    baseFilesPath = './data/split_%s.xml'
    xmlFiles = {}
    for item in tree.getroot():
        if item.tag not in xmlFiles:
            xmlFiles[item.tag] = open(baseFilesPath % item.tag, 'wb')
            xmlFiles[item.tag].write(bytes('<list>\n', 'ascii'))
        xmlFiles[item.tag].write(ET.tostring(item))
        xmlFiles[item.tag].write(bytes('\n', 'ascii'))
        item.clear()
    for file in xmlFiles:
        file.write(bytes('</list>', 'ascii'))
        file.close()

def inserts(tree, dbInserts, repoR, repoI, repoP, repoPG):
    rCrossRef = {}
    articleResoults = []
    for item in tree.getroot():
        if item.tag == "www":
            result = dbInserts.insertResearcher(item, repoR, repoI)
            if result is not None and len(result) == 2:
                rCrossRef[result["r_cross_ref"]] = result["r_key"]
        if item.tag == "article":
            result = dbInserts.insertPublicationsAsArticle(item, repoP)
            articleResoults.append(result)
        if item.tag == "inproceedings":
            result = dbInserts.insertPublicationInConf(item, repoP)
            articleResoults.append(result)
        if item.tag == "book" or item.tag == "proceedings":
            dbInserts.insertPublicationGroupFromXml(item, repoPG)
        item.clear()

    print("Totals:")
    for key in rCrossRef:
        dbInserts.insertKeyFromCrossRef(key, rCrossRef[key], repoR)
    for authorship in articleResoults:
        dbInserts.relatePublicationsWithAuthors(authorship['publication'], authorship['authorship'], repoR)
        if authorship['publication_group']['has'] == True:
            if 'journal' in authorship['publication_group']:
                pGroupTitle = authorship['publication_group']['journal']
                if 'volume' in authorship['publication_group']:
                    pGroup = repoPG.findByTitleAndVolume(pGroupTitle, authorship['publication_group']['volume'])
                else:
                    pGroup = repoPG.findByTitle(pGroupTitle)
                if pGroup is None:
                    pGroup = dbInserts.insertPublicationsGroupFromArticleResoult(authorship['publication_group'], repoPG)



###             ###
#   Arguments     #
###             ###

parser = argparse.ArgumentParser(description='Setup environment')
parser.add_argument('--ddl', type=str, help='File path for DDL')
parser.add_argument('--xml', type=str, help='File path for xml raw data')
parser.add_argument('--splitXml', type=bool, help='Set True if want to split XML by main tags')
parser.add_argument('--insert', type=bool, help='Insert the xml data into database')
args = parser.parse_args()

strTime = time.time()

dbConnection = DataBaseConnection()
if args.ddl is not None:
    dbConnection.createDatabaseFromDDL(args.ddl)

session = dbConnection.alchemySession()
repoR = ResearcherRepository(session)
repoI = InstitutionRepository(session)
repoP = PublicationRepository(session)
repoPG = PublicationGroupRepository(session)

dbInserts = DataBaseInserts(session)

errorLog = ErrorLogger()
errorLog.startObjectList('errorlist')

iterParseData(args.xml, repoR, repoI, errorLog)

errorLog.endObjectList('errorlist')

#if args.xml is not None:
#    tree = rawData(args.xml)
#    if args.splitXml is True:
#        splitXml(tree)
#    if args.insert is True:
#        inserts(tree, dbInserts, repoR, repoI)


print('TIME: ', time.time() - strTime)