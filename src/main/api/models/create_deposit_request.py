from src.main.api.models.base_model import BaseModel
from typing import Any


class CreateDepositRequest(BaseModel):
    id: int
    balance: Any
