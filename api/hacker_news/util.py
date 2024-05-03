import requests


def get_request(route):
    response = requests.get("https://hacker-news.firebaseio.com/v0" + route)
    if response.status_code == 200:
        return response.json()
    else:
        #TODO raise exceptions later or somehting
        print(f"Failed to fetch {route}")
        return None

    