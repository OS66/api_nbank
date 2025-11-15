from src.main.api.models.base_model import BaseModel
from typing import Optional, Dict, List, Any


class GetAccounts(BaseModel):
    accounts: Optional[List]