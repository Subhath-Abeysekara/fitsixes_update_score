from bson import ObjectId

from cash import set_pq, get_movement_empty, get_movement
from connection import connect_mongo_match
from get_live_matches import get_score_cards

collection_name_match = connect_mongo_match()

def check_match_state(overs , all_out , score_card , first_bat_team , second_bat_team):
    first_bat_score = score_card[first_bat_team]
    second_bat_score = score_card[second_bat_team]
    if (first_bat_score['overs']>=overs or first_bat_score['wickets']>=all_out) and (second_bat_score['overs'] >= overs or second_bat_score['wickets']>=all_out):
        return {
            "state":"finish"
        }
    elif first_bat_score['overs']>=overs or first_bat_score['wickets']>=all_out :
        return {
            "state": second_bat_team
        }
    else:
        return {
            "state": first_bat_team
        }
def update_over(scorecard , team):
    if scorecard[team]['balls'] < 0:
        scorecard[team]['overs']-=1
        scorecard[team]['balls'] = 5
    return scorecard

def update_wicket(scorecard , team):
    scorecard[team]['wickets']-=1
    scorecard[team]['balls']-=1
    return update_over(scorecard=scorecard , team=team)

def update_score(scorecard , team , key):
    print(scorecard[team])
    score_keys = {
        "sixes":6,
        "fours":4,
        "ones":1,
        "twos":2,
        "threes":3,
        "fives":5,
        "sevens":7,
        "extras_zero":1,
        "extras_one": 2,
        "extras_two": 3,
        "extras_three": 4,
        "extras_four": 5,
        "extras_five":6,
        "extras_six": 7,
        "extras_seven": 8,
        "wicket_ones":1,
        "wicket_twos":2,
        "wicket_threes":3
    }
    score = score_keys[key]
    scorecard[team]['marks'] -= score
    keys = key.split('_')
    key = keys[0]
    if key != 'extras':
        scorecard[team]['balls'] -= 1
        score = 1
        if key == 'wicket':
            key = keys[1]
            scorecard[team]['wickets'] -= 1
    if key != 'fives' and key != 'sevens':
        scorecard[team][key] -= score
    return update_over(scorecard=scorecard , team=team)

def update_dot_ball(scorecard , team):
    scorecard[team]['balls'] -= 1
    return update_over(scorecard=scorecard , team=team)

def recap_match_score(id):
    try:
        if get_movement_empty():
            return {
                "state": False,
                "message": "No Movements"
            }
        else:
            move = get_movement(id)
            id = move['id']
            key = move['key']
        match = collection_name_match.find_one({'_id': ObjectId(id)})
        print(match)
        first_bat_team = match['first_bat']
        print(first_bat_team)
        second_bat_team = "team1" if first_bat_team == "team2" else "team2"
        overs = match['overs']
        all_out = match['all_out']
        match_state = check_match_state(overs=overs, all_out=all_out, score_card=match['scorecard'],
                                        first_bat_team=first_bat_team, second_bat_team=second_bat_team)
        print(match_state)
        if match_state['state'] == "finish":
            return {
                "state": True,
                "finish_state": True
            }
        else:
            print(key)
            if key == 'zero':
                scorecard = update_dot_ball(match['scorecard'], team=match_state['state'])
            elif key == 'wicket':
                scorecard = update_wicket(match['scorecard'], team=match_state['state'])
            else:
                scorecard = update_score(match['scorecard'], team=match_state['state'], key=key)
            print(scorecard)
            result = collection_name_match.update_one({'_id': ObjectId(id)},{"$set":{'scorecard':scorecard}})
            print(result.upserted_id)
            scorecards = get_score_cards(scorecard=scorecard , id=id)
            print(scorecards)
            set_pq(scorecards)
        return {
            "state": True,
            "finish_state": False
        }
    except Exception:
        return {
            "state": False,
            "error": Exception
        }