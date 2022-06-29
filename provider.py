from abc import ABC, abstractclassmethod
from markdown_builder.document import MarkdownDocument
from money import Money

import json
import requests


class Provider(ABC):

    def provide_message(self) -> str:
        http_response = self.call_endpoint()
        return self.process_response(http_response)

    @abstractclassmethod
    def call_endpoint(self) -> requests.Response:
        pass

    @abstractclassmethod
    def process_response(self, http_response: requests.Response) -> str:
        pass

    def construct_message(self, name: str, price: int, stock: int, link: str) -> str:
        md = MarkdownDocument()
        md.append_text(f"Sumber: {self.get_provider()}")
        md.append_text(f"Nama: {name}")
        if stock >= 1:
            money: Money = Money(price, "IDR")
            md.append_text(f"Harga: {money.format('id_ID')}")
            md.append_text(f"Stok: {stock}")
        else:
            md.append_text("STOK HABIS!")
        if link != "":
            md.append_text(f"Link: {link}")
        message: str = md.contents()
        md.close()
        return message

    @abstractclassmethod
    def get_provider(self) -> str:
        pass


class TokopediaProvider(Provider):

    def __init__(self, shop_domain: str, product_key: str) -> None:
        self.shop_domain = shop_domain
        self.product_key = product_key

    def call_endpoint(self) -> requests.Response:
        url = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"

        payload = json.dumps([
            {
                "operationName": "PDPGetLayoutQuery",
                "variables": {
                    "shopDomain": f"{self.shop_domain}",
                    "productKey": f"{self.product_key}",
                    "layoutID": "",
                    "apiVersion": 1,
                    "userLocation": {
                        "addressID": "0",
                        "districtID": "2274",
                        "postalCode": "",
                        "latlon": ""
                    },
                    "extParam": ""
                },
                "query": "fragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam) {\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductHighlight\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }
        ])
        headers: dict = {
            'authority': 'gql.tokopedia.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': '_UUID_NONLOGIN_=88ce9995c86f8518c5996f64e467d72e; _UUID_NONLOGIN_.sig=zH8N2utBtpoUKXO_yLpGTzGgQPY; bm_sz=F4BC8573A3337E8EC3E6DACC04E06389~YAAQxiE1F5GZBaSBAQAAY4LzrRDZGG9qSb8UUogUox34YfftKieYnyPB8HLwKSg3RZN9umF79VVmW9iBYI3LY57nAZKQAxt0s6mlQtv8aooK8qACzVUFGNxUdOJovd1F+KphY89EHSQE8BrfrDnnaDcqLR+n1Mc7J2WbS4chICn+8k/su/X8/209UKgadbPHYWG7Z2EYozjK6iej+sYFUthMSLXoTMBF8CyjsJ19yFDZKlcW+Q7J+qrIEadAT3GC+zg74UYr3ODVzI6/cDwJpmcyprn0xWKzL6sttAi9rwblohz53as=~3555891~3228728; _SID_Tokopedia_=crf3AiYTuhRopYoC2gLoAp4GU9D8SxfMrdMtKECxNHAU8FcixmzqimeUfacilmXxZ9Nb3viQfovnto3Ep2ss7Yo198ojqokB6JsXrte-dr9kiP6GUAZ0hUZsnCChO-Sq; DID=908adef22da574a33dc944ad09f042f4a1df17952e8bda33bf98626a6142d66e703f87fccf0a92ac0fa87d64ec8b4ceb; DID_JS=OTA4YWRlZjIyZGE1NzRhMzNkYzk0NGFkMDlmMDQyZjRhMWRmMTc5NTJlOGJkYTMzYmY5ODYyNmE2MTQyZDY2ZTcwM2Y4N2ZjY2YwYTkyYWMwZmE4N2Q2NGVjOGI0Y2Vi47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; ak_bmsc=8B43579CDF4A2B3EC86D477BE38D2792~000000000000000000000000000000~YAAQxiE1F5qZBaSBAQAAuIXzrRDEUYObPpGC1r06wEAzPzMkBowpU9ZCNAnOB6oPr8HYHS9ylUSDI0ZVFHIMNzoZjXjGJmNnav0nlN4BuVXkGwRdZ7xi8D2LGzP2ERo3uovPtqaYoI0sf4ltk1WtL4Cl9+cTAHnG362xq0y82iVHAwADRfy/xr7oO1wye+R8vTzFpbN4zycksSAF8S+zBHLQJ56V2QCvJY7RyGlx6cNjs46kusmOOCCbeKxyZ0wDdWkF+40I7XhChgBDDukKow/d4ZlJNzTN/LoMPR1ftSx8xyaRcJ2eQmwPT49O9ck9pjFg+WpqCBBUkDSIF/p2+pYCLpoZVHcPFBH7y/Ody/rMqMHjgjU40usr0lgDSisKfrBgjVypydpUMaddSlo+UvTqlp+HqEcg/TW9PRtYx7nSk+nFggp9ank8GhkmmMSqjz35QF++KSR8Wk4/W45ivOzKX5MPdhoTTLMGADeHb/WCt1f7CyiqYhJXcgFO0A==; _UUID_CAS_=adfa1033-7528-4d36-b502-129dfe434dcb; _CASE_=7b22644964223a323237342c22614964223a302c226c626c223a224a616b61727461205075736174222c22634964223a3137362c226c6f6e67223a22222c226c6174223a22222c2270436f223a22222c22774964223a31323231303337352c22734964223a31313533303537332c227354797065223a223268222c22776873223a225b7b5c2277617265686f7573655f69645c223a31323231303337352c5c22736572766963655f747970655c223a5c2232685c222c5c225f5f747970656e616d655c223a5c2257617265686f757365735c227d2c7b5c2277617265686f7573655f69645c223a302c5c22736572766963655f747970655c223a5c2231356d5c222c5c225f5f747970656e616d655c223a5c2257617265686f757365735c227d5d227d; _abck=40F1AF91AA6432B0865B6B75C4058114~0~YAAQxiE1F9iZBaSBAQAA8aPzrQjPp1nEKRdmY5YvR7H9Gf3Xds3TkF3D/bmwcK6s4OjhGHotPvyamuY64RRyutQjFAin70ioTamkQxWijFGdNPcZCZUMT2EtBwRvpVcPUKgOw9pInwqCNL06+c1qJngpWXnl2QIlcGqV9KkL4TbMwgYwAmTfwdii8KqDj/vmPjff1GhwzyvShO63vtoJwY1JxxtgjKPSTMbJV37fqHxGiQlGTfHnmZ7Q7Acb8C42s9sBngAkEhsTk5z0q20cROELhZBrWQWqixjBDUhDuZXy5jqBBjsO53H9S/25z4hhfuyXwG6ICwEYZUl2gqvhMvFy8XRE/38BRDyxymoPCC3L4Qfh+9f2hyvUHuT3I4olxMai7ml2/Bl56pcRaeGxOvlr4QzVakdkljgH~-1~-1~-1; _gcl_au=1.1.165750307.1656480842; _gid=GA1.2.793316046.1656480842; _dc_gtm_UA-126956641-6=1; _ga_70947XW48P=GS1.1.1656480841.1.0.1656480841.60; _ga=GA1.2.1048257606.1656480842; _dc_gtm_UA-9801603-1=1; _abck=40F1AF91AA6432B0865B6B75C4058114~-1~YAAQxiE1FxScBaSBAQAAUXf2rQhIeRXlvJTYQluSdE8XJWY/EjD2NdNFd4+7qaDEqkNvezqFJnPIxA6doDj7JU7sBbi0YT+6Gt0T+wknpXeYg/FXwYPeo3XBJwHNbSP27iNIVwdJR2t4/cWfVJqDdsopBcyYjO627M0b6/76Di6nvfMUwDj3DOsBT00vrJtF681u9y0j9Bt8XMzsGy0giFnYIfLXgYc3IXifi9MJFECKILYh1djq9MfgxkL+EVxoOWI8OXLUaK7jKP4kcSNaBIeZeSvDzHb0cirtropzZ+cLPqO0hnJvn7+WIql5HaUflL+wdAzYmCpQEoM1KPpVGEzT1LWmruCWkwTAgM3EcqbZ9dnvCbAF59CMxteTAoUVlELc3gg0NEfVk6sRA+dBg1qOSsaIs35S8/QR~0~-1~-1',
            'origin': 'https://www.tokopedia.com',
            'referer': 'https://www.tokopedia.com/finger-land/borges-extra-light-olive-oil-minyak-zaitun-5-l',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
            'x-device': 'desktop',
            'x-source': 'tokopedia-lite',
            'x-tkpd-akamai': 'pdpGetLayout',
            'x-tkpd-lite-service': 'zeus',
            'x-version': 'c16ac3a'
        }

        return requests.request("POST", url, headers=headers, data=payload)

    def process_response(self, http_response: requests.Response) -> str:
        responses: list = json.loads(http_response.text)
        components: list = responses[0]["data"]["pdpGetLayout"]["components"]
        product_components: list = [
            c for c in components if c["name"] == "product_content"
        ]
        product_component = product_components[0]
        product_data = product_component["data"][0]

        name = product_data["name"]
        price = int(product_data["price"]["value"])
        stock = int(product_data["stock"]["value"])
        link = f"http://tokopedia.com/{self.shop_domain}/{self.product_key}"
        return self.construct_message(name, price, stock, link)

    def get_provider(self) -> str:
        return "TOKOPEDIA"


class SegariProvider(Provider):

    def __init__(self, search_keyword: str) -> None:
        self.search_keyword = search_keyword

    def call_endpoint(self) -> requests.Response:
        url = f"https://api-v2.segari.id/v1.1/products/price?agentId=311&search={self.search_keyword}&variant=WITH_ELASTICSEARCH&size=40&page=0&paginationType=slice"

        headers: dict = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://segari.id',
            'Referer': 'https://segari.id/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
        }

        return requests.request("GET", url, headers=headers, data={})

    def process_response(self, http_response: requests.Response) -> str:
        response: dict = json.loads(http_response.text)
        wrapper: dict = response["data"]
        data: list = wrapper["data"]
        datum: dict = data[0]
        product_dto: dict = datum["productDTO"]
        name: str = f'{product_dto["name"]}, {product_dto["sellingUnit"]}'
        price: int = round(datum["price"])
        stock: int = int(datum["availableQuantity"])
        link = ""
        return self.construct_message(name, price, stock, link)

    def get_provider(self) -> str:
        return "SEGARI"
