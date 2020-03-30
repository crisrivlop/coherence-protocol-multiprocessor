import numpy as np
import matplotlib.pyplot as plt
import math

def makePredictionWithExponentialModel(x,a,b):
  toret = []
  for i in x:
    toret.append(a * math.pow(i,b))
  return toret
  #return a*math.pow(x,b)


cases = [1,5,9,9,13,22,23,26,27,35,41,50,69,89,113,117,134,157,177,203,231,263,295,314]
day = range(len(cases))
days = []
for i in day:
     days.append(i+6)
 
daypredict = range(35)
dayspredict = []
for i in daypredict:
     dayspredict.append(i+6) 
 
plt.style.use('seaborn-whitegrid')

y = makePredictionWithExponentialModel(dayspredict,0.008076680,3.149611241)

plt.plot(dayspredict, y);

plt.plot(days, cases,"r");
for i in range(len(y)):
  plt.annotate(str(int(y[i])),xy=(dayspredict[i],y[i]))
plt.show()


