import sys
import json
import asyncio
import requests
from datetime import datetime, timedelta

import pyodide_http
from typing import Optional, Any

# Patch the Requests library so it works with Pyscript
pyodide_http.patch_all()

HEADER = {}
API_BASE_TEMPLATE = "https://apis.justwatch.com/content/{path}"
REQ_SESSION = requests.Session()


def close_session():
    """
    Should really use context manager
    but this should do without changing functionality. 
    """
    if isinstance(REQ_SESSION, requests.Session):
        REQ_SESSION.close()


def search_for_item(query=None, **kwargs):
    """
    Search for a movie or show. Returns a dictionary of results.

    Args:
        query (str): Search query
        **kwargs: Optional arguments to filter results.

    Returns:
        dict: Dictionary of results.
    """
    path = "titles/{}/popular".format("en_IN")
    api_url = API_BASE_TEMPLATE.format(path=path)

    if query:
        kwargs.update({"query": query})

    null = None
    payload = {
        "age_certifications": null,
        "content_types": null,
        "presentation_types": null,
        "providers": null,
        "genres": null,
        "languages": null,
        "release_year_from": null,
        "release_year_until": null,
        "monetization_types": null,
        "min_price": null,
        "max_price": null,
        "nationwide_cinema_releases_only": null,
        "scoring_filter_types": null,
        "cinema_release": null,
        "query": null,
        "page": null,
        "page_size": null,
        "timeline_type": null,
        "person_id": null
    }

    if kwargs:
        for key, value in kwargs.items():
            if key in payload.keys():
                payload[key] = value
            else:
                print("{} is not a valid keyword".format(key))

    r = REQ_SESSION.post(api_url, json=payload, headers=HEADER)

    # Client should deal with rate-limiting.
    # JustWatch may send a 429 Too Many Requests response.
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_providers():
    """
    Returns a dictionary of providers and their respective ID's.
    """
    path = "providers/locale/{}".format("en_IN")
    api_url = API_BASE_TEMPLATE.format(path=path)
    r = REQ_SESSION.get(api_url, headers=HEADER)
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_genres():
    """
    Returns a dictionary of genres and their respective ID's.
    """
    path = "genres/locale/{}".format("en_IN")
    api_url = API_BASE_TEMPLATE.format(path=path)
    r = REQ_SESSION.get(api_url, headers=HEADER)
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_title(title_id, content_type="movie"):
    """
    Returns a dictionary of title details.

    Args:
        title_id (int): ID of the title.
        content_type (str): Type of content. Either "movie" or "show".

    Returns:
        dict: Dictionary of title details.
    """
    path = "titles/{content_type}/{title_id}/locale/{locale}".format(
        content_type=content_type,
        title_id=title_id,
        locale="en_IN"
    )

    api_url = API_BASE_TEMPLATE.format(path=path)
    print(api_url)
    r = REQ_SESSION.get(api_url, headers=HEADER)
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def search_title_id(query):
    """
    Returns a dictionary of titles returned
    from search and their respective ID's.

    Args:
        query (str): Search query

    Returns:
        dict: Dictionary of titles and their respective ID's.
    """
    results = search_for_item(query)
    return {item["id"]: item["title"] for item in results["items"]}


