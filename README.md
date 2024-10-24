# RESTful APIs via Django, Flask and FastAPI

CRUD operations via Django, Flask and FastAPI (All Python Web Frameworks)


## Django Rest Framework
    DRF APIs follows industry-standard way for web services to send and receive data. Uses HTTP request methods to facilitate the request-response cycle and typically transfer data using JSON, and more rarely - HTML, XML and other formats
  
## Flask 
    Flask is a popular micro framework for building web applications. Since it is a micro-framework, it is very easy to use but lacks most of the advanced functionalities found in a full-fledged framework.
  
## FastAPI
    FastAPI is a modern, python-based high-performance web framework used to create RESTful APIs. Its key feature is speed, fewer bugs, easy to use, and production-friendly.
  
### Comparison between Django(DRF), Flask and FastAPI

1. <h4>Packages</h4>
    Comparing Django(DRF), Flask, and FastAPI; Django(DRF) has the most packages that enable reusability of code. It is a full-stack web development framework, unlike Flask and FastAPI, that are minimalistic frameworks used for building fast websites.

2. <h4>Community</h4>
    Django has the most significant community because of its wide use and popularity next to Flask, which also has a thriving community. FastAPI, on the other hand, has a small community because it’s relatively new.

3. <h4>Performance</h4>
    In performance, FastAPI comes first because it is speed-oriented, then next to Flask, and finally Django(DRF), which is not as fast as the other two.

4. <h4>Flexibility</h4>
    Flexibility is something developers value a lot, and Flask is more flexible than Django(DRF). FastAPI, on the other hand is flexible code-wise and doesn’t restrict the code layout. So we can say Flask is the most flexible among all three.

Lets dive into the codebase on how to build CRUD in the three different frameworks:

## Advisable You create a virtual environment before installing packages.

# python -m venv virtual_env_name
 
## Django(DRF)

Requirements  
```python
pip install django 
pip install djangorestframework
```

Step 1:
  After installing the packages mentioned above run the below command to create django project 
  <br>
  **Note: A project can have multiple apps but vice versa is not true.**
  ```
  django-admin startproject app #app is project name
  ```
Step 2:
    go inside project and run the below command to create an app (v1_api)
  ```
  python manage.py startapp v1_api #v1_api is app name
  ```
  
Step 3
    Registor the app -> Go to settings.py file in INSTALLED_APPS section add app name ('rest_framework','v1_api',)
 
 ```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'v1_api',
```
Step 4:
    Create models and Serializer

models.py
```python
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=80)
    product_category = models.CharField(max_length=80, default="") 

    def __str__(self):
        return self.product_name
        
```

serializer.py
```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_category')
```

Step 5:
     Logic for CRUD operations in views.py file
   
Step 6:
    Decleared the end-point in app.urls file after that we need to include in project urls.py (app.ulrs)

```python
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.product_list, name='product_list'),
]
```

app.urls
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1_api/', include('v1_api.urls')),
]
```

## Flask

Requirement
```python
pip install Flask
pip install Flask-RESTful
pip install Flask-SQLAlchemy
```

Step 1:
    imported all the required modules
```python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
```
Step2:
1. Initializing instance of flask app by declaring 
```python
app = Flask(__name__)
```

Step3:
    Configured and Creating Database
```python
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```
Step 4:
1. moving a step ahead by creating our model
```python
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_category = db.Column(db.String(80), unique=True, nullable=False)
    def __init__(self,name, dob):
        self.product_name = product_name
        self.product_category = product_category

    def __repr__(self):
        return '<Product Name %r>' % self.product_name
```
Step 5:
    List all the records
```python
api = Api(app)
class ProductsList(Resource):
    def get(self):
        return jsonify([{
            "product_id": product.product_id, 'product_name':product.product_name, "product_category":product.product_category
            } for product in Product.query.all()
        ])
```
Single record
```python
class SingleProduct(Resource):
    def get(self, num):
        product=Product.query.filter_by(id=num).first_or_404()
        return jsonify([{
            "product_id": product.product_id, 'product_name':product.product_name, "product_category":product.product_category
        }])
```
Inserting New record
```python
class NewProduct(Resource):
    def post(self):
        try:
            product_data = request.get_json()
            new_product=Product(product_data['product_name'],product_data['product_category'])
            db.session.add(new_product)
            db.session.commit()
            return {'message': 'Yaay!!!...Product Created Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}
```
Deleting particular record from the table
```python
class deleteProduct(Resource):
    def delete(self, num):
        try:
            product_data = Product.query.filter_by(product_id=num).first()
            db.session.delete(product_data)
            db.session.commit()
            return {'message': 'Yaay!!!...Product Deleted Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}
```
Updating existing record 
```python
class UpdateProduct(Resource):
    def put(self,product_id):
        try:
            get_product=Product.query.filter_by(product_id=product_id).first()
            product_data = request.get_json()
            if product_data['product_name']:
                get_product.product_name = product_data['product_name']
            if product_data["product_category"]:
                get_product.product_category = product_data['product_category']
            db.session.commit()
            return {'message': 'Yaay!!!....Product Updated Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}

    def patch(self,product_id):
        try:
            get_product=Product.query.filter_by(product_id=product_id).first()
            product_data = request.get_json()
            if product_data['product_name']:
                get_product.product_name = product_data['product_name']
            if product_data["product_category"]:
                get_product.product_category =product_data['product_category']
            db.session.commit()
            return {'message': 'Yaay!!!....Product Updated Successfully'}
        except:
            return {'message': 'Oops!!!...Something went wrong'}
```
step 7:
    End points 
```python
api.add_resource(ProductsList, '/')
api.add_resource(SingleProduct, '/<int:num>')
api.add_resource(NewProduct, '/product')
api.add_resource(deleteProduct,"/delete/<int:num>")
api.add_resource(UpdateProduct,"/product/<int:product_id>")
 ```
 
## FastAPI

Requirements
```python
pip install fastapi
pip install uvicorn
```

Step 1:
Connection with database done in database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

Step 2:
Create model in models.py 
```python
from sqlalchemy import Column, String, Integer
from database import Base
# A SQLAlchemny ORM Product
class DBProduct(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(80))
    product_category = Column(String(80))
```
Step 3:
All the logics are written in CRUD.py file


Refrences

    https://www.djangoproject.com/
    https://www.django-rest-framework.org/
    https://flask.palletsprojects.com/en/2.0.x/
    https://flask-restful.readthedocs.io/en/latest/
    https://fastapi.tiangolo.com/



Muchas Gracies!!!
- Djangod.

