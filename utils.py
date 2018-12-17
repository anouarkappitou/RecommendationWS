import json
from flask import Response

# list of utils function 

def create_notfound_json_response( message ):
    return Response( response=json.dumps( { 'status': False,
                                            'message': message } ),
                                status=404,
                                mimetype="application/json" );
