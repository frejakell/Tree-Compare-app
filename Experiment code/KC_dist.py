from ete3 import Tree,TreeStyle
import six
from itertools import combinations, permutations, product
from collections import namedtuple,OrderedDict
import numpy as np
import time

import numpy as np

class _Tree:
    
    def __init__(  self,newick=None,name=None, **kwargs):
       self._tree =Tree(newick)  
       self._tree.is_rooted = True
       self.name = name
       self.lbda=0


   
    def lowestCommonAncestor(self, root,d,d_len,depth,branch):
        if(root.is_leaf() is False):
            depth=depth+1
            branch=branch+root.dist          
            
            d,subtree_r,d_len,d_temp,branch_temp=self.lowestCommonAncestor(root.children[0],d,d_len,depth,branch)
            d,subtree_l,d_len,d_temp,branch=self.lowestCommonAncestor(root.children[1],d,d_len,depth,branch)
           
            
            for pairs in sorted(list(product(subtree_l,subtree_r))):
                pairs=''.join((sorted(pairs)))
                d[pairs]=depth
                d_len[pairs]=branch
             
            subtree_full=subtree_l+subtree_r 
            return d,subtree_full,d_len,(depth-1),branch-root.dist
            
        else:
            d_len[str(root.name)]=root.dist
            d[str(root.name)]=1
            return d,[root.name],d_len,depth-1,branch
            
        
        



def main(arg1,arg2, lbda):
    start=time.time()

    tree1 = _Tree(str(arg1))
    tree2 = _Tree(str(arg2))
    d1=dict()
    d1_len=dict()
    d2=dict()
    d2_len=dict()
    root=tree1._tree.get_tree_root()
    root2=tree2._tree.get_tree_root()  
    depth=0
  
    d1,subtrees,d1_len,depth,branch=tree1.lowestCommonAncestor(root,d1, d1_len,depth,0) 
    d2,subtrees2,d2_len,depth2,branch=tree2.lowestCommonAncestor(root2,d2,d2_len,0,0)
    V_1 = []
    V_2 = []
    
    for k,v in d1.items():
        V_1.append(((lbda)*(d1_len[k]))+((1-lbda)*(v ) ))
        V_2.append(((lbda)*(d2_len[k]))+((1-lbda)*(d2[k]) ))
        
    V_1=np.array(V_1)
    V_2=np.array(V_2)

    return(np.sqrt(((V_1 - V_2) ** 2).sum()))
    end=time.time() 

     

if __name__ == '__main__':
    s1="(((ab, ad), (ac, aa)), (ae, af));"
    s2="((ab, ad), ((ac, (af, ae)), aa));"
    main(s1,s2,0)