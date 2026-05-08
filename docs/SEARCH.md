# Search implentation

Below outlines the operations of searching through the indexing, using key techniques from search index querying, describing the implementation and complexity of each key function.

## Retrieval: Getting relevant pages from find

To retrieve documents, the system identifies all pages containing the requested search terms. For multi-word queries, an intersection operation ensures that only pages containing all terms (AND logic) are returned.

- **Implementation**: handled in `get_search_results(self, query)`
- **process**: 

    1. The system identifies sets of URLS from the text index and metadata tags for each word 
    2. It performs a set union to combine text and metadata matches for individual words. 
    3. It then calculates the intersection of these sets across all query terms

- **complexity**: $O(N \cdot M)$, Where $N$ is the number of words in the query and $M$ is the average number of pages per word in the index. 

## Ranking: Ordering the Results

Results are ordered using a sophisticated **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm combined with custom metadata weighting.

### 1. **Weighted TF-IDF Scoring**

Instead of raw frequency, we use TF-IDF to provide a numeric representation of a term's importance to a specific document relative to the entire corpus.

- **Implementation**: Handled in `calculate_relevance(self, results, query)`.
- **Metadata Boost**: Words found within a page's metadata tags receive a **1.5x score boost** prioritising categorised content.
- **Complexity**: $O(R \cdot N)$ where $R$ is the number of retrieved results (pages) and N is the query words.


### 2. **Proximity and Phrase Bonus** 

To reward documents where terms appear consecutively (indicating a phrase match), a bonus constant is added for every adjacent word pair.

- **Implementation**: Handled in `calculate_phrase_bonus(self, page, query_words)`.
- **Logic**: For every consecutive pair of query words, if their positions in the document are adjacent ($pos_2 = pos_1 + 1$), a bonus of $5.0$ is added to the total score.
- **Complexity**: $O(N \cdot P^2)$, where $N$ is the number of query words and $P$ is the average number of positions per word in a document.



## Overall Complexity 

The total complexity for a search operation is roughly:

$O(N \cdot M + R \cdot N \cdot P^2)$. 

- **Efficiency**: This is highly efficient for moderate size of P, the positions per word in a document.

- **scalability**: for massive indices, further optimisations such as search result pruning or limiting or pre-calculated IDF values would improve performance.

### Testing 

Detailed testing logs and strategies can be found here: [testing](./TESTING.md)