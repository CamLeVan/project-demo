from Controller.ytbViewer import ytbViewer

def main(search_query):
    auto = ytbViewer()
    auto.OpenYtb(search_query)

if __name__ == "__main__":
    main("your_default_search_query")  
