from flask import Blueprint, jsonify, abort
from google.cloud import firestore, exceptions

fs = firestore.Client()

dev_api_print = Blueprint('devapi', __name__)


@dev_api_print.route('/', methods=['GET'])
def get_all_collections():

    dev_collection = fs.collection(u'dev')

    try:
        tags = dev_collection.get()
        response = {'dev': sorted([i.to_dict() for i in tags], key=lambda k: k['index'])}
        return jsonify(response)

    except exceptions.NotFound:
        abort(404)


@dev_api_print.errorhandler(404)
def error400(error):
    errorresponse = {'error': 'collection not found'}
    return jsonify(errorresponse), 404
