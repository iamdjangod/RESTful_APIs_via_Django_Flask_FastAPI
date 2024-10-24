from fastapi import FastAPI, Depends
from schema import Product
from tables import DBProduct
from crud import create_product, update_product, get_product, delete_product, get_products
from database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker, Session

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Insert the data into database table    
@app.post('/products')
async def create_products_view(product: Product, db: Session = Depends(get_db)):
    db_product = create_product(db, product)
    return db_product

# get all the list of products
@app.get('/products/')
async def get_products_view(db: Session = Depends(get_db)):
    return get_products(db)

# Get a particular product from database
@app.get('/product/{product_id}')
async def get_product_view(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)


# delete particular product from table
@app.delete('/product/{product_id}')
async def delete_product_view(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)

# update particular product
@app.put('/product/{product_id}')
async def update_product_view(product_id:int,product: Product, db: Session = Depends(get_db)):
    return update_product(db,product_id, product)
