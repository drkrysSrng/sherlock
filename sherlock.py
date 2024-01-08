import logging
import glob
import re
import json
from os import makedirs, path




# DIRS
LOGDIRECTORY = "./logs/"
SOURCEDIRECTORY = "./source/"

# SOURCE
FILE_URLS = "urls_filtered.json"

# FILTERS
URL_PATTERN = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_TELEGRAM = "https?:\\/\\/(?:www\\.)?(?:t|telegram).me\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_TELEGRAM_OTHER = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}telegram[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

URL_PASTEBIN = "https?:\\/\\/(?:www\\.)?pastebin.com\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_GIT = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}github[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_ONION = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.onion"
URL_GOOGLE_PH = "https?:\\/\\/(?:www\\.)?photos.app.goo.gl\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_MATRIX = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}(?:matrix|element)[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_DISCORD = "https?:\\/\\/(?:www\\.)?discord\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_ARCHIVE = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}archive[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_MEDIAFIRE = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}mediafire[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_FILE_SHARE = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}(?:file|download|transfer|share|image|upload|dropbox|vudeo|video|stream|top4top)[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_PASTE_OTHER = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{0,256}paste[-a-zA-Z0-9@:%._\\+~#=]{0,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_MAYBE_SHORTEN = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,10}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_YOUTUBE = "https?:\\/\\/(?:www\\.)?youtube\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_YOUTUBE_SHORT = "https?:\\/\\/(?:www\\.)?youtu\\.be\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_RRSS = "https?:\\/\\/(?:www\\.)?(?:instagram|facebook|ticktok|twitter)\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_CHATTHEAVEN = "https?:\\/\\/(?:www\\.)?chat.techhaven\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
URL_MEDIA_CHATTHEAVEN = "https?:\\/\\/(?:www\\.)?media.techhaven.to\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
USER_RE = " @ ?[-a-zA-Z0-9@:%._\\+~#=]*"
URL_INVITATIONS_ROCKET = "https?:\\/\\/(?:www\\.)?go.rocket.chat\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"


# JSON DICT
TELEGRAM = "TELEGRAM"
ONION = "ONION"
PASTEBIN = "PASTEBIN"
MEDIAFIRE = "MEDIAFIRE"
SHORTEN = "SHORTEN"
MATRIX = "MATRIX"
GOOGLE_PHTOS = "GOOGLE_PHOTOS"
USERS = "USERS"
URL_OTHER = "URL_OTHER"
ARCHIVE = "ARCHIVE"
YOUTUBE = "YOUTUBE"
FILE_SHARE = "FILESHARE"
SOCIALMEDIA = "SOCIALMEDIA"
CHATTHEAVEN = "CHATTHEAVEN"
MEDIACHATTHEAVEN = "MEDIACHATTHEAVEN"
ROCKETINVITATIONS = "ROCKETINVITATIONS"
DISCORD = "DISCORD"
GITHUB = "GITHUB"



url_list = {}

url_list[TELEGRAM] = {}
url_list[ONION] = {}
url_list[PASTEBIN] = {}
url_list[MATRIX] = {}
url_list[DISCORD] = {}
url_list[GOOGLE_PHTOS] = {}
url_list[USERS] = {}
url_list[URL_OTHER] = {}
url_list[SHORTEN] = {}
url_list[MEDIAFIRE] = {}
url_list[ARCHIVE] = {}
url_list[YOUTUBE] = {}
url_list[FILE_SHARE] = {}
url_list[SOCIALMEDIA] = {}
url_list[CHATTHEAVEN] = {}
url_list[MEDIACHATTHEAVEN] = {}
url_list[ROCKETINVITATIONS] = {}
url_list[GITHUB] = {}



# LOG
if not path.exists(LOGDIRECTORY):
    makedirs(LOGDIRECTORY)

level = logging.INFO

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s",
                    encoding='utf-8',
                    level=level,
                    handlers=[
                        logging.FileHandler(f"{LOGDIRECTORY}sherlock.log"),
                        logging.StreamHandler()
                    ])



# Read json_files folder
json_user_files = glob.glob(SOURCEDIRECTORY + "*.json")

# Each User
for file in json_user_files:
    with open(file, 'r') as f:
        logging.debug(f"File {file}")

        fileLines = f.readlines()
        for content in fileLines:
            saved = False

            content = content.lower()

            telegram_list = re.findall(URL_TELEGRAM, content)
            for url in telegram_list:
                if url not in url_list[TELEGRAM]:
                    logging.debug(f"Telegram {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[TELEGRAM][url] = new_url
                saved = True # In case we save and it is already saved in the list

            telegram_list = re.findall(URL_TELEGRAM_OTHER, content)
            for url in telegram_list:
                if url not in url_list[TELEGRAM]:
                    logging.debug(f"Telegram {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[TELEGRAM][url] = new_url
                saved = True # In case we save and it is already saved in the list

            archive_list = re.findall(URL_ARCHIVE, content)
            for url in archive_list:
                if not saved and url not in url_list[ARCHIVE]:
                    logging.debug(f"Archive {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[ARCHIVE][url] = new_url
                saved = True # In case we save and it is already saved in the list

            pastebin_list = re.findall(URL_PASTEBIN, content)
            for url in pastebin_list:
                if not saved and url not in url_list[PASTEBIN]:
                    logging.debug(f"PasteBin other {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[PASTEBIN][url] = new_url
                saved = True # In case we save and it is already saved in the list

            pastebin_list = re.findall(URL_MEDIAFIRE, content)
            for url in pastebin_list:
                if not saved and url not in url_list[MEDIAFIRE]:
                    logging.debug(f"MediaFire {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[MEDIAFIRE][url] = new_url
                saved = True # In case we save and it is already saved in the list


            pastebin_list = re.findall(URL_PASTE_OTHER, content)
            for url in pastebin_list:
                if not saved and url not in url_list[PASTEBIN]:
                    logging.debug(f"Paste Other {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[PASTEBIN][url] = new_url
                saved = True # In case we save and it is already saved in the list

            gpho_list = re.findall(URL_GOOGLE_PH, content)
            for url in gpho_list:
                if not saved and url not in url_list[GOOGLE_PHTOS]:
                    logging.debug(f"Google Photos {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[GOOGLE_PHTOS][url] = new_url
                saved = True # In case we save and it is already saved in the list

            matrix_list = re.findall(URL_MATRIX, content)
            for url in matrix_list:
                if not saved and url not in url_list[MATRIX]:
                    logging.debug(f"Matrix url {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[MATRIX][url] = new_url
                saved = True # In case we save and it is already saved in the list

            discord_list = re.findall(URL_DISCORD, content)
            for url in discord_list:
                if not saved and url not in url_list[DISCORD]:
                    logging.debug(f"Discord 11 url {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[DISCORD][url] = new_url
                saved = True  # In case we save and it is already saved in the list


            onion_list = re.findall(URL_ONION, content)
            for url in onion_list:
                if not saved and url not in url_list[ONION]:
                    logging.debug(f"Onion {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[ONION][url] = new_url
                saved = True # In case we save and it is already saved in the list



            youtube_list = re.findall(URL_YOUTUBE, content)
            for url in youtube_list:
                if not saved and url not in url_list[YOUTUBE]:
                    logging.debug(f"Youtube {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[YOUTUBE][url] = new_url
                saved = True # In case we save and it is already saved in the list


            youtube_list = re.findall(URL_YOUTUBE_SHORT, content)
            for url in youtube_list:
                if not saved and url not in url_list[YOUTUBE]:
                    logging.debug(f"Youtube {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[YOUTUBE][url] = new_url
                saved = True # In case we save and it is already saved in the list


            file_list = re.findall(URL_FILE_SHARE, content)
            for url in file_list:
                if not saved and url not in url_list[FILE_SHARE]:
                    logging.debug(f"File share {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[FILE_SHARE][url] = new_url
                saved = True # In case we save and it is already saved in the list


            social_list = re.findall(URL_RRSS, content)
            for url in social_list:
                if not saved and url not in url_list[SOCIALMEDIA]:
                    logging.debug(f"Socialmedia {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[SOCIALMEDIA][url] = new_url
                saved = True # In case we save and it is already saved in the list

            heaven_list = re.findall(URL_CHATTHEAVEN, content)
            for url in heaven_list:
                if not saved and url not in url_list[CHATTHEAVEN]:
                    logging.debug(f"Chatheaven {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[CHATTHEAVEN][url] = new_url
                saved = True # In case we save and it is already saved in the list

            git_list = re.findall(URL_GIT, content)
            for url in git_list:
                if not saved and url not in url_list[GITHUB]:
                    logging.debug(f"Media chattechhaven {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[GITHUB][url] = new_url
                saved = True  # In case we save and it is already saved in the list

            invite_list = re.findall(URL_INVITATIONS_ROCKET, content)
            for url in invite_list:
                if not saved and url not in url_list[ROCKETINVITATIONS]:
                    logging.debug(f"Media chattechhaven {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[ROCKETINVITATIONS][url] = new_url
                saved = True  # In case we save and it is already saved in the list


            heaven_list = re.findall(URL_MEDIA_CHATTHEAVEN, content)
            for url in heaven_list:
                if not saved and url not in url_list[MEDIACHATTHEAVEN]:
                    logging.debug(f"Media chattechhaven {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[MEDIACHATTHEAVEN][url] = new_url
                saved = True  # In case we save and it is already saved in the list


            maybe_list = re.findall(URL_MAYBE_SHORTEN, content)
            for url in maybe_list:
                if not saved and url not in url_list[SHORTEN]:
                    logging.debug(f"Could be shorten {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[SHORTEN][url] = new_url
                saved = True # In case we save and it is already saved in the list


            url_other_list = re.findall(URL_PATTERN, content)
            for url in url_other_list:
                if not saved and url not in url_list[URL_OTHER]:
                    logging.debug(f"Url {url}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[URL_OTHER][url] = new_url
                saved = True # In case we save and it is already saved in the list


            user_list = re.findall(USER_RE, content)

            for user in user_list:
                if not saved and user not in url_list[USERS]:
                    logging.debug(f"User {user}")
                    new_url = {}
                    new_url["SOURCE"] = file
                    new_url["LINE"] = content

                    url_list[USERS][user] = new_url
                saved = True # In case we save and it is already saved in the list


with open(FILE_URLS, "w") as f:
    f.writelines(json.dumps(url_list, indent=4, sort_keys=True))


