import sqlite3

class Cache( object ):

    def __init__( self , cache_time ):

        self.cache_time = cache_time
        self.db = sqlite3.connect( ":memory:" )
        self.create_cache_table()

    def create_cache_table( self ):

        cursor = self.db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cache( id int NOT NULL,
                                                            timestamp int,
                                                            path varchar( 255 ),
                                                            PRIMARY KEY( id )''' )
        cursor.commit();


    def get_valid_model_path( self , model_name ):

        #query cache table

        query = "SELECT path FROM cache WHERE %d - timestamp  > 0" % self.cache_time;

        cursor = self.db.cursor()

        cursor.execute( query )

        return cursor.fetchone()[0]

    def save_cached_model_path( self , epoch , model_path ):

        tupl = []

        tupl[0] = epoch
        tupl[1] = model_path

        query = "INSERT INTO cache( timestamp , path ) VALUES (?,?)"

        cursor = self.db.cursor()

        cursor.execute( query , tupl )

        return cursor.commit()

