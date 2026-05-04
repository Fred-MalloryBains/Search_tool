import requests
from bs4 import BeautifulSoup
import time
import json
from src.indexer import Indexer
from urllib.parse import urljoin


class Crawler:
    def __init__(self, base_url, save_path="data/index.json"):
        self.base_url = base_url
        self.indexer = Indexer()
        self.visited_urls = set()
        self.to_visit_urls = set()
        self.to_visit_urls.add(base_url)
        self.save_path = save_path
        
    def build(self):
        while self.to_visit_urls:
            # Get next URL from frontier
            current_url = self.to_visit_urls.pop()
            
            if current_url in self.visited_urls:
                continue
            
            print(f"Crawling: {current_url}")
            soup = self.scrape_quotes(current_url)
            
            # Mark as visited immediately after fetching
            self.visited_urls.add(current_url)
            
            if not soup:
                continue
                
            # Extract quotes AND all internal links
            normalised_content, found_links = self.extract_content(soup)
            
            # Index the content
            for item in normalised_content:
                # Tip: Use the current_url as the page_id for better accuracy
                self.indexer.add_to_index(current_url, item["text"])
            
            # Add new undiscovered links to the frontier
            for link in found_links:
                if link not in self.visited_urls:
                    self.to_visit_urls.add(link)

            # Politeness window is CRITICAL here because you will hit many more pages
            time.sleep(6)
        
        self.indexer.save_to_disk(self.save_path)
            
        
                
    def scrape_quotes(self, url, page=None, tag=None):
        # Construct the URL based on the page and tag parameters
        target_url = url
        
        try:
            response = requests.get(target_url, timeout=10)
            
            if response.status_code != 200:
                print(f"Failed to retrieve: {target_url} (Status: {response.status_code})")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup 

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")
            return None
        
    
    def extract_content(self, content):
        extracted_content = []
        
        quotes = content.find_all("div", class_="quote") 
        
        for quote in quotes:
            if not quote.find("span", class_="text") or not quote.find("small", class_="author"):
                continue 
            extracted_content.append({
                "text": quote.find("span", class_="text").get_text(),
                "author": quote.find("small", class_="author").get_text(),
                "tags": [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            })

        all_found_links = []
        # Find every anchor tag on the page
        for a_tag in content.find_all("a", href=True):
            href = a_tag["href"]
            # Convert relative link to absolute link
            full_url = urljoin(self.base_url, href)
            
            # Only add the link if it belongs to the same website
            if full_url.startswith(self.base_url):
                all_found_links.append(full_url)

        normalised_content = self.normalise_content(extracted_content)
        # Return everything found
        return normalised_content, all_found_links

    def normalise_content(self, content):
        for item in content:
            item["text"] = item["text"].lower()
            item["author"] = item["author"].lower()
            item["tags"] = [tag.lower() for tag in item["tags"]]
        return content