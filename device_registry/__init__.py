import markdown
import os
import shelve

# Import the framework
from flask import Flask, g, make_response, request
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
users = {'user1':'id=0',
        'user2':'id=1',
        'user3':'id=2',
        }

app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
        db['user'] = 'user'
        db['admin'] = 'admin'
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    if not request.cookies.get('access_level'):
        with open(os.path.dirname(app.root_path) + '/index.html', 'r') as markdown_file:

            content = markdown_file.read()

            return markdown.markdown(content)
    else:
        f = open(os.path.dirname(app.root_path)+'/device_registry/' + request.cookies.get('access_level') + '.html', 'r')
        res =  make_response(f.read())
        f.close()
        return res

class Users(Resource):
    user_db = {'admin':'admin','user':'user'}
    def get(self):
        if not request.cookies.get('access_level'):
            res = make_response("Please sign in")
        else:
            f = open(os.path.dirname(app.root_path) + '/device_registry/' + request.cookies.get('access_level') + '.html', 'r')
            res = make_response(f.read())
            f.close()
        return res
    
    def post(self):
        db = get_db()
        parser = reqparse.RequestParser()
        parser.add_argument('user')
        parser.add_argument('password')
        parser.add_argument('status')
        args = parser.parse_args()
        #authenticate or logout
        if args['status'] != None:
            res = make_response("Logged out")
            res.set_cookie('access_level','',max_age=0)
            return res
        if args['user'] in db and args['password'] == self.user_db[args['user']]:
            #check for cookies
            if not request.cookies.get('access_level'):
                f = open(os.path.dirname(app.root_path) +
                        '/device_registry/' + args['user'] + '.html', 'r')
                res = make_response(f.read())
                res.set_cookie('access_level', args['user'], max_age=60*60)
                # res.set_cookie('status',args['status'],max_age=900)
            else:
                f = open(os.path.dirname(app.root_path) +'/device_registry/' + args['user'] + '.html', 'r')
                res = make_response(f.read())
                f.close()
            return res
        else:
            return {'message': 'Failure', 'data': 'Not found'}, 404
'''
class User(Resource):

    def get(self, identifier):
        

        return {'message': 'Device found', 'data': users[identifier]}, 200
'''
'''
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
'''

'''
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
'''
api.add_resource(Users,'/users/')
# api.add_resource(DeviceList, '/devices')
# api.add_resource(User, '/user/<string:identifier>')
# api.add_resource(Device, '/device/<string:identifier>')
