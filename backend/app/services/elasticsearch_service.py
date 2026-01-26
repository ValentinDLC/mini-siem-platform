"""
Elasticsearch Service
Indexes logs for fast search and analytics (Kibana compatible)
"""

from typing import Dict, List, Optional
from datetime import datetime
from backend.app.core.config import settings


class ElasticsearchService:
    def __init__(self):
        self.index_name = "siem-logs"
        try:
            from elasticsearch import Elasticsearch
            self.es = Elasticsearch(settings.elasticsearch_url)
            self.enabled = True
        except Exception as e:
            print(f"[!] Elasticsearch unavailable: {e}")
            self.enabled = False

    def create_index(self):
        if not self.enabled:
            return
        if not self.es.indices.exists(index=self.index_name):
            mapping = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "source": {"type": "keyword"},
                        "event_type": {"type": "keyword"},
                        "severity": {"type": "keyword"},
                        "ip_address": {"type": "ip"},
                        "message": {"type": "text"},
                        "raw_log": {"type": "text"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mapping)

    def index_log(self, log: Dict):
        if not self.enabled:
            return
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            **log
        }
        self.es.index(index=self.index_name, document=doc)

    def search(self, query: str, size: int = 100) -> List[Dict]:
        if not self.enabled:
            return []
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["message", "raw_log", "ip_address"]
                }
            },
            "size": size
        }
        result = self.es.search(index=self.index_name, body=body)
        return [hit["_source"] for hit in result["hits"]["hits"]]
