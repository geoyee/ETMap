from typing import Dict
import requests


def text2lnglat(text: str) -> Dict:
    ak = "9ZbPdN2o1OFN7KzvQAH4riVt6bbsQGer"
    url = "https://api.map.baidu.com/geocoding/v3/?address={}&output=json&ret_coordtype=gcj02ll&ak={}".format(
        text, ak
    )
    res = requests.get(url)
    val = res.json()
    if val["status"] == 0:
        output = {
            "lng": val["result"]["location"]["lng"],
            "lat": val["result"]["location"]["lat"],
        }
    else:
        output = None
    return output


if __name__ == "__main__":
    address = "北京市海淀区上地十街10号"
    output = text2lnglat(address)
    print(output)
