
import pprint
import urllib
import requests
import json

def getEndpoint(endpoint, parameters):
    # https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=440&count=3
    # https://store.steampowered.com / api / appdetails?appids = 440
    #baseUrl = f"https://api.steampowered.com/{endpoint}/"
    baseUrl = f"https://store.steampowered.com/api/appdetails?appids={endpoint}"
    apiKey = "D017957DE37E2848D850C6596787DC18"
    headers = {}
    payload = {}

    print("Getting Endpoint: " + baseUrl + "?" + urllib.parse.urlencode(parameters))
    response = requests.request("GET", baseUrl, headers=headers, data=payload, params=parameters)
    #print(response.text)
    return response.json()

#Steam web api documentation is here: https://partner.steamgames.com/doc/webapi
# This code pulls down news for a specific steam app. In this case, app 440 (Team Fortress 2)
# interface = "ISteamPublishedItemSearch"
# method = "ResultSetSummary"
# version = "v1"
# endpoint = f"{interface}/{method}/{version}"
#

# # This endpoint pulls down a list of all steam apps...
# interface = "ISteamApps"
# method = "GetAppList"
# version = "v2"
# endpoint = f"{interface}/{method}/{version}"
# parameters = {
#     # No parameters for this endpoint
# }
# response_data = getEndpoint(endpoint, parameters)
# pprint.pprint(response_data)
#
# with open("gameList.json", "w") as outfile:
#     json.dump(response_data, outfile)


# # This endpoint requires authentication so you need a web api key and a steam id for the desired user...
# interface = "IPlayerService"
# method = "GetRecentlyPlayedGames"
# version = "v1"
# endpoint = f"{interface}/{method}/{version}"
# parameters = {
#     'key': 'D017957DE37E2848D850C6596787DC18',
#     'steamid': '76561198159259598'
# }
#
# response_data = getEndpoint(endpoint, parameters)
# pprint.pprint(response_data)
