from uuid import uuid4
import xml.etree.ElementTree as ET
from model.Publication import PublicationType
from model.Authorship import Authorship
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
        orcid = None
        crossRef = None

        for child in item.iter():
            if child.tag == "crossref":
                crossRef = child.text
            if child.tag == "author":
                if child.text not in names:
                    names.append(child.text)
            if child.tag == "url":
                orcid = child.text
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
            researcher = repoResearcher.insertResearcher(id, name, orcid, key, mdate, xmlItem, names, aff)
            return {"researcher": researcher}
        except:
            print("Error insert research -> id: ", id, " | name: ", name, " | key: ", key)

    def insertKeyFromCrossRef(self, key, crosRef, repoResercher):
        r = repoResercher.getOneByXmlKey(key)
        r.xml_cross_reference.append(XmlKey(researcher_id=r.id, xml_key=crosRef))
        repoResercher.updateResearcher(r)

    def insertPublications(self, item, repoPublication):
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        title = ""
        year = 0
        pages = ""
        id = uuid4()
        ee = []
        authors = {}
        numAuthors = 1
        for child in item.iter():
            if child.tag == "author":
                authors[child.text] = {'position': numAuthors, 'orcid': child.attrib.get('orcid')}
                numAuthors += 1
            if child.tag == "title":
                title = child.text
            if child.tag == "year":
                year = int(child.text)
            if child.tag == "pages":
                pages = child.text
            if child.tag == "ee":
                ee.append(child.text)

        try:
            publication = repoPublication.insertPublication(id, PublicationType.article, title, year, "doi", pages, key, mdate, xmlItem, ee)
            return {"publication": publication, "authorship": authors}
        except:
            print("Error insert publication -> id: ", id, " | title: ", title, " | key: ", key)

    def relatePublicationsWithAuthors(self, publication, authors, repoResercher):
        if publication is not None:
            for author in authors:
                researcher = repoResercher.getOneByName(author)
                if researcher is not None:
                    if authors[author]['orcid'] is not None and researcher.orcid is None:
                        researcher.addOrcid(authors[author]['orcid'])
                    researcher.publications.append(Authorship(researcher=researcher, publication=publication, position=authors[author]['position']))
                    repoResercher.updateResearcher(researcher)
                else:
                    print('Author %s not in DB' % author)
