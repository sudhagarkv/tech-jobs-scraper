from typing import List, Dict
from providers.base import BaseProvider

class GreenhouseProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "greenhouse"
    
    def get_jobs(self, company: str) -> List[Dict]:
        """Fetch jobs from Greenhouse API."""
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            jobs = []
            
            for job in data.get('jobs', []):
                jobs.append({
                    'title': job.get('title', ''),
                    'company': company,
                    'location': job.get('location', {}).get('name', ''),
                    'url': job.get('absolute_url', ''),
                    'posted_date': job.get('updated_at', ''),
                    'provider': self.provider_name,
                    'description': job.get('content', '')
                })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching {company} from Greenhouse: {e}")
            return []