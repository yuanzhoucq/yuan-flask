import flask_restful as restful
from flask import Flask

app = Flask(__name__)
api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api')

if __name__ == '__main__':
    app.run(debug=True)
