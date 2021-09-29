from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from . import main
from app.models import User, Category, Item
from app import db

@main.route('/signup', methods= ['POST'])
def create_user():
    data = request.get_json()
    if data:
        hashed_password = generate_password_hash(data['password'])
        public_id=str(uuid.uuid4())
        name=str(data['name'])
        email=str(data['email'])

        new_user = User(public_id=public_id,name=name,  email=email, password = hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New User successfully created'})

    return jsonify({'message': 'Data is empty'})

@main.route('/items', methods=['GET'])
def item():
    items = Item.query.all()

    all_items =[]

    for item in items:
        item_list = {}
        item_list['id'] = item.id
        item_list['product_name'] = item.product_name
        item_list['description'] = item.description
        item_list['imageurl'] = item.imageurl
        item_list['price'] = item.price

        all_items.append(item_list)

    return jsonify({'items': all_items})

#get one item
@main.route('/item/<product_name>', methods=['GET'])
def get_one_item(product_name):
    item = Item.query.filter_by(product_name=product_name).first()
    
    if not item:
        return jsonify({'message': 'Your Item is out of stock!'})
    item_list = {}
    item_list['product_name'] = item.product_name
    item_list['description'] = item.description
    item_list['imageurl'] = item.imageurl
    item_list['price'] = item.price
    
    
    return jsonify({'item' : item_list })

@main.route('/category', methods=['GET'])
def category():
    categories = Category.query.all()

    all_categories =[]

    for category in categories:
        category_list = {}
        category_list['id'] = category.id
        category_list['name'] = category.name

        all_categories.append(category_list)


    return jsonify({'categories': all_categories})

@main.route('/category/all', methods=['POST'])
def all_categories():
    categories = Category.query.all()

    if not categories:
        return jsonify({'message': 'There are no categories!'})
        
    db.session.commit()

    return jsonify({'message': 'No categories have been added'})

@main.route('/user/<public_id>', methods=['DELETE'])
def deleteuser(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User you are trying to delete does not exist'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User has been successfully deleted'})