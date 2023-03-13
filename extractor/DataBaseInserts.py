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

    def insertPublicationsAsArticle(self, item, repoPublication):
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        id = uuid4()
        title = None
        year = None
        pages = None
        ee = []
        authors = {}
        numAuthors = 1
        pubGroup = {}
        for child in item.iter():
            if child.tag == 'author':
                authors[child.text] = {'position': numAuthors, 'orcid': child.attrib.get('orcid')}
                numAuthors += 1
            if child.tag == 'title':
                title = child.text
            if child.tag == 'year':
                year = int(child.text)
            if child.tag == 'pages':
                pages = child.text
            if child.tag == 'ee':
                ee.append(child.text)
            if child.tag == 'journal':
                pubGroup['has'] = True
                pubGroup['type'] = child.tag
                pubGroup[child.tag] = child.text
            if child.tag == 'year':
                pubGroup[child.tag] = int(child.text)
            if child.tag == 'volume':
                pubGroup[child.tag] = int(child.text)

        try:
            publication = repoPublication.insertPublication(id, title, year, pages, key, mdate, xmlItem, ee)
            return {"publication": publication, "authorship": authors, 'publication_group': pubGroup}
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

    def insertPublicationInConf(self, item, repoP):
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        id = uuid4()
        title = None
        year = None
        pages = None
        ee = []
        authors = {}
        numAuthors = 1
        pubGroup = {}
        for child in item.iter():
            if child.tag == 'author':
                authors[child.text] = {'position': numAuthors, 'orcid': child.attrib.get('orcid')}
                numAuthors += 1
            if child.tag == 'title':
                title = child.text
            if child.tag == 'year':
                year = int(child.text)
            if child.tag == 'pages':
                pages = child.text
            if child.tag == 'ee':
                ee.append(child.text)
            if child.tag == 'crossref':
                pubGroup['has'] = True
                pubGroup[child.tag] = child.text
            if child.tag == 'booktitle':
                pubGroup['has'] = True
                pubGroup[child.tag] = child.text
        try:
            publication = repoP.insertPublication(id, title, year, pages, key, mdate, xmlItem, ee)
            return {"publication": publication, "authorship": authors, 'publication_group': pubGroup}
        except:
            print("Error insert publication -> id: ", id, " | title: ", title, " | key: ", key)


    def insertPublicationGroupFromXml(self, item, repoPG):
        uuid = uuid4()
        title = None
        publisher = None
        year = None
        isbn = None
        booktitle = None
        serie = None
        volume = None
        number = None
        xmlKey = item.attrib.get('key')
        xmlMdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        for child in item.iter():
            if child.tag == "title":
                title = child.text
            if child.tag == "publisher":
                publisher = child.text
            if child.tag == "year":
                year = int(child.text)
            if child.tag == "isbn":
                isbn = child.text
            if child.tag == "booktitle":
                booktitle = child.text
            if child.tag == "serie":
                serie = child.text
            if child.tag == "volume":
                volume = int(child.text)
            if child.tag == "number":
                number = child.text

        return repoPG.insertPublicationGroup(uuid, title, publisher, year, isbn,  booktitle, serie, volume, number, xmlKey, xmlMdate, xmlItem)


    def insertPublicationsGroupFromArticleResoult(self, data, repoPG):
        uuid = uuid4()
        title = data[data['type']]
        year = None
        volume = None
        if 'year' in data:
            year = data['year']
        if 'volume' in data:
            volume = data['volume']
        repoPG.insertPublicationGroup(uuid, title, None, year, None, None, None, volume, None, None, None, None)
