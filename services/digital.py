import requests

from bs4 import BeautifulSoup


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

        results = []

        # REAL MOVIE BLOCKS

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
                        "Upcoming Digital Release"
                    ),

                    "link": full_link
                })

                # LIMIT

                if len(results) >= 10:

                    break

            except:

                continue

        return results

    except Exception as e:

        print(
            "UPCOMING DIGITAL ERROR:"
        )

        print(e)

        return []