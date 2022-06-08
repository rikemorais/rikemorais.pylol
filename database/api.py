import pandas as pd


def rgapi():
    url = "https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
    user = "5weCnbUCk3FQ4lFlEKUiut6l6w3i3l5GmHMe3hOt6jacQnw"
    api = open("tokens/.token_id").read()
    link = pd.read_json(url+user+"?api_key="+api)
    return link
