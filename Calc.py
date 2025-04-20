import Crawler
import steamApi
import math

SteamID = "76561199243535006"

crawlerData = Crawler.getSteamInfo(SteamID)
apiData = steamApi.getApiCalls(SteamID)

data = crawlerData | apiData

#   Smurf Probability calculation
print("\n"*2, "="*10,"Smurf Probability","="*10)
points = 0

if ("Friends") in data:
    points += min(20, (2 * math.sqrt(data["Friends"]))) #Continuous scaling points with cap at 20 points


if ("Level") in data:
    points += min(10, (0.3 * data["Level"]))


if ("Games") in data:
    points += min(20, (0.2 * data["Games"]))


if ("Groups") in data:
    points += min(10, (0.8 * data["Groups"]))


if ("Badges") in data:
    points += min(10, (0.6 * data["Badges"]))

print("\n")
print("Smurf probability: ", 100 - points)
print("\n")
print(data)