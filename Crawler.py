import requests
import re
from bs4 import BeautifulSoup


def Crawler():
    response = requests.get("https://steamcommunity.com/profiles/76561199243535006")
    print(response.text)    
    url_pattern = re.compile()
    return


def get_steam_info(profile_url):
    response = requests.get(profile_url)

    if response.status_code != 200:
        return f"Error: Unable to access profile (Status Code: {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")
    
    profileAwards = soup.find(class_="profile_count_link_total")
    print(profileAwards.name)

    # badges = []
    # for badge in soup.find_all("div", class_="badge_row"):
    #     badge_name = badge.find("div", class_="badge_title").text.strip()
    #     badge_xp = badge.find("div", class_="badge_info_description").text.strip()
        
    #     badges.append({"name": badge_name, "xp": badge_xp})
    #     print(badge_name, badge_xp)

    # return badges if badges else "No badges found or profile is private."

# Fetch and display the badges
badges = get_steam_info('https://steamcommunity.com/profiles/76561199243535006')

if isinstance(badges, list):
    for badge in badges:
        print(f"Badge: {badge['name']}, XP: {badge['xp']}")
else:
    print(badges)