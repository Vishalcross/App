import markdown
import os
import shelve

# Import the framework
from flask import Flask, g, make_response, request
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    if not request.cookies.get('access_level'):
        with open(os.path.dirname(app.root_path) + '/test.html', 'r') as markdown_file:

            content = markdown_file.read()

            return markdown.markdown(content)
    else:
        f = open(os.path.dirname(app.root_path)+'/device_registry/' + request.cookies.get('access_level') + '.html', 'r')
        res =  make_response(f.read())
        f.close()
        return res

class Users(Resource):
    user_db = {'admin':'admin','user':'user'}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user',required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        #authenticate
        if args['user'] in self.user_db and args['password'] == self.user_db[args['user']]:
            #check for cookies
            if not request.cookies.get('access_level'):
                f = open(os.path.dirname(app.root_path) +
                        '/device_registry/' + args['user'] + '.html', 'r')
                res = make_response(f.read())
                res.set_cookie('access_level', args['user'], max_age=60*60)
            else:
                f = open(os.path.dirname(app.root_path) +'/device_registry/' + args['user'] + '.html', 'r')
                res = make_response(f.read())
                f.close()
            return res
        else:
            return {'message': 'Failure', 'data': 'Not found'}, 404

class DeviceList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 201


class Device(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        return {'message': 'Device found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204

api.add_resource(Users,'/users/')
api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
