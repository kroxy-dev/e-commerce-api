from pydantic import BaseModel,ConfigDict,EmailStr,Field,field_validator
from decimal import Decimal
from datetime import datetime
from enum import Enum 


class OrderStatus(str,Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"




class CreateUser(BaseModel):
    username:str=Field(min_length=3,max_length=20)
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)
    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()

class LoginUser(BaseModel):
    email:EmailStr
    password:str
    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    username:str
    email:EmailStr

class Token(BaseModel):
    access_token:str
    token_type:str

class CreateProduct(BaseModel):
    name: str
    description: str
    price: Decimal = Field(gt=0,max_digits=10,decimal_places=2)
    stock: int = Field(ge=0)
    image_url: str
    is_active: bool = True

class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None,gt=0,max_digits=10,decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    is_active: bool | None = None



class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str
    description:str
    price:Decimal
    stock:int
    image_url:str
    is_active:bool 


class AddCartItem(BaseModel):
    product_id:int 
    quantity:int=Field(gt=0)

class UpdateCartItem(BaseModel):
    quantity:int=Field(gt=0)

class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id:int
    quantity:int
    product_name:str
    unit_price: Decimal 

class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: Decimal


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id:int
    product_name:str
    quantity:int
    price:Decimal

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    items:list[OrderItemResponse]
    total_price:Decimal
    status:OrderStatus
    created_at: datetime


class CheckoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    checkout_url: str