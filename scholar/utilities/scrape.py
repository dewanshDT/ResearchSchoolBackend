import requests
from bs4 import BeautifulSoup
from scholar.models import PaperIndex
from fuzzywuzzy import fuzz


class BlockedIpException(Exception):
    pass


class Response:
    def __init__(self, status, itemList, error):
        self.status = status
        self.itemList = itemList
        self.error = error


def getResearchPapers(query="", page=0):
    itemList = []
    status = 200
    error = None
    url = f'https://scholar.google.com/scholar?start={0 if page == 1 else page * 10}&hl=en&as_sdt=0%2C5&q={query.replace(" ", "+")}'
    res = requests.get(url)
    if res.status_code == 429:
        status = res.status_code
        error = res.text
        raise BlockedIpException(res)
    print(res.status_code)
    soup = BeautifulSoup(res.content, "html.parser")
    items = soup.find_all("div", class_=["s_r", "gs_or", "gs_scl"])

    for item in items:
        try:
            div = item.find("div", "gs_ri")
            title = div.h3.text.strip()
            subTitle = div.select_one("div.gs_a").text.strip()
            link = div.a["href"]
            author_a = div.select_one("div.gs_a a")
            content = div.select_one("div.gs_rs").text.strip()

            itemList.append(
                {
                    "title": title,
                    "subTitle": subTitle,
                    "link": link,
                    "author": {
                        "name": author_a.text if author_a else "",
                        "link": "https://scholar.google.com{user}".format(
                            user=author_a["href"]
                        )
                        if author_a
                        else "",
                    },
                    "content": content,
                }
            )
        except AttributeError:
            print(f"⚠️ Attribution Error at item: {title}")
        return Response(status, itemList, error)


def getPapers(query, num=5):
    paperList = []
    status = 200
    error = None
    try:
        page = 1
        paperIndex = PaperIndex.objects.all()
        while len(paperList) < num:
            res = getResearchPapers(query, page)
            papers = res.itemList
            for paper in papers:
                for index in paperIndex:
                    ratio = fuzz.partial_ratio(index.journal_name, paper["title"])
                    if ratio > 90 and len(paperList) < num:
                        paperList.append(paper)
                        print(index.serial_no, index.journal_name, ratio)
                        break
                    else:
                        continue
            page += 1
    except BlockedIpException as e:
        error = e.args[0].text
        status = 429

    return Response(status, paperList, error)
