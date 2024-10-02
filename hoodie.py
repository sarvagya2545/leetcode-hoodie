import requests

leetcode_store_url = "https://leetcode.com/store/"
discord_webhook_url = "https://discord.com/api/webhooks/1290997468149842011/HJd7Ov0O2TkWjsSxxZ3FPEB3a_rm4-s73MzXS_eZHO1T1ficQrf_C_DQwOAXtMavycXP"

def check_hoodie_available() -> bool:
    data = get_leetcode_store_data()
    is_hoodie_available = False
    for store_item in data.get("storeItems"):
        if store_item.get("itemSlug") == "leetcode_hoodie" and store_item.get("available"):
            is_hoodie_available = True
    return is_hoodie_available 

def get_leetcode_store_data():
    """
    Make a graphql request to leetcode server and check whether the hoodie is available or not
    """
    url = 'https://leetcode.com/graphql'

    payload = {
        'operationName': 'storeItems',
        'variables': {},
        'query': '''query storeItems {
            storeItems {
                itemSlug
                available
            }
        }'''
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://leetcode.com',
        'referer': 'https://leetcode.com/store/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    # curl 'https://leetcode.com/graphql' \
    # -H 'accept: */*' \
    # -H 'accept-language: en-US,en;q=0.9' \
    # -H 'content-type: application/json' \
    # -H 'origin: https://leetcode.com' \
    # -H 'priority: u=1, i' \
    # -H 'referer: https://leetcode.com/store/' \
    # -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "macOS"' \
    # -H 'sec-fetch-dest: empty' \
    # -H 'sec-fetch-mode: cors' \
    # -H 'sec-fetch-site: same-origin' \
    # -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
    # --data-raw '{"operationName":"storeItems","variables":{},"query":"query storeItems {\n  storeItems {\n    itemSlug\n    available\n}\n}\n"}'

    response = requests.post(url=url, json=payload, headers=headers)
    # print(to_curl(resp.request))
    # print(response.status_code)
    # print(response.content)

    data = response.json()
    return data.get("data")
    

def send_notification():
    """
    Send discord notification notifying about the availability of hoodie
    """
    data = {
        "content": f"Leetcode Hoodie is available! Get the hoodie: {leetcode_store_url}",
        "username": "Leetcode Hoodie Notifier"
    }

    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: status code - {response.status_code}. Error - {response.content}")    

if __name__ == "__main__":
    if check_hoodie_available():
        print("Hoodie available, sending notification")
        send_notification()
    else:
        print("Hoodie not available")