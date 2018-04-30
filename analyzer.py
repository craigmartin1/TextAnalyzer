import flask
from flask_restful import Api
app = Flask(__name__)
api = Api(app)

app.config.from_object(__name__)
app.config.from_envvar('CHAT_CONFIG', silent=True)

#Resource API AUTH
from API import resources
from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(resources.AnalyzeText, '/analyze')

#Routes
@app.route('/')
def main_page():
    return make_response(render_template('index.html'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for(main_page))

if __name__ == '__main__':
    app.run()