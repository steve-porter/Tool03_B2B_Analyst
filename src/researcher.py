import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from fake_useragent import UserAgent
from .utils import extract_company_name
import time
# Removed feedparser due to installation issues in some environments
import xml.etree.ElementTree as ET
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_website(url: str) -> str:
    """
    Scrapes the text content from a given URL using a fake user agent.
    Returns the visible text content of the page.
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate content if it's too massive
        return text[:15000] 
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def _perform_search(query: str) -> list:
    """Helper to run a single DDGS query."""
    results = []
    try:
        ddgs = DDGS()
        search_gen = ddgs.text(keywords=query, max_results=3) 
        for r in search_gen:
            results.append(r)
    except Exception as e:
        print(f"Error searching '{query}': {e}")
    return results

def _fetch_google_news_rss(company_name: str) -> list:
    """Helper to fetch Google News RSS using standard libraries."""
    results = []
    try:
        encoded_name = quote(company_name)
        rss_url = f"https://news.google.com/rss/search?q={encoded_name}&hl=en-US&gl=US&ceid=US:en"
        
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        # RSS 2.0 structure: channel -> item
        items = root.findall('./channel/item')
        
        # Take top 5 entries
        for item in items[:5]:
            title = item.find('title').text if item.find('title') is not None else "No Title"
            link = item.find('link').text if item.find('link') is not None else ""
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            
            # description in Google News often contains HTML, cleaner to just use title + date
            # But let's keep basic cleaning if needed or just pass raw. 
            # Analyzer is robust enough to handle simple HTML tags if present.
            
            results.append({
                'title': title,
                'href': link, 
                'body': f"{pubDate} - {title}", # Using title in body as summary often duplicates or is messy in RSS
                'source': 'Google News RSS'
            })
    except Exception as e:
        print(f"Error fetching Google News RSS for {company_name}: {e}")
    return results

def search_news(company_identifier: str) -> list:
    """
    Searches DuckDuckGo and Google News RSS in parallel.
    Angles: General news, Acquisitions, Partnerships, Product Launches, LinkedIn.
    Deduplicates results.
    """
    company_name = company_identifier
    if '.' in company_identifier or 'http' in company_identifier:
        company_name = extract_company_name(company_identifier)
        
    if not company_name:
        return []

    print(f"Searching news for: {company_name} (Multi-Angle + RSS)")
    
    queries = [
        f"{company_name} news",
        f"{company_name} recent acquisitions funding",
        f"{company_name} strategic partnership announcement",
        f"{company_name} new product launch",
        f"{company_name} site:linkedin.com/company"
    ]
    
    all_results = []
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Submit DDG queries
        future_to_task = {executor.submit(_perform_search, q): f"DDG: {q}" for q in queries}
        # Submit RSS fetch
        future_to_task[executor.submit(_fetch_google_news_rss, company_name)] = "Google News RSS"
        
        for future in as_completed(future_to_task):
            task_name = future_to_task[future]
            try:
                data = future.result()
                all_results.extend(data)
            except Exception as e:
                print(f"Task {task_name} failed: {e}")

    # Deduplication based on URL
    unique_links = set()
    deduped_results = []
    
    for item in all_results:
        link = item.get('href', item.get('link', ''))
        # Simple normalization to catch http vs https dupes if necessary, but exact match is usually fine for this scope
        
        if link and link not in unique_links:
            unique_links.add(link)
            deduped_results.append(item)
            
    return deduped_results
