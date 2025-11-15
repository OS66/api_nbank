from src.main.api.models.base_model import BaseModel
from typing import Optional, Dict, List, Any

class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str]
    role: str
    accounts: List[Dict[Any, Any]]

