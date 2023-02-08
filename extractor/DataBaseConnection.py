import mariadb
import yaml
import sys

def connect():
    configFile = open("../config/config.yaml", "r")
    cfg = yaml.load(configFile, yaml.Loader)

    try:
        conn = mariadb.connect(
            host=cfg['db']['host'],
            port=cfg['db']['port'],
            user=cfg['db']['user'],
            password=cfg['db']['password'],
            autocommit=True)
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
    return conn.cursor()

db = connect()
file = open('../database/mariadbDDL.sql', 'r')
for line in file.readlines():
    db.execute(line)

file.close()
db.close()
