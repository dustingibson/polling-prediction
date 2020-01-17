import math, sqlite3
from decimal import Decimal

conn = sqlite3.connect('db/db.bin')
cursor = conn.cursor()

def fillValues():
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
        cursor.execute(updateQuery)
        conn.commit()


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

#print(calcProb(1000,510))
#print(calcProbPF(388, 356))

fillValues()
conn.close()