import argparse
import os

import xml.etree.ElementTree as ET
import Parser
import time

from database.DataBaseConnection import DataBaseConnection
from database.orm.InstitutionRepository import InstitutionRepository
from database.orm.ResearcherRepository import ResearcherRepository
from extractor.DataBaseInserts import DataBaseInserts

def rawData(file):
    xml = open(file)
    tree = ET.parse(xml, Parser.parser())
    xml.close()
    return tree

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

def inserts(tree, dbInserts, repoR, repoI):
    rCrossRef = {}
    for item in tree.getroot():
        if item.tag == "www":
            result = dbInserts.insertResearcher(item, repoR, repoI)
            if result is not None and len(result) == 2:
                rCrossRef[result["r_cross_ref"]] = result["r_key"]
        item.clear()

    print("Totals:")
    for key in rCrossRef:
        dbInserts.insertKeyFromCrossRef(key, rCrossRef[key], repoR)



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

cwd = os.getcwd()
print(cwd)

session = dbConnection.alchemySession()
repoR = ResearcherRepository(session)
repoI = InstitutionRepository(session)

dbInserts = DataBaseInserts(session)

if args.xml is not None:
    tree = rawData(args.xml)
    if args.splitXml is True:
        splitXml(tree)
    if args.insert is True:
        inserts(tree, dbInserts, repoR, repoI)


print('TIME: ', time.time() - strTime)