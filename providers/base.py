from abc import ABC, abstractmethod
from typing import List, Dict
import requests

class BaseProvider(ABC):
    def __init__(self, settings: Dict):
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; job-scraper/1.0)'})
        self.timeout = settings.get('timeout', 10)
    
    @abstractmethod
    def get_jobs(self, company: str) -> List[Dict]:
        """Fetch jobs for a company. Must return list of job dicts."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return provider name."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if provider is enabled in settings."""
        return self.settings.get('enabled', True)