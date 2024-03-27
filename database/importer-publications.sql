\c metascience;

\lo_import :v1;

INSERT INTO oid_xml values (:LASTOID, :v2, now());

INSERT INTO publications
    SELECT
      gen_random_uuid(),
      'unknown',
      null,
      (xpath('//title/text()', tempTable.tempColumn))[1]::text,
      (xpath('//author/text()', tempTable.tempColumn))::varchar[],
      (xpath('//year/text()', tempTable.tempColumn))[1]::text::int,
      (regexp_match((xpath('//ee/text()', tempTable.tempColumn))::text, 'https:\/\/doi.org\/[0-9][0-9].[0-9][0-9][0-9][0-9]\/(.*)'))[1],
      (xpath('//crossref/text()', tempTable.tempColumn))[1]::text,
      (xpath('//pages/text()', tempTable.tempColumn))::varchar[],
      0,
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


SELECT count(*) from publications;