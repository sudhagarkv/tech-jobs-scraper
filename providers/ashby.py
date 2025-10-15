from typing import List, Dict
from providers.base import BaseProvider

class AshbyProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "ashby"
    
    def get_jobs(self, company: str) -> List[Dict]:
        """Fetch jobs from Ashby API."""
        try:
            url = f"https://api.ashbyhq.com/job-board/company/{company}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            jobs = []
            
            for job in data.get('jobs', []):
                location_parts = []
                if job.get('locationName'):
                    location_parts.append(job['locationName'])
                if job.get('isRemote'):
                    location_parts.append('Remote')
                
                jobs.append({
                    'title': job.get('title', ''),
                    'company': company,
                    'location': ', '.join(location_parts),
                    'url': job.get('jobUrl', ''),
                    'posted_date': job.get('publishedDate', ''),
                    'provider': self.provider_name,
                    'description': job.get('description', '')
                })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching {company} from Ashby: {e}")
            return []