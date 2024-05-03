# VERSION: 0.1
# AUTHORS: Cycloctane (Cycloctane@octane.top)

from typing import Union
from xml.etree import ElementTree
from http.client import HTTPSConnection

from novaprinter import prettyPrinter

PT_URL = ""
PT_PASSKEY = ""
PT_CATAGORIES = {
    'all': '', 'anime': '','games': '', 'movies': '',
    'music': '', 'software': '', 'tv': '',
}

class nexus:

    name: str = "NexusRSSEngine"
    url: str = PT_URL
    pt_passkey: str = PT_PASSKEY

    supported_categories: dict[str, str] = PT_CATAGORIES

    @staticmethod
    def __parse(text: str) -> None:
        search_result = ElementTree.fromstring(text)
        for item in search_result.find("channel").findall("item"):
            row: dict[str, Union[str, int, None]] = {
                'engine_url': f'https://{nexus.url}/','seeds': -1, 'leech': -1}
            row['name'] = item.findtext("title")
            row['link'] = item.find("enclosure").attrib.get('url', None)
            row['size'] = item.find("enclosure").attrib.get('length', None)
            row['desc_link'] = item.findtext('link')
            prettyPrinter(row)

    @staticmethod
    def __request(target: str, cat: str) -> str:
        conn = HTTPSConnection(nexus.url)
        conn.request("GET",
                     f"/torrentrss.php?search_mode=0&rows=50&passkey={nexus.pt_passkey}&search={target}{'&cat'+cat+'=1' if cat != '' else ''}&linktype=dl", 
                    headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})
        res = conn.getresponse()
        return res.read().decode('utf-8')


    def search(self, what: str, cat: str = 'all') -> None:
        response = nexus.__request(what, nexus.supported_categories[cat])
        nexus.__parse(response)
