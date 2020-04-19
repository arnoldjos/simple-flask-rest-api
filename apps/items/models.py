from sqlalchemy import func

from db import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def array_to_dict(cls, items):
        return [x.to_dict() for x in items]

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Item {self.name}"

    class Objects:
        @classmethod
        def create_item(cls, item_data: dict, to_dict: bool = True) -> dict:
            _item = Item(**item_data)
            item = cls.get_item_case_insensitive(_item.name)
            db.session.add(_item)
            db.session.commit()
            return item.to_dict() if to_dict else _item

        @classmethod
        def get_by_name(cls, name: str, to_dict: bool = True) -> dict:
            item = cls.get_item_case_insensitive(name)
            return item.to_dict() if to_dict and item else None

        @classmethod
        def delete_by_name(cls, name: str, to_dict: bool = True) -> dict:
            item = cls.get_item_case_insensitive(name)
            db.session.delete(item)
            db.session.commit()
            return item.to_dict() if to_dict else item

        @classmethod
        def update_by_name(cls, name: str, data: dict, to_dict: bool = True) -> dict:
            item = cls.get_item_case_insensitive(name)
            item.price = data.get("price")
            db.session.commit()
            return item.to_dict() if to_dict else item

        @classmethod
        def get_item_case_insensitive(cls, name):
            return Item.query.filter(func.lower(Item.name) == func.lower(name)).first_or_404(
                description="Item not found.")
