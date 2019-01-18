from ete3 import Tree, TreeStyle, TextFace, add_face_to_node,NodeStyle
import six
from itertools import combinations, permutations, product
from collections import namedtuple,OrderedDict
import numpy as np
import time
import os,sys

import numpy as np


        


def main(argv):
    start=time.time()
    style1 = NodeStyle()
    style1["fgcolor"] = "#0f0f0f"
    style1["size"] = 0
    #style1["vt_line_color"] = "#ff0000"
    style1["hz_line_color"] = "#ff0000"
    #style1["vt_line_width"] = 2
    style1["hz_line_width"] = 2
    #style1["vt_line_type"] = 2 # 0 solid, 1 dashed, 2 dotted
    #style1["hz_line_type"] = 2
    
    style2 = NodeStyle()
    style2["fgcolor"] = "#0f0f0f"
    style2["size"] = 0
    style2["vt_line_color"] = "#ff0000"
    #style2["hz_line_color"] = "#ff0000"
    style2["vt_line_width"] = 2
    #style2["hz_line_width"] = 2
    style2["vt_line_type"] = 2 # 0 solid, 1 dashed, 2 dotted
    #style2["hz_line_type"] = 2
    
    tree1 = Tree(str(argv[1]))
    save=int(argv[3])
    leafs=argv[2]
    leafs=leafs.replace("(","")
    leafs=leafs.replace(")","")
    leafs=leafs.replace("'","")
    leafs=leafs.replace(" ","")
    q=leafs.split(',')
    
    #tree2 = _Tree(str(arg2))
   
    se=tree1.get_common_ancestor(q)
    

    
    for n in q:
        print(n)
        node = tree1&n
        while(node.up!=se):
            node.img_style = style1
            node=node.up
    #n.img_style = style2
   
        node.img_style = style1
    ts = TreeStyle()
    ts.show_leaf_name = True
   
    
 
    
   
    if(save==1):
        if os.path.exists("crud/static/crud/Tree1.png"):
             os.remove("crud/static/crud/Tree1.png")
        tree1.render("crud/static/crud/Tree1.png", tree_style=ts)
    else:
        if os.path.exists("crud/static/crud/Tree2.png"):
             os.remove("crud/static/crud/Tree2.png")
        tree1.render("crud/static/crud/Tree2.png", tree_style=ts)
    
    return True

     

if __name__ == '__main__':
    main(sys.argv)