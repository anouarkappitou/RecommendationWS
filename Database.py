import sqlite3
import turicreate as tc

#this should be refactored :)

DATABSE_PATH = "./database/db.sqlite3"

class Database( object ):

    instance = None

    user_col_name = "userId"
    item_col_name = "movieId"
    target_col_name = "rating"

    def instance():

        if( Database.instance is None ):
            Database.instance = sqlite3.connect( DATABASE_PATH )
        return Database.instance

    def turicreate_get_ratings():
        return tc.SFrame.create( Database.instance , "SELECT * FROM rating" );
