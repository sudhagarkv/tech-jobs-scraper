from typing import List, Dict
from utils import is_relevant_job

class JobFilter:
    def __init__(self, settings: Dict):
        self.settings = settings
    
    def categorize_role(self, title: str) -> str:
        """Categorize job role based on title - use stored classification."""
        # This will be set by the filtering process
        return 'SWE'  # Default fallback
    
    def determine_level(self, title: str, description: str) -> str:
        """Determine experience level based on title and description."""
        import re
        title_lower = title.lower()
        text = f"{title} {description}".lower()
        
        # Check title first for level indicators
        if any(indicator in title_lower for indicator in ['new grad', 'graduate', 'early career']):
            return 'New Grad'
        
        if any(indicator in title_lower for indicator in ['junior', 'jr.', 'associate']):
            return 'Junior'
        
        if any(indicator in title_lower for indicator in [' i ', ' 1 ', ' one']):
            return 'Level I'
        
        # Check description for experience patterns
        if re.search(r'0[–-]1\s*years?', text) or '0 to 1 year' in text:
            return '0-1 Years'
        
        if '1 year preferred' in text or '1 year experience' in text:
            return '1 Year'
        
        # Default for entry-level jobs
        return 'Entry Level'
    
    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on location, title, and experience level."""
        filtered = []
        
        for job in jobs:
            if is_relevant_job(job, self.settings):
                # Standardize job data
                standardized = {
                    'title': job.get('title', ''),
                    'company': job.get('company', ''),
                    'location': job.get('location', ''),
                    'url': job.get('url', ''),
                    'posted_date': job.get('posted_date', ''),
                    'provider': job.get('provider', ''),
                    'description': job.get('description', '')[:500] + '...' if len(job.get('description', '')) > 500 else job.get('description', ''),
                    'role_category': self.categorize_role(job.get('title', '')),
                    'level': self.determine_level(job.get('title', ''), job.get('description', ''))
                }
                filtered.append(standardized)
        
        return filtered