import Crawler
import steamApi

SteamID = "76561199243535006"

crawlerData = Crawler.getSteamInfo(SteamID)
apiData = steamApi.getApiCalls(SteamID)

data = crawlerData | apiData

#   Smurf Probability calculation
print("\n"*2, "="*10,"Smurf Probability","="*10)
print(data)