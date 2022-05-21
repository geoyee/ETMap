from typing import List
from paddlenlp import Taskflow

try:
    from .ocr import OCRer
    from .geocoding import text2lnglat
except:
    from ocr import OCRer
    from geocoding import text2lnglat


class GeoExtracter:
    def __init__(self, city: str = "") -> None:
        self.city = city
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
            if flag in self.flags:
                # time
                if flag == self.flags[0]:
                    address.append(text)
                    text = txt + " "
                else:
                    text += txt
        # geocoding
        lnglon_list = []
        for text in address:
            if GeoExtracter.is_contains_chinese(text):
                time, address = text.split(" ")
                if address != "":
                    address = self.city + address
                    lnglon = text2lnglat(address)
                    if lnglon is not None:
                        lnglon["time"] = time.split("-")[0].rjust(5, "0")
                        lnglon["address"] = address
                        lnglon_list.append(lnglon)
        lnglon_list.sort(key=lambda k: (k.get("time", 0)), reverse=False)
        return lnglon_list

    @classmethod
    def is_contains_chinese(self, text: str) -> bool:
        for _char in text:
            if "\u4e00" <= _char <= "\u9fa5":
                return True
        return False


if __name__ == "__main__":
    path = "datas/test.png"
    geo_extracter = GeoExtracter()
    lnglon_list = geo_extracter.location(path)
    print(lnglon_list)
