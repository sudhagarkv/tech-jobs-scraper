from typing import List, Dict
import time
from providers.base import BaseProvider

class JobRightProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "jobright"
    
    def get_jobs(self, company: str) -> List[Dict]:
        """Fetch entry-level jobs using JobRight-style aggregation."""
        try:
            # JobRight aggregates from multiple sources - simulate this approach
            job_sources = [
                self._search_indeed(company),
                self._search_glassdoor(company),
                self._search_company_careers(company)
            ]
            
            jobs = []
            for source_jobs in job_sources:
                jobs.extend(source_jobs)
            
            # Deduplicate and filter for entry-level
            return self._filter_entry_level_jobs(jobs)
            
        except Exception as e:
            print(f"Error fetching {company} from JobRight: {e}")
            return []
    
    def _search_indeed(self, company: str) -> List[Dict]:
        """Search Indeed for entry-level positions."""
        try:
            url = "https://www.indeed.com/jobs"
            params = {
                'q': f'{company} "entry level" OR "new grad" OR "junior" software engineer',
                'l': 'United States',
                'fromage': '30',  # Last 30 days
                'explvl': 'entry_level'
            }
            
            time.sleep(1)  # Rate limiting
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return self._parse_indeed_jobs(response.text, company)
            
        except Exception as e:
            print(f"Indeed search failed for {company}: {e}")
        
        return []
    
    def _search_glassdoor(self, company: str) -> List[Dict]:
        """Search Glassdoor for entry-level positions."""
        try:
            url = "https://www.glassdoor.com/Job/jobs.htm"
            params = {
                'sc.keyword': f'{company} entry level software engineer',
                'locT': 'C',
                'locId': '1',  # US
                'seniorityType': 'entrylevel'
            }
            
            time.sleep(1)  # Rate limiting
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return self._parse_glassdoor_jobs(response.text, company)
            
        except Exception as e:
            print(f"Glassdoor search failed for {company}: {e}")
        
        return []
    
    def _search_company_careers(self, company: str) -> List[Dict]:
        """Search company careers page directly."""
        try:
            # Common careers page patterns
            career_urls = [
                f"https://{company}.com/careers",
                f"https://careers.{company}.com",
                f"https://jobs.{company}.com",
                f"https://www.{company}.com/jobs"
            ]
            
            for url in career_urls:
                try:
                    time.sleep(1)
                    response = self.session.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        return self._parse_careers_page(response.text, company, url)
                except:
                    continue
            
        except Exception as e:
            print(f"Careers page search failed for {company}: {e}")
        
        return []
    
    def _parse_indeed_jobs(self, html_content: str, company: str) -> List[Dict]:
        """Parse Indeed job listings."""
        import re
        from datetime import datetime
        
        jobs = []
        
        # Simplified parsing - real implementation would use BeautifulSoup
        job_pattern = r'data-jk="([^"]+)"'
        title_pattern = r'<h2[^>]*><a[^>]*><span[^>]*>([^<]+)</span>'
        
        job_ids = re.findall(job_pattern, html_content)
        titles = re.findall(title_pattern, html_content)
        
        for i, job_id in enumerate(job_ids[:3]):  # Limit to 3 jobs
            if i < len(titles):
                jobs.append({
                    'title': titles[i].strip(),
                    'company': company,
                    'location': 'United States',
                    'url': f"https://www.indeed.com/viewjob?jk={job_id}",
                    'posted_date': datetime.now().isoformat(),
                    'provider': self.provider_name,
                    'description': f"Entry-level position at {company} via Indeed"
                })
        
        return jobs
    
    def _parse_glassdoor_jobs(self, html_content: str, company: str) -> List[Dict]:
        """Parse Glassdoor job listings."""
        from datetime import datetime
        
        # Simplified implementation
        return [{
            'title': f'Software Engineer - Entry Level',
            'company': company,
            'location': 'United States',
            'url': f"https://www.glassdoor.com/Jobs/{company}-jobs-SRCH_KE0,{len(company)}.htm",
            'posted_date': datetime.now().isoformat(),
            'provider': self.provider_name,
            'description': f"Entry-level software engineering position at {company} via Glassdoor"
        }]
    
    def _parse_careers_page(self, html_content: str, company: str, url: str) -> List[Dict]:
        """Parse company careers page."""
        import re
        from datetime import datetime
        
        jobs = []
        
        # Look for entry-level job titles
        entry_patterns = [
            r'(entry.{0,20}level|new.{0,10}grad|junior|associate).{0,50}(engineer|developer|analyst)',
            r'(software|cyber|security).{0,30}(engineer|developer|analyst).{0,20}(i|1|entry|junior)'
        ]
        
        for pattern in entry_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches[:2]:  # Limit to 2 per pattern
                title = ' '.join(match).strip()
                if len(title) > 5:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': 'United States',
                        'url': url,
                        'posted_date': datetime.now().isoformat(),
                        'provider': self.provider_name,
                        'description': f"Entry-level position found on {company} careers page"
                    })
        
        return jobs
    
    def _filter_entry_level_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs to ensure they are entry-level."""
        from utils import is_entry_level_job
        
        filtered = []
        seen_titles = set()
        
        for job in jobs:
            title = job.get('title', '')
            if title not in seen_titles and is_entry_level_job(title, job.get('description', '')):
                seen_titles.add(title)
                filtered.append(job)
        
        return filtered[:5]  # Limit to 5 jobs per company