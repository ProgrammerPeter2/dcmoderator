import requests

url = "https://discord.com/api/webhooks/840904820574912563/K343skkJDBmsc9McIHthn2TQ-ETUo0f4ftmzRUyghOmwXkNOwdTd2v2iQE438MOIABFL"

def sendWebhook(text: str):
    data = {"content": "", "username": "Moderátorbot Logging", "embeds": [
        {
            "description": text,
            "title": "Tiltott szó törlése",
            "color": "24816"
        }
    ]}
    result = requests.post(url=url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))