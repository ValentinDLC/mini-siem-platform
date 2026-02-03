"""
Demo ingestion script
Collects sample logs, analyzes them, stores logs and alerts
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from backend.app.core.database import SessionLocal, init_db
from backend.app.models.database import LogEvent, Alert
from backend.app.services.log_collector import LogCollector
from backend.app.services.security_analyzer import SecurityAnalyzer


def main():
    init_db()
    db = SessionLocal()
    collector = LogCollector()
    analyzer = SecurityAnalyzer()

    sample_logs = [
        "Jul 22 10:00:00 server sshd[123]: Failed password for root from 192.168.1.50 port 22",
        "Jul 22 10:00:05 server sshd[124]: Failed password for root from 192.168.1.50 port 22",
        "Jul 22 10:00:10 server sshd[125]: Failed password for root from 192.168.1.50 port 22",
        "Jul 22 10:00:15 server sshd[126]: Failed password for root from 192.168.1.50 port 22",
        "Jul 22 10:00:20 server sshd[127]: Failed password for root from 192.168.1.50 port 22",
        "192.168.1.99 - - [22/Jul/2024:10:01:00 +0000] \"GET /admin HTTP/1.1\" 404 512",
        "192.168.1.99 - - [22/Jul/2024:10:01:01 +0000] \"POST /login HTTP/1.1\" 500 256",
    ]

    print("[*] Ingesting sample logs...")
    for line in sample_logs:
        parsed = collector.parse_line(line)
        if not parsed:
            continue

        log_event = LogEvent(**parsed)
        db.add(log_event)
        db.commit()
        db.refresh(log_event)

        alerts = analyzer.analyze_log(parsed)
        for alert in alerts:
            db_alert = Alert(
                title=alert['title'],
                description=alert['description'],
                severity=alert['severity'],
                rule_name=alert['rule_name'],
                source_ip=alert['source_ip'],
                log_event_id=log_event.id,
                status="open"
            )
            db.add(db_alert)
            print(f"[ALERT] {alert['severity'].upper()}: {alert['title']}")

    db.close()
    print("[*] Done. Start API with: uvicorn backend.app.main:app --reload")


if __name__ == "__main__":
    main()
