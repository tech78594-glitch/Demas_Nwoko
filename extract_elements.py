import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def extract_webpage_to_html(url, output_file='extracted_page.html', download_assets=False):
    """
    Extract all HTML elements from a webpage and save to a file.
    
    Args:
        url: The webpage URL to extract
        output_file: Name of the output HTML file
        download_assets: If True, downloads CSS, JS, and images locally
    """
    try:
        # Send GET request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # If download_assets is True, download external resources
        if download_assets:
            print("Downloading assets...")
            assets_dir = 'assets'
            os.makedirs(assets_dir, exist_ok=True)
            
            # Download CSS files
            for link in soup.find_all('link', rel='stylesheet'):
                if link.get('href'):
                    download_resource(link['href'], url, assets_dir, link, 'href')
            
            # Download JavaScript files
            for script in soup.find_all('script', src=True):
                download_resource(script['src'], url, assets_dir, script, 'src')
            
            # Download images
            for img in soup.find_all('img', src=True):
                download_resource(img['src'], url, assets_dir, img, 'src')
        
        # Save the HTML to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        print(f"✓ Successfully extracted HTML to '{output_file}'")
        print(f"✓ File size: {os.path.getsize(output_file)} bytes")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching the webpage: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def download_resource(resource_url, base_url, assets_dir, tag, attr):
    """Helper function to download external resources"""
    try:
        full_url = urljoin(base_url, resource_url)
        response = requests.get(full_url, timeout=5)
        response.raise_for_status()
        
        # Create filename from URL
        filename = os.path.basename(urlparse(full_url).path) or 'index'
        filepath = os.path.join(assets_dir, filename)
        
        # Save the resource
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Update the tag's attribute to point to local file
        tag[attr] = filepath
        print(f"  Downloaded: {filename}")
        
    except Exception as e:
        print(f"  Failed to download {resource_url}: {e}")

# Example usage
if __name__ == "__main__":
    # Example 1: Extract HTML only
    url = input("Enter the webpage URL: ").strip()
    extract_webpage_to_html(url, output_file='page.html', download_assets=False)
    
    # Example 2: Extract HTML and download assets (uncomment to use)
    # extract_webpage_to_html(url, output_file='page_with_assets.html', download_assets=True)