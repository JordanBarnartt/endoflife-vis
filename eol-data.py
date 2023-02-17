import requests
import json
import dataclasses
import datetime
from typing import Union

API__ALL_PRODUCTS = "https://endoflife.date/api/all.json"
API__GET_ALL_DETAILS_BASE = "https://endoflife.date/api/"


@dataclasses.dataclass
class Cycle:
    """A Python object corresponding to the endoflife.date Cycle schema."""

    cycle: str
    """Release Cycle"""

    releaseDate: datetime.date
    """Release Date for the first release in this cycle"""

    eol: Union[datetime.date, bool]
    """End of Life Date for this release cycle"""

    latest: str
    """Latest release in this cycle"""

    link: str
    """Link to changelog for the latest release, if available"""

    lts: Union[bool, str]
    """Whether this release cycle has long-term-support (LTS). Can be a date instead in YYYY-MM-DD
    format as well if the release enters LTS status on a given date."""

    support: Union[datetime.date, bool]
    """Whether this release cycle has active support"""

    discontinued: Union[datetime.date, bool]
    """Whether this cycle is now discontinued."""


def endoflife_api_all_products() -> list[str]:
    """Run endoflife.date "All Products" API request.

    Return a list of all products. Each of these can be used for the other API endpoints.
    """

    req = requests.get(API__ALL_PRODUCTS)
    products: list[str] = json.loads(req.text)

    return products


def _create_details_url(product: str) -> str:
    return API__GET_ALL_DETAILS_BASE + product + ".json"


def endoflife_api_get_all_details(product: str) -> list[Cycle]:
    url = _create_details_url(product)
    req = requests.get(url)

    cycles: list[Cycle] = []
    for c in json.loads(req.text):
        cycles.append(Cycle(**c))

    return cycles
