"""
Security Analyzer Service
Detects incidents from collected logs
"""

from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict


class SecurityAnalyzer:
    def __init__(self):
        self.failed_login_tracker = defaultdict(list)
        self.alerts = []

    def analyze_log(self, log: Dict) -> List[Dict]:
        triggered = []

        if log.get('event_type') == 'failed_login':
            triggered.extend(self._check_brute_force(log))

        if log.get('severity') == 'error':
            triggered.append({
                'title': 'Server Error Detected',
                'description': f"Error from {log.get('ip_address')}: {log.get('message')}",
                'severity': 'medium',
                'rule_name': 'server_error',
                'source_ip': log.get('ip_address')
            })

        return triggered

    def _check_brute_force(self, log: Dict) -> List[Dict]:
        ip = log.get('ip_address')
        if not ip:
            return []

        now = datetime.utcnow()
        self.failed_login_tracker[ip].append(now)
        # Keep only last 10 minutes
        self.failed_login_tracker[ip] = [
            t for t in self.failed_login_tracker[ip]
            if now - t <= timedelta(minutes=10)
        ]

        if len(self.failed_login_tracker[ip]) >= 5:
            return [{
                'title': 'Brute Force Attack Detected',
                'description': f"IP {ip} has {len(self.failed_login_tracker[ip])} failed login attempts in 10 minutes",
                'severity': 'high',
                'rule_name': 'brute_force',
                'source_ip': ip
            }]
        return []

    def reset_tracker(self):
        self.failed_login_tracker.clear()
