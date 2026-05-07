# Search implentation

Below outlines the operations of searching through the indexing, using key techniques from search index querying, describing the implementation and complexity of each key function.

## Getting relevant pages from find

To collate a set of page_urls from the index, an intersection operation is performed for each url found in `self.index[word].keys()`, this is handled in `def get_search_results(self, query):`. 

To iterate over each set of lists and find the intersection the complexity of this operation is: 

## Ordering the page results 

From the set of pages, the ordering of the returned results is determined using a weighted TF-IDF algorithm. 
Each word is tallied for every page to find the weighted prevelance compared to the total, to give a meaningful numeric representation of importance to the document, compared to ordering by raw frequency. 
To consider meta data this process is repeated and tallied to the original, with more weight being added for words matching metadata compared to text body contents. This calcualtion is carried out using the method. 

This is carried out in the method: `def get_search_results(self, query):` and has a complexity of:


To also consider prioritising proximity of the query, to penalise sparse matches and reward close ones, a bonus constant is added for each consecutive match for every word. This is carried out in `def calculate_phrase_bonus(self, page, query_words):
And has a complexity of: 


## Overall Complexity 

In total the searching of terms has a complexity of: 


And this is adequate for a moderate size search algorithm for this index size, but considerably larger indexs would require more efficient processing by splitting into different sections etc.

### Testing 

Testing outline and plan can be found here: [testing](./TESTING.md)