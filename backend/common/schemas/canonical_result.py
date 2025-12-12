from pydantic import BaseModel
from typing import Any


class CanonicalResult(BaseModel):
    summary: Any | None = None
    scores: Any | None = None