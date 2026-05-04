import json

class Index: 
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.filename = filename
    
    def load_from_disk(self):

        try:
            with open(self.filename, 'r') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            print(f"Error: Index file {self.filename} not found. Run 'build' first.")
            
    def get_search_results(self, query):
        query_words = query.lower().split()
        if not query_words:
            return set()

        intersection_pages = None # Use None to handle the first word correctly

        for word in query_words:
            if word in self.index:
                # Get the set of URLs for this specific word
                word_pages = set(self.index[word].keys())
                
                if intersection_pages is None:
                    # First word found: initialize the set
                    intersection_pages = word_pages
                else:
                    # Subsequent words: find the intersection (AND logic)
                    intersection_pages.intersection_update(word_pages)
            else:
                # Requirement: If any word in the phrase is missing, 
                # the intersection for the whole phrase is empty.
                print(f"Word '{word}' not found in index.")
                return set()

        return intersection_pages if intersection_pages else set()

    def display_results(self, results):
        if not results:
            print("No results found.")
            return
            
        print(f"Results found in {len(results)} pages:")
        for page in results:
            print(f" - {page}")
        
        
    def print_index(self, word):
        word = word.lower()
        if word in self.index:
            print(f"Word: '{word}'")
            for page_id, data in self.index[word].items():
                print(f"  Page: {page_id}")
                print(f"    Frequency: {data['frequency']}")
                print(f"    Positions: {data['positions']}")
        else:
            print(f"Word '{word}' not found in index.")