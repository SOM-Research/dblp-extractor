CREATE TABLE temp_institutions_country (
    i_uuid UUID,
    c_name TEXT
);

INSERT INTO temp_institutions_country (i_uuid, c_name)
SELECT i.uuid, c.name FROM countries as c RIGHT JOIN  institutions as i ON( i.name  ~ c.name) WHERE c.name IS NOT NULL;

DROP TABLE temp_institutions_country;

UPDATE institutions as i
SET country = sq.c_name FROM (SELECT c_name, i_uuid FROM temp_institutions_country) as sq
WHERE sq.i_uuid = uuid;

UPDATE institutions
SET country =  'Company'
WHERE
     name ~ 'eBay'
     OR name ~ 'NVIDIA'
     OR name ~ 'Nvidia'
     OR name ~ 'Toyota'
     OR name ~ 'Bosch'
     OR name ~ 'Huawei Technologies'
     OR name ~ 'JD.COM'
     OR name ~ 'Company'
     OR name ~ 'LinkedIn'
     OR name ~ 'Electronic Arts'
     OR name ~ 'iDefense'
     OR name ~ 'European Space Agency'
     OR name ~ 'Microsoft'
     OR name ~ 'Adobe'
     OR name ~ 'Alexa AI'
     OR name ~ 'Google'
     OR name ~ 'Goggle'
     OR name ~ 'Comtech'
     OR name ~ 'Amazon'
     OR name ~ 'Siemens'
     OR name ~ 'Apache'
     OR name ~ 'Facebook'
     OR name ~ 'Philips Automotive'
     OR name ~ 'Cisco'
     OR name ~ 'Nokia'
     OR name ~ 'SEMATECH'
     OR name ~ 'Pinterest'
     OR name ~ 'Lenovo'
     OR name ~ 'Samsung'
     OR name ~ 'Qualcomm'
     OR name ~ 'Uber'
     OR name ~ 'Alibaba Group'
     OR name ~ 'Yahoo'
     OR name ~ 'Telecom'
     OR name ~ 'IBM'
     OR name ~ 'cohere.ai'
     OR name ~ 'HHVISION'
     OR name ~ 'Meta'
     OR name ~ 'Intel'
     OR name ~ 'Spotify'
     OR name ~ 'Inc.'
     OR name ~ 'Ant Group'
     OR name ~ 'Boeing'
     OR name ~ 'Co.'
     OR name ~ 'Corporation'
     OR name ~ 'Corporate'
     OR name ~ 'LG Innotek'
     OR name ~ 'Volvo'
     OR name ~ 'Motorala'
     OR name ~ 'Huawei CBG'
     OR name ~ 'NASA'
;



UPDATE institutions
SET country =  'United States'
WHERE country IS NULL AND (
    name ~ 'USA'
    OR name ~ 'Alabama'
    OR name ~ 'Arizona'
    OR name ~ 'Baltimore'
    OR name ~ 'Boston'
    OR name ~ 'California'
    OR name ~ 'Californiae'
    OR name ~ 'Columbia University'
    OR name ~ 'Chicago'
    OR name ~ 'Delaware'
    OR name ~ 'Florida'
    OR name ~ 'Harvard'
    OR name ~ 'Houston'
    OR name ~ 'Iona College'
    OR name ~ 'Iowa'
    OR name ~ 'Kansas'
    OR name ~ 'Los Angeles'
    OR name ~ 'Louisiana'
    OR name ~ 'Massachusetts'
    OR name ~ 'Michigan'
    OR name ~ 'Missouri'
    OR name ~ 'Minnesota'
    OR name ~ 'Nebraska'
    OR name ~ 'New York'
    OR name ~ 'Oklahoma'
    OR name ~ 'Oak Ridge'
    OR name ~ 'Ottawa'
    OR name ~ 'Pennsylvania'
    OR name ~ 'Pittsburgh'
    OR name ~ 'Stanford'
    OR name ~ 'Tennessee'
    OR name ~ 'Texas'
    OR name ~ 'Utah'
    OR name ~ 'Virginia'
    OR name ~ 'Wisconsin'
    );

UPDATE institutions
SET country =  'Canada'
WHERE country IS NULL AND (
     name ~ 'Toronto'
     OR name ~ 'British Columbia'
    );

