from Database import *;
import turicreate as tc
from Utils import file_exists
from Cache import *
import time
        
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

class Recommendations( object ):

    def __init__( self ):
        self.model = None
        self.cached = False;

    def recommand( self , users_id = [] , num= 10 ):

        self._load_tc_dataset();

        self.load_model()

        return self.model.recommend( users_id )


    def is_cached( self ):
        return self.cached


    def set_cachable( self , cachable ):
        self.cached = cachable;


    def load_model( self ):

        loader = None

        if self.is_cached():
            loader = CachedModel()
        else:
            loader = PermanentModel()

        self.model = loader.load_model( self.model , self._model_name() , self.train )

    def _model_name( self ):
        raise Exception( "not implemented" )

    def _load_tc_dataset( self ):
        self.dataset = Database.getInstance().turicreate_get_ratings();

    def train( self ):
        raise Exception( "Not Implemented" );


class StoredModel( object ):

    def load_model( self , model , model_name , train ):
        raise Exception( "not implemented" );

class PermanentModel( StoredModel ):

    def load_model( self , model , model_name , train ):

         if model is None:

            model_path = "./models/%s" % model_name

            if not file_exists( model_path ):

                model = train()
                model.save( model_path )
            else:
                model = tc.load_model( model_path );

            return model



class CachedModel( StoredModel ):

    VALID_CACHE_TIME = 36000 # 10 HOURS

    def load_model( self , model , model_name , train ):

        if self.model is None:

            cache = Cache( CachedModelRecommendations.VALID_CACHE_TIME )

            model_path = cache.get_valid_model_path( model_name )

            if model_path is False:

                model = train()

                epoch = int( time.time() )

                trained_model_path = "./models/%s/%s" % ( epoch , model_name )

                model.save( trained_model_path )

                cache.save_cached_model_path( trained_model_path )
            else:
                model = tc.load_model( model_path );

            return model


class MatrixFactorization( Recommendations ):

    def _model_name( self ):
        return "MatrixFactorization"

    def train( self ):
        return tc.ranking_factorization_recommender.create( self.dataset ,
                                                            user_id=Database.user_col_name ,
                                                            target=Database.target_col_name,
                                                            item_id=Database.item_col_name );


# this model rank an item according to its similarity to other items
# observed for the user in question

class ItemSimilarity( Recommendations ):

    def _model_name( self ):
        return "ItemSimilarity"

    def train( self ):
        return tc.item_similarity_recommender.create( self.dataset ,
                                                            user_id=Database.user_col_name,
                                                            target=Database.target_col_name,
                                                            item_id=Database.item_col_name  );
    def recommand( self , items_id = [] , num= 10 ):

        self._load_tc_dataset();

        self.load_model()

        return self.model.recommend_from_interactions( items_id , k=num )



class ContentBased( Recommendations ):

    def _model_name( self ):
        return "ContentBased"

    def train( self ):

        return tc.item_content_recommender.create( self.dataset ,
                                                    user_id=Database.user_col_name,
                                                    target=Database.target_col_name,
                                                    item_id=Database.item_col_name,);

    def recommand( self , users_id = [] , num=10 ):

        self._load_tc_dataset();

        self.load_model()

        return self.model.recommend_from_iteractions( users_id , k=num );


class PopularityBased( Recommendations ):

    def _model_name( self ):
        return "PopularityBased"

    def train( self ):
         return tc.popularity_recommender.create( self.dataset ,
                                                user_id=Database.user_col_name ,
                                                item_id=Database.item_col_name ,
                                                target=Database.target_col_name )


class KMean( Recommendations ):

    def __model_name( self ):
        return "K-MeansClustering"

    def _load_dataset( self ):

        ratings = Database.getInstance().ratings();

        users = list( set([ int( x[0] ) for x in ratings ]) )
        movies = list( set ( [ int( x[1] ) for x in ratings ] ) )

        n_users = len( list( users ) )

        rating_matrix = dok_matrix( ( max( users ) , max(movies)  ) , dtype=np.float32 )

        for user in users:

            user_ratings = [x for x in ratings if user is int(x[0]) ]#filter( lambda x: x[0] == user  , ratings )

            for user_rating in user_ratings:

                rating_matrix[ user , int( user_rating[1] ) ] = int(user_rating[2]);

        self.k = int( ( n_users / 10 ) + 2 )

        self.rating_matrix = rating_matrix

    def load_model( self ):
        self.train();

    def train( self ):
        self.model = KMeans( n_clusters=self.k );
        self.model.fit( self.rating_matrix.tocsr() )
        print( self.model.labels_ )


    def recommand( self , users_id = [] , num = 10 ):
        self._load_dataset();
        self.train();
        print( self.model.labels_ )