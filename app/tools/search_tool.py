from langchain_core.tools import tool
from ddgs import DDGS
from app.tools.definitions.search import WebSearchInput

@tool("web_search", args_schema=WebSearchInput, return_direct=False)
def search_tool(input:str):
    """
    Find information from Internet based on user query
    """
    raw_results = DDGS().text(input, max_results=5, region="vn-vi")
    
    if not raw_results:
        return "Couldnot found appropriate content"

    context_parts = []
    for i, res in enumerate(raw_results, 1):
        title = res.get('title', 'N/A')
        body = res.get('body', 'N/A')
        href = res.get('href', 'N/A')
        part = (
            f"SOURCE_ID: {i}\n"
            f"TITLE: {title}\n"
            f"CONTENT: {body}\n"
            f"URL: {href}"
        )
        context_parts.append(part)

    optimized_context = "\n" + "-"*30 + "\n"
    optimized_context += ("\n" + "-"*30 + "\n").join(context_parts)
    return optimized_context


if __name__ == "__main__":
    query = "Doraemon là ai"
    result = search_tool.invoke(query)
    print(result)