from datetime import datetime
from pydantic import BaseModel


class ReportRequest(BaseModel):
    sickness_id: list[int] | tuple = None
    city_id: list[int] | tuple = None
    state_id: list[int] | tuple = None
    start_date: datetime
    end_date: datetime
