import json
import math

class Index: 
    """
    Class implementation of the search index, responsible for loading the index from disk,
    searching for queries, calculating relevance scores, and printing index details.
    """
    def __init__(self, filename="data/index.json"):
        self.index = {}
        self.metadata = {}
        self.filename = filename
        self.total_docs = 0
    
    """
    Defensive loading of the index from disk, with error handling for missing files.
    """
    def load_from_disk(self):

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                # create two separate dictionaries for text index and metadata for easier access
                self.index = data.get("index", {})
                self.metadata = data.get("metadata", {})
                # store total_docs for relevance calculations (DF and IDF)
                self.total_docs = len(set(page for word_data in self.index.values() for page in word_data.keys()))
        except FileNotFoundError:
            print(f"Error: Index file {self.filename} not found. Run 'build' first.")
    
    """
    Retrieves a set of pages that match the query, 
    Using the set intersect function to ensure all query words are present in the results.
    """
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

    """
    Weighted relevance calculation that considers term frequency, inverse document frequency,
    and applies a boost for metadata matches. Also includes a bonus for exact phrase matches.
    """
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
    
    """
    Apply a bonus to the relevance score if the query words appear as an exact phrase in the page content.
    This encourages results where the query is more likely to be contextually relevant.
    """
    def calculate_phrase_bonus(self, page, query_words):
        bonus = 0.0
        # check if there exists multiple query words
        if len(query_words) < 2:
            return bonus

        # Get the positions of each query word in the page content
        pos_lists = [self.index.get(w, {}).get(page, {}).get("positions", []) for w in query_words]
        
        # check for consecutive positions of query words to identify exact phrase matches
        for i in range(len(pos_lists) - 1):
            pos1 = pos_lists[i]
            pos2 = pos_lists[i+1]
            
            for p1 in pos1:
                if (p1 + 1) in pos2:
                    bonus += 5.0
        return bonus

    """
    Format and print the search results, showing the number of pages found and their relevance scores.
    """
    def display_results(self, results, query):
        ordered_results = self.calculate_relevance(results, query)
        if not ordered_results:
            print("No results found.")
            return
            
        print(f"Results found in {len(results)} pages:")
        for page, score in ordered_results:
            print(f" - {page} (Score: {score:.2f})")
        
    """
    Implementation of the print function for a specific word, showing its frequency and positions in the indexed pages.
    """   
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