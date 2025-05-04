import time
import requests

API_KEY = "9A34BC94618E00302F43601BB1671633"  # Replace with your real Steam API key
BASE    = "https://api.steampowered.com"


def safe_request(path, params, retries=3, delay=2):
    url = f"{BASE}{path}"
    for attempt in range(1, retries + 1):
        r = requests.get(url, params=params)
        if r.status_code == 429:
            time.sleep(delay)
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()


def resolve_vanity(vanity):
    r = safe_request("/ISteamUser/ResolveVanityURL/v0001/", {
        "key": API_KEY,
        "vanityurl": vanity
    })
    j = r.json()
    if j.get("response", {}).get("success") != 1:
        raise Exception("Vanity URL not found")
    return j["response"]["steamid"]


def get_player_summary(steamid):
    r = safe_request("/ISteamUser/GetPlayerSummaries/v0002/", {
        "key": API_KEY,
        "steamids": steamid
    })
    j = r.json()
    players = j.get("response", {}).get("players", [])
    if not players:
        raise Exception("No player data found (invalid ID or private).")
    return players[0]


def get_friend_count(steamid):
    r = safe_request("/ISteamUser/GetFriendList/v0001/", {
        "key": API_KEY,
        "steamid": steamid,
        "relationship": "friend"
    })
    j = r.json()
    return len(j.get("friendslist", {}).get("friends", []))


def get_owned_games(steamid):
    r = safe_request("/IPlayerService/GetOwnedGames/v0001/", {
        "key": API_KEY,
        "steamid": steamid,
        "include_appinfo": True,
        "format": "json"
    })
    j = r.json()
    return j.get("response", {}).get("games", [])

def get_top_played_games(steamid, count=3):
    games = get_owned_games(steamid)
    top = sorted(games, key=lambda g: g.get("playtime_forever", 0), reverse=True)[:count]
    return [{"name": g["name"], "minutes": g["playtime_forever"]} for g in top]



def getApiCalls(steamID, is_vanity=False):
    """
    steamID: either 64-bit ID or vanity string
    is_vanity=True: resolve via ResolveVanityURL
    """
    if is_vanity:
        steamID = resolve_vanity(steamID)

    player = get_player_summary(steamID)
    return {
        "Username": player.get("personaname", "Unknown"),
        "Avatar": player.get("avatarfull"),
        "Real Name": player.get("realname"),
        "Status": {
            0: "Offline", 1: "Online", 2: "Busy", 3: "Away",
            4: "Snooze", 5: "Looking to Trade", 6: "Looking to Play"
        }.get(player.get("personastate", 0), "Unknown"),
        "Friends": get_friend_count(steamID),
        "Games": len(get_owned_games(steamID)),
        "Steam Level": get_steam_level(steamID),
        "Badges": get_badge_count(steamID),
        "Top Games": get_top_played_games(steamID)
    }

def get_steam_level(steamid):
    r = safe_request("/IPlayerService/GetSteamLevel/v1/", {
        "key": API_KEY,
        "steamid": steamid
    })
    j = r.json()
    return j.get("response", {}).get("player_level", 0)

def get_badge_count(steamid):
    r = safe_request("/IPlayerService/GetBadges/v1/", {
        "key": API_KEY,
        "steamid": steamid
    })
    j = r.json()
    badges = j.get("response", {}).get("badges", [])
    return len(badges)
