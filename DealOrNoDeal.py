from random import seed
from random import choice

def numCases():
    print("How many cases do you want in the game? You can only chose numbers such as 9, 14, 20, 27, etc. ")
    while True:
        try:
            caseTotal = int(input())
            if caseTotal > 100:
                print ("Whoa there! Too many cases can override the game. Please choose a smaller number.")
            else:
                deductibleCaseTotal = caseTotal
                for count in range (14):
                    deductibleCaseTotal -= count
                    if deductibleCaseTotal == -1:
                        return caseTotal
                    elif deductibleCaseTotal < -1:
                        print ("Your number cannot successfully compute into this game. Please try again. Remember, you can only choose numbers such as 9, 14, 20, 27, etc. ")
                        break
        except ValueError:
            print ("Please choose numbers only.")
        
def myCase(numCase):
    while True:
        print("Which case would you like to choose as your lucky case? ")
        try:
            luckyCase = int(input())
            if luckyCase < numCase and luckyCase > 0:
                return luckyCase
            print("Im sorry, this case isn't valid as a number in this game. Please choose again. ")
        except ValueError:
            print ("Please choose a number.")


def openCase(caseFigures, myCaseFigure):
    print("Enter the case you wish to open here. If you would like to know which cases are left, enter '?cases'. If you would like to know which dollar figures are left, enter '?money'. ")
    while True:
        caseOpen = input()
        if caseOpen == "?cases":
            possChoices = []
            print ("The possible cases you can open are:", end=" ")
            for count in range(len(caseFigures)):
                if caseFigures[count] != 0:
                    possChoices.append(str(count+1))
            possChoices = ", ".join(possChoices)
            print (possChoices)
        elif caseOpen == "?money":
            possChoices = []
            print ("The possible money figures you can win are:", end=" ")
            for count in caseFigures:
                if count != 0:
                    possChoices.append(count)
            possChoices.append(myCaseFigure)
            possChoices.sort()
            for count in range(len(possChoices)):
                possChoices[count] = str(possChoices[count])
            possChoices = ", ".join(possChoices)
            print (possChoices)
        else:
            try:
                caseOpen = int(caseOpen)
                if caseOpen < 0 or caseOpen > len(caseFigures):
                    print("This number does not qualify for this game. Please reselect.")
                else:
                    if caseFigures[caseOpen-1] != 0:
                        print("$" + str(caseFigures[caseOpen-1]) + " is now out of the question.")
                        return (caseOpen-1)
                    else:
                        print("Sorry, you have already selected that case. Please choose again.")
            except ValueError:
                print("Numbers only.")

def dealOffer(caseFigures, myCaseFigure):
    sumup = sum(caseFigures) + myCaseFigure
    divlength = len(caseFigures)
    for count in caseFigures:
        if count == 0:
            divlength -= 1
    divlength += 1
    avg = sumup / divlength
    avg = int(avg * 100)
    avg *= 0.01
    print ("The banker has offered $" + str(avg) + " for your case. Would you like to accept the offer? (yes or no) ")
    yesno = input().lower()
    if yesno == "yes":
        print ("Congrats! You have won $" + str(avg) + "!")
        print ("The value in your case was $" + str(myCaseFigure) + ".")
        if myCaseFigure > avg:
            print ("You should have kept on playing!")
        else:
            print ("Good job taking a deal right before the high money values plummetted of a cliff!")
        return "Deal"
    print ("You've got guts to keep on playing!")
    return "No deal"

def finalReveal(caseFigures, veryOwn):
    for count in range (1, len(caseFigures)):
        if caseFigures[count] > caseFigures[count-1]:
            caseFigures[0] = caseFigures[count]
            caseFigures[count] = 0
    print ("You have turned down all of your offers. Would you like to go all the way and open your case or switch your case with the last remaining one? Enter '1' for the first choice and '2' for the second choice. ")
    nintendo = input()
    if nintendo == '1':
        input("Drumroll please ... (enter a random letter/number/space) ")
        print("You have won $" + str(veryOwn) + "!")
        if veryOwn < caseFigures[0]:
            print ("You should have switched cases!")
        else:
            print ("Nice job not mediating or switching!")
    else:
        input("Drumroll please ... (enter a random letter/number/space) ")
        print("You have won $" + str(caseFigures[0]) + "!")
        if veryOwn < caseFigures[0]:
            print ("Nice job not mediating or switching!")
        else:
            print ("You should have switched cases or taken the last offer!")

turnCount = 0

print("Welcome to Deal or No Deal!")
caseCount = numCases()
startCase = myCase(caseCount)
allFigures = [0] * caseCount
for count in range (len(allFigures)):
    allFigures[count] = 2 ** count

realAllFigures = [0] * caseCount
x = len(realAllFigures)

seed(1)
for count in range(x):
    temp = choice(allFigures)
    realAllFigures[count] = temp
    allFigures.remove(temp)

MyCasesCase = realAllFigures[startCase-1]
realAllFigures[startCase-1] = 0

caseRound = 0
for count in range (14):
    caseRound += count
    if caseRound == caseCount+1:
        OpenRound = count
        break

while True:
    turnCount += 1
    print("This is round " + str(turnCount) + ".")
    for rounds in range (OpenRound - turnCount + 1):
        print("You have " + str((OpenRound - turnCount + 1) - rounds) + " more cases to open this round.")
        realAllFigures[openCase(realAllFigures, MyCasesCase)] = 0
    dealOrNot = dealOffer(realAllFigures, MyCasesCase)
    if dealOrNot == "Deal":
        print("Game over! Well played.")
        break
    countnum = 0
    for count in range (len(realAllFigures)):
        if realAllFigures[count] != 0:
            countnum += 1
    if countnum == 1:
        finalReveal(realAllFigures, MyCasesCase)
        print("Game over! Well played.")
        break
