import xml.etree.ElementTree as ET
import Parser
import time
from database.orm.InstitutionRepository import InstitutionRepository
from database.orm.ResearcherRepository import ResearcherRepository
from extractor.DataBaseConnection import DataBaseConnection
from extractor.DataBaseInserts import DataBaseInsterts

def rawData(file):
    xml = open(file)
    tree = ET.parse(xml, Parser.parser())
    xml.close()
    return tree

def instertsResearchers(tree, dbInserts, repoR, repoI):
    rCrossRef = {}
    for item in tree.getroot():
        if item.tag == "www":
            result = dbInserts.insertResearcher(item, repoR, repoI)
            if result is not None and len(result) == 2:
                rCrossRef[result["r_cross_ref"]] = result["r_key"]

    print("Totals:")
    for key in rCrossRef:
        dbInserts.insertKeyFromCrossRef(key, rCrossRef[key], repoR)



strTime = time.time()

dbConnection = DataBaseConnection()
dbConnection.createDatabaseFromDDL()
session = dbConnection.alchemySession()
repoR = ResearcherRepository(session)
repoI = InstitutionRepository(session)

dbInserts = DataBaseInsterts(session)

tree = rawData(dbConnection.config()['db']['raw_data_path'])

instertsResearchers(tree, dbInserts, repoR, repoI)


print('TIME: ', time.time() - strTime)