import os 
import json
import re
import unicodedata

class Indexer:
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.metadata = {}  # For storing metadata like author, tags etc
        self.filename = filename

    def add_to_index(self, page_id, text, fields = None):
        words = self.tokenise(text)
        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}
            if page_id not in self.index[word]:
                self.index[word][page_id] = {"frequency": 0, "positions": []}
            self.index[word][page_id]["frequency"] += 1
            self.index[word][page_id]["positions"].append(position)
        
        if fields:
                if fields and page_id not in self.metadata:
                    self.metadata[page_id] = {
                        "tags": fields  # You can further split this into author/tags if needed
                    }
                else:
                    existing_tags = self.metadata[page_id]["tags"]
                    updated_tags = set(existing_tags) | set(fields) # Union of two sets
                    self.metadata[page_id]["tags"] = list(updated_tags)

    
    def save_to_disk(self):
        # Ensure the directory exists (e.g., data/)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        output = {
            "index": self.index,
            "metadata": self.metadata
        }
        with open(self.filename, 'w') as f:
            json.dump(output, f, indent=4)

    """
    Normalises and splits text into individual tokens.
    Handles dashes, punctuation, and case sensitivity.
    """
    def tokenise(self, text):
        # Normalise Unicode characters (e.g., 'é' becomes 'e' + '´')
        text = unicodedata.normalize('NFD', text)
        # Filter out the accent marks (non-spacing marks)
        text = "".join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Existing logic
        text = re.sub(r'[-–—]', ' ', text)  
        clean = re.sub(r'[^\w\s]', '', text).lower()  
        return clean.split()