import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from .nlp import filter_content
from .utils import save_to_json, resilient_request, is_relevant, clean_text

# Initialize models
kw_model = KeyBERT()
vectorizer = TfidfVectorizer()

def simple_crawl(url):
    """
    Fetches the content of the given URL and parses it as HTML.

    Args:
        url (str): The URL to fetch and parse.

    Returns:
        BeautifulSoup: The parsed HTML content of the URL, or None if the request fails.
    """
    try:
        response = resilient_request(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        # If the request fails, print an error message and return None
        print(f"Request failed: {e}")
        return None

def crawl_links(soup, base_url, keywords):
    """
    Crawl the given HTML content and extract relevant links based on the given keywords.

    Args:
        soup (BeautifulSoup): The HTML content to crawl.
        base_url (str): The base URL of the HTML content.
        keywords (list): The list of keywords to filter the links.

    Returns:
        list: A list of filtered links that match the given keywords and have a similarity score above the threshold.
    """
    vectorizer.fit(keywords)

    relevant_links = [a['href'] for a in soup.find_all('a', href=True) if is_relevant(a.text, keywords)]
    links = relevant_links[:1] #TODO change back to 5

    filtered_links = []

    for link in links:
        full_url = requests.compat.urljoin(base_url, link)

        try:
            link_content = simple_crawl(full_url).get_text()
            tfidf_matrix = vectorizer.transform([link_content])
            keyword_vector = vectorizer.transform([' '.join(keywords)])
            similarity = cosine_similarity(tfidf_matrix, keyword_vector).flatten()[0]

            if similarity >= 0.3:
                filtered_links.append(full_url)

        except Exception:
            pass

    return filtered_links


def scrape_website(url, instructions):
    """
    Scrape the given URL for information related to the given instructions.

    Args:
        url (str): The URL to scrape.
        instructions (str): The instructions to follow while scraping.

    Returns:
        list: A list of scraped information.
    """
    if instructions is None or instructions == "":
        return None
    
    print(f"Scraping {url}...")
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        soup = simple_crawl(url)
        if soup is not None:
            print(f"Extracting keywords from instructions...")
            # Extract keywords from the user input
            keywords = kw_model.extract_keywords(instructions, top_n=10)
            keywords = [keyword for keyword, _ in keywords]

            print(f"Extracted keywords: {keywords}")

            print(f"Crawling links from {url}...")
            base_url = url
            links = crawl_links(soup, base_url, keywords)

            print(f"Extracted links: {links}")

            filtered_links = [link for link in links if link.startswith(base_url)]

            print(f"Filtered links: {filtered_links}")

            print(f"Filtering content on {len(filtered_links)} pages...")
            documents = []
            for link in filtered_links:
                link_soup = simple_crawl(link)
                if link_soup is not None:
                    print(f"Filtering content on {link}...")
                    # Filter the content
                    filtered_content = filter_content(link_soup.text, keywords)

                    # Clean the content
                    cleaned_content = clean_text(" ".join(filtered_content))
                    sentences = sent_tokenize(cleaned_content)

                    # Save the content to a list of documents
                    documents.append({
                        "url": link, 
                        "content": sentences
                    })

            output_data = {
                "timestamp": timestamp,
                "results": documents
            }

            filename = "output.json"
            save_to_json(output_data, filename)
            print(f"Data saved to {filename}")

            return json.dumps(output_data, ensure_ascii=False, indent=4)
        else:
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

