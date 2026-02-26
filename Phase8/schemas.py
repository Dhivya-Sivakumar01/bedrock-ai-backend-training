from typing import Literal
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    role: Literal["Engineer", "Associate Engineer"]


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int