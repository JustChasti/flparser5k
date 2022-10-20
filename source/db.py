from aiogram.types import User, user
from .db_peewee import add_user, is_user_exists, set_state_for_user, get_state_for_user
from .logger import create_logger
from . import db_peewee


logger = create_logger(__name__)


def new_user(user: User):
    logger.info(f"/start from user {user.username}")
    is_new_user = is_user_exists(user.id)
    add_user(user.id, user.username)
    return is_new_user


def set_user_state(user: User, state: str):
    set_state_for_user(user.id, state)


def get_user_state(user: User):
    return get_state_for_user(user.id)


def get_user_balance(user: User):
    return db_peewee.get_user_balance(user.id)


def get_hours_left(user: User):
    db_peewee.renew_hours(user.id)
    return db_peewee.get_hours_left(user.id)


def add_to_balance(user: User, balance_added: float):
    return db_peewee.add_to_user_balance(user.id, balance_added)

def add_to_balance_id(user_id: int, balance_added: float):
    return db_peewee.add_to_user_balance(user_id, balance_added)

def is_sub_aviable(user: User) -> bool:
    return db_peewee.is_sub_aviable(user.id)

def load_metadata(user: User) -> dict:
    return db_peewee.load_metadata(user.id)

def load_metadata_id(user_id: int) -> dict:
    return db_peewee.load_metadata(user_id)

def store_metadata(user: User, metadata: dict):
    db_peewee.store_metadata(user.id, metadata)

def append_metadata(user: User, metadata: dict):
    old_metadata = load_metadata(user)
    new_metadata = {**old_metadata, **metadata}
    db_peewee.store_metadata(user.id, new_metadata)

def get_user_filters(user_id: int):
    return db_peewee.get_user_filters(user_id)

def set_user_filters(user: User, **filters):
    db_peewee.set_user_filters(user.id, **filters)

def get_first_autotext(user_id: int):
    return db_peewee.get_first_autotext(user_id)

def set_autotext(user: User, text: str):
    db_peewee.set_autotext(user.id, text)

def get_user_selected_categories_urn(user_id: int, site: str):
    return db_peewee.get_user_selected_categories_urn(user_id, site)

def get_categories_pair():
    """ -> (name of category, translation of category name)"""
    return db_peewee.get_categories_pair()

def get_user_selected_categories(user_id: int):
    return db_peewee.get_user_selected_categories(user_id)

def toggle_category(user_id: int, category: str):
    is_added = db_peewee.append_category_to_user(user_id, category)
    if not is_added:
        db_peewee.delete_category_of_user(user_id, category)

def decrease_user_balance(user_id: int, amount: float):
    db_peewee.decrease_user_balance(user_id, amount)

def add_hours_to_user(user_id: int, hours: int):
    db_peewee.add_hours_to_user(user_id, hours)

def clear_stop_process(user_id: int):
    db_peewee.clear_stop_process(user_id)

def add_stop_process(user_id: int):
    db_peewee.add_stop_process(user_id)

def add_admin(user: User):
    db_peewee.add_admin(user.id)

def is_user_admin(user: User):
    return db_peewee.is_user_admin(user.id)

def get_subscribers_count():
    return db_peewee.get_subscribers_count()

def change_subscription_price(days: int, price: float):
    db_peewee.change_subscription_price(days, price)

def get_subscription_price(days: int):
    return db_peewee.get_subscription_price(days)

def create_promocode(promo: str, days: int):
    db_peewee.create_promocode(promo, days)

def delete_promocode(promo: str):
    db_peewee.delete_promocode(promo)

def get_promocodes():
    return db_peewee.get_promocodes()

def get_promocodes_count():
    return db_peewee.get_promocodes_count()

print(get_promocodes())


def set_filter(user_id: int, parser: str, filter_type: str, filter_value):
    db_peewee.set_filter(user_id, parser, filter_type, filter_value)

def get_filter(user_id: int, parser: str):
    return db_peewee.get_filter(user_id, parser)

def get_user_token_count(user_id: int):
    return db_peewee.get_user_token_count(user_id)
def add_token_to_user(user_id: int, amount: int):
    db_peewee.add_token_to_user(user_id, amount)

def get_user_id(username: str):
    return db_peewee.get_user_id(username)

def set_user_show_ads(user_id: int, count: int):
    return db_peewee.set_user_show_ads(user_id, count)

def get_user_show_ads(user_id: int):
    return db_peewee.get_user_show_ads(user_id)

def decrement_user_show_ads(user_id: int):
    return db_peewee.decrement_user_show_ads(user_id)

def is_stop_process(user_id: int):
    return db_peewee.is_stop_process(user_id)
