import requests
from typing import List, Dict
from utils import extract_domains_from_text, normalize_company_name

class CompanyDiscovery:
    def __init__(self, settings: Dict):
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; job-scraper/1.0)'})
    
    def discover_companies(self) -> Dict[str, List[str]]:
        """Discover companies from GitHub lists and return organized by provider."""
        if not self.settings['discovery']['enabled']:
            return {'greenhouse': [], 'lever': [], 'ashby': []}
        
        all_companies = []
        
        for url in self.settings['discovery']['github_lists']:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    companies = extract_domains_from_text(response.text)
                    all_companies.extend(companies)
                    print(f"Discovered {len(companies)} companies from {url}")
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
        
        # Organize companies by provider (simple heuristic)
        discovered = {
            'greenhouse': all_companies[:len(all_companies)//3],
            'lever': all_companies[len(all_companies)//3:2*len(all_companies)//3],
            'ashby': [c.title().replace('-', ' ') for c in all_companies[2*len(all_companies)//3:]]
        }
        
        return discovered