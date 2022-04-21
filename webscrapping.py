import requests
from bs4 import BeautifulSoup as soup

# URL
base_url = "http://books.toscrape.com/"
index = "index"
page_url = "page-"
extension = ".html"
url = base_url + index + extension


def read_site(url):
    page_html = requests.get(url)
    return soup(page_html.text, "html.parser")


# Get Categories
def get_categories(page:soup):
    links = page.find_all("a", href=True)
    categories = {}
    for link in links:
        href = base_url + link["href"]  # .replace('index.html','page-1.html')
        text = link.text.strip()
        if "catalogue/category" in href:
            categories[text] = [href, get_categories_pages(href)]
    del categories["Books"]  # Delete Books category
    return categories


def get_categories_pages(url):
    page = read_site(url)
    total_pages = page.find_all("li", {"class": "current"})
    if total_pages:
        return int(total_pages[0].text.strip()[-1])
    else:
        return 1


def get_all_books(categories: dict) -> dict:
    books_by_category = {}
    for category, link in categories.items():
        books = []
        for page in range(1, link[1] + 1):
            if page > 1:
                page_link = str(link[0]).replace(
                    "index.html", page_url + str(page) + extension
                )
            else:
                page_link = str(link[0])
            scrape = read_site(page_link)

            for article in scrape.find_all("article"):
                books.append(article.h3.a["title"])
        books_by_category[category] = books
    return books_by_category


def get_books(links: list) -> list:
    link, page_num = links
    books = []
    for page in range(1, page_num + 1):
        if page > 1:
            page_link = str(link).replace(
                "index.html", page_url + str(page) + extension
            )
        else:
            page_link = str(link)
        scrape = read_site(page_link)
        for article in scrape.find_all("article"):
            books.append(article.h3.a["title"])
    return books


page_soup = read_site(url)
categories = get_categories(page_soup)

##%%
Christian = get_books(categories["Christian"])
print(f'====Christian Books====\n')
print(*Christian, sep = '\n')
#%%
books_by_category = get_all_books(categories)
for category, books in books_by_category.items():
    print(f'===={category} Books====\n')
    print(*books, sep='\n')
    print('\n')

