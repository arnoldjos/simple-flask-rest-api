from flask import Blueprint
from flask_restful import Api

from apps.items.resources import ItemResource, ItemListResource


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(ItemResource, "/items/<string:name>/")
api.add_resource(ItemListResource, "/items/")

