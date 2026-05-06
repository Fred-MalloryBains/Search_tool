import json
import math

class Index: 
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.metadata = {}
        self.filename = filename
        self.total_docs = 0
    
    def load_from_disk(self):

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.index = data.get("index", {})
                self.metadata = data.get("metadata", {})
                self.total_docs = len(set(page for word_data in self.index.values() for page in word_data.keys()))
        except FileNotFoundError:
            print(f"Error: Index file {self.filename} not found. Run 'build' first.")
            
    def get_search_results(self, query):
        query_words = query.lower().split()
        if not query_words:
            return set()

        intersection_pages = None

        for word in query_words:
            # 1. Find pages where the word is in the text index
            text_pages = set(self.index.get(word, {}).keys())
            
            # 2. Find pages where the word exists in the metadata tags
            metadata_pages = {page for page, meta in self.metadata.items() 
                              if word in meta.get("tags", [])}
            
            # Combine both sources for this specific word
            word_matches = text_pages.union(metadata_pages)

            if not word_matches:
                print(f"Word '{word}' not found in index or metadata.")
                return set()

            if intersection_pages is None:
                intersection_pages = word_matches
            else:
                intersection_pages.intersection_update(word_matches)

        return intersection_pages if intersection_pages else set()

    def calculate_relevance(self, results, query):
        query_words = query.lower().split()
        ranked_results = []

        for page in results:
            total_score = 0.0
            page_metadata = self.metadata.get(page, {})
            page_tags = page_metadata.get("tags", [])

            for word in query_words:
                word_data = self.index.get(word, {}).get(page, {})
                tf = word_data.get("frequency", 0)
                
                # Get Document Frequency (DF) across both index and metadata
                df = len(self.index.get(word, {}))
                if df == 0:
                    df = sum(1 for p in self.metadata if word in self.metadata[p].get("tags", []))
                
                if df > 0 and self.total_docs > 0:
                    idf = math.log(self.total_docs / df)
                    
                    # Use TF from text, or a base of 1 if it's only in metadata
                    effective_tf = tf if tf > 0 else (1 if word in page_tags else 0)
                    score = effective_tf * idf
                    
                    # Apply 1.5x boost for metadata matches
                    if word in page_tags:
                        score *= 1.5
                    
                    total_score += score
            
            total_score += self.calculate_phrase_bonus(page, query_words)
            ranked_results.append((page, total_score))

        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return ranked_results
                
    def calculate_phrase_bonus(self, page, query_words):
        bonus = 0.0
        if len(query_words) < 2:
            return bonus

        pos_lists = [self.index.get(w, {}).get(page, {}).get("positions", []) for w in query_words]
        
        for i in range(len(pos_lists) - 1):
            pos1 = pos_lists[i]
            pos2 = pos_lists[i+1]
            
            for p1 in pos1:
                if (p1 + 1) in pos2:
                    bonus += 5.0
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