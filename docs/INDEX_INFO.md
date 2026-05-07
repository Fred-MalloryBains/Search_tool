# Index Structure

The index stores the required text from the quotes and author descriptions, as well as additional information such as the author, page title and semantic tags being stored for each page as metadata. 

## Dictionary structure

The saved data is stored in a single file as specified in the coursework instructions, the dictionary structure of the saved json is as follows:

```bash
{
    {
        "index":
            {
                "word1": 
                {
                    "<url1>": 
                    { 
                        "frequency" :
                        {
                            3
                        }
                        "positions" : 
                        {
                            [0, 10, 12]
                        }
                    }
                }
            }
    }
    {
        "metata" :
            {
                "url1" :
                {
                    ['tag1', 'tag2', 'tag3', 'author']
                }
            }
    }
}

```

## Accessing the index

The index is created using `/src/crawler.py` and `src/indexer.py` to save as a json file 

Then the index is loaded in `/src/search.py` to parse the json as a dictionary and handle the required logic to find and print queries from the user in the command line.

## Searching logic

Searching algorithm logic and complexity analysis can be found here: [search.md](./SEARCH.md)