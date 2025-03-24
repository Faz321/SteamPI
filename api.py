
import json
import requests
import Crawler

API_KEY = "5A0D4B191D567190BEE11F6B57824F32"
print("-" * 26,"\n")
print("Steam Player Investigation\n")
print("-" * 26,"\n")


VanityURL = input("\nEnter Vanity URL: ")
#shortcut for test case
if VanityURL == "a":
    VanityURL = "gabelogannewell"
elif VanityURL == "skip":
    skip = True
    steamID = "76561199792929762"

if not skip:
    response = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key="+API_KEY+"&vanityurl="+VanityURL)
    jsonData = json.loads(response.text)
    if jsonData["response"]["success"] == 1:
        steamID = jsonData["response"]["steamid"]
        print("The steamID is",steamID)
    else:
        raise Exception ("SteamID not found")
    
##Info from getPlayerSummaries
response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+API_KEY+"&steamids="+steamID)
jsonData = json.loads(response.text)
print("\n"*2,"=" * 10, "User Info", "=" * 10, "\n")
print(response.text)
userstate = jsonData["response"]["players"][0]["personastate"]
match userstate:
    case 0:
        print("Current Status: Offline")
    case 1:
        print("Current Status: Online")
    case 2:
        print("Current Status: Busy")
    case 3:
        print("Current Status: Away")
    case 4:
        print("Current Status: Snooze")
    case 5:
        print("Current Status: Looking to trade")
    case 6:
        print("Current Status: Looking to play")

try:
    print("Real Name: ", jsonData["response"]["players"][0]["realname"])
    print("Last login: ", jsonData["response"]["players"][0]["lastlogin"])
except:
    print("Some info may be hidden")

##Smurf Probability calculation
print("\n"*2, "="*10,"Smurf Probability","="*10)

smurfScore = 0

##Friends Score
##Change scouring system later to continous scale
response = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key="+API_KEY+"&steamid="+steamID+"&relationship=friend")
jsonData = json.loads(response.text)
numFriends = len(jsonData["friendslist"]["friends"])
print("Friends: ", numFriends)
if numFriends >= 100:
    smurfScore += 20
elif numFriends >= 75:
    smurfScore += 15
elif numFriends >= 50:
    smurfScore += 10
elif numFriends >= 20:
    smurfScore += 5
    
##Games Score
response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+API_KEY+"&steamid="+steamID+"&format=json")
jsonData = json.loads(response.text)
gamesCount = jsonData["response"]["game_count"]
print("Games: ", gamesCount)
if gamesCount >= 51:
    smurfScore += 20
elif gamesCount >= 50:
    smurfScore += 15
elif gamesCount >= 15:
    smurfScore += 10
elif gamesCount >= 10:
    smurfScore += 5
print("\n"," "*15,100 - smurfScore, "%")


##Maybe use webcrawler for these:
##Bans Score
##Requires different API key maybe steamworks key?
##requests.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="+API_KEY+"&steamid="+steamID)

##Steam level
##requires steamworks keys
##response = requests.get("https://partner.steam-api.com/IPlayerService/GetSteamLevel/v1?key="+API_KEY+"&steamid="+steamID)

##Group List
##steamworks keys
## https://partner.steam-api.com/ISteamUser/GetUserGroupList/v1/

##Player Badges
##steamworks key / Webcrawler
##https://partner.steam-api.com/IPlayerService/GetBadges/v1/


