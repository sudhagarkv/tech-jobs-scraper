#!/usr/bin/env python3
import os
import sys
import pandas as pd
from typing import List, Dict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import load_yaml, save_json
from discovery import CompanyDiscovery
from filters import JobFilter
from providers.greenhouse import GreenhouseProvider
from providers.lever import LeverProvider
from providers.ashby import AshbyProvider
from providers.linkedin import LinkedInProvider
from providers.jobright import JobRightProvider
from providers.experimental_jobright_like import ExperimentalJobrightLikeProvider

def main():
    """Main scraper execution."""
    print("Starting job scraper...")
    
    # Load configuration
    settings = load_yaml('settings.yml')
    companies = load_yaml('companies.yml')
    
    # Initialize components
    discovery = CompanyDiscovery(settings)
    job_filter = JobFilter(settings)
    
    # Discover additional companies
    print("Discovering companies from GitHub lists...")
    discovered = discovery.discover_companies()
    
    # Merge with guaranteed companies
    for provider, company_list in discovered.items():
        if provider in companies:
            companies[provider].extend(company_list)
            companies[provider] = list(set(companies[provider]))  # Remove duplicates
    
    # Initialize providers
    providers = {
        'greenhouse': GreenhouseProvider(settings['providers']['greenhouse']),
        'lever': LeverProvider(settings['providers']['lever']),
        'ashby': AshbyProvider(settings['providers']['ashby']),
        'linkedin': LinkedInProvider(settings['providers']['linkedin']),
        'jobright': JobRightProvider(settings['providers']['jobright']),
        'experimental_jobright_like': ExperimentalJobrightLikeProvider(settings['providers']['experimental_jobright_like'])
    }
    
    all_jobs = []
    
    # Scrape each provider
    for provider_name, provider in providers.items():
        if not provider.is_enabled():
            print(f"Skipping {provider_name} (disabled)")
            continue
        
        company_list = companies.get(provider_name, [])
        print(f"Scraping {len(company_list)} companies from {provider_name}...")
        
        for company in company_list:
            try:
                jobs = provider.get_jobs(company)
                if jobs:
                    print(f"  OK {company}: {len(jobs)} jobs")
                    all_jobs.extend(jobs)
                else:
                    print(f"  FAIL {company}: no jobs found")
            except Exception as e:
                print(f"  ERROR {company}: error - {e}")
    
    print(f"\nTotal jobs fetched: {len(all_jobs)}")
    
    # Filter jobs with detailed tracking
    print("Filtering jobs...")
    
    # Track filtering statistics
    total_jobs = len(all_jobs)
    internship_count = 0
    non_us_count = 0
    
    # Pre-filter to track rejections
    from utils import has_internship_keywords, is_us_location, classify_role_by_title
    
    for job in all_jobs:
        title = job.get('title', '')
        location = job.get('location', '')
        description = job.get('description', '')
        
        if has_internship_keywords(title, description):
            internship_count += 1
        elif not is_us_location(location):
            non_us_count += 1
    
    filtered_jobs = job_filter.filter_jobs(all_jobs)
    
    # Count final results by category
    final_swe = sum(1 for job in filtered_jobs if job.get('role_category') == 'SWE')
    final_cyber = sum(1 for job in filtered_jobs if job.get('role_category') == 'Cybersecurity')
    
    print(f"Kept {len(filtered_jobs)} US jobs (SWE: {final_swe}, Cyber: {final_cyber}). Skipped internships: {internship_count}, non-US: {non_us_count}.")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Sort by posted_date DESC, then company
    from datetime import datetime, timezone
    def sort_key(job):
        posted_date = job.get('posted_date', '')
        try:
            if posted_date:
                # Handle different date formats and ensure timezone awareness
                if 'Z' in posted_date:
                    date_obj = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
                elif '+' in posted_date or '-' in posted_date[-6:]:
                    date_obj = datetime.fromisoformat(posted_date)
                else:
                    # Assume UTC if no timezone info
                    date_obj = datetime.fromisoformat(posted_date).replace(tzinfo=timezone.utc)
                return (date_obj, job.get('company', ''))
        except:
            pass
        return (datetime.min.replace(tzinfo=timezone.utc), job.get('company', ''))
    
    filtered_jobs.sort(key=sort_key, reverse=True)
    
    # Deduplicate by company + title + url
    seen = set()
    deduped_jobs = []
    for job in filtered_jobs:
        key = (job.get('company', ''), job.get('title', ''), job.get('url', ''))
        if key not in seen:
            seen.add(key)
            deduped_jobs.append(job)
    
    print(f"After deduplication: {len(deduped_jobs)} unique jobs")
    
    # Save results
    print("Saving results...")
    save_json(deduped_jobs, 'data/jobs.json')
    
    # Save as CSV
    if deduped_jobs:
        df = pd.DataFrame(deduped_jobs)
        df.to_csv('data/jobs.csv', index=False)
        print(f"Saved {len(deduped_jobs)} jobs to data/jobs.json and data/jobs.csv")
    else:
        print("No jobs to save")
    
    print("Scraping complete!")

if __name__ == "__main__":
    main()