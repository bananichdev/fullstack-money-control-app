from datetime import date

from pydantic import BaseModel
from utils.enums import OperationType


class Operation(BaseModel):
    id: int
    account_id: int
    type: OperationType
    amount: float
    operation_date: date
