from pydantic import BaseModel

class CreateOrder(BaseModel):
    customer_name: str
    product_id: int
