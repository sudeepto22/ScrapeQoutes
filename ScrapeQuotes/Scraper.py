import multiprocessing
from bs4 import BeautifulSoup
import requests
from MongoDB.Mongo import MongoConnection
from Constants.constants import ConstantVariables


class QuoteScraper(object):
    def __init__(self, url: str):
        self.url = url

    def get_quotes(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html5lib")

        quotes = list()

        table = soup.find("div", attrs={"id": "all_quotes"})

        i = 1
        for row in table.findAll("div"):
            i += 1
            quote = dict()
            if row.img:
                quote["theme"] = row.h5.text
                quote["url"] = "https://www.passiton.com" + row.a["href"]
                quote["img"] = row.img["src"]
                quote["lines"] = row.img["alt"].split("#")[0].strip()

                quote_url = quote['url']
                quote_request = requests.get(quote_url)
                quote_soup = BeautifulSoup(quote_request.content, "html5lib")
                author = quote_soup.find("p").text
                author_desc = quote_soup.find("p").find("small").text

                author_dict = dict()
                author_dict["author_name"] = author.replace(author_desc, "").strip()
                author_dict["author_desc"] = author_desc

                quote["author"] = author_dict
                i += 1
            else:
                if i % 2 == 0:
                    quote["theme"] = row.h5.text
                    quote["url"] = "https://www.passiton.com" + row.h5.a["href"]
                    quote["img"] = None
                    quote["lines"] = row.p.text
                    author = row.findAll("small")
                    author_dict = dict()
                    author_dict["author_name"] = author[0].text
                    author_dict["author_desc"] = author[1].text
                    quote["author"] = author_dict
            if quote:
                quotes.append(quote)

        return quotes

    def store_data(self):
        mongo_connection = MongoConnection(
            ConstantVariables.MONGO_PATH.value,
            ConstantVariables.DB_NAME.value,
            ConstantVariables.QUOTE_COLLECTION_NAME.value
        )
        mongo_connection.connect_mongo()
        mongo_connection.insert_many(self.get_quotes())


def process(page_start, page_end):
    for page_no in range(page_start, page_end + 1):
        print(page_no)
        quote_scraper = QuoteScraper("https://www.passiton.com/inspirational-quotes?page=" + str(page_no))
        quote_scraper.store_data()


def process_quotes():
    p1 = multiprocessing.Process(target=process, args=(1, 15))
    p2 = multiprocessing.Process(target=process, args=(16, 30))
    p3 = multiprocessing.Process(target=process, args=(31, 42))
    p4 = multiprocessing.Process(target=process, args=(43, 116))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()


if __name__ == '__main__':
    process_quotes()
