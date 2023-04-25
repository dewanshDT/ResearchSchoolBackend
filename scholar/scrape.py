import requests
from bs4 import BeautifulSoup


def getResearchPapers(query="", page=0):
    url = f'https://scholar.google.com/scholar?start={0 if page == 1 else page * 10}&hl=en&as_sdt=0%2C5&q={query.replace(" ", "+")}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_=['s_r', 'gs_or', 'gs_scl'])

    itemList = []
    for item in items:
        div = item.find('div', 'gs_ri')
        itemList.append({"title": div.h3.text, "link": div.a['href']})

    return itemList
