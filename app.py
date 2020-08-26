from flask import Flask, render_template, request, redirect, url_for, session, after_this_request, Response
from random import seed, choice
webApp = Flask(__name__)
webApp.secret_key = "dsFJKhljfhbLJDFBljbfjkbSJKBfjkbJK"

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T', 'Q'][magnitude])

@webApp.route('/')
def index():
    return redirect(url_for("home"))


@webApp.route('/home')
def home():
    return render_template("home.site.html")


@webApp.route('/numCases', methods=['POST', 'GET'])
def numCases():
    choices = [11, 16, 22, 29, 37, 46, 56, 67, 79]
    if request.method == 'GET':
        return render_template("numCases.site.html", choices=choices)
    elif request.method == "POST":
        howMany = request.form['howMany']
        howMany = int(howMany)
        deductibleCaseTotal = howMany
        for count in range(14):
            deductibleCaseTotal -= count
            if deductibleCaseTotal == 1:
                session['numCases'] = howMany
                session['roundsPerTurn'] = count
                session['currentTurn'] = 0
                session['currentRound'] = 0
                return redirect(url_for('myCase'))
        return render_template("numCases.site.html", choices=choices)


@webApp.route('/myCase', methods=['POST', 'GET'])
def myCase():
    if request.method == 'GET':
        numCases = session['numCases']
        return render_template("myCase.site.html", rangeNumCases=range(numCases))
    elif request.method == 'POST':
        whichLuckyCase = request.form['whichLuckyCase']
        whichLuckyCase = int(whichLuckyCase)
        session["myCase"] = whichLuckyCase-1
        return redirect(url_for('openCase'))


@webApp.route('/openCase', methods=['POST', 'GET'])
def openCase():
    @after_this_request
    def disableCache(response):
        response.cache_control.no_cache = True
        return response

    if request.method == 'GET':
        caseCount = session['numCases']
        currentRound = session['currentRound']
        myCase = session['myCase']
        if currentRound == 0:
            currentTurn = session['currentTurn']
            currentTurn += 1
            session['currentTurn'] = currentTurn
            if currentTurn == 1:
                allFigures = [0] * caseCount
                allFigures[0] = 1
                fivesOrTens = 5
                tensCount = 0
                increase = 0
                fiveDiv = 1
                for count in range(1, len(allFigures)):
                    strCount = str(allFigures[count-1])
                    if strCount[0] == '5':
                        if fiveDiv != 1:
                            increase = int(allFigures[count-1]/2)
                        fiveDiv = fiveDiv % 3
                        fiveDiv += 1
                    if strCount[0] == '1':
                        if fivesOrTens == 5:
                            allFigures[count] = int(strCount) * 5
                            fivesOrTens = 25
                            increase = 5 * (10 ** tensCount)
                        elif fivesOrTens == 25:
                            allFigures[count] = fivesOrTens * \
                                (10 ** (tensCount-1))
                            increase = allFigures[count]
                            fivesOrTens = 10
                        elif fivesOrTens == 10:
                            allFigures[count] = (10 ** tensCount) * 2
                            increase = allFigures[count-1]
                            fivesOrTens = 5
                        tensCount += 1
                    else:
                        allFigures[count] = int(strCount) + increase

                realAllFigures = [0] * caseCount
                x = len(realAllFigures)

                seed(1)
                for count in range(x):
                    temp = choice(allFigures)
                    realAllFigures[count] = temp
                    allFigures.remove(temp)

                session['valueCaseRemoved'] = ""
                session['moneyInMyCase'] = realAllFigures[myCase]

                realAllFigures[myCase] = 0
                allFigures = realAllFigures[:]
                for count in range (len(allFigures)):
                    allFigures[count] = human_format(allFigures[count])
                allFigures[myCase] = '?'

                session['allFigures'] = allFigures

                session["moneyCases"] = realAllFigures

                OGallFigures = realAllFigures[:]
                OGallFigures.append(session['moneyInMyCase'])
                OGallFigures.sort()
                OGallFigures.pop(0)
                session['OG'] = OGallFigures

        realAllFigures = session["moneyCases"]
        OGallFigures = session['OG']

        valueCaseRemoved = ""

        if 'valueCaseRemoved' in session and session['valueCaseRemoved'] != session['moneyInMyCase']:
            valueCaseRemoved = session['valueCaseRemoved']

        casesLeftToOpen = session['roundsPerTurn'] - session['currentRound']
        oneHalf = OGallFigures[:int(len(OGallFigures)/2)]
        twoHalf = OGallFigures[int(len(OGallFigures)/2):]
        for count in range(len(oneHalf)):
            if oneHalf[count] != 0:
                oneHalf[count] = human_format(oneHalf[count])
        for count in range(len(twoHalf)):
            if twoHalf[count] != 0:
                twoHalf[count] = human_format(twoHalf[count])
        if valueCaseRemoved != "":
            valueCaseRemoved = human_format(valueCaseRemoved)

        return render_template("openCase.site.html", realAllFigures=realAllFigures, OGallFigures=OGallFigures, valueCaseRemoved=valueCaseRemoved, casesLeftToOpen=casesLeftToOpen, oneHalf=oneHalf, twoHalf=twoHalf, allFigures = session['allFigures'])

    elif request.method == 'POST':
        caseOpen = request.form['caseIndex']
        caseFigures = session['moneyCases']
        currentRound = session['currentRound']
        roundsPerTurn = session['roundsPerTurn']
        currentRound += 1
        caseOpen = int(caseOpen) - 1
        session['valueCaseRemoved'] = caseFigures[caseOpen]
        caseFigures[caseOpen] = 0
        OGallFigures = session['OG']
        x = OGallFigures.index(session['valueCaseRemoved'])
        OGallFigures[x] = 0
        session['OG'] = OGallFigures

        session['moneyCases'] = caseFigures

        @after_this_request
        def storeSessionItems(response):
            session['currentRound'] = currentRound
            session['roundsPerTurn'] = roundsPerTurn
            return response

        if roundsPerTurn == currentRound:
            currentRound = 0
            roundsPerTurn -= 1
            return redirect(url_for('deal'))

        return redirect(url_for('openCase'))


