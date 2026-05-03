
class Indexer:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, text):
        words = text.split()
        for word in words:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(doc_id)
    
    