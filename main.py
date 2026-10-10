from fastapi import FastAPI,Depends,HTTPException
from database import engine,SessionLocal,Base
import schemas
import models 
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)
app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield (db)
    finally:
        db.close()

@app.get("/health")
def check_health():
    return {'status':"ok"}

@app.post("/products")
def add_products(data:schemas.CreateProduct,db:Session=Depends(get_db)):
    new_product=models.Product(**data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return(new_product)

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    return (db.query(models.Product).all())

@app.put("/products/{id}")
def update_product(data:schemas.UpdateProduct,id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if product is None:
        raise HTTPException(status_code=404,detail='Product not found')
    data = product.model_dump(exclude_unset=True)
    for field,value in data.items():
        setattr(product,field,value)
    db.commit()
    db.refresh(product)
    return product 

@app.delete("/product/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if product is None:
        raise HTTPException(status_code=404,detail='Product not found')
    db.delete(product)
    db.commit()
    return{'status':'deleted'}

