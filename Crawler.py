import requests
import re
from bs4 import BeautifulSoup


#Crawler takes in profile URL and returns profileData
#TODO Order of data can be changed, dont hard code data order

def get_steam_info(profile_url):
    response = requests.get(profile_url)

    if response.status_code != 200:
        return f"Error: Unable to access profile (Status Code: {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")

    #Retrieves Profile Award Number
    profileAwardsList = soup.find_all('div', class_="profile_awards")
    if len(profileAwardsList):
        profileAwardsList = profileAwardsList[0].find_all('span', class_="profile_count_link_total")
        profileAwardNumber = profileAwardsList[0].text.strip()
        print("Profile Awards: ", profileAwardNumber)
    else:
        print("Profile Award not found!")

    #Retrieves Steam Level
    profileLvlList = soup.find_all('span', class_="friendPlayerLevelNum")
    if profileLvlList:
        profileLvl = profileLvlList[0].text.strip()
        print("Steam level: ",profileLvl)
    else:
        print("Steam level not found")
    
    #Retrieves Badges
    profileBadgeList = soup.find_all('div',class_ ="profile_awards")
    if profileBadgeList:
        profileBadgeList = profileBadgeList[0].find_all('span', class_="profile_count_link_total")
        profileBadgeNumber = profileBadgeList[0].text.strip()
        print("Number of Badges: ", profileBadgeNumber)
    else:
        print("Steam level not found")
    
    #Retrieves Groups
    profileGroupList = soup.find_all('div', class_="profile_group_links profile_count_link_preview_ctn")
    if profileGroupList:
        profileGroupNumber = profileGroupList[0]
        print("Group Number: ", profileGroupNumber)
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
    profileData = soup.find_all('span', class_="profile_count_link_total")
    profileClasses = soup.find_all('span', class_="count_link_label")
    print("\nCategories Available:")
    for i in profileClasses:
        pass
        # print(i.text.strip())

    #To change, specific tags e.g Badges
    #<span class="count_link_label">Badges</span>
    #Error handling when info hidden
    return profileData

# Fetch and display the badges
#data = get_steam_info('https://steamcommunity.com/profiles/76561199243535006') #Random test profile
data = get_steam_info('https://steamcommunity.com/profiles/76561199126077786') #Random test profile


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
