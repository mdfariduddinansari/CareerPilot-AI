from typing import Any

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    success: bool = True
    data: Any = None
    message: str = 'OK'
    errors: list[str] = Field(default_factory=list)
