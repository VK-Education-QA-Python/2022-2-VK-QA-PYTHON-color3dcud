from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    name: Optional[str]
    surname: Optional[str]
    middle_name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
