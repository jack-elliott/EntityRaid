# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:06:34 2022

@author: Elliott
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def draw_graph(G):#borrowed from online
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    
def symmetrize(A):
        
    return(np.sign((A+np.transpose(A))/2))

def DiagMat(A):
    
    N = len(A)
    D = np.zeros((N,N))
    degreeVec = np.matmul(np.ones(N),A)
    
    for i in range(N):
        D[i][i] = degreeVec[i]
        
    return(D, degreeVec)
    
def LaplacianMat(A,D):
    
    return(D-A)

def FiedlerFind(L,disp):
    
    eigenVal, eigenVec = np.linalg.eig(L)
    

    
    sortedVals = np.sort(eigenVal)   
    vectorIndex = int(np.where(eigenVal == sortedVals[1])[0])
    FielderValue = eigenVal[vectorIndex]
    FiedlerVector = eigenVec[:,vectorIndex]
    
    if disp:
        plt.figure()
        plt.title("eigenvalues, \nFiedler: "+str(FielderValue))
        plt.plot(eigenVal)
        plt.show()
        
        plt.figure()
        plt.title("Fiedler Vector")
        plt.plot(FiedlerVector)
        plt.show()
    
    return(FielderValue,FiedlerVector)
    
def sortedFielder(FiedlerVector):
    
    vec = np.sort(FiedlerVector)
    
    plt.figure()
    plt.title("Sorted Fiedler Vector")
    plt.plot(vec)
    plt.show()
    
    



#let's start by initializing a given adjacency matrix'    
    
#example adjacency matrix
A = [[0,1,1,1,1,0,0,0,0,0],
     [1,0,1,0,1,0,0,0,0,0],
     [1,1,0,1,0,0,0,0,0,1],
     [1,0,1,0,1,0,0,0,0,0],
     [1,1,0,1,0,0,0,0,0,0],
     [0,0,1,0,0,0,1,1,1,0],
     [0,0,0,0,0,1,0,1,0,1],
     [0,0,0,0,0,1,0,0,1,1],
     [0,0,0,0,0,1,0,1,0,0],  
     [0,0,0,0,0,1,0,1,0,0]]

#let's symmetrize A and find the laplacian
A = symmetrize(A)

D, degreeVec = DiagMat(A)

L = LaplacianMat(A,D)

FiedlerValue, FiedlerVector = FiedlerFind(L,disp = 1)

sortedFielder(FiedlerVector)



#Let's plot A
G_A = nx.from_numpy_matrix(A)
draw_graph(G_A)



