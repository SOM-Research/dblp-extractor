import argparse
import xml.etree.ElementTree as ET
import Parser
import time
import sys
from datetime import date
import os
from database.DataBaseConnection import DataBaseConnection
from database.orm.InstitutionRepository import InstitutionRepository
from database.orm.PublicationRepository import PublicationRepository
from database.orm.PublicationVenueRepository import PublicationVenueRepository
from database.orm.ResearcherRepository import ResearcherRepository
from database.orm.PublicationGroupRepository import PublicationGroupRepository
from extractor.DataBaseInserts import DataBaseInserts
from extractor.ErrorLogger import ErrorLogger

###  SPLIT XML FILE ###
def splitXmlFile(file):
    xml = open(file, 'r')
    baseFilesPath = './data/split_%s_'+str(date.today())+'.xml'
    xmlFiles = {"article": None, "book": None, "incollection": None, "inproceedings": None, "mastersthesis": None, "phdthesis": None, "proceedings": None, "www": None}
    for xmlF in xmlFiles:
        xmlFiles[xmlF] = open(baseFilesPath % xmlF, 'wb')
        xmlFiles[xmlF].write(bytes('<list>\n', 'ascii'))
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'end':
            if item.tag in xmlFiles:
                xmlFiles[item.tag].write(ET.tostring(item))
                xmlFiles[item.tag].write(bytes('\n', 'ascii'))
                item.clear()
    for splitFile in xmlFiles:
        xmlFiles[splitFile].write(bytes('</list>', 'ascii'))
        xmlFiles[splitFile].close()
    xml.close()

### INSERT RESEARCHERS - WWW XML ITEM ###
def insertResearchers(file, dbInserts, repoR, repoI, errorLog):
    xml = open(file, 'r')
    rCrossRef = {}
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'end':
            if item.tag == 'www':
                try:
                    result = dbInserts.insertResearcher(item, repoR, repoI)
                    if result is not None and 'r_cross_ref' in result and 'r_key' in result:
                        rCrossRef[result["r_cross_ref"]] = {'crossref': result["r_key"], 'item': ET.tostring(item)}
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    errorLog.exceptionObject(exc_type.__name__, exc_value, exc_traceback)
                    errorLog.addItemErrorLogger(ET.tostring(item))
                item.clear()
    xml.close()
    errorLog.startObjectList('crossref-researchers')
    for key in rCrossRef:
        dbInserts.insertKeyFromCrossRefResearchers(key, rCrossRef[key]['crossref'], rCrossRef[key]['item'], repoR, errorLog)
    errorLog.endObjectList('crossref-researchers')

### INSERT PUBLICATION GROUP - PROCEEDINGS XML ITEM ###
def insertPublicationGroupsFromProceedings(file, dbInserts, repoR, repoPG, repoPV, errorLog):
    xml = open(file, 'r')
    rCrossRef = {}
    pubResult = None
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'end':
            if item.tag == 'proceedings':
                try:
                    result = dbInserts.insertPublicationGroupFromXml(item, repoPG, repoPV, repoR)
                    if result is not None and "r_cross_ref" in result:
                        rCrossRef[result["r_cross_ref"]] = {'crossref': result["r_key"], 'item': ET.tostring(item)}
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    errorLog.exceptionObject(exc_type.__name__, exc_value, exc_traceback)
                    errorLog.addItemErrorLogger(ET.tostring(item))
                item.clear()
    xml.close()

### INSERT PUBLICATIONS AND PUBLICATION GROUPS - BOOK XML ITEM ###
def insertPublicationsAndPublicationGroupsFromBook(file, dbInserts, repoP, repoPG, repoPV, repoR, errorLog):
    xml = open(file, 'r')
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'end':
            if item.tag == 'book':
                childType = None
                for child in item.iter():
                    # Could be more than one editor or author; but never editors AND authors are mixed.
                    if childType is None:
                        if child.tag == "editor":
                            childType = child.tag
                        if child.tag == "author":
                            childType = child.tag
                try:
                    if childType == "editor":
                        result = dbInserts.insertPublicationGroupFromXml(item, repoPG, repoPV, repoR)
                    if childType == "author":
                        pubResult = dbInserts.insertPublicationFromXML(item, repoP, repoPG, repoPV, repoR)
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    errorLog.exceptionObject(exc_type.__name__, exc_value, exc_traceback)
                    errorLog.addItemErrorLogger(ET.tostring(item))
                item.clear()
    xml.close()

