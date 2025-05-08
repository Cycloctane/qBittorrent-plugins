# VERSION: 0.4
# AUTHORS: Cycloctane (Cycloctane@octane.top)

import urllib.request
from xml.etree import ElementTree

from helpers import headers
from novaprinter import prettyPrinter

# edit pt site url and passkey here.
SITE_URL = "https://"
SITE_NAME = "NexusPHP"
PASSKEY = ""

# check catagories in /getrss.php
CATAGORIES = {
    'anime': '', 'games': '', 'movies': '',
    'music': '', 'software': '', 'tv': '',
}


class nexus:

    name = SITE_NAME
    url = SITE_URL

    supported_categories = {'all': ''} | CATAGORIES

    @classmethod
    def __print_message(cls, msg: str) -> None:
        prettyPrinter({'engine_url': cls.url, 'seeds': -1, 'leech': -1, 'size': 0,
                       'name': msg, 'link': 'no link', 'desc_link': cls.url})

    @classmethod
    def __parse(cls, text: str) -> None:
        if text == "invalid passkey": raise Exception("invalid passkey")
        try:
            search_result = ElementTree.fromstring(text)
            for item in search_result.find("channel").findall("item"):
                row = {'engine_url': cls.url, 'seeds': -1, 'leech': -1}
                row['name'] = item.findtext("title")
                row['link'] = item.find("enclosure").attrib['url']
                row['size'] = item.find("enclosure").attrib['length']
                row['desc_link'] = item.findtext('link')
                prettyPrinter(row)
        except (ElementTree.ParseError, AttributeError, KeyError):
            raise Exception("parse error")

    @classmethod
    def __request(cls, target: str, cat: str) -> str:
        req = urllib.request.Request(
            f"{cls.url}/torrentrss.php"
            f"?search_mode=0&rows=50&passkey={PASSKEY}&search={target}{'&cat'+cat+'=1' if cat != '' else ''}&linktype=dl",
            headers=headers
        )
        res = urllib.request.urlopen(req)
        if res.status != 200: raise Exception(f"http status code {res.status}")
        return res.read().decode('utf-8')

    def search(self, what: str, cat: str = 'all') -> None:
        try:
            self.__parse(self.__request(what, self.supported_categories[cat]))
        except Exception as e:
            self.__print_message("error: "+str(e))
