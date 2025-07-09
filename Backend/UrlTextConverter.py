import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def extract_text_from_url(url):
    """
    This method takes any url and returns the extracted text from the html body.
    It works by using playwright as browser emulator, that scrapes the html context.
    The html context is then parsed with bs4 to easily clean the html-content from unwanted tags and extract visible text
    This text is then returned
    :param url: url that should be scraped and parsed
    :return: meaningful text from this website
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # remove tags where no meaningful text is expected
        for tag in soup(['header', 'footer', 'nav']):
            tag.decompose()
        # Extract visible text
        text = ' '.join(soup.stripped_strings)
        # Optional: Clean up whitespace
        text = re.sub(r'\s{2,}', ' ', text)

        browser.close()

        return text

# Tutorial Code:

# results = soup.find(id="ResultsContainer")
# python_jobs = results.find_all(
#     "h2", string=lambda text: "python" in text.lower()
# )
# # Find the parent because python_jobs are only the headlines
# python_job_cards = [
#     h2_element.parent.parent.parent for h2_element in python_jobs
# ]
# #job_cards = results.find_all("div", class_="card-content")
# for job_card in python_job_cards:
#     title_element = job_card.find("h2", class_="title")
#     company_element = job_card.find("h3", class_="company")
#     location_element = job_card.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#
#     links = job_card.find_all("a")
#     for link in links:
#         link_url = link["href"]
#         print(f"Apply here: {link_url}\n")