UPDATE institutions
SET country =  'New Zealand'
WHERE country IS NULL AND (
     name ~ 'Christchurch'
    );

UPDATE institutions
SET country =  'Congo'
WHERE country IS NULL AND (
     name ~ 'Congo'
    );

UPDATE institutions
SET country =  'Finland'
WHERE country IS NULL AND (
     name ~ 'Finnland'
     OR name ~ 'Helsinki'
    );

UPDATE institutions
SET country =  'Macedonia [FYROM]'
WHERE country IS NULL AND (
     name ~ 'Macedonia'
    );

UPDATE institutions
SET country =  'Portugal'
WHERE country IS NULL AND (
     name ~ 'Lisbon'
     OR name ~ 'Lisboa'
    );


UPDATE institutions
SET country =  'Denmark'
WHERE country IS NULL AND (
     name ~ 'Copenhagen'
    );

UPDATE institutions
SET country =  'United Kingdom'
WHERE country IS NULL AND (
    name ~ 'UK'
    OR name ~ 'Uk'
    OR name ~ 'Bedfordshire'
    OR name ~ 'Birmingham'
    OR name ~ 'Cambridge'
    OR name ~ 'Edinburgh'
    OR name ~ 'Essex'
    OR name ~ 'London'
    OR name ~ 'Manchester'
    OR name ~ 'Oxford'
    OR name ~ 'Sheffield'
    OR name ~ 'Windsor'
    OR name ~ 'Wolverhampton'
    );

UPDATE institutions
SET country =  'Singapore'
WHERE country IS NULL AND (
     name ~ 'Singapor'
    );

UPDATE institutions
SET country =  'Mexico'
WHERE country IS NULL AND (
     name ~ 'BUAP'
     OR name ~ 'Guanajuato'
     OR name ~ ' de Monterrey'
    );

UPDATE institutions
SET country =  'Russia'
WHERE country IS NULL AND (
     name ~ 'Rusia'
     OR name ~ 'Moscow'
     OR name ~ 'St. Petersburg'
    );

UPDATE institutions
SET country =  'South Korea'
WHERE country IS NULL AND (
     name ~ 'Korea'
     OR name ~ 'Sungkyunkwan'
);

UPDATE institutions
SET country =  'India'
WHERE country IS NULL AND (
     name ~ 'Pilani'
     OR name ~ 'Bangalore'
);

UPDATE institutions
SET country =  'Iran'
WHERE country IS NULL AND (
     name ~ 'Yazd'
);

UPDATE institutions
SET country =  'Sweden'
WHERE country IS NULL AND (
     name ~ 'Swedish'
);

UPDATE institutions
SET country =  'China'
WHERE country IS NULL AND (
     name ~ 'Shenzhen'
     OR name ~ 'Jiaotong'
     OR name ~ 'Beijing'
     OR name ~ 'Chinese'
     OR name ~ 'Kunming'
     OR name ~ 'Shanghai'
     OR name ~ 'Peking'
     OR name ~ 'Zhejiang'
);

UPDATE institutions
SET country =  'Japan'
WHERE country IS NULL AND (
     name ~ 'Tokyo'
     OR name ~ 'Fukuoka'
     OR name ~ 'Kyushu'
     OR name ~ 'Nagoya'
     OR name ~ 'Nagaoka'
);

UPDATE institutions
SET country =  'Saudi Arabia'
WHERE country IS NULL AND (
     name ~ 'Saudia Arabia'
);

UPDATE institutions
SET country =  'Morocco'
WHERE country IS NULL AND (
     name ~ 'Maroc'
);

UPDATE institutions
SET country =  'Tunisia'
WHERE country IS NULL AND (
     name ~ 'Tunesia'
     OR name ~ 'Tunesia'
     OR name ~ 'Tunisie'
);


UPDATE institutions
SET country =  'Czech Republic'
WHERE country IS NULL AND (
     name ~ 'Prague'
     OR name ~ 'Czechia'
     OR name ~ 'Czech'
);

UPDATE institutions
SET country =  'Italy'
WHERE country IS NULL AND (
     name ~ 'Italia'
     OR name ~ 'Bologna'
     OR name ~ 'Genoa'
     OR name ~ 'Palermo'
     OR name ~ 'Roma'
     OR name ~ 'Milan'
     OR name ~ 'Milano'
     OR name ~ 'Napoli'
     OR name ~ 'Parma'
);

