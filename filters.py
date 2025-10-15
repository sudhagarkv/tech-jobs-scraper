from typing import List, Dict
from utils import is_relevant_job

class JobFilter:
    def __init__(self, settings: Dict):
        self.settings = settings
    
    def categorize_role(self, title: str) -> str:
        """Categorize job role based on title."""
        title_lower = title.lower()
        
        # Check for cybersecurity keywords
        cyber_keywords = ['security', 'cybersecurity', 'infosec', 'penetration', 'ethical hacker', 'soc', 'incident response', 'threat', 'compliance']
        if any(keyword in title_lower for keyword in cyber_keywords):
            return 'Cybersecurity'
        
        # Default to Software Engineering
        return 'Software Engineering'
    
    def determine_level(self, title: str, description: str) -> str:
        """Determine experience level based on title and description."""
        text = f"{title} {description}".lower()
        
        if any(keyword in text for keyword in ['new grad', 'graduate', 'entry level', '0-1', '0-2']):
            return 'New Grad'
        elif any(keyword in text for keyword in ['junior', 'associate', 'level 1', 'l1', 'early career']):
            return 'Entry Level'
        else:
            return 'Entry Level'  # Default for filtered jobs
    
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