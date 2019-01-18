import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from scipy.cluster import hierarchy as hier
from scipy.spatial import distance as ssd
from sklearn.manifold import MDS
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pylab





def main(a,auto):
    bins=8
    if (auto.upper()=="Y"): bins="auto"
    plt.hist(a, bins=bins)  
    plt.show()
    plt.savefig("abc.png")
    return plt 
    
 

