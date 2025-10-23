"""
YC AI Healthtech Startup Tracker - Web Scraper
Scrapes Y Combinator's startup directory for AI and healthcare companies
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import json


class YCStartupScraper:
    """Scraper for Y Combinator startup data"""

    def __init__(self):
        self.base_url = "https://www.ycombinator.com/companies"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.startups = []

    def scrape_startups(self, tags=None, batch=None):
        """
        Scrape startups from YC directory

        Args:
            tags: List of tags to filter by (e.g., ['Healthcare', 'Artificial Intelligence'])
            batch: Specific YC batch (e.g., 'W23', 'S24')
        """
        params = {}
        if tags:
            params['tags'] = tags
        if batch:
            params['batch'] = batch

        print(f"Scraping YC startups with filters: {params}")

        # Note: This is a template. Actual implementation depends on YC's website structure
        # You may need to use their API or adjust selectors based on current HTML

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # TODO: Update selectors based on actual YC website structure
            startup_cards = soup.find_all('div', class_='startup-card')  # Placeholder

            for card in startup_cards:
                startup_data = self._extract_startup_data(card)
                if startup_data:
                    self.startups.append(startup_data)

            print(f"Scraped {len(self.startups)} startups")

        except Exception as e:
            print(f"Error scraping: {e}")

    def _extract_startup_data(self, card):
        """Extract data from a startup card element"""
        try:
            data = {
                'name': card.find('h3').text.strip() if card.find('h3') else None,
                'description': card.find('p', class_='description').text.strip() if card.find('p', class_='description') else None,
                'batch': card.find('span', class_='batch').text.strip() if card.find('span', class_='batch') else None,
                'tags': [tag.text.strip() for tag in card.find_all('span', class_='tag')],
                'website': card.find('a', class_='website')['href'] if card.find('a', class_='website') else None,
                'scraped_at': datetime.now().isoformat()
            }
            return data
        except Exception as e:
            print(f"Error extracting startup data: {e}")
            return None

    def save_to_csv(self, filename='data/yc_startups.csv'):
        """Save scraped data to CSV"""
        if not self.startups:
            print("No data to save")
            return

        df = pd.DataFrame(self.startups)
        df.to_csv(filename, index=False)
        print(f"Saved {len(self.startups)} startups to {filename}")

    def save_to_json(self, filename='data/yc_startups.json'):
        """Save scraped data to JSON"""
        if not self.startups:
            print("No data to save")
            return

        with open(filename, 'w') as f:
            json.dump(self.startups, f, indent=2)
        print(f"Saved {len(self.startups)} startups to {filename}")


def main():
    """Main execution function"""
    scraper = YCStartupScraper()

    # Scrape AI and Healthcare startups
    print("Starting YC healthtech startup scraping...")
    scraper.scrape_startups(tags=['Healthcare', 'Artificial Intelligence'])

    # Save results
    scraper.save_to_csv()
    scraper.save_to_json()

    print("\nScraping complete!")


if __name__ == "__main__":
    main()
