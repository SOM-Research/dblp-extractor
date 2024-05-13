\c metascience;

\lo_import :v1;

INSERT INTO oid_xml values (:LASTOID, 'update', now());

CREATE TABLE update_temp (
    key TEXT,
    tag TEXT,
    mdate DATE,
    item TEXT,
    exists boolean
);

INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'article',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//article'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'book',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//book'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'data',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//data'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);

INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'incollection',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//incollection'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'inproceedings',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//inproceedings'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'mastersthesis',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//mastersthesis'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);

INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'phdthesis',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//phdthesis'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'proceedings',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//proceedings'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


INSERT INTO update_temp
    SELECT
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        'www',
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        tempTable.tempColumn,
        false
    FROM  unnest(
      xpath
        (   '//www'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'update' ORDER BY created_at DESC LIMIT 1)), 'UTF8'))
        )
    ) AS tempTable(tempColumn);


UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'article';
UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'book';
UPDATE update_temp as u SET exists = true FROM publication_groups as pg WHERE pg.xml_key = u.xml_key and u.tag = 'book';
UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'incollection';
UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'inproceedings';
UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'mastersthesis';
UPDATE update_temp as u SET exists = true FROM publications as p WHERE p.xml_key = u.xml_key and u.tag = 'phdthesis';
UPDATE update_temp as u SET exists = true FROM publication_groups as pg WHERE pg.xml_key = u.xml_key and u.tag = 'proceedings';
UPDATE update_temp as u SET exists = true FROM researchers as r WHERE r.xml_key = u.xml_key and u.tag = 'www';


INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'article',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'article';

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'book',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'book' and item LIKE '%<author%';



INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'data',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'data';

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'incollection',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'incollection';


INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'inproceedings',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'inproceedings';

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'mastersthesis',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'mastersthesis';

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'phdthesis',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'phdthesis';

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//author/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//journal/text()',  u.item::xml))[1]::text,
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//pages/text()',  u.item::xml))[1]::text,
      NULL,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      FALSE,
      NULL,
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'phdthesis',
       u.item
    FROM  update_temp as u WHERE u.exists = false and u.tag = 'proceedings';

INSERT INTO publication_venues AS pv
    SELECT
      gen_random_uuid(),
      (regexp_match((xpath('//@key', u.item::xml))::text, '.*\/(.*)\/.*'))[1],
      'book'
    FROM update_temp as u WHERE u.tag = 'book'
       ON CONFLICT ON CONSTRAINT publication_venues_name_unique DO NOTHING;


INSERT INTO publication_venues AS pv
    SELECT
      gen_random_uuid(),
      (regexp_match((xpath('//@key', u.item::xml))::text, '.*\/(.*)\/.*'))[1],
      'conference'
    FROM update_temp as u WHERE u.tag = 'proceedings'
       ON CONFLICT ON CONSTRAINT publication_venues_name_unique DO NOTHING;

INSERT INTO publication_groups
    SELECT
      gen_random_uuid(),
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//editor/text()',  u.item::xml))::varchar[],
      (SELECT uuid FROM publication_venues where name = ((regexp_match((xpath('//@key',  u.item::xml))::text, '.*\/(.*)\/.*'))[1])),
      (xpath('//publisher/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (xpath('//isbn/text()',  u.item::xml))::varchar[],
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/([0-9][0-9][0-9]-[0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9])'))[1],
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//booktitle/text()',  u.item::xml))[1]::text,
      (xpath('//serie/text()',  u.item::xml))[1]::text,
      (xpath('//volume/text()',  u.item::xml))[1]::text,
      (xpath('//number/text()',  u.item::xml))[1]::text,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'book',
       u.item
    FROM update_temp as u WHERE u.exists = false and u.tag = 'book' and item LIKE '%<editor%';

INSERT INTO publication_groups
    SELECT
      gen_random_uuid(),
      (xpath('//title/text()',  u.item::xml))[1]::text,
      (xpath('//editor/text()',  u.item::xml))::varchar[],
      (SELECT uuid FROM publication_venues where name = ((regexp_match((xpath('//@key',  u.item::xml))::text, '.*\/(.*)\/.*'))[1])),
      (xpath('//publisher/text()',  u.item::xml))::varchar[],
      (xpath('//year/text()',  u.item::xml))[1]::text::int,
      (xpath('//isbn/text()',  u.item::xml))::varchar[],
      (regexp_match((xpath('//ee/text()',  u.item::xml))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/([0-9][0-9][0-9]-[0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9])'))[1],
      (xpath('//crossref/text()',  u.item::xml))[1]::text,
      (xpath('//booktitle/text()',  u.item::xml))[1]::text,
      (xpath('//serie/text()',  u.item::xml))[1]::text,
      (xpath('//volume/text()',  u.item::xml))[1]::text,
      (xpath('//number/text()',  u.item::xml))[1]::text,
      (xpath('//ee/text()',  u.item::xml))::varchar[],
      (xpath('//@key',  u.item::xml))[1]::text,
      to_date((xpath('//@mdate',  u.item::xml))[1]::text, 'YYYY-MM-DD'),
      'proceedings',
       u.item
    FROM update_temp as u WHERE u.exists = false and u.tag = 'proceedings';

    INSERT INTO researchers
        SELECT
        gen_random_uuid(),
        (xpath('//author/text()', u.item::xml))[1]::text,
        (xpath('//author/text()', u.item::xml))::varchar[],
        0,
        (regexp_match((xpath('//url/text()', u.item::xml))::text, 'https:\/\/orcid.org\/([0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9])'))[1],
        (xpath('//crossref/text()', u.item::xml))[1]::text,
        (xpath('//@key', u.item::xml))[1]::text,
        to_date((xpath('//@mdate', u.item::xml))[1]::text, 'YYYY-MM-DD'),
        'www',
        u.item
    FROM update_temp as u WHERE u.exists = false and u.tag = 'www';