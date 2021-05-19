import bs4
import lxml
import requests
import time
from selenium import webdriver


STANDARD_SEARCH_URL = "https://babylonbee.com/news?sort=trending&page={page_id}"
NOT_THE_BEE = "https://notthebee.com"

def search_other_page_for_titles(count: int,
                                url = NOT_THE_BEE,  # Default settings are for notthebee.com
                                button_text = "loadMoreButton",
                                post_header = "post-heading", 
                                driver_path = 'chromedriver', 
                                ) -> list:
    '''
    Parse using selenium discrn articles.
    Disrn layout is a little more complicated then bablyon bees.
    '''
    lst = []
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    
    #while needsToLoop
    input("Press enter to start expanding.")

    iters = 0
    max_tries = 10
    tries = 0
    failed = False
    while iters < count and failed == False:
        success = False
        tries = 0
        while tries < max_tries and success == False:
            try:
                button = driver.find_element_by_id(button_text)
                button.click() # Needs a reasonable delay to wait for button to appear
                success = True
            except Exception as e:
                time.sleep(1)
                tries += 1
                if tries < max_tries:
                    continue
                print(e)
                failed = True
                break
        iters += 1
        print(iters)
    
    print ("Total Iters: " + str(iters))

    articles = driver.find_elements_by_class_name(post_header)
    for article in articles:
        article_text = article.text
        encoded_string = article_text.encode("ascii", "ignore")
        decode_string = encoded_string.decode()
        lst.append(decode_string)

    return lst


def search_page_for_titles(count: int) -> list:
    '''Parse using beautiful soup babylon bee articles'''
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

def gather_content(site_ids: iter, count_not_bee: int) -> None:
    all_titles = []
    
    # Search the other sites using selenium.
    page_titles = search_other_page_for_titles(count_not_bee)
    all_titles.extend(page_titles)

    # Search the main babylon bee.
    for site_id in site_ids:
        page_titles = search_page_for_titles(site_id)
        all_titles.extend(page_titles)
    

    print("Total titles found: " + str(len(all_titles)))
    
    with open("titles.txt", "w+") as fle:
        for title in all_titles:
            fle.write(title + '\n')

if __name__ == "__main__":
    gather_content(range(1, 335), 350)