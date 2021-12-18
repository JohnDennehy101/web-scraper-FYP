import requests

def makeWebScrapeRequest(url):
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )

    return r.content