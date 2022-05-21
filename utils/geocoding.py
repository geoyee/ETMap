from typing import Dict
import requests
from coord_convert.transform import gcj2wgs


def text2lnglat(text: str) -> Dict:
    ak = "9ZbPdN2o1OFN7KzvQAH4riVt6bbsQGer"
    url = "https://api.map.baidu.com/geocoding/v3/?address={}&output=json&ret_coordtype=gcj02ll&ak={}".format(
        text, ak
    )
    res = requests.get(url)
    val = res.json()
    if val["status"] == 0:
        wgs_lng, wgs_lat = gcj2wgs(
            val["result"]["location"]["lng"], val["result"]["location"]["lat"]
        )
        output = {"lng": wgs_lng, "lat": wgs_lat}
    else:
        output = None
    return output


if __name__ == "__main__":
    address = "北京市海淀区上地十街10号"
    output = text2lnglat(address)
    print(output)
