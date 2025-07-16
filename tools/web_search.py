# tools/web_search.py

from duckduckgo_search import ddg
import wikipedia

def search_web(query):
    try:
        results = ddg(query, max_results=1)
        if results:
            return results[0].get("body") or results[0].get("content", "")
        raise Exception("No DDG results")
    except:
        try:
            return wikipedia.summary(query, sentences=2)
        except:
            return "Sorry, I couldn't find relevant info."
