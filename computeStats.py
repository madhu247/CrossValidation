from math import sqrt
from matplotlib import pyplot as plt
import json
from scipy.interpolate import spline
import numpy as np

def standard_deviation(lst, population=True):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)

    if population is True:
        variance = ssd / num_items
    else:
        variance = ssd / (num_items - 1)
    sd = sqrt(variance)
    return sd, mean

def ZStat(sdLoocv, sdBS, meanLoocv, meanBS, numOfIterations=30):
    zNumerator =  abs(meanLoocv - meanBS)
    zDenomenator = sqrt((sdLoocv ** 2 + sdBS ** 2)/numOfIterations)
    z = zNumerator / zDenomenator
    return z

def variance(lst, mean):
    v = []
    for i in lst:
        v.append((i - mean)**2)
    return v


logFile = raw_input("\n\n\tEnter Name of file : ")
d= []
fp = open('Logs/'+logFile, 'r')
for line in fp:
    d.append(json.loads(line))


BSErrorRate = [item['ErrorRate'] for item in d if item['method'] == 'Bootstrap']
LOOCVErrorRate = [item['ErrorRate'] for item in d if item['method'] == 'LOOCV']
[s1, m1] = standard_deviation(BSErrorRate, population=False)
[s2, m2] = standard_deviation(LOOCVErrorRate, population=False)


print "\n #####################################################"
print "\n\t     Z Statistics     "
score = ZStat(s1, s2, m1, m2, 30)
print "\tZ Score : ",score
if score > 1.96:
    print "\n\tLevel of significance is 5%"
    print "\n\tOne of the two cross validation method\n\tworks better than the other"
else:
    print "\n\tThere is no significant difference \n\tbetween two cross validation techniques"
print "\n #####################################################"

plt.figure(1)
plt.subplot(211)
# plt.xlabel('Number of iterations')
plt.ylabel('Error Rate')
plt.title('Bootstrap Vs LOOCV')
x_smooth = np.linspace(1, 30, 200)
bs_smooth = spline(range(1, 31), BSErrorRate, x_smooth)
loo_smooth = spline(range(1, 31), LOOCVErrorRate, x_smooth)
plt.plot(x_smooth, bs_smooth, color = '#F60946', ls = '-', label = 'BS')
plt.plot(x_smooth, loo_smooth, color = '#0926F6', ls = '-', label = 'LOOCV')
plt.plot(range(1,31), [m1]*30, color = '#A7A3A2', linewidth=2, ls='-', label = 'mean')
plt.plot(range(1,31), [m2]*30, color = '#A7A3A2', linewidth=2, ls='-')
plt.legend(loc = 'lower left', prop={'size': 10})

plt.subplot(212)
plt.xlabel('Number of iterations')
plt.ylabel('standard deviation')
plt.plot(range(1,31), variance(BSErrorRate, m1), marker='s', color = '#F60946', ls = '--', label = 'BS')
plt.plot(range(1,31), variance(LOOCVErrorRate, m2),marker='s', color = '#0926F6', ls = '--', label = 'LOOCV')
plt.legend(loc = 'upper left', prop={'size': 10})
plt.show()
