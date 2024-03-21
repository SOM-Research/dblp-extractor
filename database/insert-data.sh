#!/bin/sh

psql -U postgres -f database/dbDDL.sql

psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_1.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_2.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_3.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_4.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_5.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_6.xml'
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_7.xml'

psql -U postgres -f database/importer-publication-venues-and-groups.sql -v v1='/data/formatted/proceedings/proceedings.xml' -v v2="'proceedings.xml'" -v v3="'//proceedings'"
psql -U postgres -f database/importer-publication-venues-and-groups.sql -v v1='/data/formatted/book/book-p-group.xml' -v v2="'book.xml'" -v v3="'//book'"

psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/mastersthesis/mastersthesis.xml' -v v2="'mastersthesis.xml'" -v v3="'//mastersthesis'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/data/data.xml' -v v2="'data.xml'" -v v3="'//data'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/phdthesis/phdthesis.xml' -v v2="'phdthesis.xml'" -v v3="'//phdthesis'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/incollection/incollection.xml' -v v2="'incollection.xml'" -v v3="'//incollection'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_1.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_2.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_3.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_4.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_5.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_6.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_7.xml' -v v2="'article.xml'" -v v3="'//article'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_1.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_2.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_3.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_4.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_5.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_6.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_7.xml' -v v2="'inproceedings.xml'" -v v3="'//inproceedings'"

psql -U postgres -f database/importer-editors.sql
