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
    if not location:
        return False
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
    """Classify role category based on title patterns - EXPANDED approach."""
    import re
    title_lower = title.lower()
    
    # Cybersecurity patterns (expanded)
    cyber_patterns = [
        r'(security|cyber|infosec)\s+(engineer|analyst|specialist|consultant)',
        r'(junior|jr\.?|associate|entry|graduate|new grad)\s+(security|cyber)',
        r'(application security|appsec|product security|cloud security|iam|identity|soc|incident response|threat|detection|grc|siem|splunk|vulnerability|pentest|devsecops)',
        r'(security|cyber)\s+(engineer|analyst)\s*(i|1|one|entry)?',
        r'information\s+security',
        r'risk\s+(analyst|engineer)',
        r'compliance\s+(analyst|engineer)',
        r'security\s+(operations|ops)',
        r'threat\s+(intelligence|hunting|analyst)',
        r'malware\s+(analyst|researcher)',
        r'forensics?\s+(analyst|investigator)',
        r'penetration\s+test',
        r'ethical\s+hack'
    ]
    
    for pattern in cyber_patterns:
        if re.search(pattern, title_lower):
            return 'Cybersecurity'
    
    # Software Engineering patterns (expanded)
    swe_patterns = [
        r'software\s+(engineer|developer)',
        r'(junior|jr\.?|associate|entry|graduate|new grad)\s+(software|engineer|developer)',
        r'(software|swe|developer|engineer)\s*(i|1|one|entry)?\b',
        r'(full\s*stack|frontend|front[-\s]*end|backend|back[-\s]*end|mobile|ios|android|web|application)\s+(engineer|developer)',
        r'(data|machine learning|ml|ai|platform|cloud|devops|site reliability|sre)\s+(engineer|developer)',
        r'(qa|quality assurance|test|testing)\s+(engineer|analyst)',
        r'systems?\s+(engineer|developer)',
        r'network\s+(engineer|administrator)',
        r'database\s+(engineer|administrator|developer)',
        r'(ui|ux)\s+(engineer|developer)',
        r'game\s+(developer|programmer)',
        r'embedded\s+(engineer|developer)',
        r'firmware\s+(engineer|developer)',
        r'hardware\s+(engineer|developer)',
        r'(programmer|coder|developer)\b',
        r'engineer\s*(i|1|one|entry)?\b'
    ]
    
    for pattern in swe_patterns:
        if re.search(pattern, title_lower):
            return 'SWE'
    
    return None

def has_internship_keywords(title: str, description: str) -> bool:
    """Check if job contains internship/co-op keywords."""
    text = f"{title} {description}".lower()
    internship_keywords = ['intern', 'internship', 'co-op', 'coop', 'apprentice', 'apprenticeship', 'fellow', 'fellowship']
    # Allow 'trainee' and 'campus' as they might be full-time programs
    return any(keyword in text for keyword in internship_keywords)

def has_entry_level_confirmation(description: str) -> bool:
    """Check if description confirms entry-level requirements - RELAXED."""
    import re
    desc_lower = description.lower()
    
    # Strong disqualifying patterns (definitely senior)
    senior_patterns = [
        r'5\+\s*years?', r'6\+\s*years?', r'7\+\s*years?', r'8\+\s*years?',
        r'senior', r'sr\.', r'lead', r'principal', r'staff', r'director', r'manager',
        r'architect', r'head of', r'vp', r'vice president', r'chief',
        r'minimum\s+[3-9]\+?\s*years?', r'at least\s+[3-9]\+?\s*years?',
        r'[3-9]\+\s*years?\s+(required|minimum|experience)'
    ]
    
    for pattern in senior_patterns:
        if re.search(pattern, desc_lower):
            return False
    
    # If no strong senior indicators, assume it could be entry-level
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
    
    # 4. Entry-level confirmation (relaxed approach)
    # Check description for strong senior indicators
    if not has_entry_level_confirmation(description):
        return False
    
    # Store role category for later use
    job['_role_category'] = role_category
    return True