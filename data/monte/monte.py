import sys,os,random, time
import statistics
 
 
all_probs2 = [
    { "weight" : 10, "prob" : 0.75 },
    { "weight" : 30, "prob" : 0.65 },
    { "weight" : 20, "prob" : 0.1 }
]
 
all_probs3 = [
    { "weight" : 10, "prob" : 0.7 },
    { "weight" : 30, "prob" : 0.4 },
    { "weight" : 40, "prob" : 0.6 },
    { "weight" : 20, "prob" : 0.2}
]
 
all_probs = [
    { "weight" : 1, "prob" : 0.95 },
    { "weight" : 2, "prob" : 0.90 },
    { "weight" : 3, "prob" : 0.85 },
    { "weight" : 4, "prob" : 0.80 },
    { "weight" : 5, "prob" : 0.75 },
    { "weight" : 6, "prob" : 0.70 },
    { "weight" : 7, "prob" : 0.65 },
    { "weight" : 8, "prob" : 0.60 },
    { "weight" : 9, "prob" : 0.55 },
    { "weight" : 10, "prob" : 0.50 },
    { "weight" : 11, "prob" : 0.45 },
    { "weight" : 12, "prob" : 0.40 },
    { "weight" : 13, "prob" : 0.35 },
    { "weight" : 14, "prob" : 0.30 },
    { "weight" : 15, "prob" : 0.25 },
    { "weight" : 16, "prob" : 0.20 },
    { "weight" : 17, "prob" : 0.15 },
    { "weight" : 18, "prob" : 0.10 },
    { "weight" : 19, "prob" : 0.05 },
]
 
def calcWeight(probStr, allProbs):
    sumWeight = 0
    cnt = 0
    for probChar in probStr:
        w = allProbs[cnt]["weight"]
        sumWeight +=  allProbs[cnt]["weight"] if probChar == '1' else 0
        cnt += 1
    return sumWeight
 
def probDraw(pos,allProbs):
    probInt = allProbs[pos]["prob"]*100
    res = random.randint(1,100)
    if( res <= probInt ):
        return True
    else:
        return False
 
def testProb():
    cnt = 0
    for i in range(0,100):
        if(probDraw(1, all_probs)):
            cnt += 1
    return cnt
 
def runMonteTest(allProbs):
    binStr = ""
    for i in range(0, len(allProbs)):
        test = probDraw(i,allProbs)
        binStr += '1' if test else '0'
    return binStr
 
def getWeight(binStr,allProbs):
    weight = 0
    for i in range(0, len(allProbs)):
        if(binStr[i] == '1'):
            weight += allProbs[i]["weight"]
    return weight
 
def runFullMonte(iter, allProbs):
    allWeights = []
    for i in range(0, iter):
        binStr = runMonteTest(allProbs)
        allWeights.append(getWeight(binStr,allProbs))
    allWeights.sort()
    return allWeights
 
def percGTE(targetWeight, allWeights):
    for i in range(0,len(allWeights)):
        if(allWeights[i] >=  targetWeight):
            return (len(allWeights) - i) / len(allWeights)
    return 0
 
def percE(targetWeight, allWeights):
    cnt = 0
    for i in range(0,len(allWeights)):
        if(allWeights[i] ==  targetWeight):
            cnt += 1
    return cnt / len(allWeights)
 
def maj(allProbs):
    sumWeight = 0
    for i in range(0, len(allProbs)):
        sumWeight += allProbs[i]["weight"]
    if sumWeight % 2 == 0:
        return sumWeight/2 + 1
    else:
        return sumWeight/2
 
def calcEV(allProbs):
    sumWeight = 0
    for i in range(0, len(allProbs)):
        sumWeight += allProbs[i]["weight"]*allProbs[i]["prob"]
    return sumWeight
 
#print(maj(all_probs2))
#print(calcEV(all_probs2))
start_time = time.time()
allWeights = runFullMonte(10000000,all_probs3)
elapsed_time = time.time() - start_time
print(elapsed_time)
#print(percGTE(maj(all_probs2), allWeights))