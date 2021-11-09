import json
import logging
from datetime import datetime
from shutil import copy2
from typing import Optional
from time import sleep
import requests

"""新着本を探す
"""

REQUEST_TIMEOUT: tuple[float, float] = (20.0, 20.0)
COVERAGE_URL: str = "https://api.openbd.jp/v1/coverage"
BOOKDATA_URL: str = "https://api.openbd.jp/v1/get?isbn={isbn}"


def request_get(url: str) -> Optional[dict]:
    for _ in range(3):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            break
        except requests.RequestException as e:
            logging.warning(e)
            sleep(5)
    else:
        logging.warning("requests error")
        return None
    if response.status_code != requests.codes.ok:
        logging.warning(response.status_code)
        logging.warning("fail request")
        return None
    sleep(1)
    try:
        return response.json()
    except ValueError as e:
        logging.error(e)
        return None


# openbdから対応している本一覧を取得する

text = request_get(COVERAGE_URL)
if text is None:
    exit(1)

current_coveraged_books = set(text)
current_date = datetime.now().strftime("%Y-%m-%d")

with open(f"{current_date}.csv", "w") as wf:
    wf.write(",".join(current_coveraged_books))

