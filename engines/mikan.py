# VERSION: 0.3
# AUTHORS: Cycloctane (Cycloctane@octane.top)

from typing import Union
from xml.etree import ElementTree
from http.client import HTTPSConnection
from urllib.parse import urlparse

from novaprinter import prettyPrinter


class mikan:

    name: str = "MikanRSS"
    url: str = "https://mikanime.tv"

    supported_categories: dict[str, str] = {
        'all': '',
        'anime': ''
    }

    @staticmethod
    def __print_message(msg: str) -> None:
        prettyPrinter({'engine_url': mikan.url,'seeds': -1, 'leech': -1, 'size': 0,
                        'name': msg, 'link': 'no link','desc_link': mikan.url})

    @staticmethod
    def __request(target: str) -> str:
        conn = HTTPSConnection(urlparse(mikan.url).hostname, urlparse(mikan.url).port, timeout=4)
        conn.request("GET", f"/RSS/Search?searchstr={target}", 
                    headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})
        res = conn.getresponse()
        if res.status != 200: raise Exception(f"http status code {res.status}")
        return res.read().decode('utf-8')

    @staticmethod
    def __parse(text: str) -> None:
        try:
            search_result = ElementTree.fromstring(text)
            if len(search_result.find("channel").findall("item")) == 0:
                mikan.__print_message("no results found")
                return
            for item in search_result.find("channel").findall("item"):
                row: dict[str, Union[str, int, None]] = {
                    'engine_url': mikan.url,'seeds': -1, 'leech': -1}
                row['name'] = item.findtext("title")
                row['link'] = item.find("enclosure").attrib.get('url', None)
                row['size'] = item.find("enclosure").attrib.get('length', None)
                if None in row.values(): raise Exception("parse error")
                row['desc_link'] = item.findtext('link')
                prettyPrinter(row)
        except (ElementTree.ParseError, AttributeError, KeyError): raise Exception("parse error")


    def search(self, what: str, cat: str = 'all') -> None:
        try:
            mikan.__parse(mikan.__request(what))
        except Exception as e:
            mikan.__print_message("error: "+str(e))
