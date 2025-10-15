from typing import List, Dict
from utils import is_relevant_job

class JobFilter:
    def __init__(self, settings: Dict):
        self.settings = settings
    
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
                    'description': job.get('description', '')[:500] + '...' if len(job.get('description', '')) > 500 else job.get('description', '')
                }
                filtered.append(standardized)
        
        return filtered