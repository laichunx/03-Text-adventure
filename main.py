import sys, logging, os, json
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Game loop functions
def render(room,moves,points):
    ''' Displays the current room, moves, and points '''
    print('\n\nMoves: {moves}'.format(moves=moves))
    print('\n\nYou are in the {name}'.format(name=room['name']))
    print(room['desc'])
    if len(room['inventory']):
        print('You see the following items:')
        for i in room['inventory']:
            print('\t{i}'.format(i=i))

def getInput(verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''

    response = input('\nWhat would you like to do? ').strip().upper().split()
    if (len(response)):
        #assume the first word is the verb
        response[0] = normalizeVerb(response[0],verbs)
    return response


def update(response,room,current,inventory):
    ''' Process the input and update the state of the world '''
    s = list(response)[0]  #We assume the verb is the first thing typed
    print(s)
    if s == "":
        print("\nSorry, I don't understand.")
        return current
    # User can check inventory
    elif s == "INVENTORY":
        print("Inventory: " + showInventory(inventory))
        return current
    # Picking up materials
    elif s == "PICK" and current == "STORAGE":
        keepPicking = True
        while(keepPicking == True):
            if(len(inventory) >= 10):
                print("------Inventory Full------")
                return current
            item = input("What do you want to pick?")
            if(item.upper() == "MEAT"):
                inventory.append("MEAT")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            elif(item.upper() == "VEGGIE" or item.upper() == "VEGESTABLE"):
                inventory.append("VEGGIE")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            elif(item.upper() == "BREAD"):
                inventory.append("BREAD")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            elif(item.upper() == "CHEESE"):
                inventory.append("CHEESE")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            elif(item.upper() == "SALT"):
                inventory.append("SALT")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            elif(item.upper() == "POTATO"):
                inventory.append("POTATO")
                print("Inventory: " + showInventory(inventory))
                keepPicking = pickingCheck()
            else:
                print("We are out of that")
                keepPicking = pickingCheck()
        return current
    # Cooking POTATO
    elif s == "COOK" and current == "FRIES":
        keepCooking = True
        while(keepCooking == True):
            item = input("What do you want to cook?")
            if(item.upper() == "SLICED-POTATO"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("SLICED-POTATO")
                    inventory[ind] = "COOKED-SLICED-POTATO"
                    print("Inventory: " + showInventory(inventory))
                    keepCooking = cookingCheck()
                else:
                    print("You do not have SLICED-POTATO in your inventory")
                    return current
            elif(item.upper() == "POTATO"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("POTATO")
                    inventory[ind] = "COOKED-POTATO"
                    print("Inventory: " + showInventory(inventory))
                    keepCooking = cookingCheck()
                else:
                    print("You do not have POTATO in your inventory")
                    return current  
            else:
                print("You cannot cook this here.")
                keepCooking = cookingCheck()

    # Cooking MEAT
    elif s == "COOK" and current == "BURGER":
        keepCooking = True
        while(keepCooking == True):
            item = input("What do you want to cook?")
            if(item.upper() == "MEAT"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("MEAT")
                    inventory[ind] = "COOKED-MEAT"
                    print("Inventory: " + showInventory(inventory))
                    keepCooking = cookingCheck()
                else:
                    print("You do not have MEAT in your inventory")
                    return current
            else:
                print("You cannot cook " + item +" here.")
                keepCooking = cookingCheck()

    # Cut Potato, Meat
    elif s == "CUT" and current == "BURGER":
        keepCutting = True
        while(keepCutting == True):
            item = input("What do you want to cut?")
            if(item.upper() == "MEAT"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("MEAT")
                    inventory.remove("MEAT")
                    print("You destory the MEAT, we don't serve sliced or diced MEAT!")
                    print("Inventory: " + showInventory(inventory))
                    keepCutting = cuttingCheck()
                else:
                    print("You do not have MEAT in your inventory")
                    return current
            elif(item.upper() == "POTATO"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("POTATO")
                    inventory[ind] = "SLICED-POTATO"
                    print("Inventory: " + showInventory(inventory))
                    keepCutting = cuttingCheck()
                else:
                    print("You do not have POTATO in your inventory")
                    return current
            elif(item.upper() == "COOKED-POTATO"):
                if(isItemInInventory(item, inventory)):
                    ind = inventory.index("COOKED-POTATO")
                    inventory[ind] = "COOKED-SLICED-POTATO"
                    print("Inventory: " + showInventory(inventory))
                    keepCutting = cuttingCheck()
                else:
                    print("You do not have POTATO in your inventory")
                    return current
            else:
                print("You cannot cut " + item +" here.")
                keepCutting = cuttingCheck()

    # Combine stuff
    elif s == "COMBINE" and current == "BURGER":
        item = input("What do you want to COMBINE?")
        if(item.upper() == "BURGER"):
            if(canCombineBurger(inventory)):
                inventory.remove("COOKED-MEAT")
                inventory.remove("CHEESE")
                inventory.remove("VEGGIE")
                inventory.remove("BREAD")
                inventory.remove("BREAD")
                inventory.append("BURGER")
                print("Inventory: " + showInventory(inventory))
                return current
            else:
                print("Fail to COMBINE BURGER")
        elif(item.upper() == "FRIES"):
            if(canCombineFries(inventory)):
                inventory.remove("SALT")
                inventory.remove("COOKED-SLICED-POTATO")
                inventory.append("FRIES")
                print("Inventory: " + showInventory(inventory))
                return current
            else:
                print("Fail to COMBINE FRIES")
                return current
        else:
            print("You can not COMBINE that.")
            return current
    
    # SERVE stuff
    elif s == "SERVE" and current == "COUNTER":
        item = input("What do you want to SERVE?")
        if(item.upper() == "BURGER"):
            if(isItemInInventory(item, inventory)):
                inventory.remove("BURGER")
                return current
            else:
                print("You don't have BURGER")
        elif(item.upper() == "FRIES"):
            if(isItemInInventory(item, inventory)):
                inventory.remove("FRIES")
                return current
            else:
                print("You don't have FRIES")
                return current
        elif(item.upper() == "DRINK"):
            if(isItemInInventory(item, inventory)):
                inventory.remove("DRINK")
                return current
            else:
                print("You don't have DRINK")
                return current
        else:
            print("You can not SERVE that.")
            return current

    elif s == 'EXITS':
        printExits(room)
        return current
    else:
        for e in room['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']
    return current

def canCombineBurger(inventory):
    if("BREAD" in inventory):
        inventory.remove("BREAD")
    else:
        return False
    if("COOKED-MEAT" in inventory and "VEGGIE" in inventory and "CHEESE" in inventory and "BREAD" in inventory):
        inventory.append("BREAD")
        return True
    else:
        inventory.append("BREAD")
        return False

def canCombineFries(inventory):
    if("COOKED-SLICED-POTATO" in inventory and "SALT" in inventory):
        return True
    else:
        return False

def isItemInInventory(item, inventory):
    if(item.upper() in inventory):
        return True
    else:
        return False

def showInventory(inventory):
    return ' '.join(inventory)

def pickingCheck():
    reply = input("Do you want to PICK other materials?")
    if(reply.upper() == "N" or reply.upper == "NO"):
        return 0
    elif(reply.upper() == "Y" or reply.upper == "YES"):
        return 1
    else:
        return 0

def cookingCheck():
    reply = input("Do you want to COOK other materials?")
    if(reply.upper() == "N" or reply.upper == "NO"):
        return 0
    elif(reply.upper() == "Y" or reply.upper == "YES"):
        return 1
    else:
        return 0

def cuttingCheck():
    reply = input("Do you want to CUT other materials?")
    if(reply.upper() == "N" or reply.upper == "NO"):
        return 0
    elif(reply.upper() == "Y" or reply.upper == "YES"):
        return 1
    else:
        return 0

# Helper functions

def printExits(room):
    e = ", ".join(str(x['verb']) for x in room['exits'])
    print('\nYou can go the following directions: {directions}'.format(directions = e))

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def end_game(winning,points,moves):
    if winning:
        print('\n\nYou have won! Congratulations')
        print('\nYou scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))
    else:
        print('\n\nThanks for playing!')
        print('\nYou scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))





def main():

    # Game name, game file, starting location, winning location(s), losing location(s)
    games = [
        (   'My Game',          'myGame.json',    'START',    [],    [])
        ,(   'My Game',          'game.json',    'START',    ['END'],    [])
        ,(  'Zork I',           'zork.json',    'WHOUS',    ['NIRVA'],  [])
        ,(  'A Nightmare',      'dream.json',    'START',   ['AWAKE'],  ['END'])
    ]

    # Ask the player to choose a game
    game = {}
    while not game:
        print('\n\nWhich game would you like to play?\n')
        for i,g in enumerate(games):
            print("{i}. {name}".format(i=i+1, name=g[0]))
        try:
            choice = int(input("\nPlease select an option: "))
            game = games[choice-1]
        except:
            continue
            
    name,gameFile,current,win,lose = game



    with open(gameFile) as json_file:
        game = json.load(json_file)

    moves = 0
    points = 0
    inventory = []

    print("\n\n\n\nWelcome to {name}!\n\n".format(name=name))
    while True:
        render(game['rooms'][current],moves,points)

        response = getInput(game['verbs'])

        if response[0] == 'QUIT':
            end_game(False,points,moves)
            break

        current = update(response,game['rooms'][current],current,inventory)
        moves += 1

        if current in win:
            end_game(True,points,moves)
            break
        if current in lose:
            end_game(False,points,moves)
            break


        
if __name__ == '__main__':
	main()