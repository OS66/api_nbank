from src.main.api.models.base_model import BaseModel


class LoginUserResponse(BaseModel):
    username: str
    role: str