UPDATE institutions
SET country =  'United Arab Emirates'
WHERE country IS NULL AND (
     name ~ 'UAE'
     OR name ~ 'Khalifa University'
);

UPDATE institutions
SET country = 'Belgium'
WHERE country IS NULL AND (
    name ~ 'Haasrode'
);

UPDATE institutions
SET country = 'Romania'
WHERE country IS NULL AND (
    name ~ 'Bucharest'
);


UPDATE institutions
SET country = 'Serbia'
WHERE country IS NULL AND (
    name ~ 'Servia'
);

UPDATE institutions
SET country = 'Greece'
WHERE country IS NULL AND (
     name ~ 'Athens'
     OR name ~ 'Athena'
     OR name ~ 'Patras'
);

UPDATE institutions
SET country = 'France'
WHERE country IS NULL AND (
     name ~ 'Paris'
     OR name ~ 'Sorbonne'
     OR name ~ 'Grenoble'
     OR name ~ 'Lyon'
     OR name ~ 'Notre Dame'
);

UPDATE institutions
SET country = 'Spain'
WHERE country IS NULL AND (
     name ~ 'Catalonia'
     OR name ~ 'Madrid'
     OR name ~ 'Sevilla'
     OR name ~ 'Spanish'
     OR name ~ 'Salamanca'
     OR name ~ 'Illes Balears'
     OR name ~ 'the Basque Country'
     OR name ~ 'Castilla-La Mancha'
     OR name ~ 'Granada'
     OR name ~ 'Jaume I University'
);

UPDATE institutions
SET country = 'Austria'
WHERE country IS NULL AND (
     name ~ 'Vienna'
     OR name ~ 'Linz'
);
UPDATE institutions
SET country = 'Australia'
WHERE country IS NULL AND (
     name ~ 'Sydney'
     OR name ~ 'Brisbane'
);

UPDATE institutions
SET country = 'Poland'
WHERE country IS NULL AND (
     name ~ 'Wroclaw'
);

UPDATE institutions
SET country = 'Ireland'
WHERE country IS NULL AND (
     name ~ 'Dublin'
);

UPDATE institutions
SET country =  'Germany'
WHERE country IS NULL AND (
     name ~ 'Berlin'
    OR name ~ 'Bochum'
    OR name ~ 'Bonn'
    OR name ~ 'Braunschweig'
    OR name ~ 'Bremen'
    OR name ~ 'Darmstadt'
    OR name ~ 'Dresden'
    OR name ~ 'Dortmund'
    OR name ~ 'Duisburg-Essen'
    OR name ~ 'Frankfurt'
    OR name ~ 'Freiburg'
    OR name ~ 'Hagen'
    OR name ~ 'Hamburg'
    OR name ~ 'Hannover'
    OR name ~ 'Karlsruhe'
    OR name ~ 'Leipzig'
    OR name ~ 'Munich'
    OR name ~ 'Nuremberg'
    OR name ~ 'Stuttgart'
    OR name ~ 'Trier'
    OR name ~ 'German'
);

UPDATE institutions
SET country =  'Turkey'
WHERE country IS NULL AND (
    name ~ 'Istanbul'
);


UPDATE institutions
SET country =  'Netherlands'
WHERE country IS NULL AND (
    name ~ 'Amsterdam'
);

UPDATE institutions
SET country =  'Argentina'
WHERE country IS NULL AND (
    name ~ 'Argentinia'
);

UPDATE institutions
SET country =  'Palestinian Territories'
WHERE country IS NULL AND (
    name ~ 'Palestine'
);

UPDATE institutions
SET country =  'Brazil'
WHERE country IS NULL AND (
    name ~ 'BR'
    OR name ~ 'Brasil'
    OR name ~ 'Rio de Janeiro'
    OR name ~ 'Rio Grande do Norte'
);

UPDATE institutions
SET country =  'Award'
WHERE country IS NULL AND (
    name ~ 'Award'
    OR name ~ 'Prize'
);

/*

\\TODO: should be all institutions with countries
 2281 INSTITUTIONS WITHOUT countries

A total of 66148 institutions that means a 3,45% is without country

 Select count(*) FROM institutions WHERE country is NULL;
 Select name FROM institutions WHERE country is NULL;

 */