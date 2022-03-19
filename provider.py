from abc import ABC, abstractclassmethod
from markdown_builder.document import MarkdownDocument

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
            md.append_text(f"Harga: {price}")
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
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-source': 'tokopedia-lite',
            'x-device': 'desktop',
            'x-tkpd-lite-service': 'zeus',
            'x-tkpd-akamai': 'pdpGetLayout',
            'sec-gpc': '1',
            'origin': 'https://www.tokopedia.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'en-US,en;q=0.9',
            'Cookie': '_abck=BF429C6FB640552EDD63CF3A40DCBF59~-1~YAAQniE1FzbmRyF/AQAAmknbYgf2Z/REhuYAjKaut0K+7+UMzIoLlo0iQk/0hhoB1nR931fD5UQY3A0K8g9gAFWLi80cXhvJtjQXhE4tzTDT5nCVZ/CK2A/Rz2OaQsweyBaOth+gxnv0GaeYWb5+KY62+03rkT7z5JQjMCs7W5ieoNYJm+HFRPXa3/4qVKldOhasaRNBnrkTBKpHWc5zbXoWWJDElE/dz+2fKkWbB/AgMDu0ug9G9lsUL3kYGP12YDd4CW1kQcBqQk/a650RKph3XRL9gk6Qf2zYDy9v8Jl9sjXczwnvFxdKMVezvZAK4ZrPlBTS1z3EwepG8MfupT2TJ4GJ38PSRuSTRy0cUP5jeoHoJsaKPJHHKG/lmVVdSW4zjFYgx5xm3/103tne+NJPAf1cLFi5mdUt~0~-1~-1; _abck=BF429C6FB640552EDD63CF3A40DCBF59~-1~YAAQtCE1Fx7tRGZ/AQAAhx/hggdD/3m+4fwhQXTqsKv9G44o+hx6Q4wEZAVIM0p0ljPYGd0T4kMbjn56DnuFE2f0ZA7L/5/yQkoU9usEtxH4rHEqPScI/x7Wn7C27t9Rh+jfybjQsdbW6SjtatrjbL4YnSwcGpuPY3S2XtwFvTvV4Ph29v9Y8/rsxlAWp7jEuWqFK1NvWeeH9QYH2ALebsJoCwhnf0WJ0GGK62dFuGUBqS+yzfDSHTJEnwfbn8Z5PAwiQK7ku+7p28RuFNQaREgDnYiqdzPgKv3y5GAJxdA7ZFjjh52BES1qIRBl/lyziMe3WudsEQZXdMFGvDe2yGzhonfB8yE4vfKxYLln7LtH21avQRQMBdJ1CKNkxxo4HsEILaaFWxx2Q7BbO3UbQCVtXpEXaZTLH2gJdQ==~-1~-1~-1; bm_sz=9ADD9106F2E975B01CCBA67D039B2050~YAAQtCE1Fx/tRGZ/AQAAhx/hgg+URPaewuO92kDf8XiYnow0u89lkJ1I6czHRSPj4k6rgAVYkdsnlNngHxIvbl8YYl5Rv4tukYhkkcovATC543gqtEGoQclEnWZJ6DXHRy8XI6SbMtpvlQWzn5LPDVOjxnDDRfghpNH9dPjiRPyeZzUBrnSpPp66t5f3zpKwUq6fJUmb84J6D3VXGnWmCFIB5Z201EIgSxsDasaKAjMHWgqqFexcUn6oWPSwFCHdgPS9PRzHfcD1S1wTDyZYjiaHj0WH5zi5awvuYcvd3bEiK+/kvcE=~4469557~3425592'
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
        url = f"https://api-v2.segari.id/v1.1/products/price?agentId=311&search={self.search_keyword}&size=40&page=0&paginationType=slice"

        headers: dict = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
            'Accept': '*/*',
            'Sec-GPC': '1',
            'Origin': 'https://segari.id',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://segari.id/',
            'Accept-Language': 'en-US,en;q=0.9'
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


class ShopeeMallProvider(Provider):

    def __init__(self, shop_id: str, item_id: str) -> None:
        self.shop_id = shop_id
        self.item_id = item_id


    def call_endpoint(self) -> requests.Response:
        url = f"https://shopee.co.id/api/v4/item/get?itemid={self.item_id}&shopid={self.shop_id}"

        payload: dict = {}
        headers: dict = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        return requests.request("GET", url, headers=headers, data=payload)


    def process_response(self, http_response: requests.Response) -> str:
        response: dict = json.loads(http_response.text)
        product = response["data"]

        name = product["name"]
        price = round(int(product["price"]) / 100000)
        stock = product["stock"]
        link = f'https://shopee.co.id/{name.replace(" ", "-")}-i.{self.shop_id}.{self.item_id}'
        return self.construct_message(name, price, stock, link)


    def get_provider(self) -> str:
        return "SHOPEE MALL"
