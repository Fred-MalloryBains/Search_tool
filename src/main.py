from src.crawler import Crawler
from src.search import Index

"""
Call the build function from src.crawler
This creates the index file on disk that we will use for searching.
"""
def build():
    print ("Starting the crawling and indexing process...")
    base_url = "http://quotes.toscrape.com/"
    crawler = Crawler(base_url)
    crawler.build()

"""
Searches for a query and prints results. Handles errors gracefully.
"""
def search(query, index):
    try:
        index.load_from_disk()
        results = index.get_search_results(query)
    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return

    if results:
        index.display_results(results, query)

"""
Print function for a specific word, returning index details. 
"""      
def print_index(word, index):
    try:
        index.load_from_disk()
        index.print_index(word)
    except Exception as e:
        print(f"An error occurred while printing index: {e}")

"""
Loads the index from disk and returns it
"""      
def load(index):
    try:
        index.load_from_disk()
        print("Index loaded successfully.")
    except Exception as e:
        print(f"An error occurred while loading index: {e}")
    return index
    
"""
Handles the interface for the search tool, 
allowing users to build the index, load it, search for queries, and print word details.
"""
if __name__ == "__main__":
    loaded_index = False
    index = Index()
    print("\n")
    print("Welcome to the Search Tool!")
    print("\n")
    print("Available commands: build, load, find <query>, print <word>, exit")
    print("---------------------------------------")
    print("\n")
    while True:
        user_input = input("search_tool> ").strip().split()
        if not user_input:
            continue
        
        command = user_input[0]
        args = user_input[1:]
        
        if command == "exit":
            print("Exiting search tool. Goodbye!")
            break
        
        if command == "find":
            if loaded_index:
                search_query = " ".join(args)
                result = search(search_query, index)
            else:
                print("Please load the index first using 'load' command.")
        elif command == "load":
            load(index)
            loaded_index = True
        
        elif command == "build":
            build()
        
        elif command == "print":
            if not args:
                print("Usage: print <word>")
                continue
            if not loaded_index:
                print("Please load the index first using 'load' command.")
                continue
            word = args[0]
            print_index(word, index)
        else:
            print(f"Unknown command: {command}. Available commands: build, load, find <query>, print <word>, exit")