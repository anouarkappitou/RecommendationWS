from Recommandations import *

class RecommendationFactory( object ):

    @staticmethod
    def create( algorithm_name ):

        algorithms = {
            "ItemSimilarity":  ItemSimilarity,
            "ContentBased" : ContentBased,
            "MatrixFactorization": MatrixFactorization,
            "KMean": KMean
        }

        ctor = algorithms.get( algorithm_name , lambda: False );

        return ctor();
