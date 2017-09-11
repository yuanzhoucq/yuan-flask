import flask_restful as restful
from flask import Flask, redirect

from FlaskProject.Transpole import Transpole

app = Flask(__name__)
api = restful.Api(app)


@app.route('/', methods=['GET'])
def index():
    return redirect('/web/')


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api/')
api.add_resource(Transpole, '/api/transpole/<string:line>/<string:direction>/<int:start_station>')

if __name__ == '__main__':
    app.run(debug=True)
