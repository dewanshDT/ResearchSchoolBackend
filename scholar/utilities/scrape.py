import requests
from bs4 import BeautifulSoup
from scholar.models import PaperIndex
from fuzzywuzzy import fuzz
import re


class BlockedIpException(Exception):
    pass


class Response:
    def __init__(self, status, itemList, error):
        self.status = status
        self.itemList = itemList
        self.error = error


def extract_authors_and_year(subtitle):
    author_pattern = r"([^-,]+(?:, [^-,]+)*)(?=\s*-\s)"  # Pattern to match author names before the dash "-"
    year_pattern = (
        r"\b(19|20)\d{2}\b"  # Pattern to match four-digit years starting with 19 or 20
    )

    author_match = re.search(author_pattern, subtitle)
    year_match = re.search(year_pattern, subtitle)

    authors = author_match.group().strip() if author_match else None
    year = int(year_match.group()) if year_match else None

    return authors, year


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
            name = subTitle.split("-")[1].split(",")[0].strip("…").strip()
            link = div.a["href"]
            author_a = div.select_one("div.gs_a a")
            content = div.select_one("div.gs_rs").text.strip()
            authors, year = extract_authors_and_year(subTitle)
            citations = (
                div.select_one("div.gs_fl")
                .find_all(recursive=False)[2]
                .text.split(" ")[2]
            )

            itemList.append(
                {
                    "title": title,
                    "journalName": name,
                    "subTitle": subTitle,
                    "link": link,
                    "year": year,
                    "author": {
                        "name": authors if authors else "",
                        "link": "https://scholar.google.com{user}".format(
                            user=author_a["href"]
                        )
                        if author_a
                        else "",
                    },
                    "content": content,
                    "citations": citations,
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
                    ratio = fuzz.partial_ratio(index.journal_name, paper["journalName"])
                    if ratio > 95 and len(paperList) < num:
                        paper[
                            "index"
                        ] = f"{index.abdc} {index.abs} {index.ft50} {index.scopus} {index.wos}".strip()
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
