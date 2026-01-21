"""
Log Collector Service
Collects logs from various sources (files, syslog, API)
"""

import time
import re
from typing import Dict, List, Optional
from datetime import datetime


class LogCollector:
    SSH_PATTERN = re.compile(
        r'(?P<timestamp>.*?)\s+.*sshd\[\d+\]:\s+(?P<message>.*)'
    )

    APACHE_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp>.*?)\]\s+"(?P<method>\w+)\s+(?P<url>.*?)\s+HTTP/.*?"\s+(?P<status>\d+)'
    )

    def parse_ssh(self, line: str) -> Optional[Dict]:
        match = self.SSH_PATTERN.search(line)
        if not match:
            return None

        message = match.group('message')
        event_type = 'info'
        severity = 'info'

        if 'Failed password' in message:
            event_type = 'failed_login'
            severity = 'warning'
        elif 'Accepted password' in message:
            event_type = 'successful_login'
            severity = 'info'
        elif 'Invalid user' in message:
            event_type = 'invalid_user'
            severity = 'warning'

        ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', message)
        ip = ip_match.group(1) if ip_match else None

        return {
            'source': 'ssh',
            'event_type': event_type,
            'severity': severity,
            'ip_address': ip,
            'message': message,
            'raw_log': line
        }

    def parse_apache(self, line: str) -> Optional[Dict]:
        match = self.APACHE_PATTERN.search(line)
        if not match:
            return None

        status = int(match.group('status'))
        severity = 'info'
        if status >= 500:
            severity = 'error'
        elif status >= 400:
            severity = 'warning'

        return {
            'source': 'apache',
            'event_type': 'http_request',
            'severity': severity,
            'ip_address': match.group('ip'),
            'message': f"{match.group('method')} {match.group('url')} -> {status}",
            'raw_log': line
        }

    def parse_line(self, line: str, source: str = 'auto') -> Optional[Dict]:
        if source == 'ssh' or (source == 'auto' and 'sshd' in line):
            return self.parse_ssh(line)
        elif source == 'apache' or (source == 'auto' and re.match(r'\d+\.\d+\.\d+\.\d+', line)):
            return self.parse_apache(line)
        return None

    def read_file(self, filepath: str, source: str = 'auto') -> List[Dict]:
        logs = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parsed = self.parse_line(line.strip(), source)
                    if parsed:
                        logs.append(parsed)
        except FileNotFoundError:
            print(f"[!] File not found: {filepath}")
        return logs

    def tail_file(self, filepath: str, callback, source: str = 'auto'):
        """Simulate real-time log streaming"""
        try:
            with open(filepath, 'r') as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        parsed = self.parse_line(line.strip(), source)
                        if parsed:
                            callback(parsed)
                    else:
                        time.sleep(0.5)
        except KeyboardInterrupt:
            print("[*] Stopping collector")
