from uuid import uuid4
import xml.etree.ElementTree as ET
from model.PublicationVenueType import PublicationVenueType
from model.XmlKey import XmlKey

class DataBaseInserts():

    def __init__(self, alchemySession, errorLogger):
        self.session = alchemySession
        self.errorLogger = errorLogger

    def insertResearcher(self, item, repoResearcher, repoInst):
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        id = uuid4()
        names = []
        aff = []
        institutions = []
        urls = []
        crossRef = None
        errorInstitutions =[]

        for child in item.iter():
            if child.tag == "crossref":
                crossRef = child.text
            if child.tag == "author":
                if child.text not in names:
                    names.append(child.text)
            if child.tag == "url":
                urls.append(child.text)
            if child.tag == "note":
                if child.attrib.get('type') == "affiliation":
                    institutions.append(child.text)
                    inst = repoInst.getOneByName(child.text)
                    if inst is None:
                        inst = repoInst.insertInstitution(uuid4(), child.text)
                    if inst is not None:
                        aff.append(inst)
                    else:
                        errorInstitutions.append(child.text)

        if len(errorInstitutions) > 0:
            self.errorLogger.startObjectList('institution-not-found')
            for institution in errorInstitutions:
                self.errorLogger.addItemErrorLogger('<institution-error>%s</institution-error>' % institution)
            self.errorLogger.addItemErrorLogger(xmlItem)
            self.errorLogger.endObjectList('institution-not-found')

        if crossRef is not None:
            return {"r_key": key, "r_cross_ref": crossRef}
        name = key
        if len(names) > 0:
            name = names[0]
        researcher = repoResearcher.insertResearcher(id, name, 0, urls, key, mdate, xmlItem, names, aff)
        return {"researcher": researcher}


    def insertKeyFromCrossRefResearchers(self, key, crosRef, item, repoResercher, errorLog):
        r = repoResercher.getOneByXmlKey(key)
        if r is not None:
            r.xml_cross_reference.append(XmlKey(researcher_id=r.id, xml_key=crosRef))
            repoResercher.updateResearcher(r)
        else:
            errorLog.addItemErrorLogger(item)

    def insertPublicationFromXML(self, item, repoP, repoPG, repoPV, repoR):
        key = item.attrib.get('key')
        mdate = item.attrib.get('mdate')
        xmlItem = ET.tostring(item)
        id = uuid4()
        type = item.tag if item.tag == 'book' else None
        title = None
        year = None
        pages = None
        booktitle = None
        series = None
        crossref = None
        ee = []
        authors = {}
        numAuthors = 1
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
                crossref = child.text
            if child.tag == 'booktitle':
                booktitle = child.text
            if child.tag == 'series':
                series = child.text

        publication = repoP.insertPublication(id, title, year, pages, type, key, mdate, xmlItem, ee)
        errorAuthors = []

        for author in authors:
            researcher = repoR.getOneByName(author)
            if researcher is not None:
                if researcher.last_year_current_alias < publication.year:
                    researcher.updateCurrentAlias(author, publication.year)
                if authors[author]['orcid'] is not None and researcher.orcid is None:
                    researcher.addOrcid(authors[author]['orcid'])
                repoP.addAuthorship(publication, researcher, authors[author]['position'])
            else:
                errorAuthors.append(author)

        if len(errorAuthors) > 0:
            self.errorLogger.startObjectList('authors-not-found')
            for author in errorAuthors:
                self.errorLogger.addItemErrorLogger('<author-error>%s</author-error>' % author)
            self.errorLogger.addItemErrorLogger(xmlItem)
            self.errorLogger.endObjectList('authors-not-found')

        if crossref is not None and crossref != key:
            pGroup = repoPG.findByXmlKey(crossref)
            if pGroup is not None:
                repoPG.addPublicationIntoPublicationGroup(pGroup, publication)

        if booktitle is not None and series is not None:
            if booktitle != title and series != title and booktitle != series:
                pGroup = repoPG.findByTitle(booktitle)
                if pGroup is None:
                    pGroup = repoPG.insertPublicationGroup(uuid4(), booktitle, None, year, None,  None, series, None,
                                                           None, None, None, None, xmlItem, None)
                repoPG.addPublicationIntoPublicationGroup(pGroup, publication)
                pVenue = repoPV.findByName(series)
                if pVenue is None:
                    pVenue = repoPV.insertPublicationVenue(uuid4(), series, PublicationVenueType.book, pGroup)
                repoPV.addPublicationGroupInVenue(pVenue, pGroup)
                return {'publication': publication, 'publication_group': pGroup, 'publication_venue': pVenue}
            if booktitle != title or series != title:
                pGroupTitle = booktitle if booktitle != title else series
                pGroup = repoPG.findByTitle(pGroupTitle)
                if pGroup is None:
                    pGroup = repoPG.insertPublicationGroup(uuid4(), pGroupTitle, None, year, None, None, series, None,
                                                           None, None, None, None, xmlItem, None)
                repoPG.addPublicationIntoPublicationGroup(pGroup, publication)
                return {'publication': publication, 'publication_group': pGroup}
        if booktitle is not None and booktitle != title:
            pGroup = repoPG.findByTitle(booktitle)
            if pGroup is None:
                pGroup = repoPG.insertPublicationGroup(uuid4(), booktitle, None, year, None, None, None, None,
                                                       None, None, None, None, xmlItem, None)
            repoPG.addPublicationIntoPublicationGroup(pGroup, publication)
            return {'publication': publication, 'publication_group': pGroup}
        if series is not None and series != title:
            pGroup = repoPG.findByTitle(series)
            if pGroup is None:
                pGroup = repoPG.insertPublicationGroup(uuid4(), series, None, year, None, None, None, None,
                                                       None, None, None, None, xmlItem, None)
            repoPG.addPublicationIntoPublicationGroup(pGroup, publication)
            return {'publication': publication, 'publication_group': pGroup}

        return {'publication': publication}

    def insertPublicationGroupFromXml(self, item, repoPG, repoPV, repoR):
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
        pVenue = None
        editors = []
        ee = []
        for child in item.iter():
            if child.tag == "editor" and child.text not in editors:
                editors.append(child.text)
            if child.tag == "title":
                title = child.text
            if child.tag == "publisher":
                publisher = child.text
            if child.tag == "year" and child.text is not None:
                year = int(child.text)
            if child.tag == "isbn":
                isbn = child.text
            if child.tag == "booktitle":
                booktitle = child.text
            if child.tag == "serie":
                serie = child.text
            if child.tag == "volume":
                volume = child.text
            if child.tag == "number":
                number = child.text
            if child.tag == 'ee':
                ee.append(child.text)

        keySplited = xmlKey.split('/')
        researchers = []
        errorEditors = []
        for editor in editors:
            researcher = repoR.getOneByName(editor)
            if researcher is None:
                errorEditors.append(editor)
            else:
                if researcher.last_year_current_alias < year:
                    researcher.updateCurrentAlias(editor, year)
                if researcher not in researchers:
                    researchers.append(researcher)

        if len(errorEditors) > 0:
            self.errorLogger.startObjectList('authors-not-found')
            for author in errorEditors:
                self.errorLogger.addItemErrorLogger('<author-error>%s</author-error>' % author)
            self.errorLogger.addItemErrorLogger(xmlItem)
            self.errorLogger.endObjectList('authors-not-found')

        pGroup = repoPG.insertPublicationGroup(uuid, title, publisher, year, isbn,  booktitle, serie, volume, number, ee, xmlKey, xmlMdate, xmlItem, researchers)

        if keySplited[0] == 'conf' or keySplited[0] == 'journals' or serie is not None:
            venueName = serie if serie is not None else keySplited[1]
            pVenue = repoPV.findByName(venueName)
            if pVenue is None:
                if serie is None:
                    venueType = PublicationVenueType.conference if keySplited[0] == 'conf' else PublicationVenueType.journal
                else:
                    venueType = PublicationVenueType.book
                pVenue = repoPV.insertPublicationVenue(uuid4(), venueName, venueType, pGroup)
            else:
                repoPV.addPublicationGroupInVenue(pVenue, pGroup)

        return {'publication_group': pGroup, 'publication_venue': pVenue}
