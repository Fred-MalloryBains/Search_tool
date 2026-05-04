import json

class Index: 
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.filename = filename
    
    def load_from_disk(self, filename):

        try:
            with open(filename, 'r') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            print(f"Error: Index file {filename} not found. Run 'build' first.")
            
    def get_search_results(self, query):
        query = query.lower()
        if query in self.index:
            return self.index[query]
        else:
            print(f"No results found for '{query}'.")
            return None
    
    def display_results(self, results):
        if results:
            print(f"Results:")
            for page_id, data in results.items():
                print(f"  Page: {page_id}")
                print(f"    Frequency: {data['frequency']}")
                print(f"    Positions: {data['positions']}")
        
        
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