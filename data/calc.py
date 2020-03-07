import math, sqlite3, requests, time, json, sys
from flask import Flask, escape, request
from decimal import Decimal
from svglib.svglib import svg2rlg

app = Flask(__name__)
baseURL = "http://localhost:3110/insertpoll?state={0}&demVotes={1}&repVotes={2}&demProb={3}&repProb={4}&date={5}&notes={6}"

def callMethod(URL):
    try:
        print("Get " + URL)
        r = requests.post(url = URL) 
        print(r)
    except:
        print("error")

def setValue(votesA, votesB, state):
    try:
        timestamp = int(time.time())
        prob = calcProbPF(votesA, votesB)
        url = baseURL.format(state, str(votesA), str(votesB), str(prob[0]), str(prob[1]), str(timestamp), "test"  )
        callMethod(url)
        return "Success"
    except:
        return "Error"

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

def setPoll(state, sampleSize, demVotes, repVotes):
    if(repVotes > 1 or demVotes > 1):
        return 'Needs to percentage'
    demVotes = int(sampleSize*demVotes)
    repVotes = int(sampleSize*repVotes)
    return setValue(demVotes, repVotes, state)

if(len(sys.argv) != 5):
    print("Usage state sample demvotes repvotes")
else:
    setPoll(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))