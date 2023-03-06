DROP DATABASE IF EXISTS metascience;
CREATE DATABASE metascience;
use metascience;

CREATE TABLE researchers (
    id UUID PRIMARY KEY,
    current_alias varchar(255),
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_item LONGTEXT
);

CREATE INDEX r_xml_keys_index ON researchers(xml_key);

CREATE TABLE researcher_xml_keys(
    researcher_id UUID,
    xml_key VARCHAR(255),
    CONSTRAINT PK_researcher_xml_keys PRIMARY KEY (researcher_id,xml_key),
    FOREIGN KEY (researcher_id) REFERENCES researchers(id)
);

CREATE TABLE researcher_names(
    researcher_id UUID,
    name VARCHAR(255),
    CONSTRAINT PK_researcher_names PRIMARY KEY (researcher_id,name),
    FOREIGN KEY (researcher_id) REFERENCES researchers(id)
);

CREATE INDEX r_names_names_index ON researcher_names(name);


ALTER TABLE researcher_names CHARACTER SET utf8 COLLATE utf8_bin;
ALTER TABLE researcher_names CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;

CREATE TABLE publication_venues(
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    type ENUM('journal', 'conference')
);

CREATE TABLE publication_groups(
    id varchar(255) PRIMARY KEY,
    title varchar(255),
    publication_venue UUID,
    publisher varchar(255),
    year int,
    isbn varchar(255),
    booktitle varchar(255),
    serie varchar(255),
    volume int,
    number int,
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_item LONGTEXT,
    FOREIGN KEY (publication_venue) REFERENCES publication_venues(id)
);

CREATE TABLE publications(
    id varchar(255) PRIMARY KEY,
    type ENUM('article','thesis'),
    publication_group VARCHAR(255),
    title varchar(255),
    year int,
    doi varchar(255),
    pages varchar(255),
    num_pages int,
    xml_key VARCHAR(255),
    xml_mdate DATE,
    xml_item LONGTEXT,
    FOREIGN KEY (publication_group) REFERENCES publication_groups(id)
);

CREATE TABLE publication_electronic_editions(
    publication_id VARCHAR(255),
    electronic_edition VARCHAR(255),
    CONSTRAINT PK_publication_electronic_editions PRIMARY KEY (publication_id,electronic_edition),
    FOREIGN KEY (publication_id) REFERENCES publications(id)
);

CREATE TABLE authorships(
    researcher_id UUID,
    publication_id VARCHAR(255),
    position int,
    CONSTRAINT PK_authorships PRIMARY KEY (researcher_id,publication_id),
    FOREIGN KEY (researcher_id) REFERENCES researchers(id),
    FOREIGN KEY (publication_id) REFERENCES publications(id)
);

CREATE TABLE publication_group_electronic_editions(
    publication_group_id VARCHAR(255),
    electronic_edition VARCHAR(255),
    CONSTRAINT PK_publication_group_electronic_editions PRIMARY KEY (publication_group_id,electronic_edition),
    FOREIGN KEY (publication_group_id) REFERENCES publication_groups(id)
);

CREATE TABLE institutions(
    id UUID PRIMARY KEY,
    name LONGTEXT
);

CREATE INDEX institution_names_index ON institutions(name);

CREATE TABLE affiliations(
    researcher_id UUID,
    institution_id UUID,
    CONSTRAINT PK_Affiliation PRIMARY KEY (researcher_id, institution_id),
    FOREIGN KEY (researcher_id) REFERENCES researchers(id),
    FOREIGN KEY (institution_id) REFERENCES institutions(id)
)