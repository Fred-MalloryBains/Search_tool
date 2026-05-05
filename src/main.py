#from Search_tool.tests.test_crawler import crawler
from src.crawler import Crawler
from src.search import Index

def build():
    print ("Starting the crawling and indexing process...")
    base_url = "http://quotes.toscrape.com/"
    crawler = Crawler(base_url)
    crawler.build()

def search(query):
    index = Index()
    try:
        index.load_from_disk()
        results = index.get_search_results(query)
    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return

    if results:
        index.display_results(results, query)
        
def print_index(word):
    index = Index()
    try:
        index.load_from_disk()
        index.print_index(word)
    except Exception as e:
        print(f"An error occurred while printing index: {e}")

def load():
    index = Index()
    try:
        index.load_from_disk()
        print("Index loaded successfully.")
    except Exception as e:
        print(f"An error occurred while loading index: {e}")
    

if __name__ == "__main__":
    while True:
        user_input = input("search_tool> ").strip().split()
        if not user_input:
            continue
        
        command = user_input[0]
        args = user_input[1:]
        
        if command == "exit":
            break
        
        if command == "find":
            search_query = " ".join(args)
            result = search(search_query)
        elif command == "load":
            load()
        
        elif command == "build":
            build()
        
        elif command == "print":
            if not args:
                print("Usage: print <word>")
                continue
            word = args[0]
            print_index(word)
            