from typing import List, Dict
from providers.base import BaseProvider

class ExperimentalJobrightLikeProvider(BaseProvider):
    """
    EXPERIMENTAL PROVIDER - DISABLED BY DEFAULT
    
    WARNING: This provider may scrape sites that have Terms of Service
    restrictions on automated access. Review ToS before enabling.
    
    This is a stub implementation for demonstration purposes only.
    """
    
    @property
    def provider_name(self) -> str:
        return "experimental_jobright_like"
    
    def get_jobs(self, company: str) -> List[Dict]:
        """Experimental job fetching - REQUIRES ToS REVIEW."""
        
        if self.is_enabled():
            print("⚠️  WARNING: Experimental provider enabled!")
            print("⚠️  Please ensure compliance with target site Terms of Service")
            print("⚠️  This provider is for demonstration only")
        
        # Stub implementation - would need actual scraping logic
        # that respects robots.txt and ToS
        return []
    
    def is_enabled(self) -> bool:
        """Override to add ToS warning."""
        enabled = super().is_enabled()
        if enabled:
            print("🚨 EXPERIMENTAL PROVIDER ENABLED - REVIEW ToS COMPLIANCE 🚨")
        return enabled