import json
import os


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


def get_accounts() -> list[str]:
    a = [["Первый", 123213412312], ["Второй", 123213412312]]
    return [x[0] for x in a]
