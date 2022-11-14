# python native imports
from dataclasses import dataclass


@dataclass
class User:
    uid: int
    first_name: str
    last_name: str
    email: str
    registered: bool