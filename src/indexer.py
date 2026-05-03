import os 
import json
import re

class Indexer:
    def __init__(self):
        self.index = {}

    def add_to_index(self, page_id, text):
        clean = re.sub(r'[^\w\s]', '', text).lower()  # Remove punctuation
        words = clean.split()
        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}
            if page_id not in self.index[word]:
                self.index[word][page_id] = {"frequency": 0, "positions": []}
            self.index[word][page_id]["frequency"] += 1
            self.index[word][page_id]["positions"].append(position)
    
    
    def save_to_disk(self, filename):
        # Ensure the directory exists (e.g., data/)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.index, f)


    def load_from_disk(self, filename):

        try:
            with open(filename, 'r') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            print(f"Error: Index file {filename} not found. Run 'build' first.")
    
    def print_word(self, word):
        """Prints the inverted index entry for a specific word."""
        word = word.lower() # Case-insensitive requirement 
        if word in self.index:
            print(json.dumps(self.index[word], indent=4))
        else:
            print(f"Word '{word}' not found in index.")

    def find_query(self, query_words):
        """Returns pages containing the search terms."""
        if not query_words:
            return []

        # Convert query to lowercase to match the index 
        query_words = [w.lower() for w in query_words]
        
        # Start with pages containing the first word
        if query_words not in self.index:
            return []
        
        common_pages = set(self.index[query_words].keys())

        # For multi-word queries, find the intersection of page sets
        for word in query_words[1:]:
            if word in self.index:
                common_pages.intersection_update(self.index[word].keys())
            else:
                return []

        return list(common_pages)