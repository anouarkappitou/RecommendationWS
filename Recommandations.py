from Database import *;
import turicreate as tc
from Utils import file_exists
from Cache import *
import time

class Recommendations( object ):

    def __init__( self ):
        self.model = None

    def recommand( self , user_id , num= 10 ):

        self._load_tc_dataset();

        self.load_model()

        return self.model.recommend( k=num )


    def load_model( self ):

         if self.model is None:

            model_name = self._model_name()

            model_path = "./models/%s" % model_name

            if not file_exists( model_path ):
                self.train()
                self.model.save( model_path )
            else:
                self.model = tc.load_model( model_path );

    def _model_name( self ):
        raise Exception( "not implemented" )

    def _load_tc_dataset( self ):
        self.dataset = Database.getInstance().turicreate_get_ratings();

    def train( self ):
        raise Exception( "Not Implemented" );


class CachedModelRecommendations( Recommendations ):

    VALID_CACHE_TIME = 36000 # 10 HOURS

    def load_model( self ):

        if self.model is None:

            model_name = self._model_name()

            cache = Cache( CachedModelRecommendations.VALID_CACHE_TIME )

            model_path = cache.get_valid_model_path( model_name )

            if model_path is False:

                self.train()

                epoch = int( time.time() )

                trained_model_path = "./models/%s/%s" % ( epoch , model_name )

                self.model.save( trained_model_path )

                cache.save_cached_model_path( trained_model_path )
            else:
                self.model = tc.load_model( model_path );


class MatrixFactorization( CachedModelRecommendations ):

    def _model_name( self ):
        return "MatrixFactorization"

    def train( self ):
        self.model = tc.ranking_factorization_recommender.create( self.dataset ,
                                                             user_id=Database.user_col_name ,
                                                             item_id=Database.item_col_name );


class ItemSimilarity( CachedModelRecommendations ):

    def _model_name( self ):
        return "ItemSimilarity"

    def train( self ):
        self.model = tc.item_similarity_recommender.create( self.dataset ,
                                                            user_id=Database.user_col_name,
                                                            item_id=Database.item_col_name  );


class ContentBased( Recommendations ):

    def _model_name( self ):
        return "ContentBased"

    def train( self ):
        self.model = tc.item_content_recommender.create( self.dataset ,
                                                    user_id=Database.user_col_name,
                                                    item_id=Database.item_col_name,
                                                    );
    def recommand( self , user_id , num=10 ):

        self._load_tc_dataset();

        self.load_model()

        return self.model.recommend_from_iteractions([0] , k=num );


class PopularityBased( Recommendations ):

    def _model_name( self ):
        return "PopularityBased"

    def train( self ):
         self.model = tc.popularity_recommender.create( self.dataset ,
                                                user_id=Database.user_col_name ,
                                                item_id=Database.item_col_name ,
                                                target=Database.target_col_name )
