from typing import List
from paddlenlp import Taskflow
from .ocr import OCRer
from .geocoding import text2lnglat


class GeoExtracter:
    def __init__(self) -> None:
        self.ocrer = OCRer()
        self.ner = Taskflow("ner")
        self.flags = ["时间类", "世界地区类", "场所类", "组织机构类"]

    def location(self, image_file: str) -> List:
        text = self.ocrer.predict(image_file)
        text_list = self.ner(text)
        address = []
        text = ""
        # address merge
        for txt, flag in text_list:
            flag = flag.split("_")[0]
            # TODO: add time
            if flag in self.flags[1:]:
                if flag == self.flags[1]:
                    address.append(text)
                    text = txt
                else:
                    text += txt
        # geocoding
        lnglon_list = []
        for text in address:
            if len(text) >= 6:
                lnglon = text2lnglat(text)
                if lnglon is not None:
                    lnglon["address"] = text
                    lnglon_list.append(lnglon)
        return lnglon_list


if __name__ == "__main__":
    path = "datas/test.png"
    geo_extracter = GeoExtracter()
    lnglon_list = geo_extracter.location(path)
    print(lnglon_list)
