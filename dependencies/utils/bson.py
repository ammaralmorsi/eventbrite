from bson import ObjectId
from bson.errors import InvalidId

from fastapi import HTTPException
from fastapi import status


def convert_to_object_id(id_in: str) -> ObjectId:
    try:
        return ObjectId(id_in)
    except InvalidId:
        raise HTTPException(detail="invalid id", status_code=status.HTTP_400_BAD_REQUEST)
