from inspect import FrameInfo
from datetime import datetime, timedelta
import json
from peewee import (
    SqliteDatabase,
    Model,
    ForeignKeyField,
    CharField,
    IntegerField,
    DateTimeField,
    BooleanField,
    FloatField,
    TextField,
)
from loguru import logger

db = SqliteDatabase("application.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    name = CharField()
    state = CharField()
    subscription_expiration_date = DateTimeField()
    is_subscription_aviable = BooleanField()
    balance = FloatField()
    metadata = CharField(default="{}")


parsers = ["gumtree", "gumtreeau", "olxro", "wallapop", "vinted"]
class Filters(BaseModel):
    user_id = IntegerField()
    max_views = IntegerField(default=100)
    parser = CharField()
    min_registration_year = IntegerField(default=2019)
    max_number_of_sellers_ads = IntegerField(default=3)
    word_blacklist = CharField(default="{}")

class Autotext(BaseModel):
    user_id = IntegerField(unique=True)
    text = TextField()

class URN(BaseModel):
    site = CharField()
    category = CharField()
    category_name = TextField()
    urn = TextField(unique=True)

class UserSelectedCategories(BaseModel):
    user_id = IntegerField()
    category = CharField()

class ProcessStop(BaseModel):
    user_id = IntegerField()

class Admin(BaseModel):
    user_id = IntegerField(unique=True)

class Promocode(BaseModel):
    promocode = CharField(unique=True)
    # expiratiod_date = DateTimeField(default="")
    days_gives = IntegerField()

class SubscriptionPrices(BaseModel):
    days = IntegerField(unique=True)
    price = FloatField()

class UserTokenAd(BaseModel):
    user_id = IntegerField(unique=True)
    token_count = IntegerField()
    ad_count = IntegerField()

class UserAdsToBeShown(BaseModel):
    user_id = IntegerField(unique=True)
    ad_count = IntegerField()


def migrate():
    db.create_tables([User, Filters, Autotext, URN, UserSelectedCategories, ProcessStop, Admin, Promocode, SubscriptionPrices, UserTokenAd, UserAdsToBeShown])
    for days, base_price in ((1, 1), (3, 1), (7, 2), (15, 4)):
        try:
            SubscriptionPrices.create(days=days, price=base_price)
        except:
            pass
    add_gumtreeau_urn()
    add_wallapop_urn()
    add_vinted_urn()
    try:
        URN.create(
            site="gumtree",
            category="kitchen-appliances",
            category_name="Кухонная техника",
            urn="https://www.gumtree.com/kitchen-appliances/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="kitchen-appliances",
            category_name="Кухонная техника",
            urn="https://www.olx.ro/d/electronice-si-electrocasnice/electrocasnice/aparate-de-gatit/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
        

    try:
        URN.create(
            site="gumtree",
            category="stereo-audio",
            category_name="Стерео аудио",
            urn="https://www.gumtree.com/stereos-audio/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="stereo-audio",
            category_name="Стерео аудио",
            urn="https://www.olx.ro/d/electronice-si-electrocasnice/audio-hi-fi-si-profesionale/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site="gumtree",
            category="baby-kids-stuff",
            category_name="Детские вещи",
            urn="https://www.gumtree.com/baby-kids-stuff/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="baby-kids-stuff",
            category_name="Детские вещи",
            urn="https://www.olx.ro/d/mama-si-copilul/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site="gumtree",
            category="cameras-studio-equipment",
            category_name="Студийное оборудование",
            urn="https://www.gumtree.com/cameras-studio-equipment/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site="gumtree",
            category="christmas-decorations",
            category_name="Рождественские украшения",
            urn="https://www.gumtree.com/christmas-decorations/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="christmas-decorations",
            category_name="Рождественские украшения",
            urn="https://www.olx.ro/d/casa-gradina/mobila-decoratiuni/decoratiuni/arad/q-decora%C8%9Biuni-de-Cr%C4%83ciun",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site="gumtree",
            category="clothing",
            category_name="Одежда",
            urn="https://www.gumtree.com/clothing/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="clothing",
            category_name="Одежда",
            urn="https://www.olx.ro/d/moda-frumusete/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="software",
            category_name="Компьютеры и ПО",
            urn="https://www.gumtree.com/software/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="software",
            category_name="Компьютеры и ПО",
            urn="https://www.olx.ro/d/servicii-afaceri-colaborari/reparatii-it-electronice-electro/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="diy-tools-materials",
            category_name="Материалы и инструменты",
            urn="https://www.gumtree.com/diy-tools-materials/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="diy-tools-materials",
            category_name="Материалы и инструменты",
            urn="https://www.olx.ro/d/oferte/q-Materiale-%C8%99i-unelte/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="health-beauty",
            category_name="Красота и здоровье",
            urn="https://www.gumtree.com/health-beauty/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="health-beauty",
            category_name="Красота и здоровье",
            urn="https://www.olx.ro/d/moda-frumusete/sanatate-frumusete/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="home-garden",
            category_name="Домашний сад",
            urn="https://www.gumtree.com/home-garden/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="home-garden",
            category_name="Домашний сад",
            urn="https://www.olx.ro/d/casa-gradina/gradina/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="house-clearance",
            category_name="Очистка дома",
            urn="https://www.gumtree.com/house-clearance/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="house-clearance",
            category_name="Очистка дома",
            urn="https://www.olx.ro/d/oferte/q-curatenie-in-casa/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="cds-dvds-games-books",
            category_name="Диски, музыка, игры и книги",
            urn="https://www.gumtree.com/cds-dvds-games-books/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="cds-dvds-games-books",
            category_name="Диски, музыка, игры и книги",
            urn="https://www.olx.ro/d/hobby-sport-turism/carti-muzica-filme/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="music-instruments",
            category_name="Музыкальные инструменты",
            urn="https://www.gumtree.com/music-instruments/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="music-instruments",
            category_name="Музыкальные инструменты",
            urn="https://www.olx.ro/d/hobby-sport-turism/carti-muzica-filme/instrumente-muzicale/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="office-furniture-equipment",
            category_name="Офисная мебель",
            urn="https://www.gumtree.com/office-furniture-equipment/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="office-furniture-equipment",
            category_name="Офисная мебель",
            urn="https://www.olx.ro/d/oferte/q-Mobila-de-birou/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="phones",
            category_name="Мобильные телефоны",
            urn="https://www.gumtree.com/phones/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="phones",
            category_name="Мобильные телефоны",
            urn="https://www.olx.ro/d/electronice-si-electrocasnice/telefoane-mobile/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="sports-leisure-travel",
            category_name="Спорт и отдых",
            urn="https://www.gumtree.com/sports-leisure-travel/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="sports-leisure-travel",
            category_name="Спорт и отдых",
            urn="https://www.olx.ro/d/hobby-sport-turism/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="tickets",
            category_name="Билеты",
            urn="https://www.gumtree.com/tickets/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="tickets",
            category_name="Билеты",
            urn="https://www.olx.ro/d/oferte/q-bilete/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site="gumtree",
            category="tv-dvd-cameras",
            category_name="Видео, ТВ, DVD",
            urn="https://www.gumtree.com/tv-dvd-cameras/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="tv-dvd-cameras",
            category_name="Видео, ТВ, DVD",
            urn="https://www.olx.ro/d/oferte/q-Video%2C-TV%2C-DVD/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site="gumtree",
            category="video-games-consoles",
            category_name="Игры, консоль",
            urn="https://www.gumtree.com/video-games-consoles/uk",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
    try:
        URN.create(
            site="olxro",
            category="video-games-consoles",
            category_name="Игры, консоль",
            urn="https://www.olx.ro/d/oferte/q-Consol%C4%83-de-jocuri/",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

def add_gumtreeau_urn():
    site = "gumtreeau"
    try:
        URN.create(
            site=site,
            category="kitchen-appliances",
            category_name="Кухонная техника",
            urn="https://www.gumtree.com.au/s-home-garden/kitchen+appliances/k0c18397r10?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
        

    try:
        URN.create(
            site=site,
            category="stereo-audio",
            category_name="Стерео аудио",
            urn="https://www.gumtree.com.au/s-stereo-systems/c21105?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="baby-kids-stuff",
            category_name="Детские вещи",
            urn="https://www.gumtree.com.au/s-baby-children/macgregor-brisbane/c18318l3005894?sort=rank?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="christmas-decorations",
            category_name="Рождественские украшения",
            urn="https://www.gumtree.com.au/s-decorative-accessories/christmas+decorations/k0c21022?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="clothing",
            category_name="Одежда",
            urn="https://www.gumtree.com.au/s-clothing-jewellery/sydney-city-sydney/c18308l3003795?sort=date?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="software",
            category_name="Компьютеры и ПО",
            urn="https://www.gumtree.com.au/s-electronics-computer/computers+and+software/k0c20045l3003795?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="diy-tools-materials",
            category_name="Материалы и инструменты",
            urn="https://www.gumtree.com.au/s-tools-diy/c18430?sort=date?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="health-beauty",
            category_name="Красота и здоровье",
            urn="https://www.gumtree.com.au/s-miscellaneous-goods/beauty/k0c18319?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="home-garden",
            category_name="Домашний сад",
            urn="https://www.gumtree.com.au/s-home-garden/c18397?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="house-clearance",
            category_name="Очистка дома",
            urn="https://www.gumtree.com.au/s-home-garden/house+clearance/k0c18397?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="cds-dvds-games-books",
            category_name="Диски, музыка, игры и книги",
            urn="https://www.gumtree.com.au/s-books-music-games/c18393?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="music-instruments",
            category_name="Музыкальные инструменты",
            urn="https://www.gumtree.com.au/s-musical-instruments/c18409?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="office-furniture-equipment?sort=rank",
            category_name="Офисная мебель",
            urn="https://www.gumtree.com.au/s-furniture/office+furniture/k0c20073?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="phones",
            category_name="Мобильные телефоны",
            urn="https://www.gumtree.com.au/s-phones/c18313?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="sports-leisure-travel",
            category_name="Спорт и отдых",
            urn="https://www.gumtree.com.au/s-sport-fitness/c18314?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="tickets",
            category_name="Билеты",
            urn="https://www.gumtree.com.au/s-tickets/c18361?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="tv-dvd-cameras",
            category_name="Видео, ТВ, DVD",
            urn="https://www.gumtree.com.au/s-electronics-computer/tv+dvd+cameras/k0c20045?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="video-games-consoles",
            category_name="Игры, консоль",
            urn="https://www.gumtree.com.au/s-video-games-consoles/c18459?sort=rank",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

def add_wallapop_urn():
    site = "wallapop"
    try:
        URN.create(
            site=site,
            category="kitchen-appliances",
            category_name="Кухонная техника",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=00c87519-ea11-46f4-b95b-c583faf07996&country_code=ES&items_count=200&density_type=20&filters_source=quick_filters&order_by=closest&step=0&category_ids=13100&object_type_id=10175%2C9447&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
        

    try:
        URN.create(
            site=site,
            category="stereo-audio",
            category_name="Стерео аудио",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=estereo+y+audio&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=8c7cd797-5e4a-43e8-8e40-998731138d9b&country_code=ES&items_count=200&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="baby-kids-stuff",
            category_name="Детские вещи",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=0f7b9e28-731d-4880-a3f4-bf6786a4397c&country_code=ES&items_count=40&density_type=20&filters_source=seo_landing&order_by=closest&step=0&category_ids=12461&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="christmas-decorations",
            category_name="Рождественские украшения",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=decoraciones+de+navidad&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=b46efc94-f392-4641-b9f3-03573283265d&country_code=ES&items_count=38&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="clothing",
            category_name="Одежда",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=04cc918f-7788-4219-8105-7e2643aa984a&country_code=ES&items_count=40&density_type=20&filters_source=seo_landing&order_by=closest&step=0&category_ids=12465&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="software",
            category_name="Компьютеры и ПО",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=ae1fd583-8e99-4597-8024-c3c72d6e79de&country_code=ES&items_count=40&density_type=20&filters_source=quick_filters&order_by=closest&step=0&category_ids=15000&object_type_id=10137%2C10133%2C10132%2C10130%2C10134%2C10136&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="diy-tools-materials",
            category_name="Материалы и инструменты",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=materiales+y+herramientas&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=8adeb924-9f19-47ce-b147-599ba4a0bbcd&country_code=ES&items_count=40&filters_source=quick_filters&order_by=most_relevance&step=0&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="health-beauty",
            category_name="Красота и здоровье",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=belleza+y+salud&latitude=40.41956&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=dd24a36b-2c7f-45e0-8804-5e6de77efc9a&country_code=ES&items_count=77&density_type=20&filters_source=search_box&order_by=closest&step=4&longitude=-3.69196",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="home-garden",
            category_name="Домашний сад",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=cc26482a-7030-4933-8f8d-8a6999aa4c5e&country_code=ES&items_count=40&density_type=20&filters_source=seo_landing&order_by=closest&step=0&category_ids=12467&longitude=-3.71178",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="house-clearance",
            category_name="Очистка дома",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=liquidacion+de+la+casa&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=45188462-eed8-4545-9832-d4e63774a60f&country_code=ES&items_count=40&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="cds-dvds-games-books",
            category_name="Диски, музыка, игры и книги",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=discos%2C+musica%2C+juegos+y+libros&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=5d8d0ab7-f24e-4c65-b5e9-8c36207d5e7d&country_code=ES&items_count=40&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="music-instruments",
            category_name="Музыкальные инструменты",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=instrumentos+musicales&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=1f54918c-877f-4da3-8411-3e879eb3697f&country_code=ES&items_count=80&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="office-furniture-equipment",
            category_name="Офисная мебель",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=muebles+de+oficina&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=5fcea08c-4756-4306-83f0-afab2a3de18d&country_code=ES&items_count=40&filters_source=search_box&order_by=most_relevance&step=0&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="phones",
            category_name="Мобильные телефоны",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=97735651-c7ed-4069-9217-7374f8d25592&country_code=ES&items_count=32&density_type=20&filters_source=quick_filters&order_by=closest&step=0&category_ids=16000&object_type_id=9447&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="sports-leisure-travel",
            category_name="Спорт и отдых",
            urn="ttps://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=8196cd16-91c3-4461-9b87-ab2029aa4edd&country_code=ES&items_count=78&density_type=20&filters_source=quick_filters&order_by=closest&step=0&category_ids=12579&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="tickets",
            category_name="Билеты",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=entradas&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=d4c1dc30-1418-44f8-b84c-7983f396194c&country_code=ES&items_count=79&filters_source=quick_filters&order_by=most_relevance&step=0&category_ids=18000&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="tv-dvd-cameras",
            category_name="Видео, ТВ, DVD",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=video%2C+television%2C+dvd&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=a329231f-4392-40e6-88f2-32b4cd4c4982&country_code=ES&items_count=78&filters_source=quick_filters&order_by=most_relevance&step=0&category_ids=12545&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="video-games-consoles",
            category_name="Игры, консоль",
            urn="https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords=consola+de+juegos&latitude=40.418965&start={last_id}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=ddbfaef9-f94c-425d-8ae9-16157f275e20&country_code=ES&items_count=80&filters_source=quick_filters&order_by=most_relevance&step=0&longitude=-3.711781",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

def add_vinted_urn():
    # catalog_id, search_text, is_search = url.split("|")
    site = "vinted"
    try:
        URN.create(
            site=site,
            category="kitchen-appliances",
            category_name="Кухонная техника",
            urn="1920||0",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")
        

    try:
        URN.create(
            site=site,
            category="stereo-audio",
            category_name="Стерео аудио",
            urn="|audio#estéreo|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="baby-kids-stuff",
            category_name="Детские вещи",
            urn="1193||0",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="christmas-decorations",
            category_name="Рождественские украшения",
            urn="|Decoración#navideña|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="clothing",
            category_name="Одежда",
            urn="2050||0",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="software",
            category_name="Компьютеры и ПО",
            urn="|computadoras#y|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="diy-tools-materials",
            category_name="Материалы и инструменты",
            urn="|materiales#y#herramientas|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="health-beauty",
            category_name="Красота и здоровье",
            urn="146||0",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="home-garden",
            category_name="Домашний сад",
            urn="|Hogar#&#Jardín|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="house-clearance",
            category_name="Очистка дома",
            urn="|limpieza#de#la#casa|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="cds-dvds-games-books",
            category_name="Диски, музыка, игры и книги",
            urn="2309||1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="music-instruments",
            category_name="Музыкальные инструменты",
            urn="|instrumentos#musicales|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="office-furniture-equipment?sort=rank",
            category_name="Офисная мебель",
            urn="|Muebles#de#oficina|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="phones",
            category_name="Мобильные телефоны",
            urn="|Celulares|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="sports-leisure-travel",
            category_name="Спорт и отдых",
            urn="|Deportes#y#Recreación|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

    # try:
    #     URN.create(
    #         site=site,
    #         category="tickets",
    #         category_name="Билеты",
    #         urn="",
    #     )
    # except:
    #     print(f"skipping line {FrameInfo.lineno}")

    try:
        URN.create(
            site=site,
            category="tv-dvd-cameras",
            category_name="Видео, ТВ, DVD",
            urn="|vídeo,#televisión,#dvd|1",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")


    try:
        URN.create(
            site=site,
            category="video-games-consoles",
            category_name="Игры, консоль",
            urn="2313||0",
        )
    except:
        print(f"skipping line {FrameInfo.lineno}")

def _add_user_unsafe(user_id: int, username: str):
    time = datetime.utcnow()
    # time += timedelta(minutes=30) + timedelta(hours=3)  # перевожу дельту во время и перевожу UTC в МСК
    time -= timedelta(hours=3)
    min_ad_date = time.strftime("%d.%m.%Y")
    User.create(
        id=user_id,
        name=username,
        state="",
        subscription_expiration_date=datetime.now(),
        is_subscription_aviable=False,
        balance=0.0,
        metadata = json.dumps({"max_views": 10000, "min_register_year": 2019, "max_ads": 3, "word_blacklist": [], "token_use_amount": 20, "min_ad_date": min_ad_date, "parser": "olxpl"})
    )
    # Autotext.create(user_id=user_id, text="Ненастроенный автотекст")
    # UserTokenAd.create(user_id=user_id, token_count=0, ad_count=0)

def add_all_filters(user_id: int):
    for parser in parsers:
        print("stage1")
        if not Filters.select().where((Filters.user_id == user_id) & (Filters.parser == parser)).exists():
            print("stage2")
            Filters.create(
                    user_id=user_id,
                    parser=parser
                    )

def is_user_exists(user_id: int) -> bool:
    is_exists = User.select().where(User.id == user_id).exists()
    logger.info(f"Checking user {user_id}, exists: {is_exists}")
    return is_exists


def add_user(user_id: int, username: str):
    if not is_user_exists(user_id):
        _add_user_unsafe(user_id, username)
    print("FILTERSR")
    add_all_filters(user_id)
    try:
        Autotext.create(user_id=user_id, text="Ненастроенный автотекст")
    except:
        pass
    try:
        UserTokenAd.create(user_id=user_id, token_count=0, ad_count=0)
    except:
        pass


def set_state_for_user(user_id: int, state: str):
    User.update(state=state).where(User.id == user_id).execute()


def get_state_for_user(user_id: int):
    user = User.select().where(User.id == user_id).get()
    return user.state


def get_user_balance(user_id: int):
    user = User.select().where(User.id == user_id).get()
    return user.balance


def get_hours_left(user_id: int) -> int:
    user = User.select().where(User.id == user_id).get()
    date = user.subscription_expiration_date
    print(f"THERE: {date}")
    if date < datetime.now():
        print("YEEEEESSS")
        date = datetime.now()
    left = int((date - datetime.now()).total_seconds() // 3600)
    return left if left >= 0 else 0


def add_to_user_balance(user_id: int, amount: float):
    user = User.select().where(User.id == user_id).get()
    User.update(balance=user.balance + amount).where(User.id == user_id).execute()

# def get_user_filters(user_id: int, parser: str):
#     # user = User.select().where(User.id == user_id).get()
#     return Filters.select().where(Filters.user_id == user_id and Filters.parser == parser).get()

def is_sub_aviable(user_id: int):
    renew_hours(user_id)
    user = User.select().where(User.id == user_id).get()
    return user.is_subscription_aviable

def load_metadata(user_id: int):
    user = User.select().where(User.id == user_id).get()
    return json.loads(user.metadata)

def store_metadata(user_id: int, metadata: dict):
    str_metadata = json.dumps(metadata)
    User.update(metadata=str_metadata).where(User.id == user_id).execute()

def get_filter(user_id: int, parser: str):
    # filter = Filters.select().where(Filters.user_id == user_id).get()
    # return filter
    return Filters.select().where((Filters.user_id == user_id) & (Filters.parser == parser)).get()

def set_filter(user_id: int, parser: str, filter_type: str, filter_value):
    if filter_type == "max_views":
        Filters.update(max_views=filter_value).where(Filters.user_id == user_id and Filters.parser == parser).execute()
    elif filter_type == "min_register_year":
        Filters.update(min_registration_year=filter_value).where(Filters.user_id == user_id and Filters.parser == parser).execute()
    elif filter_type == "max_ads":
        Filters.update(max_number_of_sellers_ads=filter_value).where(Filters.user_id == user_id and Filters.parser == parser).execute()
    elif filter_type == "word_blacklist":
        Filters.update(word_blacklist=filter_value).where(Filters.user_id == user_id and Filters.parser == parser).execute()

def set_autotext(user_id: int, text: str):
    is_exists = Autotext.select().where(Autotext.user_id == user_id).exists()
    if is_exists:
        Autotext.update(text=text).where(Autotext.user_id == user_id).execute()
    else:
        Autotext.create(user_id = user_id, text = text)

def get_first_autotext(user_id: int):
    autotext = Autotext.select().where(Autotext.user_id == user_id).get()
    return autotext.text

def get_user_selected_categories_urn(user_id: int, site: str):
    urns = []
    print("NOTIMPLEMENTED: lists all urns of site")
    categories = get_user_selected_categories(user_id)
    for urn in URN.select().where(URN.site == site):
        if urn.category in categories:
            urns.append(urn.urn)
    return urns

def get_user_selected_categories_name(user_id: int, site: str):
    urns = []
    categories = get_user_selected_categories(user_id)
    for urn in URN.select().where(URN.site == site):
        if urn.category in categories:
            urns.append(urn.urn)
    return urns

def get_user_selected_categories(user_id: int):
    categories = []
    for category in UserSelectedCategories.select().where(UserSelectedCategories.user_id == user_id):
        categories.append(category.category)
    return categories

def get_categories_pair() -> list[tuple[str, str]]:
    """ -> (name of category, translation of category name)"""
    pair = []
    for urn in URN.select():
        category_name: str = urn.category_name
        pair.append((urn.category, category_name))
    return pair

def append_category_to_user(user_id: int, category: str):
    is_selected = UserSelectedCategories.select().where(UserSelectedCategories.user_id == user_id).where(UserSelectedCategories.category == category).exists()
    if not is_selected:
        UserSelectedCategories.create(user_id=user_id, category=category)
        return True
    else:
        return False

def delete_category_of_user(user_id: int, category: str):
    is_selected = UserSelectedCategories.select().where(UserSelectedCategories.user_id == user_id and UserSelectedCategories.category == category).exists()
    if is_selected:
        UserSelectedCategories.delete().where(UserSelectedCategories.user_id == user_id and UserSelectedCategories.category == category).execute()
        return True
    else:
        return False

def renew_hours(user_id: int):
    if get_hours_left(user_id) == 0:
        User.update(is_subscription_aviable=False).where(User.id == user_id).execute()
    else:
        User.update(is_subscription_aviable=True).where(User.id == user_id).execute()

def decrease_user_balance(user_id: int, amount: float):
    user = User.select().where(User.id == user_id).get()
    User.update(balance=user.balance-amount).where(User.id == user_id).execute()

def add_hours_to_user(user_id: int, hours: int):
    user = User.select().where(User.id == user_id).get()
    print("SUBEXCPIRE")
    time = user.subscription_expiration_date
    if user.subscription_expiration_date < datetime.now():
        time = datetime.now()
    print(time+timedelta(hours=hours))
    User.update(subscription_expiration_date=time+timedelta(hours=hours)).where(User.id == user_id).execute()

def clear_stop_process(user_id: int):
    ProcessStop.delete().where(ProcessStop.user_id == user_id).execute()

def add_stop_process(user_id: int):
    ProcessStop.create(user_id=user_id)

def is_stop_process(user_id: int):
    return ProcessStop.select().where(ProcessStop.user_id == user_id).exists()

def add_admin(user_id: int):
    Admin.create(user_id=user_id)

def is_user_admin(user_id: int):
    return Admin.select().where(Admin.user_id ==  user_id).exists()

def get_subscribers_count():
    return User.select().where(User.is_subscription_aviable == True).count()

def change_subscription_price(days: int, price: float):
    SubscriptionPrices.update(price=price).where(SubscriptionPrices.days == days).execute()

def get_subscription_price(days: int):
    sub = SubscriptionPrices.select().where(SubscriptionPrices.days == days).get()
    return sub.price

def create_promocode(promo: str, days: int):
    Promocode.create(promocode=promo, days_gives=days)

def delete_promocode(promo):
    Promocode.delete().where(Promocode.promocode == promo).execute()

def get_promocodes():
    promos = []
    for promocode in Promocode.select():
        promos.append((promocode.promocode, promocode.days_gives))

    return promos

def get_promocodes_count():
    return Promocode.select().count()

def get_user_token_count(user_id: int):
    return UserTokenAd.select().where(UserTokenAd.user_id == user_id).get().token_count

def add_token_to_user(user_id: int, amount: int):
    user_amount_old = get_user_token_count(user_id)
    UserTokenAd.update(token_count=user_amount_old+amount).where(UserTokenAd.user_id == user_id).execute()

def get_user_id(username: str):
    return User.select().where(User.name == username).get().id

def set_user_show_ads(user_id: int, count: int):
    UserTokenAd.update(ad_count=count).where(UserTokenAd.user_id == user_id).execute()

def get_user_show_ads(user_id: int):
    return UserTokenAd.select().where(UserTokenAd.user_id == user_id).get().ad_count

def decrement_user_show_ads(user_id: int):
    count = get_user_show_ads(user_id)
    UserTokenAd.update(ad_count=count - 1).where(UserTokenAd.user_id == user_id).execute()
    if count > 0:
        return True
    else:
        return False
