import math, sqlite3
from flask import Flask, escape, request
from decimal import Decimal
import time, json

app = Flask(__name__)

def fillValues():
    try:
        with sqlite3.connect("db/db.bin") as conn:
            timestamp = int(time.time())
            cursor = conn.cursor()
            query = "SELECT MAX(DATE),ID,STATE,VOTES_A,VOTES_B FROM POLLS WHERE PROB_A IS NULL OR PROB_B IS NULL GROUP BY STATE"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                id = row[1]
                state = row[2]
                votesA = row[3]
                votesB = row[4]
                prob = calcProbPF(votesA, votesB)
                #updateQuery = "UPDATE POLLS SET PROB_A=" + str(format(prob[0], '.5g')) + " PROB_B=" + str(format(prob[1], '.5g')) + " WHERE ID=" + str(id)
                updateQuery = "UPDATE POLLS SET PROB_A=" + str(Decimal(prob[0])) + ", PROB_B=" + str(Decimal(prob[1])) + " WHERE ID=" + str(id)
                stateUpdateQuery = "UPDATE STATES SET PROB_A=" + str(Decimal(prob[0])) + ", PROB_B=" + str(Decimal(prob[1])) + ", LAST_UPDATE=" + str(timestamp) + " WHERE NAME='" + str(state) + "'"
                print(stateUpdateQuery)
                cursor.execute(updateQuery)
                conn.commit()
                cursor.execute(stateUpdateQuery)
                conn.commit()
            return "Success"
    except:
        return "Error"
        

def setValue(votesA, votesB, state):
    try:
        with sqlite3.connect("db/db.bin") as conn:
            cursor = conn.cursor()
            timestamp = int(time.time())
            query = "INSERT INTO POLLS (VOTES_A, VOTES_B, STATE, DATE) VALUES (" + str(votesA) + "," + str(votesB) + ",'" + state +"'," + str(timestamp) + ")"
            cursor.execute(query)
            conn.commit()
        fillValues()
        return "Success"
    except:
        return "Error"

def getAllProb():
    with sqlite3.connect("db/db.bin") as conn:
        cursor = conn.cursor()
        query = "SELECT MAX(DATE),STATE,PROB_A,PROB_B FROM POLLS WHERE PROB_A IS NOT NULL OR PROB_B IS NOT NULL GROUP BY STATE"
        cursor.execute(query)
        data = cursor.fetchall()
        jsonData = []
        for row in data:
            allData = {}
            print(row)
            allData['state'] = row[1]
            allData['probA'] = row[2]
            allData['probB'] = row[3]
            jsonData.append(allData)
        return json.dumps(jsonData)

def getPredictions():
     with sqlite3.connect("db/db.bin") as conn:
        cursor = conn.cursor()
        query = "SELECT MAX(DATE),PROB_A,PROB_B FROM POLLS WHERE PROB_A IS NOT NULL OR PROB_B IS NOT NULL GROUP BY STATE"
        cursor.execute(query)
        data = cursor.fetchall()
        jsonData = []
        for row in data:
            allData = {}
            print(row)
            allData['state'] = row[1]
            allData['probA'] = row[2]
            allData['probB'] = row[3]
            jsonData.append(allData)
        return json.dumps(jsonData)

def getStates():
     with sqlite3.connect("db/db.bin") as conn:
        cursor = conn.cursor()
        query = "SELECT NAME, POINTS, PROB_A, PROB_B FROM STATE"
        cursor.execute(query)
        data = cursor.fetchall()
        allData = {}
        for row in data:
            allData = {}
        return allData 

def nCr(n,r):
    f = math.factorial
    return Decimal(f(n) // f(r) // f(n-r))

def adjustPrecision(num):
    if num >= 0.99999:
        num = 1
    if num <= 0.00001:
        num = 0
    return num

def calcProb(N, k, tie=False):
    p = Decimal(k / N)
    print(p)
    probWin = 0
    probTie = 0
    probLoss = 0
    for i in range(0, N + 1):
        s = i
        f = N-i 
        curProb = nCr(N, i)*Decimal((p**s))*Decimal(((1-p)**(f)))
        if s > f:
            probWin += curProb
        elif s < f:
            probLoss += curProb
        elif s == f:
            probTie += curProb
    if tie:
         [probWin, probTie, probLoss]
    else:
        print([probWin, probTie, probLoss])
        probWin = adjustPrecision((probWin) / (probWin + probLoss))
        probLoss = adjustPrecision((probLoss) / (probWin + probLoss))
        return [probWin, probLoss]

def calcProbPF(s, f, tie=False):
    return calcProb(s + f, s, tie)

@app.route('/getAllProb', methods=['GET', 'POST'])
def getAllProb():
    print(request.args.get('test'))
    return getAllProb()

@app.route('/sendPoll', methods=['POST'])
def setPoll():
    demVotes = Decimal(request.args.get('demVotes'))
    repVotes = Decimal(request.args.get('repVotes'))
    sampleSize = int(request.args.get('sampleSize'))
    state = request.args.get('state')

    if(repVotes > 1 or demVotes > 1):
        return 'Needs to percentage'

    demVotes = int(sampleSize*demVotes)
    repVotes = int(sampleSize*repVotes)

    return setValue(demVotes, repVotes, state)

#fillValues()
print(calcProbPF(5000,5001))

app.run()