### INSERT PUBLICATIONS - ARTICLE INCOLLECTION INPROCEEDINGS MASTERTHESIS AND PHDTHESIS XML ITEM ###
def insertPublications(file, dbInserts, repoP, repoPG, repoPV, repoR, errorLog):
    xml = open(file, 'r')
    for event, item in ET.iterparse(xml, ["start", "end"], parser=Parser.parser()):
        if event == 'end':
            if item.tag == 'article' \
                    or item.tag == 'incollection'\
                    or item.tag == 'inproceedings'\
                    or item.tag == 'mastersthesis'\
                    or item.tag == 'phdthesis':
                try:
                    pubResult = dbInserts.insertPublicationFromXML(item, repoP, repoPG, repoPV, repoR)
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    errorLog.exceptionObject(exc_type.__name__, exc_value, exc_traceback)
                    errorLog.addItemErrorLogger(ET.tostring(item))
                item.clear()
    xml.close()

### FIND SPLITED XML FILES ###
def getSplitXmlFiles():
    dataPath = './data/'
    files = [f for f in os.listdir(dataPath) if os.path.isfile(os.path.join(dataPath, f)) and (f.startswith('split_') and f.endswith('.xml'))]
    if len(files) > 0:
        dates = [f.split('_')[2].split('.')[0] for f in files]
        recent = max(dates)
        xmlFiles = [f for f in files if (f.split('_')[2].split('.')[0]) == recent]
        dictFiles = {}
        for file in xmlFiles:
            dictFiles[file.split('_')[1]] = file
        return dictFiles
    return None

def main():
    ###             ###
    #   Arguments     #
    ###             ###
    parser = argparse.ArgumentParser(description='Setup environment')
    parser.add_argument('--ddl', type=str, help='File path for DDL')
    parser.add_argument('--xml', type=str, help='File path for xml raw data')
    parser.add_argument('--splitXml', type=bool, help='Set True if want to split XML by main tags')
    parser.add_argument('--insert', type=bool, help='Insert the xml data into database')
    parser.add_argument('--skip', nargs='*', help='Skip a kind of data. Options: ["article", "book", "incollection", "inproceedings", "mastersthesis", "phdthesis", "proceedings", "www"]')
    args = parser.parse_args()

    strTime = time.time()

    ###  SPLIT PROCESS  ###
    print('Split')
    if args.xml is not None and args.splitXml is True:
        print('Start split')
        splitXmlFile(args.xml)

    ###  CREATE DATABASE ###
    print('Create DB')
    dbConnection = DataBaseConnection()
    if args.ddl is not None:
        print('Start Create DB')
        dbConnection.createDatabaseFromDDL(args.ddl)

    ###  INSERTS  ###
    print('Inserts')
    # find the split xml
    xmlFiles = getSplitXmlFiles()

    # start a session instance
    session = dbConnection.alchemySession()

    # instances of data repositories
    repoR = ResearcherRepository(session)
    repoI = InstitutionRepository(session)
    repoP = PublicationRepository(session)
    repoPG = PublicationGroupRepository(session)
    repoPV = PublicationVenueRepository(session)

    errorLog = ErrorLogger()
    dbInserts = DataBaseInserts(session, errorLog)

    # start error logger
    errorLog.startObjectList('errorlist')
    if args.skip is None:
        args.skip = []

    if xmlFiles is not None:
        # Researchers
        if "www" not in args.skip:
            print('./data/'+xmlFiles['www'])
            insertResearchers('./data/'+xmlFiles['www'], dbInserts, repoR, repoI, errorLog)
        # Publication groups
        if "proceedings" not in args.skip:
            print('./data/'+xmlFiles['proceedings'])
            insertPublicationGroupsFromProceedings('./data/'+xmlFiles['proceedings'], dbInserts, repoR, repoPG, repoPV, errorLog)
        # Publication groups and publications
        if "book" not in args.skip:
            print('./data/'+xmlFiles['book'])
            insertPublicationsAndPublicationGroupsFromBook('./data/'+xmlFiles['book'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)
        # Publications
        if "inproceedings" not in args.skip:
            print('./data/'+xmlFiles['inproceedings'])
            insertPublications('./data/'+xmlFiles['inproceedings'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)
        # Publications
        if "incollection" not in args.skip:
            print('./data/'+xmlFiles['incollection'])
            insertPublications('./data/'+xmlFiles['incollection'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)
        # Publications
        if "mastersthesis" not in args.skip:
            print('./data/'+xmlFiles['mastersthesis'])
            insertPublications('./data/'+xmlFiles['mastersthesis'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)
        # Publications
        if "phdthesis" not in args.skip:
            print('./data/'+xmlFiles['phdthesis'])
            insertPublications('./data/'+xmlFiles['phdthesis'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)
        # Publications
        if "article" not in args.skip:
            print('./data/'+xmlFiles['article'])
            insertPublications('./data/'+xmlFiles['article'], dbInserts, repoP, repoPG, repoPV, repoR, errorLog)

    # end error logger
    errorLog.endObjectList('errorlist')

    print('TIME: ', time.time() - strTime)

if __name__ == "__main__":
    main()