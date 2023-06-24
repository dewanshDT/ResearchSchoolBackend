from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup
import requests
import re


# itemList = []
# status = 200
# error = None
# url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=peri+peri&btnG="
# res = requests.get(url)
# print(res.status_code)
# soup = BeautifulSoup(res.content, "html.parser")
# items = soup.find_all("div", class_=["s_r", "gs_or", "gs_scl"])
# print(len(items))

# for item in items:
#     div = item.find("div", "gs_ri")
#     title = div.h3.text.strip()
#     subTitle = div.select_one("div.gs_a").text.strip()
#     link = div.a["href"]
#     author_a = div.select_one("div.gs_a a")
#     content = div.select_one("div.gs_rs").text.strip()
#     name = subTitle.split("-")

#     print(name)

#     itemList.append(
#         {
#             "title": title,
#             "subTitle": subTitle,
#             "link": link,
#             "author": {
#                 "name": author_a.text if author_a else "",
#                 "link": "https://scholar.google.com{user}".format(
#                     user=author_a["href"]
#                 )
#                 if author_a
#                 else "",
#             },
#             "content": content,
#         }
#     )


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
    print(res.status_code)
    soup = BeautifulSoup(res.content, "html.parser")
    items = soup.find_all("div", class_=["s_r", "gs_or", "gs_scl"])

    for item in items:
        try:
            div = item.find("div", "gs_ri")
            title = div.h3.text.strip()
            subTitle = div.select_one("div.gs_a").text.strip()
            citations = (
                div.select_one("div.gs_fl")
                .find_all(recursive=False)[2]
                .text.split(" ")[2]
            )
            name = subTitle.split("-")[1].split(",")[0].strip("…").strip()
            link = div.a["href"]
            author_a = div.select_one("div.gs_a a")
            content = div.select_one("div.gs_rs").text.strip()
            yearlist = subTitle.split(",")[-1].strip().split(" - ")
            authors, year = extract_authors_and_year(subTitle)

            # print(author_a.text)
            # print(author_a["href"])
            # print(subTitle)
            # print(year)
            # print(authors)
            print(title)

            # itemList.append(
            #     {
            #         "title": title,
            #         "journalName": name,
            #         "subTitle": subTitle,
            #         "link": link,
            #         "author": {
            #             "name": author_a.text if author_a else "",
            #             "link": "https://scholar.google.com{user}".format(
            #                 user=author_a["href"]
            #             )
            #             if author_a
            #             else "",
            #         },
            #         "content": content,
            #     }
            # )

        except AttributeError:
            print(f"⚠️ Attribution Error at item: {title}")
        except:
            print("something went wrong")


getResearchPapers("fuzzy logic")

ratio = fuzz.partial_ratio("mera naam", "mera naam shyaam hai")
print(ratio)
