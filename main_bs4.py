import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'http://quotes.toscrape.com'
quotes_data = []
authors_data = []


def scrape_author_info(about_url):
    response = requests.get(about_url)
    if response.status_code == 200:
        about_soup = BeautifulSoup(response.text, 'html.parser')
        born_date_tag = about_soup.find('span', class_='author-born-date')
        born_date = born_date_tag.get_text(strip=True) if born_date_tag else ''
        born_location_tag = about_soup.find('span', class_='author-born-location')
        born_location = born_location_tag.get_text(strip=True) if born_location_tag else ''
        description_tag = about_soup.find('div', class_='author-description')
        description = description_tag.get_text(strip=True) if description_tag else ''
        return born_date, born_location, description
    return '', '', ''


def scrape_quotes(url):
    response = requests.get(url)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({'quote': text, 'author': author, 'tags': tags})

        author_name = author
        about_link = quote.find('a', href=True, string='(about)')
        if about_link:
            about_url = BASE_URL + about_link['href']
            born_date, born_location, description = scrape_author_info(about_url)
            authors_data.append({
                'fullname': author_name,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            })

    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_link = next_page.find('a')['href']
        next_page_url = BASE_URL + next_page_link
        scrape_quotes(next_page_url)


if __name__ == '__main__':

    start_url = BASE_URL
    scrape_quotes(start_url)

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)
