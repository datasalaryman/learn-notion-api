from time import sleep
from typing import Dict, Optional

import requests
from loguru import logger
from typing_extensions import Literal

from src.settings import (
    LINKS_DB_ID,
    NOTION_BASE_URL,
    NOTION_TOKEN,
    PAGE_ID,
    PROPERTY_ID,
)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}


def get_all_data(
    url: str,
    headers: Dict,
    data: Optional[Dict],
    method: str = Literal["get", "post"],
) -> Dict:

    method_map = {
        "get": requests.get,
        "post": requests.post,
    }

    if not data:
        data = {}

    request_func = method_map[method]

    response = request_func(url, headers=headers, json=data)

    result = response.json()["results"]

    while response.json()["has_more"]:
        sleep(0.333)
        data["start_cursor"] = response.json()["next_cursor"]
        response = request_func(url, headers=headers, json=data)
        result += response.json()["results"]

    return result


# 1. Get all uuids of the areas under Data Science
# 2. Get all the links of those areas
# 3. Transfer the links to the Data Science Area

# 1.
page_url = "".join(
    [
        NOTION_BASE_URL,
        "v1/pages/",
        PAGE_ID,
        "/properties/",
        PROPERTY_ID,
    ]
)

logger.info(f"Loading data from {page_url}")

try:
    res = requests.get(page_url, headers=headers)

    logger.info(f"Database loaded with STATUS CODE: {res.status_code}")
except TimeoutError as e:
    raise e

child_areas = [item["relation"]["id"] for item in res.json()["results"]]

logger.info(child_areas)

# 2.
query_url = NOTION_BASE_URL + "v1/databases/" + LINKS_DB_ID + "/query"

logger.info(f"Loading data from {query_url}")

link_ids = []

for area in child_areas:
    data = {
        "filter": {
            "property": "Areas",
            "relation": {"contains": area},
        },
    }

    link_ids += [
        row["id"]
        for row in get_all_data(
            url=query_url, headers=headers, data=data, method="post"
        )
    ]

logger.info(link_ids)

# 3.

for link in link_ids:
    update_url = NOTION_BASE_URL + "v1/pages/" + link

    data = {
        "properties": {
            "GII%5D": {
                "relation": [
                    {"id": PAGE_ID},
                ]
            },
            "i%7D%3C%7C": {"checkbox": False},
            "en%7DX": {"relation": []},
        }
    }
    sleep(0.333)
    res = requests.patch(update_url, headers=headers, json=data)

    logger.info(res.status_code)