def countCasesLeft(caseFigures):
    casesLeft = 0
    for count in caseFigures:
        if count != 0:
            casesLeft += 1
    return casesLeft


@webApp.route('/deal', methods=['POST', 'GET'])
def deal():
    if request.method == 'GET':
        caseFigures = session['moneyCases']
        myCaseFigure = session['moneyInMyCase']
        sumup = sum(caseFigures) + myCaseFigure
        divlength = len(caseFigures)
        for count in caseFigures:
            if count == 0:
                divlength -= 1
        divlength += 1
        avg = sumup / divlength
        avg = int(avg * 100)
        avg *= 0.01
        session['avg'] = avg
        avg = '{:,.0f}'.format(avg)
        if countCasesLeft(caseFigures) == 1:
            finalOffer = True
        else:
            finalOffer = False
        return render_template('deal.site.html', theOffer=avg, finalOffer=finalOffer)
    elif request.method == 'POST':
        choice = request.form['choice']
        if choice == 'Deal':
            session['choice'] = 'Deal'
            return redirect(url_for('finalReveal'))
        else:
            caseFigures = session['moneyCases']
            if countCasesLeft(caseFigures) == 1:
                return redirect(url_for('switch'))
            return redirect(url_for('openCase'))


def findFinalCase():
    moneyCases = session['moneyCases']
    for ind, val in enumerate(moneyCases):
        if val != 0:
            return ind, val


@webApp.route('/switch', methods=['POST', 'GET'])
def switch():
    if request.method == "GET":
        return render_template('switch.site.html')
    elif request.method == "POST":
        choice = request.form['choice']
        if choice == 'Keep':
            session['choice'] = 'Keep'
            return redirect(url_for('finalReveal'))
        else:
            session['choice'] = 'Switch'
            ind, val = findFinalCase()
            moneyCases = session['moneyCases']
            moneyCases[ind] = session['moneyInMyCase']
            session['moneyInMyCase'] = val
            session['moneyCases'] = moneyCases

            return redirect(url_for('finalReveal'))


@webApp.route('/finalReveal')
def finalReveal():
    ind, val = findFinalCase()
    if session['choice'] == 'Deal':
        theCase = session['avg']
    else:
        theCase = session['moneyInMyCase']
    printTheCase = '{:,.0f}'.format(theCase)
    printVal = human_format(val)
    printInCase = human_format(session['moneyInMyCase'])
    return render_template('finalReveal.site.html', printTheCase=printTheCase, printOtherCase=printVal, theCase=theCase, otherCase=val, choice=session['choice'], inCase=session['moneyInMyCase'], printInCase=printInCase)

def app():
    return webApp
