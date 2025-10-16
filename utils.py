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
    import re
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

def is_us_location(location: str) -> bool:
    """Check if location is US-based."""
    import re
    location = location.lower().strip()
    
    # Direct US indicators
    us_indicators = ['united states', 'usa', 'u.s.', ' us ', 'remote (us)', 'us-remote', 'remote - united states']
    if any(indicator in location for indicator in us_indicators):
        return True
    
    # US state codes
    us_states = [
        'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
        'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
        'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'dc', 'pr'
    ]
    
    # Check for "City, ST" pattern
    state_pattern = r'\b(' + '|'.join(us_states) + r')\b'
    if re.search(state_pattern, location):
        return True
    
    return False

def classify_role_by_title(title: str) -> str:
    """Classify role category based on title patterns - TITLE FIRST approach."""
    import re
    title_lower = title.lower()
    
    # Cybersecurity patterns
    cyber_patterns = [
        r'(security|cyber)\s+(engineer|analyst)\s*(i|1|one)?\b',
        r'(junior|jr\.?|associate)\s+(security|cyber)\s+(engineer|analyst)',
        r'(application security|appsec|product security|cloud security|iam|identity|soc|incident response|threat|detection|grc|siem|splunk|vulnerability|pentest)',
        r'(graduate|new grad|early career)\s+(security|cyber)'
    ]
    
    for pattern in cyber_patterns:
        if re.search(pattern, title_lower):
            return 'Cybersecurity'
    
    # Software Engineering patterns
    swe_patterns = [
        r'software engineer\s*(i|1|one)\b',
        r'(junior|jr\.?|associate)\s+(software|swe|developer|engineer)',
        r'(software|swe|developer)\s*(i|1|one)\b',
        r'(graduate|new grad|early career)\s+software',
        r'(full\s*stack|frontend|front[-\s]*end|backend|back[-\s]*end|mobile|ios|android)\s+(engineer|developer)'
    ]
    
    for pattern in swe_patterns:
        if re.search(pattern, title_lower):
            return 'SWE'
    
    return None

def has_internship_keywords(title: str, description: str) -> bool:
    """Check if job contains internship/co-op keywords."""
    text = f"{title} {description}".lower()
    internship_keywords = ['intern', 'internship', 'co-op', 'coop', 'trainee', 'apprentice', 'apprenticeship', 'campus', 'fellow', 'fellowship']
    return any(keyword in text for keyword in internship_keywords)

def has_entry_level_confirmation(description: str) -> bool:
    """Check if description confirms entry-level requirements."""
    import re
    desc_lower = description.lower()
    
    # Entry-level patterns
    entry_patterns = [
        r'0[–-]1\s*years?', r'0\s*to\s*1\s*years?', r'1\s*year\s*preferred',
        r'0[–-]1\s*year\b', r'0\s*to\s*1\s*year\b'
    ]
    
    for pattern in entry_patterns:
        if re.search(pattern, desc_lower):
            return True
    
    # Check for disqualifying patterns
    senior_patterns = [r'2\+\s*years?', r'3\+\s*years?', r'4\+\s*years?', r'5\+\s*years?']
    for pattern in senior_patterns:
        if re.search(pattern, desc_lower):
            return False
    
    return True

def is_relevant_job(job: Dict, settings: Dict) -> bool:
    """Check if job matches criteria with title-first classification."""
    from datetime import datetime, timedelta
    
    title = job.get('title', '')
    location = job.get('location', '')
    description = job.get('description', '')
    
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
    
    # 1. Exclude internships first
    if has_internship_keywords(title, description):
        return False
    
    # 2. Check US location
    if not is_us_location(location):
        return False
    
    # 3. Title-first classification
    role_category = classify_role_by_title(title)
    if not role_category:
        return False
    
    # 4. Entry-level confirmation (optional secondary check)
    # If title already indicates entry-level, we're good
    # Otherwise, check description for confirmation
    title_lower = title.lower()
    title_entry_indicators = ['junior', 'jr.', 'associate', 'graduate', 'new grad', 'early career', ' i ', ' 1 ', ' one']
    has_title_entry = any(indicator in title_lower for indicator in title_entry_indicators)
    
    if not has_title_entry:
        if not has_entry_level_confirmation(description):
            return False
    
    # Store role category for later use
    job['_role_category'] = role_category
    return True