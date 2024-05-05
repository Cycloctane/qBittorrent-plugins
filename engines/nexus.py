# VERSION: 0.3
# AUTHORS: Cycloctane (Cycloctane@octane.top)

from typing import Union
from xml.etree import ElementTree
from http.client import HTTPSConnection
from urllib.parse import urlparse

from novaprinter import prettyPrinter

# edit pt site url and passkey here.
SITE_URL = "https://"
PASSKEY = ""

# check catagories in /getrss.php
CATAGORIES = {
    'anime': '','games': '', 'movies': '',
    'music': '', 'software': '', 'tv': '',
}


class nexus:

    name: str = "NexusRSS"
    url: str = SITE_URL

    supported_categories: dict[str, str] = {'all': ''} | CATAGORIES

    @staticmethod
    def __print_message(msg: str) -> None:
        prettyPrinter({'engine_url': nexus.url,'seeds': -1, 'leech': -1, 'size': 0,
                        'name': msg, 'link': 'no link','desc_link': nexus.url})

    @staticmethod
    def __parse(text: str) -> None:
        if text == "invalid passkey": raise Exception("invalid passkey")
        try:
            search_result = ElementTree.fromstring(text)
            if len(search_result.find("channel").findall("item")) == 0:
                nexus.__print_message("no results found")
                return
            for item in search_result.find("channel").findall("item"):
                row: dict[str, Union[str, int, None]] = {
                    'engine_url': nexus.url,'seeds': -1, 'leech': -1}
                row['name'] = item.findtext("title")
                row['link'] = item.find("enclosure").attrib.get('url', None)
                row['size'] = item.find("enclosure").attrib.get('length', None)
                if None in row.values(): raise Exception("parse error")
                row['desc_link'] = item.findtext('link')
                prettyPrinter(row)
        except (ElementTree.ParseError, AttributeError, KeyError): raise Exception("parse error")

    @staticmethod
    def __request(target: str, cat: str) -> str:
        conn = HTTPSConnection(urlparse(nexus.url).hostname, urlparse(nexus.url).port, timeout=4)
        conn.request("GET",
                     f"/torrentrss.php?search_mode=0&rows=50&passkey={PASSKEY}&search={target}{'&cat'+cat+'=1' if cat != '' else ''}&linktype=dl", 
                    headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})
        res = conn.getresponse()
        if res.status != 200: raise Exception(f"http status code {res.status}")
        return res.read().decode('utf-8')


    def search(self, what: str, cat: str = 'all') -> None:
        try:
            nexus.__parse(nexus.__request(what, nexus.supported_categories[cat]))
        except Exception as e:
            nexus.__print_message("error: "+str(e))
