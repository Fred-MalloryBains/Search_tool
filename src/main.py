from src.crawler import Crawler

def build():
    print ("Starting the crawling and indexing process...")
    base_url = "http://quotes.toscrape.com/"
    crawler = Crawler(base_url)
    crawler.build()


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
            
        elif command == "load":
            pass
        
        elif command == "build":
            build()
            