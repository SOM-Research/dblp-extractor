import psycopg2
import sqlalchemy
import sys
import yaml
from sqlalchemy.orm import Session

class DataBaseConnection():

    def __init__(self):
        self.base = None
        self.session = None

    def config(self):
        configFile = open("../config/config.yaml", "r")
        return yaml.load(configFile, yaml.Loader)

    def connection(self):
        cfg = self.config()
        try:
            conn = psycopg2.connect("dbname=metascience user=postgres")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)
        return conn

    def connect(self):
        conn = self.connection()
        return conn.cursor()


    def alchemySession(self):
        if self.session is None:
            cfg = self.config()
            txt = "postgresql+psycopg2://" + cfg['db']['user'] + ":" + cfg['db']['password'] + "@" + cfg['db'][
                'host'] + ":" + str(cfg['db']['port']) + "/" + cfg['db']['db']
            engine = sqlalchemy.create_engine(txt)
            session = sqlalchemy.orm.sessionmaker()
            session.configure(bind=engine)
            self.session = session()
        return self.session