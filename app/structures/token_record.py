# python native imports
from dataclasses import dataclass


@dataclass
class TokenRecord:
    token: str
    email: str
    issued_epoch: str