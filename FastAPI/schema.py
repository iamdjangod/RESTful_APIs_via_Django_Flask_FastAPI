from typing import Optional, Set
from pydantic import BaseModel

class Product(BaseModel):
    product_name: str
    product_category: str
    
