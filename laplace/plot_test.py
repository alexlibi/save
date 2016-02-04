import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


fig1 = plt.figure()
a = fig1.add_subplot(111, projection='3d')
    
# x, y = range(10), range(10)
# X, Y = np.meshgrid(x,y)
# print('X:',X,'Y:',Y)
#a.plot_surface([1,1,1],[1,2,3],[0,0,0],rstride=1, cstride=1, cmap=plt.cm.coolwarm, linewidth=0.1)
    
fig2 = plt.figure()
b = fig2.add_subplot(111, projection='3d')   
b.quiver([0,0][1,1], [0.5,0.5][2,2])
    
    
plt.show()