def get_season(season_id):
    """
    Fetches season details from the API, based on season_id.

    Args:
        season_id (int): ID of the season.

    Returns:
        dict: Dictionary of season details.
    """
    header = HEADER
    path = "titles/show_season/{}/locale/{}".format(
        season_id, "en_IN"
    )
    api_url = API_BASE_TEMPLATE.format(path=path)
    r = REQ_SESSION.get(api_url, headers=header)

    # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_episodes(show_id, page=""):
    """
    Fetches episodes details from the API, based on show_id.
    API returns 200 episodes (from newest to oldest) but takes a "page" param.

    Args:
        show_id (int): ID of the show.
        page (int): Page number to fetch.

    Returns:
        dict: Dictionary of episodes details.
    """
    header = HEADER
    path = "titles/show/{}/locale/{}/newest_episodes".format(show_id, "en_IN")
    api_url = API_BASE_TEMPLATE.format(path=path)

    if page:
        api_url += "?page={}".format(page)

    r = REQ_SESSION.get(api_url, headers=header)

    # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_cinema_times(title_id, content_type="movie", **kwargs):
    """
    Returns a dictionary of cinema times for a given title.

    Args:
        title_id (int): ID of the title.
        content_type (str): Type of content. Either "movie" or "show".
        **kwargs: Optional arguments to filter results.

    Returns:
        dict: Dictionary of cinema times.
    """
    null = None
    payload = {
        "date": null,
        "latitude": null,
        "longitude": null,
        "radius": 20000
    }

    if kwargs:
        for key, value in kwargs.items():
            if key in payload.keys():
                payload[key] = value
            else:
                print("{} is not a valid keyword".format(key))

    header = HEADER
    path = "titles/{}/{}/showtimes".format(content_type, title_id)
    api_url = API_BASE_TEMPLATE.format(path=path)
    r = REQ_SESSION.get(api_url, params=payload, headers=header)

    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_cinema_details(**kwargs):
    """
    Returns a dictionary of cinema details.

    Args:
        **kwargs: Optional arguments to filter results.

    Returns:
        dict: Dictionary of cinema details.
    """
    null = None
    payload = {
        "latitude": null,
        "longitude": null,
        "radius": 20000
    }

    if kwargs:
        for key, value in kwargs.items():
            if key in payload.keys():
                payload[key] = value
            elif key == "date":
                pass
            else:
                print("{} is not a valid keyword".format(key))

    header = HEADER
    path = "cinemas/{}".format("en_IN")
    api_url = API_BASE_TEMPLATE.format(path=path)
    r = REQ_SESSION.get(api_url, params=payload, headers=header)

    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_upcoming_cinema(weeks_offset, nationwide_cinema_releases_only=True):
    """
    Returns a dictionary of upcoming cinema releases.

    Args:
        weeks_offset (int): Number of weeks to offset from current date.
        nationwide_cinema_releases_only (bool): Whether to return only nationwide releases.

    Returns:
        dict: Dictionary of upcoming cinema releases.
    """
    header = HEADER
    payload = {
        "nationwide_cinema_releases_only": nationwide_cinema_releases_only,
        "body": {}
    }
    now_date = datetime.now()
    td = timedelta(weeks=weeks_offset)
    year_month_day = (now_date + td).isocalendar()
    path = "titles/movie/upcoming/{}/{}/locale/{}".format(
        year_month_day[0], year_month_day[1], "en_IN"
    )
    api_url = API_BASE_TEMPLATE.format(path=path)

    # this throws an error if you go too many weeks forward,
    # so return a blank payload if we hit an error
    try:
        r = REQ_SESSION.get(api_url, params=payload, headers=header)

        # Client should deal with rate-limiting.
        # JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()
    except:
        return {"page": 0, "page_size": 0, "total_pages": 1, "total_results": 0, "items": []}


def get_certifications(content_type="movie"):
    """
    Returns a dictionary of certifications for a given content type.

    Args:
        content_type (str): Type of content. Either "movie" or "show".

    Returns:
        dict: Dictionary of certifications.
    """
    header = HEADER
    payload = {"country": "IN", "object_type": content_type}
    api_url = API_BASE_TEMPLATE.format(path="age_certifications")
    r = REQ_SESSION.get(api_url, params=payload, headers=header)

    # Client should deal with rate-limiting.
    # JustWatch may send a 429 Too Many Requests response.
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()


def get_person_detail(person_id):
    """
    Returns a dictionary of person details.

    Args:
        person_id (int): ID of the person.

    Returns:
        dict: Dictionary of person details.
    """
    path = "titles/person/{person_id}/locale/{locale}".format(
        person_id=person_id, locale="en_IN"
    )
    api_url = API_BASE_TEMPLATE.format(path=path)

    r = REQ_SESSION.get(api_url, headers=HEADER)
    r.raise_for_status()   # Raises requests.exceptions.HTTPError if r.status_code != 200

    return r.json()
