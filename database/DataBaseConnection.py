import mariadb
import sqlalchemy
import sys
import yaml
from sqlalchemy.orm import Session

class DataBaseConnection():

    def __init__(self):
        self.base = None
        self.session = None

    def config(self):
        """
        Get the configuration file
        :return:
        """
        configFile = open("./config/config.yaml", "r")
        return yaml.load(configFile, yaml.Loader)

    def connection(self):
        cfg = self.config()
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
        return conn

    def connect(self):
        """
        Connect to the DB
        :return: DataBase Connection
        """
        conn = self.connection()
        return conn.cursor()

    def createDatabaseFromDDL(self, filePath):
        """
        Create a DataBase from a DDL file given
        :param filePath: DDL file
        """
        db = self.connect()
        ddlFile = open(filePath)
        for line in ddlFile.read().split(';'):
            if (line != ''):
                line += ';'
                print(line)
                db.execute(line)
        db.close()
        ddlFile.close()

    def alchemySession(self):
        """
        Start a Alchemy Session or return the curren session
        :return: Alchemy Session
        """
        if self.session is None:
            cfg = self.config()
            txt = "mariadb+mariadbconnector://" + cfg['db']['user'] + ":" + cfg['db']['password'] + "@" + cfg['db'][
                'host'] + ":" + str(cfg['db']['port']) + "/" + cfg['db']['db']
            engine = sqlalchemy.create_engine(txt)
            session = sqlalchemy.orm.sessionmaker()
            session.configure(bind=engine)
            self.session = session()
        return self.session