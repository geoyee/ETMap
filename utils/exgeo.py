from typing import Dict
import jionlp
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
        self.start_flags = ["时间类"]
        self.v_flags = ["场景事件"]
        self.end_flags = ["w"]  # "w" is punctuation
        self.end_txts = ["；", "、", "，", "。"]  # chinese split punctuation

    def location(self, image_file: str) -> Dict:
        text = self.ocrer.predict(image_file)
        text_list = self.ner(text)
        # print(text_list)
        address_list = []
        text = ""
        # address merge
        for idx, (txt, flag) in enumerate(text_list):
            flag = flag.split("_")[0]
            # start when get a time word
            if flag in self.start_flags:
                text = txt + " "
            # stop when get a chinese split punctuation
            elif flag in self.end_flags and txt in self.end_txts:
                address_list.append(text)
                text = ""
            # skip when get a verb after time
            elif flag in self.v_flags and text_list[idx - 1][-1] in self.start_flags:
                pass
            # add word
            else:
                text += txt
        # geocoding
        time_dict = {}
        md_time = ""  # month and day
        for idx, text in enumerate(address_list):
            if GeoExtracter.is_contains_chinese(text):
                if " " not in text:  # just have address
                    time = address_list[idx - 1].split(" ")[0]
                    address = text
                else:
                    time, address = text.split(" ")
                if address == "":
                    md_time = time
                else:  # just have address
                    address = jionlp.parse_location(
                        self.city + address, change2new=True, town_village=True
                    )["full_location"]
                    # FIXME: update this func: remove punctuation
                    for sign in ["(", ")", "（", "）"]:
                        address = address.replace(sign, "")
                    lnglon = text2lnglat(address)
                    if lnglon is not None:
                        lnglon["time"] = time.split("-")[0].rjust(5, "0")
                        lnglon["address"] = address
                        if md_time not in time_dict.keys():
                            time_dict[md_time] = [lnglon]
                        else:
                            time_dict[md_time].append(lnglon)
        for _, v in time_dict.items():
            v.sort(key=lambda k: (k.get("time", 0)), reverse=False)
        return time_dict

    @classmethod
    def is_contains_chinese(self, text: str) -> bool:
        for _char in text:
            if "\u4e00" <= _char <= "\u9fa5":
                return True
        return False


if __name__ == "__main__":
    path = "data/test.png"
    geo_extracter = GeoExtracter("沈阳市")
    time_dict = geo_extracter.location(path)
    print(time_dict)
