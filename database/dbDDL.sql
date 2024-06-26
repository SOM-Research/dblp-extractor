DROP DATABASE IF EXISTS metascience;

CREATE DATABASE metascience;

\c metascience;

CREATE EXTENSION pg_trgm;

CREATE TABLE oid_xml (
    oid INT PRIMARY KEY,
    xml varchar(255),
    created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE researchers (
    uuid UUID PRIMARY KEY,
    current_alias varchar(255),
    names TEXT[],
    last_year_current_alias int default 0,
    orcid varchar(255),
    crossref varchar(255),
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_tag varchar(255),
    xml_item TEXT
);

CREATE INDEX researcher_names_index ON researchers(names);
CREATE INDEX researcher_xml_key_index ON researchers(xml_key);
CREATE INDEX researcher_xml_tag_index ON researchers(xml_tag);
CREATE INDEX researcher_xml_mdate_index ON researchers(xml_mdate);

-- ALTER TABLE researcher_names CHARACTER SET utf8 COLLATE utf8_bin;
-- ALTER TABLE researcher_names CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;

CREATE TYPE publication_venues_type as ENUM ('journal', 'conference', 'book', 'workshop', 'unknown');

CREATE TABLE publication_venues(
    uuid UUID PRIMARY KEY,
    name VARCHAR(255),
    type publication_venues_type
);

ALTER TABLE publication_venues ADD CONSTRAINT publication_venues_name_unique UNIQUE (name);
CREATE INDEX p_venue_names_index ON publication_venues(name);

CREATE TABLE publication_groups(
    uuid UUID PRIMARY KEY,
    title TEXT,
    editors TEXT[],
    publication_venue UUID,
    publisher varchar(255),
    year int,
    isbn TEXT[],
    doi varchar (255),
    crossref varchar (255),
    booktitle TEXT,
    serie varchar(255),
    volume varchar(255),
    number varchar(255),
    electronic_edition TEXT[],
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_tag varchar(255),
    xml_item TEXT,
    FOREIGN KEY (publication_venue) REFERENCES publication_venues(uuid)
);

CREATE INDEX p_group_title_index ON publication_groups(title);
CREATE INDEX p_group_editors_index ON publication_groups(editors);
CREATE INDEX p_group_xml_key_index ON publication_groups(xml_key);
CREATE INDEX p_group_xml_tag_index ON publication_groups(xml_tag);
CREATE INDEX p_group_xml_mdate_index ON publication_groups(xml_mdate);

CREATE TYPE publications_type as ENUM ('journal','thesis', 'conference', 'workshop', 'book', 'unknown');
CREATE TABLE publications(
    uuid UUID PRIMARY KEY,
    type publications_type,
    publication_group_uuid UUID,
    title TEXT,
    authors TEXT[],
    year int,
    doi TEXT,
    journal varchar(255),
    crossref TEXT,
    pages TEXT,
    num_pages int,
    electronic_edition TEXT[],
    is_corrigendum BOOLEAN DEFAULT FALSE,
    corrigendum_of UUID DEFAULT NULL,
    xml_key TEXT,
    xml_mdate DATE,
    xml_tag varchar(255),
    xml_item TEXT,
    FOREIGN KEY (publication_group_uuid) REFERENCES publication_groups(uuid)
);
CREATE INDEX publication_type_index ON publications(type);
CREATE INDEX publication_title_index ON publications(title);
CREATE INDEX publication_xml_key_index ON publications(xml_key);
CREATE INDEX publication_xml_tag_index ON publications(xml_tag);
CREATE INDEX publication_xml_mdate_index ON publications(xml_mdate);

CREATE TABLE authorships(
    researcher_uuid UUID,
    publication_uuid UUID,
    position int,
    CONSTRAINT PK_authorships PRIMARY KEY (researcher_uuid,publication_uuid, position),
    FOREIGN KEY (researcher_uuid) REFERENCES researchers(uuid),
    FOREIGN KEY (publication_uuid) REFERENCES publications(uuid)
);

CREATE TABLE editors(
    researcher_uuid UUID,
    publication_group_uuid UUID,
    position int,
    CONSTRAINT PK_editorships PRIMARY KEY (researcher_uuid,publication_group_uuid),
    FOREIGN KEY (researcher_uuid) REFERENCES researchers(uuid),
    FOREIGN KEY (publication_group_uuid) REFERENCES publication_groups(uuid)
);

CREATE TABLE institutions(
    uuid UUID PRIMARY KEY,
    name TEXT,
    version_names TEXT[],
    country TEXT
);

ALTER TABLE institutions ADD CONSTRAINT institutions_name_unique UNIQUE (name);
CREATE INDEX institutions_name_index ON institutions USING gist (name gist_trgm_ops);

CREATE TABLE affiliations(
    researcher_uuid UUID,
    institution_uuid UUID,
    CONSTRAINT PK_Affiliation PRIMARY KEY (researcher_uuid, institution_uuid),
    FOREIGN KEY (researcher_uuid) REFERENCES researchers(uuid),
    FOREIGN KEY (institution_uuid) REFERENCES institutions(uuid)
);