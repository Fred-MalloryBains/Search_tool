import json
import math

class Index: 
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.filename = filename
        self.total_docs = 0
    
    def load_from_disk(self):

        try:
            with open(self.filename, 'r') as f:
                self.index = json.load(f)
                self.total_docs = len(set(page for word_data in self.index.values() for page in word_data.keys()))
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
                    # First word found: initialise the set
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

    def calculate_relevance(self, results, query):
        ## use TF-IDF to rank results based on relevance to the query
        query_words = query.lower().split()
        ranked_results = []

        for page in results:
            total_score = 0.0
            for word in query_words:
                # Term frequency
                tf = self.index.get(word, {}).get(page, {}).get("frequency", 0)
                field_tokens = self.index.get(word, {}).get(page, {}).get("fields", [])
                # Get Document Frequency (DF)
                # How many pages contain this specific word?
                df = len(self.index.get(word, {}))
                
                # Calculate Inverse Document Frequency (IDF)
                # If the word isn't in the index, IDF is 0 to avoid division by zero
                if df > 0 and self.total_docs > 0:
                    idf = math.log(self.total_docs / df)
                    score = tf * idf
                    
                    if word in field_tokens:
                        score *= 1.5 # Boost score if word is in a relevant field
                else:
                    idf = 0
                
                # Add the TF-IDF contribution for this word to the page's total score
                total_score += (tf * idf)
                
            ranked_results.append((page, total_score))

        # Sort results by score in descending order
        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return ranked_results
                
    def calculate_phrase_bonus(self, page, query_words):
        bonus = 0.0
        # Only possible if there are at least 2 words
        if len(query_words) < 2:
            return bonus

        # Get positions for all words in this page
        pos_lists = [self.index.get(w, {}).get(page, {}).get("positions", []) for w in query_words]
        
        # Simple check: are words adjacent?
        for i in range(len(pos_lists) - 1):
            pos1 = pos_lists[i]
            pos2 = pos_lists[i+1]
            
            for p1 in pos1:
                if (p1 + 1) in pos2:
                    bonus += 5.0 # High bonus for exact sequence
        return bonus

    def display_results(self, results, query):
        ordered_results = self.calculate_relevance(results, query)
        if not ordered_results:
            print("No results found.")
            return
            
        print(f"Results found in {len(results)} pages:")
        for page, score in ordered_results:
            print(f" - {page} (Score: {score:.2f})")
        
        
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