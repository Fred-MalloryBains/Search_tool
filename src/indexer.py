import os 
import json
import re

class Indexer:
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.filename = filename

    def add_to_index(self, page_id, text, fields):
        text = re.sub(r'[-–—]', ' ', text)  # Replace dashes with space
        clean = re.sub(r'[^\w\s]', '', text).lower()  # Remove punctuation
        words = clean.split()
        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}
            if page_id not in self.index[word]:
                self.index[word][page_id] = {"frequency": 0, "positions": []}
            self.index[word][page_id]["fields"] = fields
            self.index[word][page_id]["frequency"] += 1
            self.index[word][page_id]["positions"].append(position)
    
    
    def save_to_disk(self):
        # Ensure the directory exists (e.g., data/)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as f:
            json.dump(self.index, f, indent=4)
    
