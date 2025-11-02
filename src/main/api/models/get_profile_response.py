from pydantic import BaseModel

class GetProfileResponse(BaseModel):
    username: str
    password: str
    role: str
