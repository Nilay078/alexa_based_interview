from sqlalchemy import create_engine

print("in dao __init__")


class DatabaseConnection:
    def connectDatabase(self):
        print('in connectDatabase')
        engine = create_engine(
            'mysql+pymysql://root:root12345@database-1.cagxrz2nrfum.us-east-1.rds.amazonaws.com/pythondb')

        return engine


databaseConnection = DatabaseConnection()
engine = databaseConnection.connectDatabase()
