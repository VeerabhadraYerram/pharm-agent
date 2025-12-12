from pydantic import BaseModel
from typing import Any


class CanonicalResult(BaseModel):
    data : Any | None = None