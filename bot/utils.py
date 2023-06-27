import json
import os
from database import session
from models import UnregisteredUser, RegisteredUser, Account


def read_json_properties(filename: str, properties: list) -> list:
    with open(filename, "r") as file:
        data = json.load(file)
        return [data[prop] for prop in properties]


CWD = os.getcwd()
BOT_DIR = os.path.join(CWD, "bot")
MARKETPLACES_DIR = os.path.join(BOT_DIR, "marketplaces")
AVAILABLE_MARKETPLACES = read_json_properties(
    os.path.join(MARKETPLACES_DIR, "marketplaces.json"),
    ["marketplaces"],
)[0]


def get_accounts_by_marketplace(marketplace: str) -> list[str]:
    accounts = session.query(Account).where(Account.marketplace == marketplace).all()
    return [account.name for account in accounts]
