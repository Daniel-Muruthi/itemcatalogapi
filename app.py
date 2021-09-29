from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import uuid
import os


# This will initialize the app

app = Flask(__name__)

app.config['SECRET_KEY'] ='catalog123'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://moringa:muruthi1995@localhost/catalog'
app.config["DEBUG"] = True

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
    admin=db.Column(db.Boolean)

    @property
    def jsfrmt(self):
        '''
        Will return data in a json format
        '''
        return {
            'id' : self.id,
            'name': self.name,
            'public_id': 
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
def item():
    items = Item.query.all()

    all_items =[]

    for item in items:
        id = item['id']
        name = item['name']

    return jsonify({'items': all_items})

@app.route('/category', methods=['GET'])
def item():
    categories = Category.query.all()

    all_categories =[]

    for category in categories:
        id = item['id']
        name = item['name']


    return jsonify({'categories': all_categories})



if __name__=="__main__":
    app.run()
