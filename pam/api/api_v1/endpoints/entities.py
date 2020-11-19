from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

router = APIRouter()


@router.get("/", tags=["entities"])
def read_root():
    return {"Hello": "World"}


@router.get("/entities/{item_id}", tags=["entities"])
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
