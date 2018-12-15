from flask import Flask
from flask import request
from RecommandationFactory import *

app = Flask( __name__ );

@app.route( "/<algorithm>/<int:user_id>/<int:num_of_recommendations>" )
def recommand( algorithm , user_id , num_of_recommendations ):

    algo_instance = RecommendationFactory.create( algorithm );

    return algo_instance.recommand( user_id , num_of_recommendations );

    #jsonify the recommandations
