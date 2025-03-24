import requests
import re
from bs4 import BeautifulSoup


#Crawler takes in profile URL and returns profileData
#TODO Fix Bans website uses javascript

def getSteamInfo(steamID):
    '''
    Retrieves User info through webcrawler

    Arguements:
    steamID - string that contains user steamID

    Returns:
    data - dict containing the user information
    
    '''
    data = {}
    response = requests.get("https://steamcommunity.com/profiles/" + steamID)

    if response.status_code != 200:
        return f"Error: Unable to access profile (Status Code: {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")

    #Retrieves Profile Award Number
    profileAwardsList = soup.find_all('div', class_="profile_awards")
    if len(profileAwardsList):
        profileAwardsList = profileAwardsList[0].find_all('span', class_="profile_count_link_total")
        profileAwardNumber = profileAwardsList[0].text.strip()
        print("Profile Awards: ", profileAwardNumber)
        data["Profile Awards"] = int(profileAwardNumber)
    else:
        print("Profile Award not found!")

    #Retrieves Steam Level
    profileLvlList = soup.find_all('span', class_="friendPlayerLevelNum")
    if profileLvlList:
        profileLvl = profileLvlList[0].text.strip()
        print("Steam level: ",profileLvl)
        data["Level"] = int(profileLvl)
    else:
        print("Steam level not found")
    
    #Retrieves Badges
    profileBadgeList = soup.find_all('div',class_ ="profile_badges")
    if profileBadgeList:
        profileBadgeList = profileBadgeList[0].find_all('span', class_="profile_count_link_total")
        profileBadgeNumber = profileBadgeList[0].text.strip()
        print("Number of Badges: ", profileBadgeNumber)
        data["Badges"] = int(profileBadgeNumber)
    else:
        print("Steam level not found")
    
    #Retrieves Groups
    profileGroupList = soup.find_all('div', class_="profile_group_links")
    if profileGroupList:
        profileGroupNumber = profileGroupList[0].find_all('span', class_="profile_count_link_total")
        profileGroupNumber = profileGroupNumber[0].text.strip()
        print("Group Number: ", profileGroupNumber)
        data["Groups"] = int(profileGroupNumber)
    else:
        print("Groups not found!")

    #Retrieves Bans
    #Bans require javascript so cant use basic requests
    bansResponse = requests.get("https://vaclist.net/account/" + steamID)

    if bansResponse.status_code != 200:
        print (f"Error: Unable to access profile (Status Code: {bansResponse.status_code})")
        return False

    miso = BeautifulSoup(bansResponse.text, 'html.parser')
    miso = miso.find_all('span', string='bans')

    return data

    #Steam page contains multiple "profile_count_link_total"
    #Indexs:
    # 0 - Profile Awards
    # 1 - Badges
    # 2 - Games
    # 3 - Inventory
    # 4 - Reviews
    # 5 - Guides
    # 6 - Artwork
    # 7 - Friends

    #To change, specific tags e.g Badges
    #<span class="count_link_label">Badges</span>
    #Error handling when info hidden

# Fetch and display the badges
data = get_steam_info('76561199243535006') #Random test profie
#data = get_steam_info('76561199126077786') #Random test profile

##shit way to do this error prone:
# print("\nSome Information may be hidden")
# print("Profile Awards: ", data[0].text.strip())
# print("Badges: ", data[1].text.strip())
# print("Games: ", data[2].text.strip())
# print("Inventory: ", data[3].text.strip())
# print("Reviews: ", data[4].text.strip())
# print("Guides: ", data[5].text.strip())
# print("Artwork: ", data[6].text.strip())
# print("Friends: ", data[7].text.strip())
