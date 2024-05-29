import requests
from bs4 import BeautifulSoup as sp
data_string = ""

def recommand_list(soup):

    mw_content = soup.find("div", class_ = "mw-content-ltr mw-parser-output")

    mw_headline = soup.find_all("span", class_ = "mw-headline")
    mw_ul = mw_content.find_all("ul")

    for headline in mw_headline:
        for ul in mw_ul:
            for li in ul.find_all("li"):
                continue


def goto_(url):
    global data_string
    response = requests.get(url)
    soup = sp(response.text, "html.parser")

    #class="mw-body-header vector-page-titlebar"
    #<h1 id="firstHeading" class="firstHeading mw-first-heading">

    title = soup.find('header', class_ = "mw-body-header vector-page-titlebar")
    title = title.find('h1', class_ = "firstHeading mw-first-heading")
    content = soup.find('div', class_ = "mw-content-ltr mw-parser-output")

    #tocright
    if content.find('div', class_="tocright"):
        recommand_list(soup)
    else:

        try:
            profile = content.find_all('p')[1]
            data_string += title.text + "\n" + profile.text + "\n\n"

        except:

            pass


def search_result_info(soup):

    for result in soup.find_all("div", class_="mw-search-result-heading"):
        title = result.find("a")['title']
        link = f"https://en.wikipedia.org{result.find('a')['href']}"
        goto_(link)


def search_information_from_wiki(key_word):

    global data_string
    data_string = ""

    #key_words = extract_keywords(text)

    #for index, key_word in keyword.items():
    #    print(index, key_word) 
    key_word = key_word.replace(" ","+")
    error_word = f"The page \"{key_word}\" does not exist. You can create a draft and submit it for review or request that a redirect be created, but consider checking the search results below to see whether the topic is already covered."
    url = f"https://en.wikipedia.org/w/index.php?search={key_word}&title=Special:Search&profile=advanced&fulltext=1&ns0=1"

    response = requests.get(url)
    soup = sp(response.text, "html.parser")


    search_result = soup.find("div", class_ = "mw-search-results-info").text.strip()

    if search_result == error_word.strip():

        data_string = f'I did not find anything, sorry.'

    else:

        search_result_info(soup)

    return data_string

