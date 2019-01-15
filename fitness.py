import random
vals = ["tendrils","darkrit","lotus"]
decksize = 100
cardmax = 100#remove these into a config file

def choiceSort(i):
    return (i["w"]+1)/(i["c"]+1)

def generateDeck():
    ret = {}
    for i in vals:
        ret[i] = 0
    c = 0
    while c < decksize:
        t = random.choice(vals)
        if ret[t] < cardmax:
            ret[t] += 1
            c += 1
    return ret

def initGamestate():
    ret = {}
    ret["u"] = 0
    ret["b"] = 0
    ret["r"] = 0
    ret["g"] = 0
    ret["mana"] = 0
    ret["storm"] = 0
    ret["life"] = 20
    ret["health"] = 20
    ret["hand"] = 7
    ret["land"] = 1
    ret["grave"] = 0
    ret["riteflame"] = 0
    return ret

def newnode(): #creates a new node in the monte carlo tree
    node = {}
    node["c"] = 0 #count the number of times that a node has been visited
    node["w"] = 0 #count the number of times that the game was won after this node was visited
    node["children"] = []
    return node

def tendrils(deck,gamestate,node):
    if gamestate["mana"] < 4 or gamestate["b"] < 2:
        return 0
    gamestate["storm"] += 1
    gamestate["life"] -= gamestate["storm"] * 2
    if gamestate["life"] < 0:
        return 1
    gamestate["hand"] -= 1
    deck["tendrils"] -= 1
    return sim(deck,gamestate,node)

def darkrit(deck,gamestate,node):
    if gamestate["mana"] < 1 or gamestate["b"] < 1:
        return 0
    gamestate["mana"] += 2
    gamestate["b"] += 2
    gamestate["storm"] += 1
    gamestate["hand"] -= 1
    deck["darkrit"] -= 1
    return sim(deck,gamestate,node)

def lotus(deck,gamestate,node):
    gamestate["storm"] += 1
    gamestate["hand"] -= 1
    gamestate["mana"] += 1
    deck["lotus"] -= 1
    return sim(deck,gamestate,node)

def sim(deck, gamestate, node): #recursive function for a round of monte carlo simulation
    if gamestate["hand"] < 1:
        return 0
    node["c"] += 1
    if not len(node["children"]):
        for i in deck:
            if deck[i]:
                new = newnode()
                new["name"] = i
                node["children"].append(new)
        if not len(node["children"]):
            return 0
    c = 1
    node["children"].sort(key=choiceSort)
    v = random.random() #number to pick a card at random
    c = 1 #keep track of the chance a card hasn't been played yet
    print(deck)
    d = sum(deck.values()) #count of cards in the deck for calculations
    print(deck,d)
    choice = -1
    while v >= 0:
        choice += 1
        notc = 1.0
        for i in range(0,gamestate["hand"]):
            if notc:
                notc *= (d - deck[node["children"][choice]["name"]] - i)
                notc /= (d - i)
        chance = 1 - notc
        chance *= c
        d -= deck[node["children"][choice]["name"]]
        c -= chance
        v -= chance
    chosen = node["children"][choice]
    w = globals()[chosen["name"]](deck,gamestate,chosen)
    node["w"] += w
    return w

def fitness(deck, iters): #calculates fitness for the deck using monte carlo function
    tree = newnode()
    print(deck)
    for i in range(0,iters):
        sim(dict(deck),initGamestate(), tree)
    print("Done")
