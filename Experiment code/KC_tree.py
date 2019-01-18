from ete3 import Tree, TreeStyle, TextFace, add_face_to_node,NodeStyle
import six
from itertools import combinations, permutations, product
from collections import namedtuple,OrderedDict
import numpy as np
import time
import os,sys

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
            hola = TextFace("m:" + str(depth-1))
            root.add_face(hola, column=0, position = "branch-top")
            #hola = TextFace("  M:"+str(branch-root.dist))
            #root.add_face(hola, column=1, position = "branch-top")
            for pairs in sorted(list(product(subtree_l,subtree_r))):
                pairs=','.join((sorted(pairs)))
                d[pairs]=depth
                d_len[pairs]=branch
             
            subtree_full=subtree_l+subtree_r 
            return d,subtree_full,d_len,(depth-1),branch-root.dist
            
        else:
            d_len[str(root.name)]=root.dist
            d[str(root.name)]=1
            return d,[root.name],d_len,depth-1,branch
            
        
        
def drawtree( tree1, node,depth,branch):
        if(node.is_leaf() is False):
            depth=depth+1
            branch=branch+node.dist          
            tree1=lowestCommonAncestor(tree1,node.children[0],depth,branch)
            tree1=lowestCommonAncestor(tree1,node.children[1],depth,branch)
            hola = TextFace("hola")
            return tree1
            
        else:
            return tree1 
            
        


def main(argv):
    start=time.time()

    tree1 = _Tree(str(argv[1]))
    save=int(argv[2])
    #tree2 = _Tree(str(arg2))
    
    d1=dict()
    d1_len=dict()
    d2=dict()
    d2_len=dict()
    root=tree1._tree.get_tree_root()
    #root2=tree2._tree.get_tree_root()  
    depth=0
  
    d1,subtrees,d1_len,depth,branch=tree1.lowestCommonAncestor(root,d1, d1_len,depth,0) 
    #d2,subtrees2,d2_len,depth2,branch=tree2.lowestCommonAncestor(root2,d2,d2_len,0,0)
   
    L=[]
    for leaf in tree1._tree:
        L.append(leaf.name)
    L=sorted(L)
    '''
    for keys in d1:
        list=keys.split(",")
        
        if(len(list)==1):
            node_current=tree1.search_nodes(name=list[0])[0]
            node_current.set_style(nstyle)
            node_current.add_face(hola, column=0, position = "branch-top")
        else:
            node_current = tree1.get_common_ancestor(L[0],L[1])
            node_current.set_style(nstyle)
            node_current.add_face(hola, column=0, position = "branch-top")
    '''
    ts = TreeStyle()
    ts.show_leaf_name = True
    
   
    if(save==1):
        if os.path.exists("crud/static/crud/Tree1.png"):
             os.remove("crud/static/crud/Tree1.png")
        tree1._tree.render("crud/static/crud/Tree1.png", tree_style=ts)
    else:
        if os.path.exists("crud/static/crud/Tree2.png"):
             os.remove("crud/static/crud/Tree2.png")
        tree1._tree.render("crud/static/crud/Tree2.png", tree_style=ts)
    
    return True

     

if __name__ == '__main__':
    main(sys.argv)