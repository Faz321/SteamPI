#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from modules import crawler
import modules.steam_api as steam_api
import math


def compute_smurf_probability(steamID):
    """
    Fetches data from crawler and Steam API, then computes a "smurf probability" score.

    Returns:
      tuple: (smurf_probability (float), merged_data (dict))
    """
    # Attempt to fetch crawler data
    try:
        crawlerData = crawler.getSteamInfo(steamID)
    except Exception as e:
        print(f"Error fetching crawler data for {steamID}: {e}")
        crawlerData = {}

    # Attempt to fetch API data
    try:
        apiData = steam_api.getApiCalls(steamID)
    except Exception as e:
        print(f"Error fetching API data for {steamID}: {e}")
        apiData = {}

    # Merge dictionaries (Python 3.9+)
    data = crawlerData | apiData

    # Compute points
    points = 0.0
    if "Friends" in data:
        points += min(20, 2 * math.sqrt(data["Friends"]))
    if "Level" in data:
        points += min(10, 0.3 * data["Level"])
    
    # Process Games: support longer list of games
    if "Games" in data:
        if isinstance(data["Games"], list):
            games_count = len(data["Games"])
            games_list = data["Games"]
        else:
            games_count = data["Games"]
            games_list = []
        points += min(20, 0.2 * games_count)
    else:
        games_count = 0
        games_list = []
    
    # Process Groups: capture list and count
    if "Groups" in data:
        if isinstance(data["Groups"], list):
            groups_count = len(data["Groups"])
            groups_list = data["Groups"]
        else:
            groups_count = data["Groups"]
            groups_list = []
        points += min(10, 0.8 * groups_count)
    else:
        groups_count = 0
        groups_list = []
    
    # Process Communities: new addition
    if "Communities" in data:
        if isinstance(data["Communities"], list):
            communities_count = len(data["Communities"])
            communities_list = data["Communities"]
        else:
            communities_count = data["Communities"]
            communities_list = []
        points += min(5, 0.5 * communities_count)
    else:
        communities_count = 0
        communities_list = []
    
    if "Badges" in data:
        points += min(10, 0.6 * data["Badges"])
    
    smurf_probability = 100 - points
    data["games_list"] = games_list
    data["groups_count"] = groups_count
    data["groups_list"] = groups_list
    data["communities_count"] = communities_count
    data["communities_list"] = communities_list
    return smurf_probability, data


def main():
    # Example SteamID; replace with dynamic input if needed
    SteamID = "76561199243535006"

    print("\n" * 2, "=" * 10, "Smurf Probability", "=" * 10)
    probability, data = compute_smurf_probability(SteamID)
    print(f"\nSmurf probability: {probability}")
    print(f"Games List: {data.get('games_list', [])}")
    print(f"Groups Count: {data.get('groups_count', 0)}")
    print(f"Communities Count: {data.get('communities_count', 0)}")
    print(data)

if __name__ == '__main__':
    main()
