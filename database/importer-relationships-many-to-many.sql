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
