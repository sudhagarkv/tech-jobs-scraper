# US Entry-Level Tech Jobs Scraper & Site

Automated job scraper that collects entry-level and new-grad tech positions from major companies and displays them on a modern web interface.

## Features

- 🔄 **Auto-updates daily** via GitHub Actions
- 📅 **3-month job filter** - only shows recent postings
- 🌐 **Modern web interface** with filters and search
- 🚀 **Hosted on Vercel** with automatic deployments
- 📊 **Multiple job sources** (Greenhouse, Lever, Ashby)

## Live Site

The site automatically updates daily with new job postings.

## Data Sources

- **Greenhouse API** - Major tech companies
- **Lever API** - Startups and scale-ups  
- **Ashby API** - Modern companies
- **GitHub Discovery** - Additional companies from hiring lists

## Filters Applied

- **Location**: US-based positions + Remote
- **Experience**: Entry-level, New-grad, 0-1 years
- **Roles**: Software Engineering, Cybersecurity
- **Recency**: Last 3 months only

## Architecture

- **Scraper**: Python with requests, runs daily via GitHub Actions
- **Frontend**: React + TypeScript + Tailwind CSS
- **Hosting**: Vercel with automatic deployments
- **Data**: JSON file updated daily, cached with timestamps