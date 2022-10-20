import traceback
from aiohttp import ClientSession
from modules import db_peewee
import urllib.parse
import requests
from modules import db
from sys import argv
from aiogram import Bot
import asyncio
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
import json
import cloudscraper
import random
import orjson

from proxies import proxy_list

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))

script, user_id, url_and_range = argv
try:
    script, user_id, url_and_range = argv
except:
    print("direct mode")

proxies = proxy_list
# proxies = [
#         {"http": "http://wpdwojfo:9hndmvl35d3m@84.21.191.193:7728"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@84.21.191.238:7773"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@45.95.99.52:7612"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@45.95.99.98:7658"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@193.8.94.225:9270"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@185.199.229.156:7492"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@185.199.228.220:7300"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@185.199.231.45:8382"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@188.74.210.21:6100"},
#         {"http": "http://wpdwojfo:9hndmvl35d3m@45.155.68.129:8133"},
#         ]

async def parse(user_id: int, url: str, range_):
    print("PARSER CATCHED")
    db_peewee.clear_stop_process(user_id)
    autotext = urllib.parse.quote(db.get_first_autotext(user_id))
    if url.startswith("https://www.gumtree.com.au/s-ad/"):
        data = await url_parse(url)
        if data:
            formated = (
                    f"[{prevent_escape(data.name)}]({data.link})\n"
                    f"📘*Имя продавца*: {data.seller_name}\n"
                    f"📆*Продавец на Gumtree*: {data.published}\n"
                    f"☎️*Номер продавца*: [{data.phone}](tel://tel_format{data.phone})\n"
                    f"📲*WhatsApp продавца*: [WhatsApp](https://wa.me/{tel_format(data.phone)})\n"
                    f"📬*Автотекст*: [Связаться](https://wa.me/{tel_format(data.phone)}?text={autotext})\n"
                    f"💼*Количество объявлений у продавца*: {data.ads_count}\n"
                    f"🕑*Объявление выложено*: {data.date_posted}\n"
                    f"📮*Адрес*: {data.address}\n"
                    f"👀*Просмотров у объявления*: {data.views}\n"
                    f"💵*Цена*: {data.price}\n"
                    f"\n*Описание*:\n{data.description[:200]}\n"
                    )
            # print(formated)
            await bot.send_photo(user_id, photo=data.photo, caption=formated, parse_mode="MARKDOWN")
    for page in range_:
        datas = await parse_page(f"{url}&page={page}")
        # print(datas)
        # for data in datas:
        #     if data:
        #         print(str(data))
        #         # if matches_filter(user_id, data):
        #         if True:
        #             if data.phone:
        #                 autotext = urllib.parse.quote(db.get_first_autotext(user_id))
        #                 phone_info = (
        #                         f"☎️Номер продавца: `{data.phone}`\n"
        #                         f"📲WhatsApp продавца: [WhatsApp](https://wa.me/{tel_format(data.phone)})\n"
        #                         f"📬Автотекст: [Связаться](https://wa.me/{tel_format(data.phone)}?text={autotext})\n" if data.phone != "unaviable" else ""
        #                         f"\n"
        #                         )
        #             else:
        #                 phone_info = ""
        #                 continue
        #             formated = (
        #                 f"✍️ Название: *{prevent_escape(data.name)}*\n"
        #                 f"📘Имя продавца: `{data.seller_name}`\n"
        #                 f"📆Продавец на Gumtree: `{data.published}`\n"
        #                 f"📮Адрес: `{data.address}`\n"
        #                 f"💵Цена: `{data.price}`\n"
        #                 f"\n"
        #                 f"💼Количество объявлений у продавца: *{data.ads_count}*\n"
        #                 f"🕑Объявление выложено: *{data.date_posted}*\n"
        #                 f"\n"
        #                 f"📌 [Ссылка на объявление]({data.link})\n" +
        #                 phone_info +
        #                 f"\n"
        #                 f"*Описание*:\n`{data.description[:200]}`\n"
        #                     )
        #             print(formated)
        #             await bot.send_photo(user_id, photo=data.photo, caption=formated, parse_mode="MARKDOWN")
        #     if db_peewee.is_stop_process(user_id): break
        if db_peewee.is_stop_process(user_id): break
        # break

def tel_format(tel):
    return tel.replace(" ", "")

def prevent_escape(string: str):
    return string.replace("]", r"\]")

