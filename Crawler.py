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

    #Retrieves Profile Award Number
    profileAwardsList = soup.find_all('div', class_="profile_awards")
    if profileAwardList:
        profileAwardList = profileAwardsList[0].find_all('span', class_="profile_count_link_total")
        profileAwardNumber = profileAwardList[0].text.strip()
        print("Profile Awards: ", profileAwardNumber)
    else:
        print("Profile Award not found!")

    profileClasses = soup.find_all('span', class_="count_link_label")
    profileLvl = soup.find_all('span', class_="friendPlayerLevelNum")

    profileData = soup.find_all('span', class_="profile_count_link_total")
    print("\nCategories Available:")
    for i in profileClasses:
        print(i.text.strip())

    print("Steam Level: ", profileLvl[0].text.strip())
    #To change, specific tags e.g Badges
    #<span class="count_link_label">Badges</span>
    #Error handling when info hidden
    return profileData

# Fetch and display the badges
data = get_steam_info('https://steamcommunity.com/profiles/76561199243535006') #Random test profile
#data = get_steam_info('https://steamcommunity.com/profiles/76561199126077786') #Random test profile
print("\nSome Information may be hidden")
print("Profile Awards: ", data[0].text.strip())
print("Badges: ", data[1].text.strip())
print("Games: ", data[2].text.strip())
print("Inventory: ", data[3].text.strip())
print("Reviews: ", data[4].text.strip())
print("Guides: ", data[5].text.strip())
print("Artwork: ", data[6].text.strip())
print("Friends: ", data[7].text.strip())
