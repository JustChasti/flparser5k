import aiohttp
from bs4 import BeautifulSoup
import requests
import asyncio
from aiogram import Bot
from models.entities import Entity


example_category_urls = (
    'https://www.quoka.de/computer/apple-computer/',
    'https://www.quoka.de/tiermarkt/katzen/',
    'https://www.quoka.de/stellenmarkt/'
)


async def get_category_pages(category: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(category) as response:
            page = await response.text()
    soup = BeautifulSoup(page, "html.parser")
    navigation_bar = soup.find('div', class_='page-navigation-bottom rslt-pagination-container style-facelift')
    pages = []
    try:
        max_num = navigation_bar.find('a', class_='nothing').text.split('von ')[1]
    except AttributeError:
        max_num = 1
    if max_num == 1:
        pages.append(category)
    else:
        category_id = navigation_bar.find('a', class_='t-pgntn-blue').get('href').split('/kleinanzeigen/cat_')[1].split('_ct_0_page')[0]
        for i in range(int(max_num)):
            pages.append(f'https://www.quoka.de/qmca/search/search.html?redirect=0&catid={category_id}&pageno={i+1}')

    return pages


def get_pages(categories: tuple) -> list:
    page_list = []
    for i in categories:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_category_pages(i))
        loop.run_until_complete(future)
        pages = future.result()
        page_list.extend(pages)

    return page_list


def get_item_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    item_links = soup.findAll('a', class_='qaheadline item fn')
    links = []
    for i in item_links:
        links.append(f"https://www.quoka.de{i.get('href')}")
    return links


async def create_item(url, bot):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page = await response.text()
    soup = BeautifulSoup(page, "html.parser")
    item_data = soup.find('div', class_='cnt')
    price = item_data.find('div', class_='price has-type').text
    name = item_data.find('h1', attrs={'itemprop': 'name'}).text
    description = item_data.find('div', attrs={'itemprop': 'description'})
    product = Entity(url, price=price, name=name, description=description)
    await send_message(product, bot)


async def send_message(product: Entity, bot):
    await bot.send_message(362340468, f"Информация о продукте {product.description}")


bot = Bot(token="")
pages = get_pages(example_category_urls)
page = pages[0]
items = get_item_links(page)
for i in items:
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(create_item(i, bot))
    loop.run_until_complete(future)
