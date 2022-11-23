# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:06:34 2022

@author: Elliott
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 
 



#let's start by initializing a given adjacency matrix'    
    

edgeList = [[0,2],
            [0,1],
            [2,3],
            [2,4],
            [3,1],
            [3,2],
            [4,1],
            [6,1],
            [6,3],
            [9,5],
            [4,3],
            [7,8],
            [9,8],
            [4,5],
            [7,5],
            [5,8],
            [12,13],
            [13,14],
            [12,14],
            [9,10],
            [10,11],
            [10,13],
            [11,14]
            ]



"""here's where we'll wrap everything"""
def main(edgeList):
    
    #this allows the user to decide which of the partitioning methods to implement
    #as of writing, only the bipartition will be implemented 
    bipartition = 1
    kway = 0
    
    #Build the adjacency from the edge list
    A = edgeToAdjacency(edgeList,nodeCount = "Auto")
    
    #run the spectral partitioning method
    Cluster1,Cluster2 = spectralPartition(A)
                       
# =============================================================================
#     edge1,edge2 = ClusterSeparation(Cluster1,Cluster2,edgeList)  
# =============================================================================
        
    
#Wrapping the spectral partitioning method   
def spectralPartition(A):
            
    #symmetrize the adjacency matrix favoring adding ties
    A = symmetrize(A)
    
    #find the Laplacian matrix
    D, degreeVec = DegMat(A)
    L = LaplacianMat(A,D)

    #identify the fiedler value and matrix. If desired, plot the eigenvalues of L and the Fiedler Vector
    FiedlerValue, FiedlerVector = FiedlerFind(L,disp = 0)
    
    #sort the fiedler vector in ascending order, display if desired
    sortedFiedler = sortFiedler(FiedlerVector,disp = 1)
    
    #split the adjacency matrix according to the largest spectral gap in the fiedler vector
    Cluster1,Cluster2 = FiedlerGap(sortedFiedler)
    
    #Return the node indices of the two clusters
    return(Cluster1,Cluster2)
        
# =============================================================================
# def kWayKFind(L):
#     
#     eigenVal, eigenVec = np.linalg.eig(L)
# 
#     sortedVals = np.flip(np.sort(eigenVal))  
#     plt.figure()
#     plt.plot(sortedVals)
#     plt.show()
#     gaps = []
#     
#     for i in range(len(sortedVals)-1):
#         gaps.append(sortedVals[i] - sortedVals[i+1])
#     
#     maxGapIter = int(np.where(gaps == np.max(gaps))[0])
# 
#     return(maxGapIter)
#     
# =============================================================================
    
#separate two clusters'edge lists into two edge lists
def ClusterSeparation(Cluster1,Cluster2,edgeList):
     
    edge1 = []
    edge2 = []
    for i in range(len(edgeList)):
        if edgeList[i][0] in Cluster1:
            if edgeList[i][1] in Cluster1:
                edge1.append(edgeList[i])
        elif edgeList[i][1] in Cluster2:
            edge2.append(edgeList[i])
                
    return(edge1,edge2)

def FiedlerGap(sortedFiedler):
    
    print("Applying maximum Fiedler gap bipartite separation")
    gaps = []
    
    for i in range(len(sortedFiedler)-1):
        gaps.append(sortedFiedler[i+1][1] - sortedFiedler[i][1])
    
    maxGapIter = int(np.where(gaps == np.max(gaps))[0])
    print("\tmax eigengap: " +str(np.max(gaps))+"\n\tbetween indices: "+str(sortedFiedler[maxGapIter][0])+" and "+str(sortedFiedler[maxGapIter+1][0]))

    Cluster1 = sortedFiedler[:maxGapIter+1,0]
    Cluster2 = sortedFiedler[maxGapIter+1:,0]
    
    print("Clusters: ")
    
    print("\t"+str(Cluster1))
    print("\t"+str(Cluster2))
    
    return(Cluster1,Cluster2)
    
    
def draw_graph(A):#borrowed from online
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    plt.show()
    
def symmetrize(A):
        
    return(np.sign((A+np.transpose(A))/2))

def DegMat(A):
    
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
    
def sortFiedler(FiedlerVector,disp):
    
    N = len(FiedlerVector)
    indices = np.linspace(0,N,N+1)
    
    aggregate = []
    for i in range(N):
        aggregate.append([int(indices[i]),FiedlerVector[i]])
    
    aggregate = np.asarray(aggregate)
    vec = aggregate[aggregate[:,1].argsort()]
    
    if disp:
        
        plt.figure()
        plt.title("Sorted Fiedler Vector")
        plt.plot(vec[:,1])
        plt.show()
        
    return(vec)
    
def edgeToAdjacency(edgeList,nodeCount = "Auto"):
    
    #find the necessary size of the adjacency matrix, 
    #NOTE if isolates are not within the max of the edge list, will be left out
    if nodeCount == "Auto":        
        N = np.amax(edgeList)+1

    else: 
        N = nodeCount
        
    #initialize the NxN adjacency Matrix A
    A = np.zeros((N,N))

    #add the edges to A
    for i in range(len(edgeList)):
        A[edgeList[i][0]][edgeList[i][1]] = 1
    
    draw_graph(A)
        
    return(np.asarray(A))

main(edgeList)





