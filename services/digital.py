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

        import re

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

                movie_url = (
                    "https://www.dvdsreleasedates.com"
                    + href
                )

                # OPEN MOVIE PAGE

                movie_response = requests.get(
                    movie_url,
                    headers=headers,
                    timeout=10
                )

                movie_soup = BeautifulSoup(
                    movie_response.text,
                    "lxml"
                )

                movie_text = movie_soup.get_text(
                    " ",
                    strip=True
                )

                # FIND DATE

                matches = re.findall(
                    r"([A-Z][a-z]+ \d{1,2}, \d{4})",
                    movie_text
                )

                release_date = None

                for date_str in matches:

                    try:

                        release_date = (
                            datetime.strptime(
                                date_str,
                                "%B %d, %Y"
                            )
                        )

                        break

                    except:

                        try:

                            release_date = (
                                datetime.strptime(
                                    date_str,
                                    "%b %d, %Y"
                                )
                            )

                            break

                        except:

                            continue

                if not release_date:
                    continue

                # FILTER RANGE

                if release_date < today:
                    continue

                if release_date > limit_date:
                    continue

                # TMDB

                rating = "?"

                poster_url = None

                tmdb_results = search_content(
                    title
                )

                if tmdb_results:

                    tmdb = tmdb_results[0]

                    rating = round(
                        tmdb.get(
                            "vote_average",
                            0
                        ),
                        1
                    )

                    poster = tmdb.get(
                        "poster_path"
                    )

                    if poster:

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

                    "link": movie_url
                })

            except Exception as e:

                print(
                    "DIGITAL ITEM ERROR:"
                )

                print(e)

                continue

        # SORT

        results.sort(
            key=lambda x:
            x["release_date"]
        )

        return results[:10]

    except Exception as e:

        print(
            "UPCOMING DIGITAL ERROR:"
        )

        print(e)

        return []