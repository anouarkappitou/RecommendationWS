import sqlite3
import turicreate as tc

#this should be refactored :)

DATABASE_PATH = "./database/db.sqlite3"

class Database:
    # Here will be the instance stored.
    __instance = None


    user_col_name = "userId"
    item_col_name = "movieId"
    target_col_name = "rating"

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Database.__instance == None:
            Database()
        return Database.__instance 

    def __init__(self):

        """ Virtually private constructor. """
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            self.__connect();

    def __connect( self ):
        self.__db_instance = sqlite3.connect( DATABASE_PATH )

    def turicreate_get_ratings(self):
        return tc.SFrame.from_sql( self.__db_instance , "SELECT * FROM ratings");

    def all_users( self ):

        crsr = self.__db_instance.cursor();

        crsr.execute( "SELECT id FROM users");

        result = crsr.fetchall();

        return result;

    def ratings( self ):

        crsr = self.__db_instance.cursor();

        crsr.execute( "SELECT * FROM ratings");

        result = crsr.fetchall();

        return result;
