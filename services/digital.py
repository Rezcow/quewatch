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

        cards = soup.select(
            ".results li"
        )

        for card in cards[:5]:

            try:

                title_el = card.select_one(
                    "h4 a"
                )

                if not title_el:
                    continue

                title = (
                    title_el.get_text(
                        strip=True
                    )
                )

                link = (
                    "https://www.dvdsreleasedates.com"
                    + title_el["href"]
                )

                poster_el = card.select_one(
                    "img"
                )

                poster = ""

                if poster_el:

                    poster = poster_el.get(
                        "src",
                        ""
                    )

                release_text = ""

                meta = card.select_one(
                    ".meta"
                )

                if meta:

                    release_text = (
                        meta.get_text(
                            " ",
                            strip=True
                        )
                    )

                results.append({

                    "title": title,

                    "link": link,

                    "poster": poster,

                    "release": release_text
                })

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

        cards = soup.select(
            ".calendar .card"
        )

        for card in cards[:10]:

            try:

                title_el = card.select_one(
                    "h4 a"
                )

                if not title_el:
                    continue

                title = (
                    title_el.get_text(
                        strip=True
                    )
                )

                link = (
                    "https://www.dvdsreleasedates.com"
                    + title_el["href"]
                )

                date_el = card.select_one(
                    ".date"
                )

                release_date = ""

                if date_el:

                    release_date = (
                        date_el.get_text(
                            " ",
                            strip=True
                        )
                    )

                results.append({

                    "title": title,

                    "release": release_date,

                    "link": link
                })

            except:

                continue

        return results

    except Exception as e:

        print(
            "UPCOMING DIGITAL ERROR:"
        )

        print(e)

        return []