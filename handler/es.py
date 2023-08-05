from flask import Blueprint
from middleware.authentication import Authentication
from datalayer.es import ElasticSearch_
from handler.response import articles
import flask
# them es vào tầng service

es = Blueprint("es", __name__)
authentication = Authentication()
elsearch = ElasticSearch_()
response = articles()


@es.route("/v2/articles", methods=["POST"])
@authentication.jwt_required_authentication
def add_data_to_es():

    elsearch.add_data()
    return response.add_success()


@es.route("/v2/articles", methods=["GET"])
@authentication.jwt_required_authentication
def search_document():

    data = flask.request.json

    field_name = data['field_name']
    query = data['query']

    result = elsearch.search_document(query, field_name)

    documents = []

    hits = result['hits']['hits']

    for hit in hits:
        documents.append(hit['_source'])

    return {
        "status": 200,
        "documents": documents
    }
