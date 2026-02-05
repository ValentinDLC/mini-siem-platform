"""
Pydantic schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class LogEventCreate(BaseModel):
    source: str
    event_type: str
    severity: str = "info"
    ip_address: Optional[str] = None
    username: Optional[str] = None
    message: str
    raw_log: str
    log_metadata: Optional[Dict[str, Any]] = None


class LogEventResponse(LogEventCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class AlertCreate(BaseModel):
    title: str
    description: str
    severity: str = "medium"
    source_ip: Optional[str] = None
    rule_name: str
    log_event_id: Optional[int] = None


class AlertResponse(AlertCreate):
    id: int
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True


class RuleCreate(BaseModel):
    name: str
    description: str
    severity: str = "medium"
    condition: Dict[str, Any]


class RuleResponse(RuleCreate):
    id: int
    enabled: bool

    class Config:
        from_attributes = True
