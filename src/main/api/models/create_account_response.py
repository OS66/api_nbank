from src.main.api.models.base_model import BaseModel
from typing import List

class CreateAccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List