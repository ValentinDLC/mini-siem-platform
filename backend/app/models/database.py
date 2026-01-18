"""
Database models for Mini SIEM Platform
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class LogEvent(Base):
    __tablename__ = "log_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source = Column(String(50), index=True)
    event_type = Column(String(50), index=True)
    severity = Column(String(20), default="info", index=True)
    ip_address = Column(String(45), nullable=True, index=True)
    username = Column(String(100), nullable=True)
    message = Column(Text)
    raw_log = Column(Text)
    metadata = Column(JSON, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    title = Column(String(200))
    description = Column(Text)
    severity = Column(String(20), index=True)
    status = Column(String(20), default="open", index=True)
    source_ip = Column(String(45), nullable=True, index=True)
    rule_name = Column(String(100))
    log_event_id = Column(Integer, nullable=True)


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    enabled = Column(Boolean, default=True)
    severity = Column(String(20), default="medium")
    condition = Column(JSON)
