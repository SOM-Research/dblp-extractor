CREATE TABLE authorships_temp (
    researcher_uuid UUID,
    researcher_name text,
    position int,
    publication_uuid UUID,
    year_publication int,
    type publications_type,
    year_frist_publication int,
    num_publications int,
    has_publications_before BOOLEAN DEFAULT FALSE,
    CONSTRAINT PK_authorships_temp PRIMARY KEY (researcher_uuid,publication_uuid, position),
    FOREIGN KEY (researcher_uuid) REFERENCES researchers(uuid),
    FOREIGN KEY (publication_uuid) REFERENCES publications(uuid)
);
Insert into authorships_temp
Select r.uuid, r.current_alias, a.position, p.uuid, p.year, p.type, false
FROM publications as p right join authorships as a ON (a.publication_uuid = p.uuid)
                    left join researchers as r ON (a.researcher_uuid = r.uuid)
Where a.position = 1;

Update authorships_temp as t
set has_publications_before = a.has_pubs
FROM (Select distinct a.researcher_uuid as researcher_uuid, true as has_pubs from authorships as a left join publications as p ON (a.publication_uuid = p.uuid) where p.year < 2000) AS a
where t.researcher_uuid = a.researcher_uuid;

Update authorships_temp as t
set year_frist_publication = a.first_pub_year
FROM
 (Select distinct a.researcher_uuid as researcher_uuid, p.year as first_pub_year from authorships as a left join publications as p ON (a.publication_uuid = p.uuid) group by a.researcher_uuid, p.year) AS a
where t.researcher_uuid = a.researcher_uuid;

Update authorships_temp as t
set num_publications = a.total
FROM (
SELECT researcher_uuid, COUNT(*) as total FROM authorships_temp group by researcher_uuid
) as a
where t.researcher_uuid = a.researcher_uuid;


CREATE TABLE confs_and_journals_uuid
(
    uuid                   UUID PRIMARY KEY,
    publication_group_name text
)

INSERT INTO confs_and_journals_uuid
SELECT p.uuid, p.journal
FROM publications as p
WHERE p.journal in ('Softw. Syst. Model.', 'IEEE Trans. Software Eng.', 'ACM Trans. Softw. Eng. Methodol.', 'IEEE Softw.', 'Commun. ACM', 'Inf. Softw. Technol.', 'Empir. Softw. Eng.', 'J. Object Technol.', 'J. Syst. Softw.');

INSERT INTO confs_and_journals_uuid
SELECT p.uuid, pg.booktitle
FROM publications as p LEFT JOIN publication_groups as pg ON (p.publication_group_uuid = pg.uuid)
WHERE pg.booktitle in ('SLE', 'ICSE', 'CAiSE', 'MoDELS', 'ICWE', 'WWW', 'ICMT', 'EMMSAD', 'SANER', 'RCIS', 'MSR', 'ESEM', 'FASE', 'SAC')
             or (pg.booktitle = 'ER' AND pg.title like 'Conceptual Modeling%')
;
