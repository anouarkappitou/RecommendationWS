import json
from flask import Response
import os.path

# list of utils function 

def create_notfound_json_response( message ):
    return Response( response=json.dumps( { 'status': False,
                                            'message': message } ),
                                status=404,
                                mimetype="application/json" );


def file_exists( path ):
    return os.path.isdir( path )
