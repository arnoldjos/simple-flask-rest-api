from flask import abort
from flask_restful import Resource, reqparse

from .models import Item


class SharedResource:
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field is required.")
    parser.add_argument("name", type=str, required=False, help="This field is required.")


class ItemResource(Resource, SharedResource):
    def get(self, name):
        item = Item.Objects.get_by_name(name)
        return ({"result": item}, 200) if item else abort(404, description="Item not found.")

    def delete(self, name):
        item = Item.Objects.delete_by_name(name)
        return {"result": item, "deleted": True}, 200

    def put(self, name):
        data = self.parser.parse_args()
        item = Item.Objects.update_by_name(name, data)
        return item, 200


class ItemListResource(Resource, SharedResource):
    def get(self):
        return {"result": Item.array_to_dict(Item.query.all())}

    def post(self):
        item = Item.Objects.create_item(self.parser.parse_args())
        return ({"result": item}, 201) if item else (self.error_handler("Item already exists.", 400))
