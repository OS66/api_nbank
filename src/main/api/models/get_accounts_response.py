from src.main.api.models.base_model import BaseModel
from typing import Optional, Dict, List, Any

class GetAccountsResponse(BaseModel): 
    accounts: Optional[List[Dict[Any, Any]]]

