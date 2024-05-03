\c metascience;

\lo_import :v1;

    INSERT INTO oid_xml values (:LASTOID, 'www.xml', NOW());

    INSERT INTO researchers
        SELECT
        gen_random_uuid(),
        (xpath('//author/text()', tempTable.tempColumn))[1]::text,
        (xpath('//author/text()', tempTable.tempColumn))::varchar[],
        0,
        (regexp_match((xpath('//url/text()', tempTable.tempColumn))::text, 'https:\/\/orcid.org\/([0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9])'))[1],
        (xpath('//crossref/text()', tempTable.tempColumn))[1]::text,
        (xpath('//@key', tempTable.tempColumn))[1]::text,
        to_date((xpath('//@mdate', tempTable.tempColumn))[1]::text, 'YYYY-MM-DD'),
        :v2,
        tempTable.tempColumn
    FROM unnest(
      xpath
        (    '//www'
            ,XMLPARSE(DOCUMENT convert_from(lo_get((SELECT oid FROM oid_xml WHERE xml = 'www.xml' ORDER BY created_at DESC LIMIT 1)), 'LATIN1'))
        )
    ) AS tempTable(tempColumn);

SELECT count(*) FROM researchers;