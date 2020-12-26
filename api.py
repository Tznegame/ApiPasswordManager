import flask
import json
from flask import request
from service.websiteservice import WebsiteService
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, InternalServerError

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

webservice = WebsiteService()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/get/website', methods=['GET'])
def api_get():
    query_parameters = request.args
    return webservice.visualizzaDati(query_parameters)


@app.route('/api/v1/add/website', methods=['POST'])
def api_add():
    query_parameters = request.json
    return webservice.aggiungiRecord(query_parameters)


@app.route('/api/v1/modify/website', methods=['PUT'])
def api_put():
    query_parameters = request.json
    return webservice.modificaRecord(query_parameters)


@app.route('/api/v1/delete/website', methods=['DELETE'])
def api_delete():
    query_parameters = request.json
    return webservice.eliminaRecord(query_parameters)


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


print("Connection active")

#app.run(host='192.168.1.2')
app.run()