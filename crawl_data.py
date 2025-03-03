import pandas as pd
import time
import random
import re

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome driver
WEBDRIVER_DELAY_TIME = 10
TIMEOUT = 10
service = Service('/usr/bin/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.headless = True

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(TIMEOUT)
wait = WebDriverWait(driver, WEBDRIVER_DELAY_TIME)


def extract_poem_links(drivers, page_idx):
    """Extracts poem links from a given page index."""
    main_url = f"https://www.thivien.net/searchpoem.php?PoemType=16&ViewType=1&Country=2&Age[]=3&Page={page_idx}"
    driver.get(main_url)
    time.sleep(random.uniform(1, 3))
    
    content_tags_xpath = (
        "//*[@class='page-content container']"
        "//div[@class='page-content-main']"
        "//div[@class='list-item']"
    )
    content_tags = driver.find_elements(By.XPATH, content_tags_xpath)
    
    poem_links = []
    for tag in content_tags:
        try:
            link_element = tag.find_element(By.XPATH, ".//h4[@class='list-item-header']/a")
            poem_links.append({
                "title": link_element.text,
                "url": link_element.get_attribute("href"),
            })
        except Exception as e:
            print(f"Error extracting link: {e}")
            continue
    return poem_links


def clean_poem_html(html):
    """Cleans the poem HTML content by removing unnecessary tags."""
    html = re.sub(r"<img.*?>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<i>.*?</i>", "", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<b>(.*?)</b>(?!\s*(?:<br\s*/?>\s*){2,})", r"\1", html, flags=re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</?p>", "", html, flags=re.IGNORECASE)
    return html.strip()


def scrape_poem(driver, poem_url):
    """Scrapes an individual poem from a given URL."""
    driver.get(poem_url)
    time.sleep(random.uniform(3, 5))
    
    # Extract the title from the page header
    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//header[@class='page-header']/h1"))
        )
        title = title_element.text.strip()
        title = re.sub(r'^["\'"\u201C\u201D\u2033]+|["\'"\u201C\u201D\u2033]+$', '', title)
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = ""
    
    # Extract the poem content
    try:
        poem_content_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.poem-content"))
        )
        html_content = poem_content_tag.get_attribute("innerHTML")
        content = clean_poem_html(html_content)
    except Exception as e:
        print(f"Error extracting content: {e}")
        poem_src = ""
    
    # Extract the source information
    try:
        poem_src_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='small']"))
        )
        poem_src = poem_src_tag.text
    except Exception as e:
        print(f"Error extracting source: {e}")
        poem_src = ""
    
    poem = {"title": title, "content": content, "source": poem_src, "url": poem_url}
    return [poem]


def scrape_poems(driver, num_pages=10):
    """Scrapes poems from multiple pages."""
    datasets = []
    for page_idx in tqdm(range(1, num_pages + 1)):
        poem_links = extract_poem_links(driver, page_idx)
        for poem in poem_links:
            try:
                poems = scrape_poem(driver, poem["url"])
                datasets.extend(poems)
            except Exception as e:
                print(f"Error scraping poem: {e}")
                continue
    return datasets


if __name__ == "__main__":
    datasets = scrape_poems(driver, num_pages=10)
    driver.quit()

    df = pd.DataFrame(datasets)
    df.to_csv("poem_data.csv", index=False)
