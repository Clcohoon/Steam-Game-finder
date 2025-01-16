import json
import steam_connect
import pprint
f = open('gameList.json')
data = json.load(f)
f.close()

data = data["applist"]["apps"]
# print(data)
gameDict = {}
for i in data:
    gameDict[i["appid"]] = i["name"]
# print(len(gameDict))


game_id_list = ['934700', '553850', '1151340', '2519060', '377160', '1658280', '381210', '1174180', '1812450', '1492070']
# game_id_list = gameDict
# endpoint is the idnumber for a game
def gameSort(gameDict):
    gameInfoDict = {}

    for i in game_id_list:
        endpoint = str(i)
        parameters = {}
        response_data = steam_connect.getEndpoint(endpoint, parameters)
        if response_data[endpoint]['success'] == "False":
            pprint.pprint(response_data)
        else:
            try:
                game_tags = response_data[endpoint]['data']['categories']
                game_tag_list = []
                for a in game_tags:
                    game_tag_list.append(a['description'])
                game_genres = response_data[endpoint]['data']['genres']
                for e in game_genres:
                    game_tag_list.append(e['description'])
                # pprint.pprint(game_tag_list)
                if response_data[endpoint]['data']['is_free'] == "true":
                    game_price = 0
                else:

                    game_price = response_data[endpoint]['data']['price_overview']['final_formatted']
                    # print(game_price)

                    if game_price[0] == "C":
                        game_price = game_price[game_price.find("$") + 2:game_price.find(".") + 3]
                        game_price = float(game_price.replace(" ", ""))
                        game_price = game_price * 0.73
                    elif game_price[0] == "$":
                        game_price = game_price[game_price.find("$")+1:game_price.find(".")+3]
                        game_price = float(game_price.replace(" ", ""))
                    elif game_price[0] == "₩":
                        game_price.replace(",", "")
                        game_price = game_price.replace("₩", "")
                        if " " in game_price:
                            game_price = game_price.replace(" ", "")
                        game_price = float(game_price) * 0.00073
                    elif game_price[0] == "₹":
                        game_price.replace(",", "")
                        game_price = game_price.replace("₹", "")
                        if " " in game_price:
                            game_price = game_price.replace(" ", "")
                        game_price = float(game_price) * 0.012
                    elif game_price[0] == "£":
                        if "," in game_price:
                            game_price.replace(",", "")
                        game_price = game_price.replace("£", "")
                        if " " in game_price:
                            game_price = game_price.replace(" ", "")
                        game_price = float(game_price) * 1.25
                    elif game_price[0] == "€":
                        if "," in game_price:
                            game_price.replace(",", "")
                        game_price = game_price.replace("€", "")
                        if " " in game_price:
                            game_price = game_price.replace(" ", "")
                        game_price = float(game_price) * 1.07
                    elif "¥" in game_price:
                        game_price.replace(",", "")
                        game_price = game_price[game_price.find("¥")+1:]
                        if " " in game_price:
                            game_price = game_price.replace(" ", "")
                        game_price = float(game_price) * 0.0064
                    else:
                        print("error, could not grab price in USD")

                info = response_data[endpoint]['data']['short_description']
                game_info = ""
                for o in info:
                    game_info = game_info + o.strip("\n")
                gameInfoDict[gameDict[int(i)]] = {"Price": game_price, "Tag List": game_tag_list, "Game Information": game_info}
            except:
                print("Error grabbing directory")
    # pprint.pprint(gameInfoDict)


    return gameInfoDict

