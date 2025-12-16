from urllib.parse import urlparse

def extract_company_name(url: str) -> str:
    """
    Extracts the company name from a URL.
    E.g., 'https://www.salesforce.com/products' -> 'salesforce'
    """
    if not url:
        return ""
    
    # Ensure protocol is present for urlparse to work correctly if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    parsed = urlparse(url)
    netloc = parsed.netloc
    
    # Remove 'www.' if present
    if netloc.startswith('www.'):
        netloc = netloc[4:]
        
    # Split by dot and take the first part as the company name
    # This is a heuristic and might need refinement for complex domains (e.g. co.uk)
    # But compliant with V1 requirements for simplicity.
    parts = netloc.split('.')
    if parts:
        return parts[0]
    return ""
