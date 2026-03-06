# -*- coding: utf-8 -*-
"""
Check OKX OnchainOS API documentation
"""

import requests
from bs4 import BeautifulSoup

def fetch_okx_docs():
    """Fetch OKX OnchainOS documentation"""
    url = "https://web3.okx.com/zh-hans/onchainos/dev-docs/home/run-your-first-dapp"
    
    try:
        print("Fetching OKX OnchainOS documentation...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("Successfully fetched documentation")
            print(f"URL: {url}")
            print(f"Status: {response.status_code}")
            print(f"Content length: {len(response.text)} characters")
            
            # Save to file
            with open('okx_docs.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print("\nDocumentation saved to: okx_docs.html")
            
            # Extract key information
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find code blocks
            code_blocks = soup.find_all('code')
            print(f"\nFound {len(code_blocks)} code blocks")
            
            # Find API endpoints
            api_endpoints = []
            for text in soup.stripped_strings:
                if 'api' in text.lower() and 'okx' in text.lower():
                    api_endpoints.append(text)
            
            if api_endpoints:
                print(f"\nFound {len(api_endpoints)} API endpoint references")
                for endpoint in api_endpoints[:5]:
                    print(f"  - {endpoint}")
            
            return True
        else:
            print(f"Failed to fetch documentation: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error fetching documentation: {str(e)}")
        return False

if __name__ == '__main__':
    fetch_okx_docs()
