from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define the Item model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory database
items_db = []

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    # Check if the item with the same id already exists
    for db_item in items_db:
        if db_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(index)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")
