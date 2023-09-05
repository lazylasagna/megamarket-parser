import json

import requests
from mysql.connector import connect, Error

url = 'https://megamarket.ru/catalog/smartfony/'

cookies = {
    'spid': '1693912042676_b6114a46ecbab87c6884a10d1806a0d3_brhnxlfjm6j3gqdp',
    'spsc': '1693912042676_205d00a1781e8977e2e0a67ba0e90aa6_a5476469b72f558bb72e6aae99c6a060',
    '_ym_uid': '1693912021492043451',
    '_ym_d': '1693912021',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
    'device_id': '64a8e116-4bdc-11ee-ae43-0242ac1e0004',
    'sbermegamarket_token': 'e05d31f0-7db9-4bd0-9f45-3f9a868691c4',
    'ecom_token': 'e05d31f0-7db9-4bd0-9f45-3f9a868691c4',
    '_ga': 'GA1.1.1562800114.1693912022',
    'isOldUser': 'true',
    '_sa': 'SA1.22d25c62-1e62-4e1f-ae71-43cbf08f2afb.1693912022',
    '__zzatw-smm': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UbN1ddHBEkWA4hPwsXXFU+NVQOPHVXLw0uOF4tbx5lUFwoRFdUCSYfF3dnFRtQSxgvS18+bX0yUCs5Lmw=jGrqoA==',
    'region_info': '%7B%22displayName%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%22%2C%22kladrId%22%3A%225000000000000%22%2C%22isDeliveryEnabled%22%3Atrue%2C%22geo%22%3A%7B%22lat%22%3A55.755814%2C%22lon%22%3A37.617635%7D%2C%22id%22%3A%2250%22%7D',
    '_ga_W49D2LL5S1': 'GS1.1.1693912021.1.1.1693912782.57.0.0',
    'cfidsw-smm': 'b4BBiidIcZeso+wgFM7E772GAxEoET9+kpWABOKV3f0GtzD6TM4ttARDpPncWU2ia+Dotew5SjMDp+RwpmFdcjtvUsC6llZ59i11K6YocBgBkvP0Kuon8evHMnXGYZAulMv+vIbU2FprIO8cCTro5EnoP5VuLQ1/gTKl4A==',
    'cfidsw-smm': 'b4BBiidIcZeso+wgFM7E772GAxEoET9+kpWABOKV3f0GtzD6TM4ttARDpPncWU2ia+Dotew5SjMDp+RwpmFdcjtvUsC6llZ59i11K6YocBgBkvP0Kuon8evHMnXGYZAulMv+vIbU2FprIO8cCTro5EnoP5VuLQ1/gTKl4A==',
}

headers = {
    'authority': 'megamarket.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Opera GX";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX 03)',
}
try:
    with connect(
            host="localhost",
            user='',
            password='',
            database="products",
    ) as connection:
        response = requests.get(url, cookies=cookies, headers=headers).text
        response = response[response.index('<script>') + 24:]
        response = response[response.index('<script>') + 30:]
        response = response[:response.index('</script>')]
        response = '[' + response + ']'
        response = response.replace('}', '', 1)
        response = response.replace('undefined', '"undefined"')
        products_data = json.loads(response)
        items = [item["hydratorState"]["PlpStore"]["listingData"]["items"] for item in products_data]
        insert_products_query = """
        INSERT INTO products
        (title, url, price, discount)
        VALUES ( %s, %s, %s, %s )
        """
        array = []
        for item in items:
            for item2 in item:
                array = [(item2['goods']['title'][17:], item2['goods']['webUrl'], item2['price'],
                         item2['bonusAmount'])]
                with connection.cursor() as cursor:
                    cursor.executemany(insert_products_query,
                                       array)
                    connection.commit()
                # print(item2['goods']['webUrl'])
                # print(str(item2['goods']['title'])[17:])
                # print(item2['price'])
                # print(item2['bonusAmount'])

except Error as e:
    print(e)
