import requests

from bs4 import BeautifulSoup

from datetime import (
    datetime,
    timedelta
)

from services.tmdb import (
    search_content
)


# SEARCH DIGITAL RELEASE

def search_digital_release(query):

    try:

        url = (
            "https://www.dvdsreleasedates.com/search/"
        )

        params = {
            "q": query
        }

        headers = {
            "User-Agent":
            (
                "Mozilla/5.0"
            )
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        results = []

        movie_links = soup.select(
            "a[href*='/movies/']"
        )

        seen = set()

        for link_el in movie_links:

            try:

                href = link_el.get(
                    "href",
                    ""
                )

                if not href:
                    continue

                if href in seen:
                    continue

                seen.add(href)

                img = link_el.select_one(
                    "img"
                )

                if not img:
                    continue

                title = img.get(
                    "alt",
                    ""
                ).strip()

                if not title:
                    continue

                full_link = (
                    "https://www.dvdsreleasedates.com"
                    + href
                )

                results.append({

                    "title": title,

                    "release": (
                        "Digital Release"
                    ),

                    "link": full_link
                })

                if len(results) >= 5:

                    break

            except:

                continue

        return results

    except Exception as e:

        print(
            "DIGITAL SEARCH ERROR:"
        )

        print(e)

        return []


# UPCOMING DIGITAL RELEASES

def get_upcoming_digital():

    try:

        url = (
            "https://www.dvdsreleasedates.com/"
            "digital-releases/"
        )

        headers = {
            "User-Agent":
            (
                "Mozilla/5.0"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        today = datetime.today()

        limit_date = (
            today + timedelta(days=30)
        )

        results = []

        movie_links = soup.select(
            "a[href*='/movies/']"
        )

        seen = set()

        for link_el in movie_links:

            try:

                href = link_el.get(
                    "href",
                    ""
                )

                if not href:
                    continue

                if href in seen:
                    continue

                seen.add(href)

                img = link_el.select_one(
                    "img"
                )

                if not img:
                    continue

                title = img.get(
                    "alt",
                    ""
                ).strip()

                if not title:
                    continue

                # TMDB FILTER
                # REMOVE LOW QUALITY RESULTS

                tmdb_results = search_content(
                    title
                )

                if not tmdb_results:
                    continue

                tmdb = tmdb_results[0]

                popularity = tmdb.get(
                    "popularity",
                    0
                )

                vote_count = tmdb.get(
                    "vote_count",
                    0
                )

                poster = tmdb.get(
                    "poster_path"
                )

                rating = round(
                    tmdb.get(
                        "vote_average",
                        0
                    ),
                    1
                )

                # FILTER BAD RESULTS

                if popularity < 15:
                    continue

                if vote_count < 25:
                    continue

                if not poster:
                    continue

                # TRY TO FIND DATE

                parent = link_el.parent

                text = parent.get_text(
                    " ",
                    strip=True
                )

                release_date = None

                possible_formats = [

                    "%B %d, %Y",
                    "%b %d, %Y"

                ]

                for word in text.split():

                    pass

                import re

                match = re.search(
                    r"([A-Z][a-z]+ \d{1,2}, \d{4})",
                    text
                )

                if match:

                    date_str = match.group(1)

                    for fmt in possible_formats:

                        try:

                            release_date = (
                                datetime.strptime(
                                    date_str,
                                    fmt
                                )
                            )

                            break

                        except:

                            continue

                if not release_date:
                    continue

                # DATE FILTER

                if release_date < today:
                    continue

                if release_date > limit_date:
                    continue

                full_link = (
                    "https://www.dvdsreleasedates.com"
                    + href
                )

                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster
                )

                results.append({

                    "title": title,

                    "release_date": release_date,

                    "release": release_date.strftime(
                        "%d %b %Y"
                    ),

                    "rating": rating,

                    "poster": poster_url,

                    "link": full_link,

                    "popularity": popularity
                })

            except Exception as e:

                print(
                    "DIGITAL ITEM ERROR:"
                )

                print(e)

                continue

        # SORT BY DATE

        results.sort(
            key=lambda x:
            x["release_date"]
        )

        # LIMIT

        return results[:10]

    except Exception as e:

        print(
            "UPCOMING DIGITAL ERROR:"
        )

        print(e)

        return []