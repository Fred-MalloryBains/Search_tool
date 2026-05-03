import requests
from bs4 import BeautifulSoup
import time
import json
from indexer import Indexer


class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.indexer = Indexer()
        self.visited_urls = set()
        
    def build(self):
        current_page = 1
        while True:
            # 1. Fetch the soup from the page
            soup = self.scrape_quotes(self.base_url, page=current_page)
            if not soup:
                break
                
            # 2. Extract and normalize content (quotes and the 'Next' page link)
            normalised_content, next_page = self.extract_content(soup)
            
            # 3. Feed each quote to the indexer
            page_id = f"{self.base_url}page/{current_page}/"
            for item in normalised_content:
                # counting frequencies, and recording positions.
                self.indexer.add_to_index(page_id, item["text"])
            
            # 4. Check if there is a next page to crawl
            if not next_page:
                break
                
            # 5. MANDATORY: Politeness window 
            print(f"Waiting 6 seconds before next request...")
            time.sleep(6)
            current_page += 1
        
        # 6. Save the final index to the data/ folder 
        self.indexer.save_to_disk("data/index.json")
            
        
                
    def scrape_quotes(self, url, page=None, tag=None):
        # Construct the URL based on the page and tag parameters
        if tag:
            target_url = f"{url.rstrip('/')}/tag/{tag}/page/{page if page else 1}/"
        else:
            target_url = f"{url.rstrip('/')}/page/{page if page else 1}/"
        
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
        
        quotes = content.find_all("div", class_="quote")  # ✅ FIX
        
        for quote in quotes:
            extracted_content.append({
                "text": quote.find("span", class_="text").get_text(),
                "author": quote.find("small", class_="author").get_text(),
                "tags": [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            })

        next_page = None
        next_button = content.find("li", class_="next")
        if next_button:
            next_page = next_button.find("a")["href"]
        
        normalised_content = self.normalise_content(extracted_content)
        return normalised_content, next_page
    
    def normalise_content(self, content):
        for item in content:
            item["text"] = item["text"].lower()
            item["author"] = item["author"].lower()
            item["tags"] = [tag.lower() for tag in item["tags"]]
        return content