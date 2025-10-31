from typing import Any, Dict, Optional

from src.main.api.models.base_model import BaseModel


class UpdateProfileResponse(BaseModel):
    customer: Dict[str, Any]
    message: Optional[str] = None
