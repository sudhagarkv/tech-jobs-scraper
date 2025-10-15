import re
import json
import yaml
from typing import List, Dict, Any

def load_yaml(filepath: str) -> Dict[str, Any]:
    """Load YAML configuration file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def save_json(data: List[Dict], filepath: str):
    """Save data as JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def extract_domains_from_text(text: str) -> List[str]:
    """Extract company domains/names from markdown text."""
    domains = []
    # Match markdown links with company domains
    link_pattern = r'\[([^\]]+)\]\(https?://(?:www\.)?([^/\)]+)'
    matches = re.findall(link_pattern, text, re.IGNORECASE)
    
    for name, domain in matches:
        # Clean domain and extract company name
        domain = domain.lower().replace('www.', '')
        company = domain.split('.')[0]
        if len(company) > 2 and company not in ['github', 'linkedin', 'glassdoor']:
            domains.append(company)
    
    return list(set(domains))

def normalize_company_name(name: str) -> str:
    """Normalize company name for API slugs."""
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

def is_relevant_job(job: Dict, settings: Dict) -> bool:
    """Check if job matches our criteria."""
    from datetime import datetime, timedelta
    
    title = job.get('title', '').lower()
    location = job.get('location', '').lower()
    
    # Check if job is within 3 months
    posted_date = job.get('posted_date', '')
    if posted_date:
        try:
            job_date = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
            three_months_ago = datetime.now() - timedelta(days=90)
            if job_date < three_months_ago:
                return False
        except:
            pass  # If date parsing fails, continue with other filters
    
    # Check location
    us_locations = [loc.lower() for loc in settings['filters']['locations']]
    if not any(loc in location for loc in us_locations):
        return False
    
    # Check job title relevance
    all_titles = []
    all_titles.extend([t.lower() for t in settings['filters']['job_titles']['software_engineering']])
    all_titles.extend([t.lower() for t in settings['filters']['job_titles']['cybersecurity']])
    
    if not any(keyword in title for keyword in all_titles):
        return False
    
    # Check experience level
    experience_keywords = [exp.lower() for exp in settings['filters']['experience_levels']]
    job_text = f"{title} {job.get('description', '')}".lower()
    
    return any(keyword in job_text for keyword in experience_keywords)