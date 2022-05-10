import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from data import users, offers, orders
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(30))


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offers(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def main():
    db.create_all()
    insert_data()
    app.run(debug=True)


def insert_data():
    new_users = []
    new_offers = []
    new_orders = []
    for user in users:
        new_users.append(
            User(
                id=user['id'],
                first_name=user["first_name"],
                last_name=user["last_name"],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
        )
    for order in orders:
        new_orders.append(
            Orders(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
        )
    for offer in offers:
        new_orders.append(
            Offers(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
        )
    with db.session.begin():
        db.session.add_all(new_users)
        db.session.add_all(new_offers)
        db.session.add_all(new_orders)


@app.route('/', methods=['GET', 'POST'])
def orders_index():
    if request.method == 'GET':
        data = []
        for order in Orders.query.all():
            data.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id,
            })
        return jsonify(data)


if __name__ == "__main__":
    main()
