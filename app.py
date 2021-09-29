from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os


# This will initialize the app

app = Flask(__name__)

app.config['SECRET_KEY'] ='catalog123'

# configure sql
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://moringa:muruthi1995@localhost/catalog'
app.config["DEBUG"] = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

api = Api(app)
db = SQLAlchemy(app)

###################################################################
items = [
    {
        'id': 1,
        'name': 'colgate',
        'description': 'Your favorite toothpaste',
        'imageurl': "https://www.seekpng.com/ipng/u2q8u2o0u2q8y3y3_colgate-png-image-colgate-strong-teeth-toothpaste/",
        'price':230 
    }
]
###################################################################

# db model for users

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    public_id=db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    @property
    def jsfrmt(self):
        '''
        Will return data in a json format
        '''
        return {
            'id' : self.id,
            'name': self.name,
            'public_id': self.public_id,
            'email': self.email,
            'password': self.password,

        }


#db model for item categories

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    @property
    def jsfrmt(self):
        '''
        Will return data in a json format
        '''
        return {
            'id' : self.id,
            'name': self.name
        }

# db Model for items
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    imageurl = db.Column(db.String(255))
    price = db.Column(db.Integer)

    @property
    def jsfrmt(self):
        '''
        Will return data in a json format
        '''
        return {
            'id' : self.id,
            'name': self.name,
            'description': self.description,
            'imageurl' : self.imageurl,
            'price' : self.price
        }


###########Routes####################

@app.route('/user', methods=['GET'])
def user():
    users = User.query.all()

    all_users =[]

    for item in items:
        name_list = {}
        name_list.id = item['id']
        name_list.name = item['name']
        name_list.description = item['description']
        name_list.imageurl = item['imageurl']
        name_list.price = item['price']

        all_users.append(name_list)

    return jsonify({'items': all_users})

@app.route('/user', method=['POST'])
def create_user():
    data = request.get_json()

    passcode = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password = passcode, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New User successfully created'})

@app.route('/items', methods=['GET'])
def item():
    items = Item.query.all()

    all_items =[]

    for item in items:
        item_list = {}
        item_list.id = item['id']
        item_list.name = item['name']
        item_list.description = item['description']
        item_list.imageurl = item['imageurl']
        item_list.price = item['price']

        all_items.append(item_list)

    return jsonify({'items': all_items})

@app.route('/category', methods=['GET'])
def category():
    categories = Category.query.all()

    all_categories =[]

    for category in categories:
        category_list = {}
        category_list.id = category['id']
        category_list.name = category['name']

        all_categories.append(category_list)


    return jsonify({'categories': all_categories})



if __name__=="__main__":
    app.run()
