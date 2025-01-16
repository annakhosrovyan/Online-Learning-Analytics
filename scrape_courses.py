import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise Exception(f"Failed to fetch {url}. Status code: {response.status_code}")

def extract_course_titles(soup):
    return [item.get_text() for item in soup.find_all('h3', class_="cds-CommonCard-title css-6ecy9b")]

def extract_course_organizations(soup):
    return [item['title'] for item in soup.find_all('div', class_='css-18juqt8 cds-ProductCard-partners')]

def extract_course_urls(soup):
    base_url = "https://www.coursera.org"
    links = [item['href'] for item in soup.find_all('a', class_="cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142")]
    return [base_url + link for link in links]

def extract_course_ratings(soup):
    return [item.get_text() for item in soup.find_all('span', class_='css-6ecy9b')]

def extract_course_metadata(soup):
    return [item.get_text() for item in soup.find_all('div', class_='cds-CommonCard-metadata')]

def extract_course_skills(soup):
    return [item.get_text() for item in soup.find_all('div', class_='cds-CommonCard-bodyContent')]


def scrape_coursera_courses(url, max_pages=1):
    courses = []
    for page_number in range(1, max_pages + 1):
        print(f"Scraping page {page_number}...")
        page_url = f"{url}?page={page_number}"
        soup = fetch_page_content(page_url)
        
        titles = extract_course_titles(soup)
        organizations = extract_course_organizations(soup)
        urls = extract_course_urls(soup)
        ratings = extract_course_ratings(soup)
        metadata = extract_course_metadata(soup)
        skills = extract_course_skills(soup)

        for i in range(len(titles)):
            courses.append({
                "Title": titles[i] if i < len(titles) else None,
                "Organization": organizations[i] if i < len(organizations) else None,
                "URL": urls[i] if i < len(urls) else None,
                "Rating": ratings[i] if i < len(ratings) else None,
                "Metadata": metadata[i] if i < len(metadata) else None,
                "Skills": skills[i] if i < len(skills) else None,
            })

    df = pd.DataFrame(courses)
    return df


if __name__ == "__main__":
    base_url = "https://www.coursera.org/courses"
    max_pages = 83  
    
    try:
        course_data = scrape_coursera_courses(base_url, max_pages=max_pages)
        course_data.to_csv("data.csv", index=False, encoding='utf-8')
        print("Data saved")
    except Exception as e:
        print(f"Error: {e}")