def matches_filter(user_id: int, data):
    filters = db.get_filter(user_id, "gumtreeau")
    return True
    match_max_views = data.views < filters.max_views
    match_registration_year = data.registration_year > filters.min_registration_year
    match_number_of_sellers_ads = data.sellers_ads < filters.max_number_of_sellers_ads
    match_word_blacklist = not any([x in json.loads(filters.word_blacklist) for x in data.text.split()])
    return all([match_max_views, match_registration_year, match_number_of_sellers_ads, match_word_blacklist])

class Data:
    def __init__(
            self,
            views = None,
            registration_year = None,
            sellers_ads = None,
            text = None,
            price = None,
            address = None,
            published = None,
            years_registred = None,
            link = None,
            name: str | None = None,
            photo: str | None = None,
            seller_name: str | None = None,
            ads_count: int | None = None,
            date_posted: str | None = None,
            description: str | None = None,
            phone: str | None = None
            ):
        self.views = views
        self.registration_year = registration_year
        self.sellers_ads = sellers_ads
        self.text = text
        self.price = price
        self.address = address
        self.published = published
        self.years_registred = years_registred
        self.link = link
        self.name = name
        self.photo = photo
        self.seller_name = seller_name
        self.ads_count = ads_count
        self.date_posted = date_posted
        self.description = description
        self.phone = phone
    def __str__(self):
        return str(self.__dict__)

async def parse_page(page_url: str):
    s = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'android',
                    'desktop': False
                }
            )
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }
    page_raw = s.get(page_url, headers=headers, proxies=random.choice(proxies))
    with open("test.html", "w") as file:
        file.write(page_raw.text)
    page = BeautifulSoup(page_raw.text, "html.parser")
    # links = tuple(map(lambda x: "https://www.gumtree.com.au" + x["href"] if x["href"][0] == "/" else x["href"], page.findAll("a", class_="user-ad-row-new-design user-ad-row-new-design--featured-or-premium user-ad-row-new-design--cars-category link link--base-color-inherit link--hover-color-none link--no-underline")))
    links = tuple(map(lambda x: "https://www.gumtree.com.au" + x["href"] if x["href"][0] == "/" else x["href"], page.findAll("a", class_="user-ad-row-new-design link link--base-color-inherit link--hover-color-none link--no-underline")))
    # print(links)
    all_datas = []
    for link in links:
        if link.startswith("https://www.gumtree.com.au/s-ad"):
            print(link)
            try:
                data = await url_parse(link)
                if data:
                    print(str(data))
                    # if matches_filter(user_id, data):
                    if True:
                        if data.phone:
                            autotext = urllib.parse.quote(db.get_first_autotext(int(user_id)))
                            phone_info = (
                                    f"☎️Номер продавца: `{data.phone}`\n"
                                    f"📲WhatsApp продавца: [WhatsApp](https://wa.me/{tel_format(data.phone)})\n"
                                    f"📬Автотекст: [Связаться](https://wa.me/{tel_format(data.phone)}?text={autotext})\n" if data.phone != "unaviable" else ""
                                    f"\n"
                                    )
                        else:
                            phone_info = ""
                            continue
                        formated = (
                            f"✍️ Название: *{prevent_escape(data.name)}*\n"
                            f"📘Имя продавца: `{data.seller_name}`\n"
                            f"📆Продавец на Gumtree: `{data.published}`\n"
                            f"📮Адрес: `{data.address}`\n"
                            f"💵Цена: `{data.price}`\n"
                            f"\n"
                            f"💼Количество объявлений у продавца: *{data.ads_count}*\n"
                            f"🕑Объявление выложено: *{data.date_posted}*\n"
                            f"\n"
                            f"📌 [Ссылка на объявление]({data.link})\n" +
                            phone_info +
                            f"\n"
                            f"*Описание*:\n`{data.description[:200]}`\n"
                                )
                        print(formated)
                        await bot.send_photo(int(user_id), photo=data.photo, caption=formated, parse_mode="MARKDOWN")
                else:
                    print("NODATA 111111")
                if db_peewee.is_stop_process(int(user_id)): break
            except Exception as e:
                await bot.send_message(958170391, f"Catched Exception: {e}\nTraceback: {traceback.format_exc()}")
                continue
            # print(data)
            all_datas.append(data)
            # break

    return all_datas

