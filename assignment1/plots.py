import matplotlib.pyplot as plt
import math 




exhaustive = [2**(x)-1 for x in range(2,45+1)]
greedy_sparse_points = {x:x-1 for x in range(3,46+1)}

greedy_sparse_points_1more_edge = {x:x for x in range(3,45+1)}

greedy_sparse = [sum([math.comb(y,z) for z in range(1,math.floor(x/2)+1)]) for x,y in greedy_sparse_points.items()]

greedy_sparse_plus_1 = [sum([math.comb(y,z) for z in range(1,math.floor(x/2)+1)]) for x,y in greedy_sparse_points_1more_edge.items()]

greedy_complete_points = {x:int(x*(x-1)/2) for x in range(3,10+1)}

greedy_complete = [sum([math.comb(y,z) for z in range(1,math.floor(x/2)+1)]) for x,y in greedy_complete_points.items()]


plt.plot(greedy_sparse_points.values(),exhaustive,'x',color="black",label="Exhaustive")
plt.plot(greedy_sparse_points.values(),greedy_sparse,'--',color="red",label="Greedy Worst Case, N-1 Edges")
plt.plot(greedy_sparse_points_1more_edge.values(),greedy_sparse_plus_1,'o',color="green",label="Greedy Worst Case, N Edges")
plt.plot(greedy_complete_points.values(),greedy_complete,'x',color="blue",label="Greedy Worst Case, Complete")
plt.legend()
plt.xlabel("Edges")
plt.ylabel("Solutions")
plt.title("Solutions/Edges")
plt.show()

#THIS IS WORTHLESS DUE TO ALL THE OTHER UNDERLYING STUFF I'D HAVE TO TALK ABOUT, WILL STILL COMMIT FOR REUSE PURPOSES