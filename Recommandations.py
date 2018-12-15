from Database import *;
import turicreate as tc
import sqlite3

class Recommendations( object ):

    def recommand( self , user_id , num= 10 ):
        raise Exception( "not implemented" )


    def _load_tc_dataset( self ):

        link = sqlite3.connect( "./database/db.sqlite3" )
        self.dataset = tc.SFrame.from_sql( link , "SELECT * FROM rating" )


class MatrixFactorization( Recommendations ):

    def recommand( self , user_id , num= 10 ):

        #load data from database
        self._load_tc_dataset();
        
        model = tc.ranking_factorization_recommender.create( self.dataset ,
                                                             user_id=Database.user_col_name ,
                                                             item_id=Database.item_col_name ,
                                                             target=Database.target_col_name );

        return model.recommend()

class ItemSimilarity( Recommendations ):

    def recommand( self , user_id , num=10 ):

        self._load_tc_dataset();

        model = tc.item_similarity_recommender.create( self.dataset ,
                                                       user_id=Database.user_col_name ,
                                                       item_id=Database.item_col_name  );

        return model.recommend();


class ContentBased( Recommendations ):

    def recommand( self , user_id , num=10 ):

        self._load_tc_dataset();

        model = tc.item_content_recommender.create( self.dataset ,
                                                    user_id='userId',
                                                    item_id='movieId',
                                                    );

        return model.recommend_from_iteractions([0]);


class PopularityBased( Recommendations ):

    def recommand( self , user_id , num= 10 ):

        self._load_tc_dataset();

        model = tc.popularity_recommender.create( self.dataset ,
                                                user_id=Database.user_col_name ,
                                                item_id=Database.item_col_name ,
                                                target=Database.target_col_name );

        return model.recommend();