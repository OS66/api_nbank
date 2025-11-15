from typing import Dict, Callable
from abc import ABC, abstractmethod

from src.main.api.models.base_model import BaseModel
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.configs.config import Config

class Requester(ABC):
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable):
        self.headers = request_spec.get('headers')
        self.base_url  = Config.get("backendUrl")
        self.response_spec = response_spec

    # @abstractmethod
    # def post(self, model:BaseModel): ...

    # @abstractmethod
    # def get(self, model:BaseModel): ...


