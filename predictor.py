import time
import utils

import numpy as np
from sklearn.linear_model import LinearRegression

import asyncio
import aiohttp


class Predictor:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def predict_next_value(self, sequence):
        sequence = list(map(lambda x: float(str(x).replace(',', '.')), sequence))

        # Подготовка данных для обучения модели
        X = np.array(range(len(sequence))).reshape(-1, 1)  # Входные данные (индексы элементов последовательности)
        y = np.array(sequence)  # Выходные данные (значения последовательности)

        # Создание и обучение модели линейной регрессии
        model = LinearRegression()
        model.fit(X, y)

        # Предсказание следующего значения
        next_index = len(sequence)
        next_value = model.predict([[next_index]])

        return round(next_value.tolist()[0], 4)
    
    async def fetch(self, url, session):
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return
                return await response.json()
        except Exception as e:
            return str(e)

    async def fetch_all_async(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(url, session) for url in urls]
            responses = await asyncio.gather(*tasks)
            return responses

    def get_price_history(self, product_id):
        product_id = str(product_id)
        urls = [
            f'https://basket-01.wbbasket.ru/vol{product_id[:2]}/part{product_id[:4]}/{product_id}/info/price-history.json',
            f'https://basket-01.wbbasket.ru/vol{product_id[:3]}/part{product_id[:5]}/{product_id}/info/price-history.json',
            f'https://basket-02.wbbasket.ru/vol{product_id[:3]}/part{product_id[:5]}/{product_id}/info/price-history.json',
            f'https://basket-03.wbbasket.ru/vol{product_id[:3]}/part{product_id[:5]}/{product_id}/info/price-history.json',
            f'https://basket-04.wbbasket.ru/vol{product_id[:3]}/part{product_id[:5]}/{product_id}/info/price-history.json',
            f'https://basket-05.wbbasket.ru/vol{product_id[:3]}/part{product_id[:5]}/{product_id}/info/price-history.json',
            f'https://basket-05.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-06.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-07.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-08.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-09.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-10.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-11.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-12.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-13.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-14.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
            f'https://basket-15.wbbasket.ru/vol{product_id[:4]}/part{product_id[:6]}/{product_id}/info/price-history.json',
        ]

        answers = self.loop.run_until_complete(self.fetch_all_async(urls))

        for answer in answers:
            if answer:
                return answer    

    def predict(self, product_id):
        curent_price = utils.get_product_info(product_id)['price']
        price_history = self.get_price_history(product_id)    

        x = []    
        y = []

        count = 0
        for item in price_history:
            curency = count

            x.append(curency)
            y.append(item['price']['RUB'] // 100) 

            count += 1

        x.append(count)
        y.append(curent_price)     

        x.append(count + 1)
        y.append(self.predict_next_value(y))

        return x, y

# product_id = 229222042

# curent_price = utils.get_product_info(product_id)['price']
# price_history = utils.get_price_history(product_id)

# x = []
# y = []

# for item in price_history:
#     curency = utils.get_usd_to_rub_rate(item['dt'])

#     x.append(curency)
#     y.append(item['price']['RUB'] // 100)


# # x.append(utils.get_usd_to_rub_rate(time.time()))
# # y.append(curent_price)

# next_curency = predict_next_value(x)
# price = predict_next_value(y)


# fig, ax = plt.subplots()
# ax.plot(x, y, label='Изменение цены')
# ax.plot([x[-1], next_curency], [y[-1], price], label='Следующая цена')
# # ax.set_title('Пример графика')
# ax.set_xlabel('Курс доллара')
# ax.set_ylabel('Стоимость товара')

# ax.grid(True)
# ax.legend()

# plt.show()

# print(y + [predict_next_value(y)])
# print(x + [predict_next_value(x)])