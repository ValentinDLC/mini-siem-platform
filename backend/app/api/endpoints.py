"""
API Endpoints for Mini SIEM Platform
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.app.core.database import get_db
from backend.app.models.database import LogEvent, Alert, Rule
from backend.app.schemas.siem_schemas import (
    LogEventCreate, LogEventResponse,
    AlertCreate, AlertResponse,
    RuleCreate, RuleResponse
)

router = APIRouter()


@router.post("/logs/", response_model=LogEventResponse)
def create_log(log: LogEventCreate, db: Session = Depends(get_db)):
    db_log = LogEvent(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/logs/", response_model=List[LogEventResponse])
def get_logs(
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    severity: Optional[str] = None,
    ip: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(LogEvent)
    if source:
        query = query.filter(LogEvent.source == source)
    if severity:
        query = query.filter(LogEvent.severity == severity)
    if ip:
        query = query.filter(LogEvent.ip_address == ip)
    return query.offset(skip).limit(limit).all()


@router.get("/logs/search/", response_model=List[LogEventResponse])
def search_logs(
    q: str = Query(..., description="Search term in message or raw_log"),
    db: Session = Depends(get_db)
):
    return db.query(LogEvent).filter(
        (LogEvent.message.contains(q)) | (LogEvent.raw_log.contains(q))
    ).all()


@router.post("/alerts/", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/alerts/", response_model=List[AlertResponse])
def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    return query.order_by(Alert.timestamp.desc()).all()


@router.put("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "acknowledged"
    db.commit()
    return {"message": "Alert acknowledged"}


@router.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    total_logs = db.query(LogEvent).count()
    total_alerts = db.query(Alert).count()
    open_alerts = db.query(Alert).filter(Alert.status == "open").count()
    critical_alerts = db.query(Alert).filter(Alert.severity == "critical").count()

    return {
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "critical_alerts": critical_alerts,
        "timestamp": datetime.utcnow()
    }
