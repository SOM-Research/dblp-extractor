from uuid import uuid4
import xml.etree.ElementTree as ET
from model.XmlKey import XmlKey

class DataBaseInserts():

    def __init__(self, alchemySession):
        self.session = alchemySession

    def insertResearcher(self, item, repoResearcher, repoInst):
        institutionNotSaved = 0
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        id = uuid4()
        names = []
        aff = []
        institutions = []
        crossRef = None
        for child in item.iter():
            if child.tag == "crossref":
                crossRef = child.text
            if child.tag == "author":
                if child.text not in names:
                    names.append(child.text)
            if child.tag == "note":
                if child.attrib.get('type') == "affiliation":
                    institutions.append(child.text)
                    inst = repoInst.getOneByName(child.text)
                    if inst is None:
                        inst = repoInst.insertInstitution(uuid4(), child.text)
                    if inst is not None:
                        aff.append(inst)
                    else:
                        institutionNotSaved += 1
                        print("Intsitution not saved: ", child.text)
                        print("Total institutions not saved: ", institutionNotSaved)
        if crossRef is not None:
            return {"r_key": key, "r_cross_ref": crossRef}


        name = key
        if len(names) > 0:
            name = names[0]
        try:
            researcher = repoResearcher.insertResearcher(id, name, key, mdate, xmlItem, names, aff)
            return {"researcher": researcher}
        except:
            print("Error insert research -> id: ", id, " | name: ", name, " | key: ", key)

    def insertKeyFromCrossRef(self, key, crosRef, repoResercher):
        r = repoResercher.getOneByXmlKey(key)
        r.xml_cross_reference.append(XmlKey(researcher_id=r.id, xml_key=crosRef))
        repoResercher.updateResearcher(r)
