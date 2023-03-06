# dblp-extractor

This project is aim to be an extractor to search dblp data. 

DBLP is an open bibliographic information on major computer science journals and proceedings.

## Repository structure

* _config_:  you can find a `config_example.yaml` as example for the configuration of the tool, and which parameters of there are mandatory. 

* _data_: is where all raw data is expected. There is a `data_example.xml` looks like dblp xml file, but has only a few items. To replicate all projects you should download the [original xml file](https://dblp.org/xml/release/).

* _database_: includes the DDL file and the repositories to interact with the database. Also, it includes the class to connect with the database.

* _extractor_: this folder contains the classes and modules needed to interact between the xml raw data and database.

* _model_: where all model elements are placed.

## Set Up
1. Install project dependencies; in the root project you will find the `requirements.txt`:

    ```console
    pip install -r requirements.txt
    ```

2. Copy or rename  `config_example.yaml` to `config.yaml`, this file is added into `.gitignore` file to avoid push sensitive data. Modify this file with the database configuration. If  `db` name (now *metascience*) is changed; it should be changed in ddl file as well.

3. Execute `setup.py`; in the first time you should add at least `--ddl` and `--xml` arguments:
   * `--ddl` argument is for ddl file.
   * `--xml` argument is for xml file.
   * `--splitXml` needs a xml file and splits this file by first level xml children.
   * `--insert` needs a xml file and is aim to insert all xml data into database.

    This is to only creates database:
    ```console
    python extractor/setup.py --ddl "../database/mariadbDDL.sql" --xml "../data/data_example.xml"
    ```
    
    This is to create and insert database: 
    ```console
    python extractor/setup.py --ddl "../database/mariadbDDL.sql" --xml "../data/data_example.xml --insert True"
    ```

    This is to split the xml:
    ```console
    python extractor/setup.py  --xml "../data/data_example.xml --splitXml True"
    ```
    
    If the four parameters are applied, the inserts are from original xml, and not for the new generated by the split.