\c metascience;

CREATE TABLE temp_researchers (res_uuid UUID, name TEXT);
CREATE INDEX temp_researchers_name ON temp_researchers(name);
INSERT INTO temp_researchers SELECT uuid, unnest(names) FROM researchers;

CREATE TABLE temp_pub_groups (pg_uuid UUID, editor TEXT, position int);
CREATE INDEX temp_pub_groups_editor ON temp_pub_groups(editor);
INSERT INTO temp_pub_groups SELECT uuid, unnest(editors), 0 FROM publication_groups;
INSERT INTO temp_pub_groups
  SELECT t.pg_uuid, t.editor, array_position(pg.editors, t.editor)
  FROM publication_groups AS pg RIGHT JOIN temp_pub_groups as t ON (pg.uuid = t.pg_uuid);
DELETE FROM temp_pub_groups WHERE position = 0;
INSERT INTO editors
  SELECT r.res_uuid, t.pg_uuid, t.position
  FROM temp_researchers as r RIGHT JOIN temp_pub_groups AS t ON (r.name = t.editor)
ON CONFLICT ON CONSTRAINT PK_editorships DO NOTHING;

CREATE TABLE temp_publications (pub_uuid UUID, author TEXT, position int);
CREATE INDEX temp_publications_author ON temp_publications(author);
INSERT INTO temp_publications SELECT uuid, unnest(authors), 0 FROM publications;
INSERT INTO temp_publications
    SELECT t.pub_uuid, t.author, array_position(p.authors, t.author)
    FROM publications AS p RIGHT JOIN temp_publications AS t ON (p.uuid = t.pub_uuid);
DELETE FROM temp_publications WHERE position = 0;
INSERT INTO authorships SELECT r.res_uuid, t.pub_uuid, t.position
    FROM temp_researchers AS r RIGHT JOIN temp_publications AS t ON (r.name = t.author)
ON CONFLICT ON CONSTRAINT PK_authorships DO NOTHING;

DROP TABLE temp_pub_groups;
DROP TABLE temp_researchers;
DROP TABLE temp_publications;

CREATE TABLE countries (
    country varchar(2),
    latitude FLOAT,
    longitude FLOAT,
    name TEXT
);

COPY countries (country, latitude, longitude, name)
FROM '/data/csv/countries.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE resercher_institution_temp (
    researcher_uuid UUID PRIMARY KEY,
    institution TEXT
);

CREATE INDEX resercher_institution_temp_institution_name_index ON resercher_institution_temp(institution);

INSERT INTO resercher_institution_temp (researcher_uuid, institution)
   SELECT uuid, (xpath('//note[@type="affiliation"]/text()', xml_item::xml))[1]::text
   FROM researchers
   WHERE (xpath('//note[@type="affiliation"]/text()', xml_item::xml))[1]::text IS NOT NULL ;

DELETE FROM resercher_institution_temp WHERE  institution = ' ';

INSERT INTO institutions (uuid, name, version_names)
    SELECT DISTINCT ON (institution) gen_random_uuid(), institution, ARRAY[institution] FROM resercher_institution_temp;

INSERT INTO affiliations (researcher_uuid, institution_uuid)
SELECT ri.researcher_uuid, i.uuid FROM resercher_institution_temp as ri LEFT JOIN institutions as i ON (ri.institution = i.name);

DROP TABLE resercher_institution_temp;



CREATE TABLE pub_group_temp
(
    uuid             UUID,
    publication_uuid UUID
);
CREATE INDEX uuid_index_in_temp ON pub_group_temp(uuid);
CREATE INDEX pub_uuid_index_in_temp ON pub_group_temp(publication_uuid);

INSERT INTO pub_group_temp
    SELECT pg.uuid, p.uuid
    FROM publication_groups as pg LEFT JOIN publications AS p ON (pg.xml_key = p.crossref);

UPDATE publications
SET publication_group_uuid = pub_group_temp.uuid
FROM pub_group_temp WHERE pub_group_temp.publication_uuid = publications.uuid;

DROP TABLE pub_group_temp;



CREATE TABLE pub_group_tem
    uuid             UUID,
    publication_uuid UUID,
    title            TEXT,
    key TEXT
);
CREATE INDEX uuid_index_in_temp ON pub_group_temp(uuid);
CREATE INDEX pub_uuid_index_in_temp ON pub_group_temp(publication_uuid);
CREATE INDEX title_index_in_temp ON pub_group_temp(title);
CREATE INDEX key_index_in_temp ON pub_group_temp(title);

INSERT INTO pub_group_temp
  SELECT
      gen_random_uuid(),
      p.uuid,
      (regexp_match((xpath('//@key', p.xml_item::xml))::text, '^.*\/(.*)\/.*$'))[1],
      p.xml_key
    FROM publications as p where p.crossref is null;

UPDATE pub_group_temp as p1 SET title = p2.title
FROM (
    SELECT p.uuid, (regexp_match(p.key, '^.*/(.*)/[0-9][0-9]/.*$'))[1], p.key, p.title
    FROM pub_group_temp as p
    WHERE (regexp_match(p.key, '^.*/(.*)/[0-9][0-9]/.*$'))[1] IS NOT NULL
    ) as p2
WHERE p2.uuid = p1.uuid;
UPDATE pub_group_temp
SET title = (regexp_match(key, '^.*/(.*)/[0-9][0-9]/.*$'))[1]
WHERE
    (regexp_match(key, '^.*/(.*)/[0-9][0-9]/.*$'))[1] IS NOT NULL
  AND title ~ '^[0-9][0-9]$';

  INSERT INTO publication_venues AS pv
    SELECT DISTINCT ON (title)
      uuid,
      title,
      'unknown'
    FROM pub_group_temp
       ON CONFLICT ON CONSTRAINT publication_venues_name_unique DO NOTHING;

UPDATE publication_venues as pv
SET type = 'journal'
FROM (SELECT title FROM pub_group_temp WHERE key LIKE 'journals/%') AS s
WHERE s.title = pv.name;

UPDATE publication_venues as pv
SET type = 'conference'
FROM (SELECT title FROM pub_group_temp WHERE key LIKE 'conf/%') AS s
WHERE s.title = pv.name;

UPDATE publication_venues as pv
SET type = 'book'
FROM (SELECT title FROM pub_group_temp WHERE key LIKE 'books/%') AS s
WHERE s.title = pv.name;

DROP TABLE pub_group_temp;

UPDATE publications SET type = 'conference' WHERE xml_key LIKE 'conf/%';
UPDATE publications SET type = 'journal' WHERE xml_key LIKE 'journals/%';
UPDATE publications SET type = 'book' WHERE xml_key LIKE 'books/%' AND type = 'unknown';
UPDATE publications SET type = 'thesis' WHERE xml_tag = 'phdthesis' OR xml_tag = 'mastersthesis';
UPDATE publications SET type = 'workshop' WHERE xml_item LIKE '%workshop%' AND (type = 'unknown' OR type = 'conference');