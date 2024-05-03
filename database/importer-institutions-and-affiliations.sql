\c metascience




   Select
       (regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1] as afil,
       (regexp_match(i.name, '^(.+?),'))[1] as insti,
       similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], (regexp_match(i.name, '^(.*),'))[1]) as similarity
   from
       researchers as r
     JOIN
       institutions as i
     ON (similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], (regexp_match(i.name, '^(.*),'))[1]) > 0.86)
LIMIT 10;

   Select
       (regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1] as afil,
       i.name as insti,
       similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], i.name) as similarity
   from
       researchers as r
     JOIN
       institutions as i
     ON (similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], i.name) > 0.86)
LIMIT 10;


Select (regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1] as afil, i.name as insti,  word_similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], i.name) as similarity from researchers as r JOIN institutions as i ON ( word_similarity((regexp_match(r.xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1], i.name) > 0.86) LIMIT 10;



SELECT
    i1.full_name,
    i1.short_name,
    i2.full_name,
    i2.short_name,
    similarity(i1.full_name, i2.full_name),
    similarity(i1.full_name, i2.short_name),
    i1.similarity,
    i2.similarity
FROM institutions_temp as i1
    JOIN institutions_temp as i2
    ON (similarity(i1.full_name, i2.full_name) > 0.6)
WHERE i1.similarity = 1 and i2.similarity < 1;
