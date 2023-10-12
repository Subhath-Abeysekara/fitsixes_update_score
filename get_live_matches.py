import requests

import env


def get_live_matches():
    url = env.FIT_SIXES_URL
    validate_res = requests.get(url=url)
    print(validate_res.json())
    return validate_res.json()['data']['matches']['matches']

def get_score_cards(id , scorecard):
    matches = get_live_matches()
    score_cards = []
    for match in matches:
        if id == match['id']:
            score_card = {
                "match_id": match['id'],
                "team1": scorecard['team1'],
                "team2": scorecard['team2']
            }
        else:
            score_card = {
                "match_id": match['id'],
                "team1": match['scorecard']['team1'],
                "team2": match['scorecard']['team2']
            }
        score_cards.append(score_card)
    return score_cards
