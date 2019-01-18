import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
import sklearn
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster import hierarchy as hier
from scipy.spatial import distance as ssd
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import cut_tree
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import ward, dendrogram,complete,average
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pylab
import rf_dist 
import T_dist
import pylab
import Q_dist
import KC_dist




def main(tempSim,mode,Cluster,Text):
    distances=np.array(tempSim)
    distArray = ssd.squareform(distances)
    fc='b'
    if (Cluster.upper()=="Y"):
            linkage_matrix = average(distArray)
            fc= hier.fcluster(linkage_matrix, 6, criterion='maxclust')
    if mode=="2D":
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
       
        pos = mds.fit_transform(distances)
        xs, ys = pos[:, 0], pos[:, 1]
        plt.scatter(xs, ys, c=fc)
        if (Text.upper()=="Y"): 
            for x, y, name in zip(xs, ys, trees):
                plt.text(x, y, "tree" + name)
        plt.show()
    else:
            fig = plt.figure()
            subpl = fig.add_subplot(111,projection='3d')
            mds = MDS(n_components=3,dissimilarity="precomputed", random_state=6)
            pos = mds.fit_transform(distances)
            xs, ys,zs = pos[:, 0], pos[:, 1], pos[:, 2]
            subpl.scatter(pos[:, 0], pos[:, 1], pos[:, 2],c=fc)
            if (Text.upper()=="Y"): 
                for x, y,z,name in zip(xs, ys, zs, trees):
                    subpl.text(x, y, z, "tree" + name)
            plt.show()

           
 

array = []
tree1=[]
tree2=[]
dist=[]
with open("Random_200.txt") as f:
    for line in f:
         array.append(line.replace('\n', ''))

n_samples = len(array)
seed = np.random.RandomState(seed=2)


trees=[]
Histro=[]
tempSim=[]
for x in range (0,len(array)):
    trees.append(str(x))
    temp=[]
    for y in range (0,len(array)):
        dist=KC_dist.main(array[x], array[y],0)
        temp.append(dist)
        Histro.append(dist)
    tempSim.append(temp)

main(tempSim,"3D","N","Y")