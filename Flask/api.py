from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


  
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_category = db.Column(db.String(80), unique=True, nullable=False)
    def __init__(self,product_id, product_name, product_category):
        self.product_id = product_id
        self.product_name = product_name
        self.product_category = product_category

    def __repr__(self):
        return '<Product Name %r>' % self.product_name

api = Api(app)
class ProductsList(Resource):
    def get(self):
        return jsonify([{
            "product_id": product.product_id, "product_name":product.product_name, "product_category":product.product_category
            } for product in Product.query.all()
        ])

class SingleProduct(Resource):
    def get(self, num):
        product=Product.query.filter_by(product_id=num).first_or_404()
        return jsonify([{
            "product_id": product.product_id, "product_name":product.product_name, "product_category":product.product_category
        }])


class NewProduct(Resource):
    def post(self):
        try:
            product_data = request.get_json()
            new_product=Product(product_data['product_name'], product_data['product_category'])
            db.session.add(new_product)
            db.session.commit()
            return {'message': 'Yaay!!!...Product Created Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}

class deleteProduct(Resource):
    def delete(self, num):
        try:
            product_data = Product.query.filter_by(product_id=num).first()
            db.session.delete(product_data)
            db.session.commit()
            return {'message': 'Yaay!!!...Product Deleted Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}

class UpdateProduct(Resource):
    def put(self,product_id):
        try:
            product_data=Product.query.filter_by(product_id=product_id).first()
            new_product = request.get_json()
            if new_product["product_name"]:
                product_data.product_name=new_product['product_name']
            if new_product["product_category"]:
                product_data.product_category =new_product['product_category']
            db.session.commit()
            return {'message': 'Yaay!!!....Product Updated Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}

    def patch(self,product_id):
        try:
            product_data = Product.query.filter_by(product_id=product_id).first()
            new_product = request.get_json()
            if new_product["product_name"]:
                product_data.product_name=new_product['product_name']
            if new_product["product_category"]:
                product_data.product_category = new_product['product_category']
            db.session.commit()
            return {'message': 'Yaay!!!....Product Updated Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}

  
api.add_resource(ProductsList, '/')
api.add_resource(SingleProduct, '/<int:num>')
api.add_resource(NewProduct, '/product')
api.add_resource(deleteProduct,"/delete/<int:num>")
api.add_resource(UpdateProduct,"/product/<int:product_id>")
 
# driver function
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug = True)