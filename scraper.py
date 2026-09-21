import csv
import json
import logging
import re
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://www.hamrah-mechanic.com"
SEARCH_URL = f"{BASE_URL}/cars-for-sale/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fa,en;q=0.9",
}


def build_search_url(body_type: str, km_status: int, price_range: str) -> str:
    """
    Build Hamrah Mechanic search URL.
    km_status: 2 for used (کارکرده), 3 for zero/new (صفر)
    price_range: e.g. '500,1000', '1000,5000', '5000,10000'
    """
    url = f"{SEARCH_URL}?kmStatus={km_status}&bodytype={body_type}&price={price_range}"
    if km_status == 3:
        url += "&km=0"
    return url


def fetch_cars(
    body_type: str,
    km_status: int,
    price_range: str,
    timeout: int = 15
) -> Dict[str, Any]:
    """
    Scrape car listings from Hamrah Mechanic.
    Returns a dictionary with:
      - 'cars': list of car dicts
      - 'search_url': direct link to search page
      - 'total_count': total cars found on site
    """
    target_url = build_search_url(body_type, km_status, price_range)
    cars: List[Dict[str, Any]] = []
    total_count: Optional[int] = None

    try:
        response = requests.get(target_url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Primary parser: Next.js __NEXT_DATA__ SSR JSON
        next_data_script = soup.find("script", id="__NEXT_DATA__")
        if next_data_script and next_data_script.string:
            try:
                data = json.loads(next_data_script.string)
                page_cars = (
                    data.get("props", {})
                    .get("pageProps", {})
                    .get("cars", {})
                )
                total_count = page_cars.get("totalCount")
                raw_list = page_cars.get("list", [])

                for item in raw_list:
                    name = item.get("carNamePersian") or ""
                    type_name = item.get("carTypeName") or ""
                    title = f"{name} ({type_name})" if type_name else name

                    price_val = item.get("price")
                    if isinstance(price_val, (int, float)) and price_val > 0:
                        price_str = f"{price_val:,} تومان"
                    else:
                        price_str = "توافقی / استعلامی"

                    year = item.get("carYear")
                    km = item.get("km")
                    if isinstance(km, (int, float)):
                        km_str = f"{km:,} کیلومتر" if km > 0 else "صفر کیلومتر"
                    elif km:
                        km_str = f"{km} کیلومتر"
                    else:
                        km_str = "صفر کیلومتر" if km_status == 3 else "نامشخص"

                    location = item.get("carLocation") or "نامشخص"
                    color = item.get("carColorName") or ""
                    gearbox = item.get("gearBoxPersian") or ""

                    detail_link = item.get("exhibitionDetailUrl") or ""
                    if detail_link and not detail_link.startswith("http"):
                        detail_link = f"{BASE_URL}{detail_link}"

                    cars.append({
                        "name": title.strip() or "خودرو بدون عنوان",
                        "price": price_str,
                        "year": str(year) if year else "نامشخص",
                        "km": km_str,
                        "location": location,
                        "color": color,
                        "gearbox": gearbox,
                        "url": detail_link,
                    })
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.warning(f"Failed to parse __NEXT_DATA__: {e}")

        # 2. Fallback parser: HTML card scanning
        if not cars:
            cards = soup.find_all(
                "div",
                class_=lambda cl: cl and "carCard_card-container" in cl
            )
            for card in cards:
                title_tag = card.find(
                    class_=lambda cl: cl and ("header__name" in cl or "title" in cl.lower())
                )
                price_tag = card.find(
                    class_=lambda cl: cl and ("price-container" in cl or "cost" in cl.lower())
                )
                link_tag = card.find("a", href=True)

                if title_tag:
                    title = title_tag.get_text(strip=True)
                    price = price_tag.get_text(strip=True) if price_tag else "توافقی"
                    url = link_tag["href"] if link_tag else ""
                    if url and not url.startswith("http"):
                        url = f"{BASE_URL}{url}"

                    cars.append({
                        "name": title,
                        "price": price,
                        "year": "نامشخص",
                        "km": "نامشخص",
                        "location": "نامشخص",
                        "color": "",
                        "gearbox": "",
                        "url": url,
                    })

    except requests.RequestException as e:
        logger.error(f"HTTP request failed for {target_url}: {e}")

    return {
        "cars": cars,
        "search_url": target_url,
        "total_count": total_count if total_count is not None else len(cars),
    }


def save_cars_to_csv(cars: List[Dict[str, Any]], filepath: str = "car.csv") -> None:
    """
    Save cars to a CSV file with utf-8-sig encoding for proper Persian text display in Excel.
    """
    fieldnames = ["نام خودرو", "قیمت", "سال ساخت", "کارکرد", "موقعیت", "رنگ", "گیربکس", "لینک"]
    try:
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            for c in cars:
                writer.writerow([
                    c.get("name", ""),
                    c.get("price", ""),
                    c.get("year", ""),
                    c.get("km", ""),
                    c.get("location", ""),
                    c.get("color", ""),
                    c.get("gearbox", ""),
                    c.get("url", ""),
                ])
    except IOError as e:
        logger.error(f"Failed to write CSV to {filepath}: {e}")
