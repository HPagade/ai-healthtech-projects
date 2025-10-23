"""
Startup Job Market Analysis - Job Scraper
Scrapes job postings from YC and healthtech startups
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import json


class JobScraper:
    """Scraper for startup job postings"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.jobs = []

    def scrape_yc_jobs(self, tags=None):
        """
        Scrape YC Work at a Startup jobs

        Args:
            tags: Filter by tags (e.g., ['Healthcare', 'AI'])
        """
        base_url = "https://www.ycombinator.com/jobs"

        print(f"Scraping YC jobs...")

        # Note: Actual implementation depends on YC's job board structure
        # This is a template structure

        params = {}
        if tags:
            params['tags'] = ','.join(tags)

        try:
            response = requests.get(base_url, headers=self.headers, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # TODO: Update selectors based on actual website structure
            job_cards = soup.find_all('div', class_='job-listing')

            for card in job_cards:
                job_data = self._extract_job_data(card)
                if job_data:
                    self.jobs.append(job_data)

            print(f"Scraped {len(self.jobs)} jobs")

        except Exception as e:
            print(f"Error scraping: {e}")

    def _extract_job_data(self, card):
        """Extract job information from listing card"""
        try:
            data = {
                'title': card.find('h3').text.strip() if card.find('h3') else None,
                'company': card.find('div', class_='company-name').text.strip() if card.find('div', class_='company-name') else None,
                'location': card.find('span', class_='location').text.strip() if card.find('span', class_='location') else None,
                'job_type': card.find('span', class_='job-type').text.strip() if card.find('span', class_='job-type') else None,
                'experience_level': card.find('span', class_='experience').text.strip() if card.find('span', class_='experience') else None,
                'salary_range': card.find('span', class_='salary').text.strip() if card.find('span', class_='salary') else None,
                'description': card.find('p', class_='description').text.strip() if card.find('p', class_='description') else None,
                'tags': [tag.text.strip() for tag in card.find_all('span', class_='tag')],
                'posted_date': datetime.now().isoformat(),
                'url': card.find('a')['href'] if card.find('a') else None
            }
            return data
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None

    def generate_sample_data(self, n_jobs=200):
        """Generate sample job data for demonstration"""
        import random

        job_titles = [
            'Product Manager', 'Software Engineer', 'Data Scientist',
            'Machine Learning Engineer', 'Healthcare Data Analyst',
            'Clinical Product Manager', 'AI Research Scientist',
            'Backend Engineer', 'Frontend Developer', 'Full Stack Engineer',
            'DevOps Engineer', 'UX Designer', 'Growth Manager',
            'Customer Success Manager', 'Sales Executive'
        ]

        companies = [
            'HealthAI', 'MedTech Solutions', 'CareAI', 'Vital Labs',
            'Genomics Inc', 'TeleMed', 'PharmaTech', 'BioInnovate',
            'DiagnosticAI', 'PatientFirst', 'MedData', 'HealthOS'
        ]

        locations = [
            'San Francisco, CA', 'New York, NY', 'Boston, MA',
            'Remote', 'Austin, TX', 'Seattle, WA', 'Los Angeles, CA'
        ]

        job_types = ['Full-time', 'Part-time', 'Contract', 'Internship']

        experience_levels = ['Entry Level', 'Mid Level', 'Senior', 'Lead', 'Principal']

        tags_pool = [
            'Healthcare', 'AI', 'Machine Learning', 'Python', 'React',
            'AWS', 'Data Science', 'Clinical', 'B2B', 'SaaS',
            'Remote', 'Medical Devices', 'EHR', 'HIPAA', 'Biotech'
        ]

        for i in range(n_jobs):
            salary_min = random.randint(60, 180) * 1000
            salary_max = salary_min + random.randint(20, 60) * 1000

            job = {
                'title': random.choice(job_titles),
                'company': random.choice(companies),
                'location': random.choice(locations),
                'job_type': random.choice(job_types),
                'experience_level': random.choice(experience_levels),
                'salary_range': f'${salary_min:,} - ${salary_max:,}',
                'salary_min': salary_min,
                'salary_max': salary_max,
                'description': f'Looking for talented {random.choice(job_titles)} to join our team.',
                'tags': random.sample(tags_pool, k=random.randint(3, 6)),
                'posted_date': datetime.now().isoformat(),
                'url': f'https://example.com/jobs/{i}'
            }
            self.jobs.append(job)

        print(f"Generated {n_jobs} sample jobs")

    def save_to_csv(self, filename='data/jobs.csv'):
        """Save job data to CSV"""
        if not self.jobs:
            print("No jobs to save")
            return

        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        print(f"Saved {len(self.jobs)} jobs to {filename}")

    def save_to_json(self, filename='data/jobs.json'):
        """Save job data to JSON"""
        if not self.jobs:
            print("No jobs to save")
            return

        with open(filename, 'w') as f:
            json.dump(self.jobs, f, indent=2)
        print(f"Saved {len(self.jobs)} jobs to {filename}")


def main():
    """Main execution"""
    scraper = JobScraper()

    # Generate sample data (replace with actual scraping in production)
    scraper.generate_sample_data(n_jobs=200)

    # Save data
    scraper.save_to_csv()
    scraper.save_to_json()

    print("\nJob scraping complete!")


if __name__ == "__main__":
    main()