def questionnaire(gameInfoDict):
    print("This program will give you recommendations for games to play on Steam based off of a short questionaire")
    gameOptions = gameInfoDict
    cost = float(input("What is the maximum price you would like to spend on a game? (input in USD) "))
    while cost < 0:
        print("Please input a price that is greater than or equal to 0")
        cost = float(input("What is the maximum price you would like to spend on a game? (input in USD) "))
    games = gameOptions.copy()
    for option, value in gameOptions.items():
        if float(value['Price']) > cost:
            del games[option]
    gameOptions = games.copy()
    controllerSupport = input("Is controller support important to you? (please type in yes or no) ")
    while True:
        if controllerSupport.lower() == "no":
            break
        elif controllerSupport.lower() == "yes":
            for option, value in gameOptions.items():
                if 'Full controller support' not in value['Tag List']:
                    if 'Partial Controller Support' not in value['Tag List']:
                        del games[option]
            break
        else:
            print("please input either yes or no")
            controllerSupport = input("Is controller support important to you? ")
    gameOptions = games.copy()

    remotePlay = input("Is remote play important to you? (please type in yes or no) ")
    while True:
        if remotePlay.lower() == "no":
            break
        elif remotePlay.lower() == "yes":
            for option, value in gameOptions.items():
                if 'Remote Play on Phone' not in value['Tag List']:
                    if 'Remote Play on Tablet' not in value['Tag List']:
                        if 'Remote Play on TV' not in value['Tag List']:
                            del games[option]
            break
        else:
            print("please input either yes or no")
            remotePlay = input("Is remote play important to you? ")
    gameOptions = games.copy()
    waysToPlay = input("Do you prefer to play single-player or multi-player? (please type single or multi) ")
    while True:
        if waysToPlay.lower() == "single":
            for option, value in gameOptions.items():
                if 'Single-player' not in value['Tag List']:
                    del games[option]
            break
        elif waysToPlay.lower() == "multi":
            for option, value in gameOptions.items():
                if 'Multi-player' not in value['Tag List']:
                    if 'Online PvP' not in value['Tag List']:
                        if 'Online Co-op' not in value['Tag List']:
                            del games[option]
            crossPlay = input("Is cross-play important to you? (please input yes or no) ")
            while True:
                if crossPlay.lower() == "no":
                    break
                elif crossPlay.lower() == "yes":
                    for value in gameOptions:
                        if 'Cross-Platform Multiplayer' not in value['Tag List']:
                            del games[option]
                    break
                else:
                    print("please input either yes or no")
                    crossPlay = input("Is cross-play support important to you? ")
            break
        else:
            print("please input either single or multi")
            waysToPlay = input("Do you prefer to play single-player or multi-player? ")
    gameOptions = games.copy()
    print("The last step will be to pick out a few tags relevant to the type of game that you would like to play\nPlease be sparing on how many you choose because this is an early test so the pool of games being used to test with is small")
    tags = {"I": "Indie", "M": "MMO", "AD": "Adventure", "R": "RPG", "SIM": "Simulation", "AC": "Action", "ST": "Strategy", "EA": "Early Access"}
    print(f"Here is the current list of tags to pick from:")
    for tag in tags:
        print(f"To add {tags[tag]}, input {tag}")
    while True:
        tagSelection = input("Please input one of the above tag keys, or input quit to stop selecting: ")
        if tagSelection.upper() in tags:
            for option, value in gameOptions.items():
                if tags[tagSelection.upper()] not in value['Tag List']:
                    del games[option]
        elif tagSelection.lower() == "quit":
            break
        else:
            print("Error, that is not one of the above tag keys")
            tagSelection = input("Please input one of the above tag keys, or input quit to stop selecting: ")
    gameOptions = games.copy()
    if len(gameOptions) == 0:
        print("I'm sorry, our limited test pool of games did not have an option that fit your requests")
    elif len(gameOptions) == 1:
        print("Here is the game that fits your choices")
        pprint.pprint(gameOptions)
    else:
        print("Here are the games that fit your choices")
        pprint.pprint(gameOptions)


gameInfoDict = gameSort(gameDict)
questionnaire(gameInfoDict)


# if price is free then set game price = 0 instead
# age limit
# recommendations
# ideally link game options to store page with https://store.steampowered.com/app/ plus id number
# can go through and create a translator for all currencies
# just need to instead of going through the small list, go through gameList.json and have it filter out all the null requests
# in addition, add all of the proper tags to the list instead of just the ones relevant to the small list