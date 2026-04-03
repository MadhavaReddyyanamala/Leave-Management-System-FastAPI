from datetime import date
from pydantic import BaseModel, EmailStr, field_validator


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str

    @field_validator("end_date")
    @classmethod
    def end_date_must_be_valid(cls, v, info):
        start_date = info.data.get("start_date")
        if start_date and v < start_date:
            raise ValueError("End date cannot be earlier than start date")
        return v


class LeaveUpdate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str

    @field_validator("end_date")
    @classmethod
    def end_date_must_be_valid(cls, v, info):
        start_date = info.data.get("start_date")
        if start_date and v < start_date:
            raise ValueError("End date cannot be earlier than start date")
        return v


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str 
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str

    class Config:
        from_attributes = True