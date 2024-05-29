CREATE TABLE temporal_researchers_not_in (
    researcher_uuid UUID
);
CREATE INDEX INDEX_researcher_temp_table ON temporal_researchers_not_in(researcher_uuid);

/* 396667 researchers not in temporal decision */
INSERT INTO temporal_researchers_not_in
SELECT DISTINCT a.researcher_uuid
            FROM authorships AS a RIGHT JOIN publications AS p ON (a.publication_uuid = p.uuid)
            WHERE p.year < 2000;


CREATE TABLE publications_per_researchers_after_2000 (
researcher_uuid UUID,
publication_uuid UUID,
published_year INT,
publication_type publications_type);
CREATE INDEX INDEX_researcher_FROM_table_view ON publications_per_researchers_after_2000(researcher_uuid);
CREATE INDEX INDEX_publication_FROM_table_view ON publications_per_researchers_after_2000(publication_uuid);
CREATE INDEX INDEX_year_FROM_table_view ON publications_per_researchers_after_2000(published_year);
CREATE INDEX INDEX_type_FROM_table_view ON publications_per_researchers_after_2000(publication_type);


INSERT INTO publications_per_researchers_after_2000
SELECT 
    a.researcher_uuid AS researcher_uuid, 
    a.publication_uuid AS publication_uuid, 
    p.year AS published_year, 
    p.type AS publication_type
FROM authorships AS a RIGHT JOIN publications AS p ON (a.publication_uuid = p.uuid) 
WHERE 
    a.position = 1 AND 
    p.year >= 2000 AND 
    p.type IN ('journal', 'conference', 'workshop') AND 
    a.researcher_uuid NOT IN (SELECT t.researcher_uuid FROM temporal_researchers_not_in AS t);

DROP TABLE temporal_researchers_not_in;
