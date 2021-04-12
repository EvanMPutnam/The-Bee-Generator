import bs4
import lxml
import requests

STANDARD_SEARCH_URL = "https://babylonbee.com/news?sort=trending&page={page_id}"

def search_page_for_titles(count: int) -> list:
    print ("Processing page: " + str(count))

    url = STANDARD_SEARCH_URL.format(page_id = count)
    request = requests.get(url)
    html = request.text

    results = []
    soup = bs4.BeautifulSoup(html, features='lxml')
    divs = soup.find_all('article-card')
    for item in divs:
        title = item[':title']
        title = title.strip("\"")
        results.append(title)
    
    return results

def gather_content(site_ids: iter) -> None:
    all_titles = []
    for site_id in site_ids:
        page_titles = search_page_for_titles(site_id)
        all_titles.extend(page_titles)

    print("Total titles found: " + str(len(all_titles)))
    
    with open("titles.txt", "w+") as fle:
        for title in all_titles:
            fle.write(title + '\n')

if __name__ == "__main__":
    gather_content(range(1, 335))