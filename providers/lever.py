from typing import List, Dict
from providers.base import BaseProvider

class LeverProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "lever"
    
    def get_jobs(self, company: str) -> List[Dict]:
        """Fetch jobs from Lever API."""
        try:
            url = f"https://api.lever.co/v0/postings/{company}?mode=json"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            jobs = []
            
            for job in data:
                location = job.get('categories', {}).get('location', '')
                if isinstance(location, list):
                    location = ', '.join(location)
                
                jobs.append({
                    'title': job.get('text', ''),
                    'company': company,
                    'location': location,
                    'url': job.get('hostedUrl', ''),
                    'posted_date': job.get('createdAt', ''),
                    'provider': self.provider_name,
                    'description': job.get('description', '')
                })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching {company} from Lever: {e}")
            return []