import requests
from bs4 import BeautifulSoup

def safe_int(text):
    try:
        return int(text.replace(',', '').strip())
    except (ValueError, AttributeError):
        return 0

def getSteamInfo(steamID):
    '''
    Retrieves user info through web crawler.

    Arguments:
        steamID - string that contains user steamID

    Returns:
        data - dict containing the user information
    '''
    data = {}
    profile_url = f"https://steamcommunity.com/profiles/{steamID}"
    response = requests.get(profile_url)

    if response.status_code != 200:
        print(f"Error: Unable to access profile (Status Code: {response.status_code})")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    # Profile Awards
    try:
        award_text = soup.select_one('.profile_awards .profile_count_link_total')
        if award_text:
            data["Profile Awards"] = safe_int(award_text.text)
        else:
            print("Profile Award not found.")
    except Exception as e:
        print(f"Error fetching profile awards: {e}")

    # Steam Level
    try:
        level_text = soup.select_one('.friendPlayerLevelNum')
        if level_text:
            data["Level"] = safe_int(level_text.text)
        else:
            print("Steam level not found.")
    except Exception as e:
        print(f"Error fetching steam level: {e}")

    # Badges
    try:
        badge_text = soup.select_one('.profile_badges .profile_count_link_total')
        if badge_text:
            data["Badges"] = safe_int(badge_text.text)
        else:
            print("Badges not found.")
    except Exception as e:
        print(f"Error fetching badges: {e}")

    # Groups
    try:
        group_text = soup.select_one('.profile_group_links .profile_count_link_total')
        if group_text:
            data["Groups"] = safe_int(group_text.text)
        else:
            print("Groups not found.")
    except Exception as e:
        print(f"Error fetching groups: {e}")

    # Basic ban detection (Note: Limited by JavaScript rendering)
    try:
        bans_url = f"https://vaclist.net/account/{steamID}"
        bans_response = requests.get(bans_url)
        if bans_response.status_code == 200:
            vac_soup = BeautifulSoup(bans_response.text, 'html.parser')
            has_bans = vac_soup.find('span', string='bans')
            data["Possible Bans Detected"] = bool(has_bans)
        else:
            print(f"Unable to access ban data. Status: {bans_response.status_code}")
    except Exception as e:
        print(f"Error checking for bans: {e}")

    return data
