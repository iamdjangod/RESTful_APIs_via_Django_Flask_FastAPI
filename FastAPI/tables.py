from sqlalchemy import Column, String, Integer
from database import Base



# A SQLAlchemny ORM Product
class DBProduct(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name= Column(String(80))
    product_category = Column(String(80))