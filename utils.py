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
    """Classify role category based on title patterns - COMPREHENSIVE approach."""
    import re
    title_lower = title.lower()
    
    # Cybersecurity patterns (comprehensive)
    cyber_patterns = [
        r'(security|cyber|infosec)\s+(engineer|analyst|specialist|consultant|architect)',
        r'(junior|jr\.?|associate|entry|graduate|new grad|early career)\s+(security|cyber)',
        r'(application security|appsec|product security|cloud security|iam|identity|soc|incident response|threat|detection|grc|siem|splunk|vulnerability|pentest|devsecops)',
        r'(security|cyber)\s+(engineer|analyst|specialist)\s*(i|1|one|entry|junior|associate)?',
        r'information\s+(security|assurance)',
        r'(risk|compliance|governance)\s+(analyst|engineer|specialist)',
        r'security\s+(operations|ops|architect|consultant)',
        r'(threat|vulnerability)\s+(intelligence|hunting|analyst|researcher|management)',
        r'(malware|forensics?)\s+(analyst|researcher|investigator|engineer)',
        r'(penetration|pen)\s*test',
        r'ethical\s+hack',
        r'(red|blue)\s+team',
        r'(security|cyber)\s+(consultant|advisor|specialist)',
        r'(identity|access)\s+(management|analyst)',
        r'(incident|emergency)\s+response',
        r'security\s+(audit|assessment)',
        r'(cryptography|crypto)\s+(engineer|analyst)',
        r'(network|endpoint|cloud)\s+security'
    ]
    
    for pattern in cyber_patterns:
        if re.search(pattern, title_lower):
            return 'Cybersecurity'
    
    # Software Engineering patterns (comprehensive)
    swe_patterns = [
        r'software\s+(engineer|developer|architect)',
        r'(junior|jr\.?|associate|entry|graduate|new grad|early career)\s+(software|engineer|developer|programmer)',
        r'(software|swe|developer|engineer|programmer)\s*(i|1|one|entry|junior|associate)?\b',
        r'(full\s*stack|frontend|front[-\s]*end|backend|back[-\s]*end|mobile|ios|android|web|application)\s+(engineer|developer)',
        r'(data|machine learning|ml|ai|platform|cloud|devops|site reliability|sre)\s+(engineer|developer)',
        r'(qa|quality assurance|test|testing|automation)\s+(engineer|analyst|developer)',
        r'(systems?|infrastructure|platform)\s+(engineer|developer|administrator)',
        r'(network|database|cloud)\s+(engineer|administrator|developer)',
        r'(ui|ux|frontend|backend)\s+(engineer|developer)',
        r'(game|mobile|web|desktop)\s+(developer|programmer|engineer)',
        r'(embedded|firmware|hardware)\s+(engineer|developer)',
        r'(api|microservices|distributed systems)\s+(engineer|developer)',
        r'(devops|sre|reliability)\s+(engineer|specialist)',
        r'(build|release|deployment)\s+(engineer|specialist)',
        r'(performance|scalability)\s+(engineer|specialist)',
        r'(security|application security)\s+(engineer|developer)',
        r'(blockchain|cryptocurrency)\s+(engineer|developer)',
        r'(ar|vr|graphics)\s+(engineer|developer)',
        r'(compiler|language)\s+(engineer|developer)',
        r'(robotics|autonomous)\s+(engineer|developer)',
        r'(programmer|coder|developer)\b(?!.*manager|.*director|.*lead)',
        r'engineer\s*(i|1|one|entry|junior|associate)?\b(?!.*senior|.*lead|.*principal)',
        r'(technical|software)\s+(consultant|analyst)(?!.*senior|.*lead)',
        r'(solutions|integration)\s+(engineer|developer)(?!.*senior|.*lead)',
        r'(research|development)\s+(engineer|scientist)(?!.*senior|.*lead|.*principal)'
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

def analyze_experience_requirements(title: str, description: str) -> Dict[str, any]:
    """Analyze experience requirements from title and description."""
    import re
    text = f"{title} {description}".lower()
    
    # Extract years of experience mentioned
    years_patterns = [
        r'(\d+)\+?\s*years?\s*(of\s+)?(experience|exp)',
        r'(\d+)\+?\s*years?\s*(required|minimum|preferred)',
        r'minimum\s+(\d+)\+?\s*years?',
        r'at least\s+(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s*in\s+',
        r'(\d+)\+?\s*years?\s*with\s+'
    ]
    
    years_found = []
    for pattern in years_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                years_found.extend([int(m) for m in match if m.isdigit()])
            elif match.isdigit():
                years_found.append(int(match))
    
    max_years = max(years_found) if years_found else 0
    
    # Check for seniority indicators in title
    title_senior_patterns = [
        r'\b(senior|sr\.?|lead|principal|staff|architect|director|manager|head\s+of|vp|vice\s+president|chief)\b',
        r'\b(ii|iii|iv|2|3|4|5)\b'  # Level indicators
    ]
    
    has_senior_title = any(re.search(pattern, title.lower()) for pattern in title_senior_patterns)
    
    # Check for entry-level indicators
    entry_patterns = [
        r'\b(entry\s*level|new\s*grad|junior|jr\.?|associate|graduate|recent\s*graduate|early\s*career)\b',
        r'\b(level\s*1|l1|i\b|one)\b',
        r'\b(0[-\s]*[12]?\s*years?)\b'
    ]
    
    has_entry_indicators = any(re.search(pattern, text) for pattern in entry_patterns)
    
    return {
        'max_years_required': max_years,
        'has_senior_title': has_senior_title,
        'has_entry_indicators': has_entry_indicators,
        'years_mentioned': years_found
    }

def is_entry_level_job(title: str, description: str) -> bool:
    """Strict entry-level filtering based on requirements analysis."""
    analysis = analyze_experience_requirements(title, description)
    
    # Immediate disqualifiers
    if analysis['has_senior_title']:
        return False
    
    # If more than 2 years required, not entry level
    if analysis['max_years_required'] > 2:
        return False
    
    # If has explicit entry-level indicators, it's good
    if analysis['has_entry_indicators']:
        return True
    
    # If no years mentioned and no senior title, could be entry level
    if analysis['max_years_required'] == 0:
        return True
    
    # If 0-2 years mentioned, it's entry level
    if analysis['max_years_required'] <= 2:
        return True
    
    return False

def is_relevant_job(job: Dict, settings: Dict) -> bool:
    """Check if job matches criteria with strict entry-level filtering."""
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
    
    # 4. STRICT entry-level confirmation
    if not is_entry_level_job(title, description):
        return False
    
    # Store role category for later use
    job['_role_category'] = role_category
    return True