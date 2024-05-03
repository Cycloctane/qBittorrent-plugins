# VERSION: 0.1
# AUTHORS: Cycloctane (Cycloctane@octane.top)

from typing import Union
from xml.etree import ElementTree
from http.client import HTTPSConnection

from novaprinter import prettyPrinter

MIKAN_URL = "mikanime.tv"

class mikan:

    url: str = MIKAN_URL
    name: str = "MikanRSSEngine"

    supported_categories = {
        'all': '',
        'anime': ''
    }

    @staticmethod
    def __request(target: str) -> str:
        conn = HTTPSConnection(mikan.url)
        conn.request("GET", f"/RSS/Search?searchstr={target}", 
                    headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})
        res = conn.getresponse()
        return res.read().decode('utf-8')

    @staticmethod
    def __parse(text: str) -> None:
        search_result = ElementTree.fromstring(text)
        for item in search_result.find("channel").findall("item"):
            row: dict[str, Union[str, int, None]] = {
                'engine_url': 'https://mikanime.tv/','seeds': -1, 'leech': -1}
            row['name'] = item.findtext("title")
            row['link'] = item.find("enclosure").attrib.get('url', None)
            row['size'] = item.find("enclosure").attrib.get('length', None)
            row['desc_link'] = item.findtext('link')
            prettyPrinter(row)


    def search(self, what: str, cat: str = 'all') -> None:
        response = mikan.__request(what)
        mikan.__parse(response)