async def url_parse(url: str):
    print(f"parsing url {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }
    # proxy = None

    async with ClientSession(headers=headers,) as session:
        async with session.get(url=url, proxy=random.choice(proxies)["http"]) as response:
            status = response.status
            source = await response.text()
    # print(f"!!!!!!!!!! {source=}")
    if status != 200:
        return
    
    soup = BeautifulSoup(source, 'html.parser')
    
    # --- Ищем тот <script>, в котором есть "window.clientData"
    # script = soup.find(name='script', string=re.compile(r'window.clientData'))
    script = soup.find("script", string=re.compile(r"window.APP_DATA"))
    if not script:
        return
    else:
        script = script.text
    # ---
    
    # Чистка лишнего, для конвертации в Json
    # data_ad = re.sub(r'window.__PAGE_TRANSLATIONS__= ', '', script)
    data_ad = str(script).split("window.APP_DATA = ", maxsplit=1)[-1].rsplit(";})()", maxsplit=1)[0].strip()
    # print(data_ad[100:])
    data_ad = json.loads(data_ad)
    with open("back.json", "w") as file:
        file.write(json.dumps(data_ad, indent=4))
    # data_ad = orjson.loads(data_ad)
    print("data_ad=")
    print(data_ad)
    # print(dir(data_ad))
    
    # Данные объявления
    ad_info = data_ad["vip"]["item"]
    # print(ad_info)


    ad_views = ad_info["numberOfViews"]
    ad_id = ad_info["id"]
    try:
        seller_phone = await get_phone(ad_id)
        seller_phone = "+61" + seller_phone
    except Exception as e:
        await bot.send_message(958170391, f"Catched Exception: {e}\nTraceback: {traceback.format_exc()}")
        seller_phone = ""
    await bot.send_message(958170391, f"Phone: {seller_phone}")
    print(f"!!!!!!!!!!!!!!!!!!!!! {ad_views=}")
    # price_ad = soup.find("h3", class_="css-okktvh-Text eu5v0x0").text
    price_ad = ad_info["priceText"]
    address_ad = ad_info["mapAddress"]
    title = ad_info['title']

    seller_info = data_ad["vip"]["seller"]
    posting_seller = f"с {seller_info['memberSince']}"
    photo_preview = ad_info["mainImageUrl"]
    seller_name = seller_info["name"]
    try:
        seller_info = await parse_seller(seller_info["id"])
    except:
        seller_info = Seller(ads_count="unaviable")

    posted_date = ad_info["mainAttributes"][0]["name"]
    description = ad_info["description"].replace("<br/><br/>", "\n").replace("<br/>", "\n")

    data = Data(
            price = price_ad,
            address = address_ad,
            published = posting_seller,
            link = url,
            name = title,
            photo = photo_preview,
            seller_name = seller_name,
            ads_count = seller_info.ads_count,
            date_posted = posted_date,
            views = ad_views,
            description = description,
            phone = seller_phone
            )
    # print(data)

    return data

class Seller:
    def __init__(self, ads_count: int | None = None):
        self.ads_count = ads_count

async def parse_seller(id: str) -> Seller | None:
    url = f"https://www.gumtree.com.au/j-list-active-ads.json?userId={id}&pageNumber=2&pageSize=24"
    # css-19ucd76
    print(f"parsing seller url {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }
    # proxy = None

    async with ClientSession(headers=headers) as session:
        async with session.get(url=url, proxy=random.choice(proxies)["http"]) as response:
            status = response.status
            source = await response.text()
    # print(f"!!!!!!!!!! {source=}")
    if status != 200:
        return
    
    data = json.loads(source)

    seller = Seller(ads_count=data["sellerNumberAds"])

    return seller

async def get_views(ad_id: int) -> int | None:
    url = f"https://www.olx.ro/api/v1/offers/{ad_id}/page-views/"
    print(f"parsing url {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'ro',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'X-Client': 'DESKTOP',
        'X-Device-Id': '78e6e8e6-cb0d-4feb-b7e6-b13555c328c7',
        'X-Platform-Type': 'mobile-html5',
        'Version': 'v1.19',
        'Origin': 'https://www.olx.ro',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Authorization': 'Bearer 20919150a6d67ee9f8404ce745e1bdc19a00ed21',
        'Referer': 'https://www.olx.ro/d/oferta/suzuki-vitara-s-1-4-turbo-euro-6-140-cp-IDgpBZL.html',
        'Connection': 'keep-alive',
    }
    # proxy = None

    async with ClientSession(headers=headers) as session:
        async with session.post(url=url, headers=headers, proxy=random.choice(proxies)["http"]) as response:
            status = response.status
            source = await response.text()
    # print(f"!!!!!!!!!! {source=}")
    if status != 200:
        return

    return json.loads(source)["data"]

async def get_phone(ad_id: int):
    url = f"https://www.olx.ro/api/v1/offers/{ad_id}/limited-phones/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type,x-user-tests',
        'Referer': 'https://www.olx.ro/',
        'Origin': 'https://www.olx.ro',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    
    response = requests.options('https://friction.olxgroup.com/challenge', headers=headers)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'X-User-Tests': 'eyJkZWNpc2lvbi0zNzciOiJiIiwiZGVjaXNpb24tNTM2IjoiYSIsImRvLTI4MjAiOiJiIiwiZXItMTU5OCI6ImIiLCJlci0xNjk3IjoiYSIsImVyLTE3MDgiOiJjIiwiZXItMTcyNSI6ImEiLCJldW9uYi01MjQiOiJiIiwiam9icy0zNDgyIjoiYSIsImpvYnMtMzcyMiI6ImEiLCJqb2JzLTM3MjgiOiJiIiwib2VzeC0xNTQ3IjoiYiIsIm9lc3gtMTc3MCI6ImIiLCJvZXN4LTE4MDMiOiJiIn0=',
        'Origin': 'https://www.olx.ro',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Referer': 'https://www.olx.ro/',
        'Connection': 'keep-alive',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    
    json_data = {
        'action': 'reveal_phone_number',
        'aud': 'atlas',
        'actor': {
            'username': '568679962',
        },
        'scene': {
            'origin': 'olx.ro',
        },
    }
    response = requests.post('https://friction.olxgroup.com/challenge', headers=headers, json=json_data, proxies=random.choice(proxies))
    
    context = json.loads(response.text)["context"]
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type',
        'Referer': 'https://www.olx.ro/',
        'Origin': 'https://www.olx.ro',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    
    response = requests.options('https://friction.olxgroup.com/exchange', headers=headers, proxies=random.choice(proxies))
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'Origin': 'https://www.olx.ro',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Referer': 'https://www.olx.ro/',
        'Connection': 'keep-alive',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    
    json_data = {
        'context': context,
        'response': '',
    }
    
    response = requests.post('https://friction.olxgroup.com/exchange', headers=headers, json=json_data, proxies=random.choice(proxies))
    token = json.loads(response.text)["token"]
    
    
    cookies = {
        'laquesis': 'decision-377@b#decision-536@a#do-2820@b#er-1598@b#er-1697@a#er-1708@c#er-1725@a#euonb-524@b#jobs-3482@a#jobs-3722@a#jobs-3728@b#oesx-1547@b#oesx-1770@b#oesx-1803@b',
        'laquesisff': 'aut-388#aut-716#buy-2489#buy-2811#dat-2874#decision-256#euonb-114#euonb-48#kuna-307#oesx-1437#oesx-1452#oesx-1643#oesx-645#oesx-867#olxeu-29763#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-544#srt-545#srt-684#srt-899#uacc-69',
        'lqstatus': '1660749226|182ac4bd1afx5fd0b490|decision-377||',
        'deviceGUID': '89ff259a-97e8-42fc-bab9-ee5c10bf553b',
        'user_adblock_status': 'false',
        'newrelic_cdn_name': 'CF',
        'PHPSESSID': '8r1ldnosshscd1mduac4t9bqmg',
        'a_access_token': '20919150a6d67ee9f8404ce745e1bdc19a00ed21',
        'a_refresh_token': '6b9f1ea63ecbe85a7740e610814b53b05545655a',
        'a_grant_type': 'device',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Aug+17+2022+20%3A00%3A40+GMT%2B0500+(Yekaterinburg+Standard+Time)&version=6.18.0&isIABGlobal=false&hosts=&genVendors=V9%3A0%2C&consentId=381ca37a-bd8c-438b-ab05-836df5a8620c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=RU%3BBA&AwaitingReconsent=false',
        'observed_aui': 'cf343fc4251f4fcaa3c301c48249a48c',
        'user_id': '568679962',
        'user_business_status': 'private',
        'session_start_date': '1660750268119',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2022-08-17%2019%3A53%3A51%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ro%2Fd%2Foferta%2Fwolkswagen-golf-gtd-IDgdHB0.html%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2022-08-17%2019%3A53%3A51%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ro%2Fd%2Foferta%2Fwolkswagen-golf-gtd-IDgdHB0.html%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%3B%20rv%3A102.0%29%20Gecko%2F20100101%20Firefox%2F102.0',
        'sbjs_session': 'pgs%3D5%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.ro%2Fd%2Foferta%2Fwolkswagen-golf-gtd-IDgdHB0.html',
        'dfp_segment': '%5B%5D',
        'dfp_user_id': '35e06571-d894-4d64-be1f-35bb3a46b767-ver2',
        'onap': '182ac4bd1afx5fd0b490-1-182ac4bd1afx5fd0b490-7-1660750241',
        'ldTd': 'true',
        '_gcl_au': '1.1.20949366.1660748033',
        '_tt_enable_cookie': '1',
        '_ttp': '5668fd90-6b39-4c8f-b3fa-6ae73e4aff06',
        'evid_0046': '9f551deb-5d88-404c-b378-97c558179593',
        'adptset_0046': '1',
        'OptanonAlertBoxClosed': '2022-08-17T14:54:02.055Z',
        'eupubconsent-v2': 'CPd4gnzPd4gnzAcABBENCcCsAP_AAH_AAAYgI8Nf_X__b2_j-_5_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbOydYGH9_n1_zuZKY7_____7z_v-v______f_7-3f3__p_3_-__e_V_99zfn9_____9vP___9v-_9__________3_7BHYAkw1biALsSxwJtowigRAjCsJDqBQAUUAwtEFhA6uCnZXAT6whYAIBQBGBECHEFGDAIABAIAkIiAkCPBAIgCIBAACABUAhAARsAgsALAwCAAUA0LFGKAIQJCDIgIjlMCAiRIKCeysQSg70NMIQ6ywAoNH_FQgIlACFYGQkLByHBEgJeLJAsxRvkAIwQoBRKgAAAAA.f_gAD_gAAAAA',
        'OTAdditionalConsentString': '1~89.2008.2072.2322.2465.2501.2999.3028.3225.3226.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300.3306.3307.3308.3314.3315.3316',
        'evid_set_0046': '2',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'ro',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.olx.ro/d/oferta/wolkswagen-golf-gtd-IDgdHB0.html',
        'Authorization': 'Bearer 20919150a6d67ee9f8404ce745e1bdc19a00ed21',
        'X-Client': 'DESKTOP',
        'X-Device-Id': '89ff259a-97e8-42fc-bab9-ee5c10bf553b',
        'X-Platform-Type': 'mobile-html5',
        'friction-token': token,
        'Version': 'v1.19',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    response = requests.get('https://www.olx.ro/api/v1/offers/242143168/limited-phones/', cookies=cookies, headers=headers, proxies=random.choice(proxies))

    print(response.text)
    return json.loads(response.text)["data"]["phones"][0]


# async def test():
#     data = await get_phone(239687226)
#     print(data)
# asyncio.run(test())
# exit()

    



def get_last_page_number(url: str):
    pass


# url, range_start, range_end = url_and_range.split()
print(url_and_range)
url, *range_ = url_and_range.split()
if len(range_) == 1:
    range_start = 1
    range_end = get_last_page_number(url) or "9999999999"
else:
    range_start = range_[0]
    range_end = range_[1]

asyncio.run(parse(int(user_id), url, range(int(range_start), int(range_end) + 1)))
# try:
#     url, range_start, range_end = url_and_range.split()
    
#     asyncio.run(parse(int(user_id), url, range(int(range_start), int(range_end) + 1)))
# except:
#     print("direct mode")

# async def main():
#     # data = await url_parse("https://www.gusdfmtree.com/p/nissan/2019-19-nissan-micra-0.9-ig-t-n-connecta-5d-89-bhp/1434426051")
#     # data = await url_parse("https://www.gumtree.com/p/bmw/2018-bmw-m2-3.0-m240i-2d-335-bhp-coupe-petrol-automatic/1438206250")
#     data = await parse_page("https://www.gumtree.com/cars/uk/page2")
#     print(data)
#     for d in data:
#         print(d)
# asyncio.run(main())
# asyncio.run(parse_page("https://www.olx.ro/d/auto-masini-moto-ambarcatiuni/autoturisme/"))
