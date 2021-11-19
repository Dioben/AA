from matplotlib import pyplot
import random
values = [1,3,13,63,321,1683,8989,48639]


pyplot.plot(values)
pyplot.xticks(range(len(values)),values)
pyplot.show()