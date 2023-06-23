import requests
from config import MPSTATS_TOKEN

ID = 156259549
headers = {
    "Content-Type": "application/json",
    "X-Mpstats-TOKEN": MPSTATS_TOKEN,
}
resp = requests.get(
    url=f"https://mpstats.io/api/wb/get/item/156259549/by_category?auth-token={MPSTATS_TOKEN}",
    headers=headers,
)
# data = {"ids": [156259549]}
# resp = requests.post(
#     url=f"https://mpstats.io/api/wb/get/items/batch", headers=headers, json=data
# )
print(resp.json())
