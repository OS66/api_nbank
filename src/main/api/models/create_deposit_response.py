from src.main.api.models.base_model import BaseModel


class CreateDepositResponse(BaseModel):
    balance: float
