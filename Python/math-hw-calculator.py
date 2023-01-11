# - Was too lazy to do my math hw so i made a calculator for it

# - Math funcs
def getMidpoint(pt1: list, pt2: list):
    midpoint = []
    for i in range(2):
        midpoint.append((pt1[i] + pt2[i])/2)
    return midpoint

def getEndpoint(pt1: list, midpoint: list):
    pt2 = []
    for i in range(2):
        length = pt1[i] - midpoint[i]
        newAxis = midpoint[i] - length
        pt2.append(newAxis)
    return pt2

def getDistance(pt1: list, midpoint: list):
    dist = []
    for i in range(2):
        dist.append(midpoint[i] - pt1[i])
    return dist

# - Input demands
def demandText(message: str, verifyList: list):
    print(message)
    userInput = input().lower()

    inputVerified = False
    for content in verifyList:
        if userInput == content:
            inputVerified = True
            break
    
    if not inputVerified:
        return demandText(message, verifyList)
    return userInput

def demandCord(message: str):
    print(message)
    userInput = input().split(",")

    if len(userInput) != 2:
        return demandCord(message)
    else:
        for i in range(2):
            try:
                float(userInput[i])
            except:
                return demandCord(message)
            else:
                userInput[i] = float(userInput[i])
        return userInput

# - Processing & Output
while True:
    userInput = demandText("What do you want to get?\na) Midpoint\tb) Endpoint", ["a", "b"])
    if userInput == "a":
        pt1 = demandCord("What's pt1?:")
        pt2 = demandCord("What's pt2?:")
        midpoint = getMidpoint(pt1, pt2)
        print("The midpoint is:", midpoint)

        decision = demandText("Would you like to get the distance between pt1 and midpoint? (y/n)", ["y", "n"])
        if decision == "y":
            dist = getDistance(pt1, midpoint)
            print("The distance is:", dist)
    else:
        pt1 = demandCord("What's pt1?:")
        midpoint = demandCord("What is the midpoint?:")
        pt2 = getEndpoint(pt1, midpoint)
        print("The missing endpoint is:", pt2)

    repeatLoop = demandText("Would you like to use this program again? (y/n)", ["y", "n"])
    if repeatLoop == "n":
        print("\nProgram exited.")
        break
