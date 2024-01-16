"""
MangaDex info reader

Retrieves data about a particular manga by title.
"""

from typing import List

import requests
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


"""
Arguments:
    title (str): Manga title
    lang (str, optional): Get data in this ISO 639-1 language code. Defaults to "en".
    
"""
class MangaDexReader(BaseReader):
    def __init__(
        self,
        title: str,
        lang: str = "en"
    ):
        self.title = title
        self.lang = lang
        self.base_url = "https://api.mangadex.org"


    def load_data(self) -> List[Document]:
        manga_request = requests.get(
            f"{self.base_url}/manga",
            params={"title": self.title}
        )
        manga = manga_request.json()['data'][0]
        print(manga)

        chapter_request = requests.get(
            f"{self.base_url}/manga/{manga['id']}/feed",
            params={'translatedLanguage[]': [self.lang]}
        )
        chapters = chapter_request.json()

        tags = [tag['attributes']['name'].get(self.lang, None) for tag in manga['attributes']['tags']]
        tags = []
        for tag in manga['attributes']['tags']:
            tag_name_dict = tag['attributes']['name']
            if self.lang in tag_name_dict:
                tags.append(tag_name_dict[self.lang])

        print(chapters)
        extra_info={
            'id': manga['id'],
            'description': manga['attributes']['description'].get(self.lang, ''),
            'original_language': manga['attributes']['originalLanguage'] or '',
            'tags': tags,
            'chapter_count': chapters['total'],
            # TODO get author
            # TODO get artist
            # TODO get latest chapter number and date
        }

        print(extra_info)
        doc = Document(
            text=manga['attributes']['title'].get(self.lang, self.title),
        )
        print(doc)

if __name__ == "__main__":
    reader = MangaDexReader(
        title = 'Grand Blue Dreaming',
        lang = 'en'
    )

    reader.load_data()
