import httpx
url = "https://j9y2xa0vx0.execute-api.us-east-1.amazonaws.com/api/scatter/bpa2hu"
def populate_queue():
    payload = httpx.post(url).json
    return "queue populated"