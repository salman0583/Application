import oracledb
import configparser
 
 
class tsbdb:
 
    def __init__(self, dbConfig):
        self.dbConfig = dbConfig
        self.connect()
 
    def connect(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.connection = oracledb.connect(
            user=config.get("Database", "username"),
            password=config.get("Database", "password"),
            dsn=config.get("Database", "dsn"),
        )
 
def database_connect():
    # Read database configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    dbConfig = {
        "username": config.get("Database", "username"),
        "password": config.get("Database", "password"),
        "dsn": config.get("Database", "dsn"),
    }
 
    # Create an instance of tsbdb class
    tsb_db = tsbdb(dbConfig)
    return tsb_db