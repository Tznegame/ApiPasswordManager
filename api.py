import flask
from flask import request
from service.websiteservice import WebsiteService

app = flask.Flask(__name__)
app.config["DEBUG"] = True
webservice = WebsiteService("nome")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/get/website', methods=['GET'])
def api_get():
    query_parameters = request.args
    return webservice.visualizzaDati(cnx, key, query_parameters)

@app.route('/api/v1/add/website', methods=['POST'])
def api_add():
    query_parameters = request.json
    return webservice.aggiungiRecord(cnx, key, query_parameters)


@app.route('/api/v1/modify/website', methods=['PUT'])
def api_put():
    query_parameters = request.json
    return webservice.modificaRecord(cnx, key, query_parameters)

@app.route('/api/v1/delete/website', methods=['DELETE'])
def api_delete():
    query_parameters = request.json
    return webservice.eliminaRecord(cnx, key, query_parameters)
    
key = webservice.recuperaChiave()
cnx = webservice.api_startup()
print("Connection succed")

app.run()
