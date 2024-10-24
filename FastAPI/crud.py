from tables import DBProduct
from sqlalchemy.orm import Session
from schema import Product

def create_product(db: Session, product: Product):
    db_product =DBProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(DBProduct).all()

def get_product(db: Session, product_id: int):
    return db.query(DBProduct).where(DBProduct.product_id == product_id).first()

def delete_product(db: Session, product_id: int):
    db.delete(db.query(DBProduct).where(DBProduct.product_id == product_id).first())
    db.commit()
    return "Yaay!!!...Product Deleted Successfully"

def update_product(db: Session, product_id: int,product: Product ):
    data=db.query(DBProduct).where(DBProduct.product_id == product_id).first()
    data.product_name=product.product_name
    data.product_category=product.product_category
    db.add(data)
    db.commit()
    db.refresh(data)
    return "Yaay!!!...Product Updated Successfully"