
class Indexer:
    def __init__(self):
        self.index = {}

    def add_to_index(self, page_id, text):
        words = text.split()
        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}
            if page_id not in self.index[word]:
                self.index[word][page_id] = {"frequency": 0, "positions": []}
            self.index[word][page_id]["frequency"] += 1
            self.index[word][page_id]["positions"].append(position)
    
    