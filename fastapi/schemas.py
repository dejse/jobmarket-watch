"""Pydantic schemas for data validation"""
from pydantic import BaseModel
from datetime import date
from typing import Optional


class JobDataSchema(BaseModel):
    """Schema for job market data"""
    id: Optional[int] = None
    date: date
    location: str
    job_count: int
    
    class Config:
        from_attributes = True


class JobDataCreate(BaseModel):
    """Schema for creating job data"""
    date: date
    location: str
    job_count: int
