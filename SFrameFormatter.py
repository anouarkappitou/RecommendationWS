import json

class SFrameFormatter( object ):

    def __init__( self , recommendations ):

        self.recommendations = recommendations;

    def to_json( self ):

        recommendations = self.recommendations;

        return json.dumps({"movies": list(recommendations["movieId"]), "score": list(recommendations["score"])})

