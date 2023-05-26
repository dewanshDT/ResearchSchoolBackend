from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup
import requests


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


def getResearchPapers(query="", page=0):
    itemList = []
    status = 200
    error = None
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=shopping&btnG="
    res = requests.get(url)
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
            name = subTitle.split("-")[1].split(",")[0].strip("…").strip()
            print(name)

            # itemList.append(
            #     {
            #         "title": title,
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
        # print(itemList)


getResearchPapers()

ratio = fuzz.partial_ratio("mera naam", "mera naam shyaam hai")
print(ratio)
