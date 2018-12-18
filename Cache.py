import sqlite3
import time

class Cache( object ):

    __instance = None

    def __new__(cls, arg):
        if Cache.__instance is not None:
            return Cache.__instance
        Cache.__instance = object.__new__(cls)
        Cache.__instance.db = sqlite3.connect(":memory:")
        return Cache.__instance

    def __init__( self , cache_time ):
        self.cache_time = cache_time
        self.create_cache_table()

    def create_cache_table( self ):

        cursor = self.db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cache( id INTEGER,
                                                            time timestamp default (strftime('%s', 'now')), 
                                                            path varchar( 255 ),
                                                            PRIMARY KEY( id ))''' )
        self.db.commit();


    def get_valid_model_path( self , model_name ):

        #query cache table
        
        query = "SELECT path FROM cache WHERE strftime('%s' , 'now' ) - time < 36000 AND instr( path ,'" + model_name + "' ) > 0"; 

        print( query )

        cursor = self.db.cursor()

        cursor.execute( query )

        row = cursor.fetchone()

        if row is None:
            return False

        return row[0]

    def save_cached_model_path( self , model_path ):

        tupl = []
        tupl.append( model_path )

        query = "INSERT INTO cache( path ) VALUES (?)"

        cursor = self.db.cursor()

        cursor.execute( query , tupl )

        return self.db.commit()

