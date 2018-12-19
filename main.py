from flask import Flask
from flask import request
from RecommandationFactory import *
from SFrameFormatter import *
from Utils import *

app = Flask( __name__ );

@app.route( "/<algorithm>/<int:user_id>/<int:num_of_recommendations>" )
def recommand( algorithm , user_id , num_of_recommendations ):

    algo_instance = RecommendationFactory.create( algorithm );

    if( algo_instance is False ):
        response = create_notfound_json_response( message="algorithm not found" )
    else:
        items_id = [user_id]
        formater = SFrameFormatter( algo_instance.recommand( items_id , num_of_recommendations ) );
        response = Response( response=formater.to_json(),
                            status=200,
                            mimetype="application/json" )

    return response;
