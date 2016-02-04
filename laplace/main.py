'''
Created on 17. Jän. 2016

@author: alexander
'''

import copy
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    '''Verschiedene Dateien zur Berechnung. Vorsicht: Zylinder braucht sehr lange und verwendet viel RAM.'''
        
#     f=open('laplace_daten/dach_ko60x60.dat','r')
#     f=open('laplace_daten/loch_ko60x60.dat','r')
#     f=open('laplace_daten/dach_l_ko60x60.dat','r')
    f=open('laplace_daten/pl_ko60x60.dat','r')
#     f=open('laplace_daten/zyl-100x100-20-49-0.dat','r')
#     f=open('laplace_daten/zyl_1040x1040_400_500_0.dat','r')
    
    '''Datei einlesen'''
    data=f.read().strip().split('\n')
    f.close()
   
    for i in range(len(data)):
        data[i]=data[i].strip().split()
    
    '''Original der Daten sichern, damit nach jeder Iteration die Differenz berechnet werden kann.'''
    data_orig=copy.deepcopy(data)
    
    '''* bezeichnen fixes Potential. Umwandlung in float.'''
    for i in range(1,len(data_orig)):
        for j in range(1,len(data_orig[i])):
            if str(data_orig[i][j])[0]!='*':
                data_orig[i][j]=float(data_orig[i][j])
    
    '''r=abs(res); wird verwendet, um Residuen zu berechnen.'''
    r = [[0 for i in range(len(data))]for j in range(len(data[0]))]
    res = copy.deepcopy(r)
    
    SUM1 = 0
    cnt=0
    w=1.7
    
    while 1:
        cnt+=1
        tmp=0
        for i in range(1,len(data)-1):
            for j in range(1,len(data[i])-1):
                if str(data[i][j])[0]=="*":
                    pass          
                else:
                    '''temp ist liste mit U1,U2,U3,U4'''
                    temp=[]
                                        
                    if str(data[i-1][j])[0]=='*': temp.append(float(data[i-1][j][1:]))
                    else:temp.append(float(data[i-1][j]))
                                        
                    if str(data[i][j-1])[0]=='*': temp.append(float(data[i][j-1][1:]))
                    else: temp.append(float(data[i][j-1]))
                        
                    if str(data[i+1][j])[0]=='*': temp.append(float(data[i+1][j][1:]))
                    else: temp.append(float(data[i+1][j]))
                        
                    if str(data[i][j+1])[0]=='*': temp.append(float(data[i][j+1][1:]))
                    else: temp.append(float(data[i][j+1]))
                    
                    res[i][j] = 0.25*(sum(temp)) - float(data[i][j])
                    r[i][j] = abs(res[i][j])
                    
                    ''' Kann auskommentiert werden, wenn ohne Relaxationsmethonde gerechnet werden soll.'''                    
                    data[i][j] = float(data[i][j]) + w * res[i][j]

                    
            tmp+=sum(r[i])
        SUM2 = tmp
#         print('SUM1:',SUM1,'SUM2:',SUM2)
        print(round(abs(SUM2-SUM1),2))
        if abs(SUM2-SUM1) < len(data)**2/100000:
            print('Zahl der Durchlaefe:', cnt)
            break
        SUM1=SUM2
            
    #for i in range(len(data)):
    #    print(data[i])
    
    data_float=copy.deepcopy(data)
    
    for i in range(len(data_float)):
        for j in range(len(data_float[i])):
            if str(data_float[i][j])[0]=='*':
                data_float[i][j]=float(data_float[i][j][1:])
    
#     for i in range(len(data_float)):
#         print(data_float[i])
    vx = [[0 for i in range(len(data_float))]for j in range(len(data_float[0]))]
    vy = copy.deepcopy(vx)
    vxn = copy.deepcopy(vx)
    vyn = copy.deepcopy(vx)
    #print(data_float)
    
    for i in range (1, len(data)-1):
        for j in range(1,len(data[i])-1):
            vx[i][j] = data_float[i-1][j]-data_float[i+1][j]
            vy[i][j] = data_float[i][j-1]-data_float[i][j+1]
            vxn[i][j] = vx[i][j]/np.sqrt(vx[i][j]**2+vy[i][j]**2)
            vyn[i][j] = vy[i][j]/np.sqrt(vx[i][j]**2+vy[i][j]**2)
    
    
    
    x, y = range(len(data_float)),range(len(data_float[0]))
    X, Y = np.meshgrid(x,y)
    
    fig1 = plt.figure()
    a = fig1.add_subplot(111, projection='3d')
    a.plot_surface(Y,X,data_float,rstride=1, cstride=1, cmap=plt.cm.coolwarm, linewidth=0.1)
    
    fig2 = plt.figure()
    plt.quiver(Y, X, vx, vy)
        
    fig3 = plt.figure()
    plt.quiver(Y, X, vxn, vyn)
    
    
    
    plt.show()