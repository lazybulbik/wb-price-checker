import requests


def get_product_info(product_id):
    result_dict = requests.get(
        f'https://card.wb.ru/cards/detail?spp=28&regions=80,64,83,4,38,33,70,82,69,68,86,30,40,48,1,22,66,31&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=2,12,7,3,6,18,21&sppFixGeo=4&dest=-1075831,-115134,-956089,-1017011&nm={product_id}').json()

    # return result_dict

    if bool(result_dict['data']['products']):
        name = result_dict['data']['products'][0]['name']
        brand = result_dict['data']['products'][0]['brand']
        price = result_dict['data']['products'][0]['salePriceU'] // 100
        rating = result_dict['data']['products'][0]['reviewRating']
        feedbacks = result_dict['data']['products'][0]['feedbacks']
        url = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'

        return {'name': name, 'price': price, 'brand': brand, 'rating': rating, 'feedbacks': feedbacks, 'url': url}


import urllib.parse
import json

def get_user_id(query):
    # Ссылка, из которой нужно извлечь user_id
    url = query

    # Разбираем URL на компоненты
    parsed_url = urllib.parse.parse_qs(url)

    # Извлекаем параметр 'user' и декодируем его
    user_param = parsed_url['user'][0]
    user_data = json.loads(urllib.parse.unquote(user_param))

    # Извлекаем user_id
    user_id = user_data['id']

    return user_id