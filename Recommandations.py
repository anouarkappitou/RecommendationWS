from Database import *;
import turicreate as tc

class Recommendations( object ):

    def recommand( self , user_id , num= 10 ):
        raise Exception( "not implemented" )


    def _load_tc_dataset( self ):
        self.dataset = Database.getInstance().turicreate_get_ratings();


    


class MatrixFactorization( Recommendations ):

    def recommand( self , user_id , num= 10 ):

        #load data from database
        self._load_tc_dataset();
        
        model = tc.ranking_factorization_recommender.create( self.dataset ,
                                                             user_id=Database.user_col_name ,
                                                             item_id=Database.item_col_name ,
                                                             target=Database.target_col_name );
        return model.recommend( k=num )

class ItemSimilarity( Recommendations ):

    def recommand( self , user_id , num=10 ):

        self._load_tc_dataset();

        model = tc.item_similarity_recommender.create( self.dataset ,
                                                       user_id=Database.user_col_name ,
                                                       item_id=Database.item_col_name  );

        return model.recommend( k=num )


class ContentBased( Recommendations ):

    def recommand( self , user_id , num=10 ):

        self._load_tc_dataset();

        model = tc.item_content_recommender.create( self.dataset ,
                                                    user_id=Database.user_col_name,
                                                    item_id=Database.item_col_name,
                                                    );

        return model.recommend_from_iteractions([0] , k=num );


class PopularityBased( Recommendations ):

    def recommand( self , user_id , num= 10 ):

        self._load_tc_dataset();

        model = tc.popularity_recommender.create( self.dataset ,
                                                user_id=Database.user_col_name ,
                                                item_id=Database.item_col_name ,
                                                target=Database.target_col_name );

        return model.recommend( k=num )
