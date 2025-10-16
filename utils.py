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
    """Check if job matches our criteria - STRICT entry-level only."""
    from datetime import datetime, timedelta
    import re
    
    title = job.get('title', '').lower()
    location = job.get('location', '').lower()
    description = job.get('description', '').lower()
    
    # Check if job is within 3 months
    posted_date = job.get('posted_date', '')
    if posted_date:
        try:
            job_date = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
            three_months_ago = datetime.now() - timedelta(days=90)
            if job_date < three_months_ago:
                return False
        except:
            pass
    
    # Check location
    us_locations = [loc.lower() for loc in settings['filters']['locations']]
    if not any(loc in location for loc in us_locations):
        return False
    
    # STRICT: Exclude senior roles first
    job_text = f"{title} {description}".lower()
    senior_keywords = [
        'senior', 'sr.', 'sr ', 'lead', 'principal', 'staff', 'director', 'manager',
        'architect', 'head of', 'vp ', 'vice president', 'chief',
        '3+ years', '4+ years', '5+ years', '6+ years', '3-5 years', '4-6 years',
        '3 years', '4 years', '5 years', '6 years', 'minimum 3', 'minimum 4', 'minimum 5',
        'at least 3', 'at least 4', 'at least 5', 'experienced', 'expert'
    ]
    
    if any(keyword in job_text for keyword in senior_keywords):
        return False
    
    # Check job title relevance
    all_titles = []
    all_titles.extend([t.lower() for t in settings['filters']['job_titles']['software_engineering']])
    all_titles.extend([t.lower() for t in settings['filters']['job_titles']['cybersecurity']])
    
    title_match = any(keyword in title for keyword in all_titles)
    
    if not title_match:
        general_roles = ['engineer', 'developer', 'analyst', 'specialist']
        title_match = any(role in title for role in general_roles)
    
    if not title_match:
        return False
    
    # STRICT: Must have entry-level indicators
    entry_keywords = [
        'new grad', 'graduate', 'entry level', 'entry-level', 'junior', 'jr.',
        '0-1', '0-2', '0-3', '0 years', '1 year', '2 years', 'associate',
        'level 1', 'l1', 'early career', 'recent graduate', 'college hire',
        'university graduate', 'campus hire', 'trainee', 'intern'
    ]
    
    has_entry_keywords = any(keyword in job_text for keyword in entry_keywords)
    
    # Also check for patterns like "0-1 years", "1-2 years" etc.
    year_patterns = [r'0[-\s]*1\s*year', r'0[-\s]*2\s*year', r'0[-\s]*3\s*year', r'1[-\s]*2\s*year']
    has_year_pattern = any(re.search(pattern, job_text) for pattern in year_patterns)
    
    return has_entry_keywords or has_year_pattern