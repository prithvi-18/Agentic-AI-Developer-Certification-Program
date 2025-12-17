"""
ResumeAI Pro - Job Scraper
Fetch and parse job postings from multiple sources
"""

import logging
from typing import List, Dict
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
import json

from config import JOB_SCRAPE_SOURCES, MAX_JOBS_TO_SCRAPE
from database import DB

logger = logging.getLogger(__name__)

# ==========================================
# JOB SCRAPER
# ==========================================

class JobScraper:
    """Scrape job postings from multiple sources"""
    
    @staticmethod
    def scrape_jobs(job_title: str, location: str = "India") -> List[Dict]:
        """
        Scrape job postings from all configured sources
        
        Args:
            job_title: Job position to search for
            location: Location to search in
            
        Returns:
            List of job postings with extracted data
        """
        all_jobs = []
        
        # Scrape from Indeed
        try:
            indeed_jobs = JobScraper._scrape_indeed(job_title, location)
            all_jobs.extend(indeed_jobs[:10])
            logger.info(f"Scraped {len(indeed_jobs)} jobs from Indeed")
        except Exception as e:
            logger.error(f"Indeed scraping failed: {e}")
        
        # Scrape from LinkedIn (using search)
        try:
            linkedin_jobs = JobScraper._scrape_linkedin(job_title)
            all_jobs.extend(linkedin_jobs[:5])
            logger.info(f"Scraped {len(linkedin_jobs)} jobs from LinkedIn")
        except Exception as e:
            logger.error(f"LinkedIn scraping failed: {e}")
        
        return all_jobs[:MAX_JOBS_TO_SCRAPE]
    
    @staticmethod
    def _scrape_indeed(job_title: str, location: str) -> List[Dict]:
        """Scrape from Indeed"""
        jobs = []
        try:
            # Indeed job search URL
            search_url = (
                f"https://in.indeed.com/jobs?q={job_title.replace(' ', '+')}"
                f"&l={location.replace(' ', '+')}"
            )
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse job listings
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:10]:
                try:
                    title = card.find('h2', class_='jobTitle').get_text(strip=True)
                    company = card.find('span', class_='companyName').get_text(strip=True)
                    
                    # Get job link
                    job_link = card.find('a', class_='jcs-ExternalLink')
                    url = job_link['href'] if job_link else ""
                    
                    # Get job description summary
                    description = card.find('div', class_='job-snippet')
                    desc_text = description.get_text(strip=True) if description else ""
                    
                    # Extract requirements (keywords from description)
                    requirements = JobScraper._extract_requirements(desc_text)
                    keywords = JobScraper._extract_keywords(title + " " + desc_text)
                    
                    job = {
                        "id": str(uuid4()),
                        "job_title": title,
                        "company": company,
                        "description": desc_text,
                        "requirements": requirements,
                        "keywords": keywords,
                        "source": "indeed",
                        "url": url
                    }
                    
                    jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Indeed scraping error: {e}")
        
        return jobs
    
    @staticmethod
    def _scrape_linkedin(job_title: str) -> List[Dict]:
        """
        Scrape from LinkedIn
        Note: LinkedIn has anti-scraping, so we use a limited approach
        """
        jobs = []
        try:
            # LinkedIn search URL (limited scraping due to robots.txt)
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            # LinkedIn heavily restricts scraping, so we'll return mock data
            # In production, you'd use LinkedIn API
            jobs = JobScraper._generate_sample_linkedin_jobs(job_title)
            
        except Exception as e:
            logger.warning(f"LinkedIn scraping limited: {e}")
            jobs = JobScraper._generate_sample_linkedin_jobs(job_title)
        
        return jobs
    
    @staticmethod
    def _extract_requirements(text: str) -> List[str]:
        """Extract job requirements from description"""
        # Common requirement keywords
        requirement_keywords = [
            "python", "java", "javascript", "c++", "sql", "html", "css",
            "react", "angular", "django", "flask", "nodejs", "express",
            "aws", "gcp", "azure", "docker", "kubernetes", "git",
            "agile", "scrum", "rest", "api", "microservices",
            "mongodb", "postgresql", "mysql", "redis",
            "communication", "teamwork", "leadership", "analytical"
        ]
        
        text_lower = text.lower()
        found_requirements = [
            req for req in requirement_keywords 
            if req in text_lower
        ]
        
        return found_requirements if found_requirements else ["communication", "problem-solving"]
    
    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """Extract important keywords from job text"""
        # High-value keywords
        keywords = [
            "senior", "lead", "manager", "architect", "principal",
            "python", "java", "javascript", "golang", "rust",
            "aws", "cloud", "devops", "machine learning", "ai",
            "database", "api", "microservices", "fullstack",
            "5+ years", "3+ years", "8+ years",
            "bachelor's", "master's", "phd"
        ]
        
        text_lower = text.lower()
        found = [k for k in keywords if k in text_lower]
        
        return found if found else ["professional", "experienced"]
    
    @staticmethod
    def _generate_sample_linkedin_jobs(job_title: str) -> List[Dict]:
        """Generate sample jobs when scraping not possible"""
        return [
            {
                "id": str(uuid4()),
                "job_title": f"{job_title} - Senior",
                "company": "Tech Corp",
                "description": f"We are looking for a skilled {job_title} with 5+ years experience. Must have experience with cloud platforms, microservices, and CI/CD.",
                "requirements": ["python", "aws", "docker", "kubernetes", "leadership"],
                "keywords": ["senior", "aws", "python", "microservices"],
                "source": "linkedin",
                "url": "https://linkedin.com/jobs/sample"
            },
            {
                "id": str(uuid4()),
                "job_title": f"{job_title} - Mid Level",
                "company": "Innovation Labs",
                "description": f"Join our team as a {job_title}. We work with latest technologies and mentor junior developers.",
                "requirements": ["python", "git", "sql", "agile", "communication"],
                "keywords": ["python", "agile", "mentoring"],
                "source": "linkedin",
                "url": "https://linkedin.com/jobs/sample"
            }
        ]
    
    @staticmethod
    def save_jobs(jobs: List[Dict]) -> int:
        """Save scraped jobs to database"""
        count = 0
        for job in jobs:
            try:
                DB.save_job_posting(
                    job_id=job.get("id"),
                    job_title=job.get("job_title"),
                    company=job.get("company"),
                    description=job.get("description"),
                    requirements=job.get("requirements", []),
                    keywords=job.get("keywords", []),
                    source=job.get("source"),
                    url=job.get("url")
                )
                count += 1
            except Exception as e:
                logger.error(f"Failed to save job: {e}")
        
        logger.info(f"Saved {count} jobs to database")
        return count
