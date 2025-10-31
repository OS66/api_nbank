from typing import Union

from src.main.api.models.base_model import BaseModel


class CreateTransferRequest(BaseModel):
    senderAccountId: int
    receiverAccountId: int
    amount: Union[int, float]
