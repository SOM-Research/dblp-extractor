\c metascience;

\lo_import :v1;

INSERT INTO oid_xml values (:LASTOID, :v2, now());

  INSERT INTO publication_venues AS pv
    SELECT
      gen_random_uuid(),
      (regexp_match((xpath('//@key', tempTable.tempColumn))::text, '.*\/(.*)\/.*'))[1],
      'unknown'
    FROM unnest(
      xpath
        (    :v3
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = :v2 ORDER BY created_at DESC LIMIT 1)), 'LATIN1'))
        )
    ) AS tempTable(tempColumn)
       ON CONFLICT ON CONSTRAINT publication_venues_name_unique DO NOTHING;

  INSERT INTO publication_groups
    SELECT
      gen_random_uuid(),
      (xpath('//title/text()', tempTable.tempColumn))[1]::text,
      (xpath('//editor/text()', tempTable.tempColumn))::varchar[],
      (SELECT uuid FROM publication_venues where name = ((regexp_match((xpath('//@key', tempTable.tempColumn))::text, '.*\/(.*)\/.*'))[1])),
      (xpath('//publisher/text()', tempTable.tempColumn))::varchar[],
      (xpath('//year/text()', tempTable.tempColumn))[1]::text::int,
      (xpath('//isbn/text()', tempTable.tempColumn))::varchar[],
      (regexp_match((xpath('//ee/text()', tempTable.tempColumn))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/([0-9][0-9][0-9]-[0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9])'))[1],
      (xpath('//crossref/text()', tempTable.tempColumn))[1]::text,
      (xpath('//booktitle/text()', tempTable.tempColumn))[1]::text,
      (xpath('//serie/text()', tempTable.tempColumn))[1]::text,
      (xpath('//volume/text()', tempTable.tempColumn))[1]::text,
      (xpath('//number/text()', tempTable.tempColumn))[1]::text,
      (xpath('//ee/text()', tempTable.tempColumn))::varchar[],
      (xpath('//@key', tempTable.tempColumn))[1]::text,
      to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
      tempTable.tempColumn
    FROM unnest(
      xpath
        (    :v3
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = :v2 ORDER BY created_at DESC LIMIT 1)), 'LATIN1'))
        )
    ) AS tempTable(tempColumn);

SELECT count(*) from publication_groups;