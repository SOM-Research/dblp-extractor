DROP DATABASE IF EXISTS metascience;
CREATE DATABASE metascience;
use metascience;

CREATE TABLE Researcher (
    id varchar(255) PRIMARY KEY ,
    currentAlias varchar(255),
    xmlKey VARCHAR(255),
    xmlMdate DATE,
    xmlItem LONGTEXT
);

CREATE TABLE ResearcherName(
    researcherId VARCHAR(255),
    name VARCHAR(255),
    CONSTRAINT PK_Researcher_Name PRIMARY KEY (researcherId,name),
    FOREIGN KEY (researcherId) REFERENCES Researcher(id)
);

CREATE TABLE PublicationVenue(
    id VARCHAR(255) PRIMARY KEY,
    type ENUM('journal', 'conference')
);

CREATE TABLE PublicationGroup(
    id varchar(255) PRIMARY KEY,
    title varchar(255),
    publicationVenue VARCHAR(255),
    publisher varchar(255),
    year int,
    isbn varchar(255),
    booktitle varchar(255),
    serie varchar(255),
    volume int,
    number int,
    xmlKey VARCHAR(255),
    xmlMdate DATE,
    xmlItem LONGTEXT,
    FOREIGN KEY (publicationVenue) REFERENCES PublicationVenue(id)
);

CREATE TABLE Publication(
    id varchar(255) PRIMARY KEY,
    type ENUM('article','thesis'),
    publicationGroup VARCHAR(255),
    title varchar(255),
    year int,
    doi varchar(255),
    pages varchar(255),
    numPages int,
    xmlKey VARCHAR(255),
    xmlMdate DATE,
    xmlItem LONGTEXT,
    FOREIGN KEY (publicationGroup) REFERENCES PublicationGroup(id)
);

CREATE TABLE PublicationEE(
    publicationId VARCHAR(255),
    electronicEdition VARCHAR(255),
    CONSTRAINT PK_Publication_EE PRIMARY KEY (publicationId,electronicEdition),
    FOREIGN KEY (publicationId) REFERENCES Publication(id)
);

CREATE TABLE Authorship(
    researcherId VARCHAR(255),
    publicationId VARCHAR(255),
    position int,
    CONSTRAINT PK_Authorship PRIMARY KEY (researcherId,publicationId),
    FOREIGN KEY (researcherId) REFERENCES Researcher(id),
    FOREIGN KEY (publicationId) REFERENCES Publication(id)
);

CREATE TABLE PublicationGroupEE(
    publicationGroupId VARCHAR(255),
    electronicEdition VARCHAR(255),
    CONSTRAINT PK_PublicationGroup_EE PRIMARY KEY (publicationGroupId,electronicEdition),
    FOREIGN KEY (publicationGroupId) REFERENCES PublicationGroup(id)
);