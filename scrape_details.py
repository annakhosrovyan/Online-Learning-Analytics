import pandas as pd
from bs4 import BeautifulSoup
import requests

def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise Exception(f"Failed to fetch {url}. Status code: {response.status_code}")

def scrape_course_details(course_url):
    try:
        soup = fetch_page_content(course_url)

        languages_available = "Not available"
        enroll = "Not available"
        assignments_count = "Not available"
        taught_language = "Not available"

        enroll = soup.find_all('div', class_="css-1qi3xup")[0].get_text() if soup.find_all('div', class_="css-1qi3xup") else "Not available"

        details = soup.find_all('div', class_="cds-9 css-9271ok cds-11 cds-grid-item cds-56 cds-64 cds-76")
        for detail in details:
            if "Assessments" in detail.get_text():
                assignments_text = detail.find('p', class_='css-vac8rf')
                assignments_count = assignments_text.get_text() if assignments_text else "Not available"
            elif "Taught in" in detail.get_text():
                taught_language_text = detail.find('span')
                taught_language = taught_language_text.get_text() if taught_language_text else "Not available"
                available_languages_button = detail.find('button')
                languages_available = available_languages_button.get_text() if available_languages_button else "Not available"

        return {
            "URL": course_url,
            "Languages Available": languages_available,
            "Enroll Information": enroll,
            "Assignments Count": assignments_count,
            "Taught Language": taught_language
        }
    except Exception as e:
        print(f"Error scraping {course_url}: {e}")
        return {
            "URL": course_url,
            "Languages Available": "Error",
            "Enroll Information": "Error",
            "Assignments Count": "Error",
            "Taught Language": "Error"
        }

if __name__ == "__main__":
    df = pd.read_csv("data.csv")  
    print("Loaded initial course data.")

    course_metadata = []

    for url in df['URL']:
        print(f"Scraping details for {url}...")
        course_details = scrape_course_details(url)
        course_metadata.append(course_details)

    enriched_df = pd.DataFrame(course_metadata)
    enriched_df.to_csv("course_metadata.csv", index=False, encoding='utf-8')

    print("Enriched data with language and course details saved to 'course_metadata.csv'")
