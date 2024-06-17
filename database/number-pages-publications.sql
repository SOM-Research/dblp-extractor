\c metascience

/*
    UPDATE publications.num_pages
*/


UPDATE publications
SET num_pages = pages::int
WHERE pages ~ '^[0-9]{1,4}$';

UPDATE publications
SET num_pages =
    ((regexp_match(pages, '[0-9]{1,5}-(.*)'))[1])::int
    -
    ((regexp_match(pages, '(.*)-[0-9]{1,5}'))[1])::int
WHERE pages ~ '^[0-9]{1,5}-[0-9]{1,5}$';

UPDATE publications
SET num_pages =
    ((regexp_match(pages, '^[0-9]{1,10}:[0-9]{1,3}-[0-9]{1,10}:(.*)$'))[1])::int
    -
    ((regexp_match(pages, '^[0-9]{1,10}:(.*)-[0-9]{1,10}:[0-9]{1,3}$'))[1])::int
WHERE pages ~ '^[0-9]{1,10}:[0-9]{1,3}-[0-9]{1,10}:[0-9]{1,3}$';

/*

 \\TODO: should be all publications with num_pages
 74456 PUBLICATIONS WITHOUT num_pages

 Total of 6100821 publications has pages then
1,22% of publications without pages.


SELECT count(*) FROM publications WHERE num_pages = 0;
SELECT pages FROM publications WHERE num_pages = 0;

 */


/*
regexp_match(w, '^Corrigendum to"(.*)"\.$')

            (select 'Corrigendum to "Fine-Grained Control-Flow Integrity Based on Points-to Analysis for CPS".' as w)


(regexp_match(xml_item, '<note.*type="affiliation".*>(.*)<\/note>'))[1]



Select xml_key from publications where title LIKE LIKE '%' ||
      select (regexp_match(title, '^Corrigendum to "(.*)".'))[1] as t_c, xml_key as key_c from publications where title like 'Corrigendum to %'
      '%';

Select p1.xml_key, p2.xml_key from publications as p1 JOIN publications as p2 ON (p1.title LIKE 'Corrigendum to %');
*/


