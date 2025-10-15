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
    
    # Filter jobs
    print("Filtering jobs...")
    filtered_jobs = job_filter.filter_jobs(all_jobs)
    print(f"Relevant jobs after filtering: {len(filtered_jobs)}")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save results
    print("Saving results...")
    save_json(filtered_jobs, 'data/jobs.json')
    
    # Save as CSV
    if filtered_jobs:
        df = pd.DataFrame(filtered_jobs)
        df.to_csv('data/jobs.csv', index=False)
        print(f"Saved {len(filtered_jobs)} jobs to data/jobs.json and data/jobs.csv")
    else:
        print("No jobs to save")
    
    print("Scraping complete!")

if __name__ == "__main__":
    main()