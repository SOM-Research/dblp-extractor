DROP DATABASE IF EXISTS metascience;

CREATE DATABASE metascience;

\c metascience;

CREATE TABLE oid_xml (
    oid INT PRIMARY KEY,
    xml varchar(255)
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
    xml_item TEXT
);

-- ALTER TABLE researcher_names CHARACTER SET utf8 COLLATE utf8_bin;
-- ALTER TABLE researcher_names CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;

CREATE TYPE publication_venues_type as ENUM ('journal', 'conference', 'book', 'unknown');

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
    booktitle TEXT,
    serie varchar(255),
    volume varchar(255),
    number varchar(255),
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_item TEXT,
    FOREIGN KEY (publication_venue) REFERENCES publication_venues(uuid)
);
CREATE INDEX p_group_title_index ON publication_groups(title);
CREATE INDEX p_group_xml_key_index ON publication_groups(xml_key);

CREATE TYPE publications_type as ENUM ('journal','thesis', 'conference', 'book');

CREATE TABLE publications(
    uuid UUID PRIMARY KEY,
    type publications_type,
    publication_group_uuid UUID,
    title TEXT,
    year int,
    doi varchar(255),
    pages varchar(255),
    num_pages int,
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_item TEXT,
    FOREIGN KEY (publication_group_uuid) REFERENCES publication_groups(uuid)
);
CREATE INDEX publication_type_index ON publications(type);
CREATE INDEX publication_title_index ON publications(title);
CREATE INDEX publication_xml_key_index ON publications(xml_key);

CREATE TABLE publication_electronic_editions(
    publication_uuid UUID,
    electronic_edition VARCHAR(255),
    CONSTRAINT PK_publication_electronic_editions PRIMARY KEY (publication_uuid,electronic_edition),
    FOREIGN KEY (publication_uuid) REFERENCES publications(uuid)
);

CREATE INDEX publication_ee_index ON publication_electronic_editions(electronic_edition);

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


CREATE TABLE publication_group_electronic_editions(
    publication_group_uuid UUID,
    electronic_edition VARCHAR(255),
    CONSTRAINT PK_publication_group_electronic_editions PRIMARY KEY (publication_group_uuid,electronic_edition),
    FOREIGN KEY (publication_group_uuid) REFERENCES publication_groups(uuid)
);

CREATE INDEX p_group_ee_index ON publication_group_electronic_editions(electronic_edition);

CREATE TABLE institutions(
    uuid UUID PRIMARY KEY,
    name TEXT
);

CREATE INDEX institution_names_index ON institutions(name);

CREATE TABLE affiliations(
    researcher_uuid UUID,
    institution_uuid UUID,
    CONSTRAINT PK_Affiliation PRIMARY KEY (researcher_uuid, institution_uuid),
    FOREIGN KEY (researcher_uuid) REFERENCES researchers(uuid),
    FOREIGN KEY (institution_uuid) REFERENCES institutions(uuid)
);