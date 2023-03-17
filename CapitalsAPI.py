# Imports
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import json
import re

class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

# Initialize App
app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/you')

api = Api(app)


@app.route("/")
def hello():
    return "Hello World from Flask"

# Limitations: API is case sensitive
class Capitals(Resource):
    # Only need GET for you.com, none of the other parts of REST
    def get(self):
        # Get argument
        args = request.args.get('Nations')
        # Set up wiki page
        wiki = "https://www.wikipedia.com/wiki/"
        # Load Data
        f = open("data.json")
        data = json.load(f)
        
        # Check if arguments are passed
        if args is not None:
            # Split arguments into list in order to account for nations like the United States
            args2 = args.split()
            found = False
            # Find nations in statements, i.e. "Capital of Japan" it'll just pass Japan as an argument
            for x in args2:
                if x in data['Nations']:
                    args = x
                    found = True
                    break
            # Check for two word countries
            if found == False:
                for i in range(0, len(args2)-1):
                    word = args2[i] + " " + args2[i+1]
                    if word in data['Nations']:
                        args = word
                        found == True
                        break
            # Check for three word countries
            if found == False:
                for i in range(0, len(args2)-2):
                    word = args2[i] + " " + args2[i+1] + " " + args2[i+2]
                    if word in data['Nations']:
                        args = word
                        found == True
                        break
            # Check if nation is in data set
            if args in list(data['Nations']):
                # Get capital name for wiki page
                capName = data['Nations'][args]['Capital']
                # Replace spaces with '_' to fit wiki url syntax
                capName2 = re.sub('\s+', '_', capName)
                wiki = wiki+capName2
                # Set up return dictionary
                dict2 = {'Nations': args}
                dict2['dataArr'] = [data['Nations'][args], {'Capital': wiki}]
                #dict2 = data['Nations'][args]
                #dict2['wiki'] = wiki
                # Return dictionary with status code 200 (OK)
                return dict2, 200
            else:
                # Nation not found with 404 status code
                return {'message': f"'{args}' nation not found."}, 404
               # return {'message': "Nation not Found"}, 404
        
        return data, 200

# '/country' is entry point
api.add_resource(Capitals, '/country', '/api/country')

# Run app
if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
