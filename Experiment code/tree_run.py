import os,sys
from ete3 import Tree,TreeStyle
from itertools import combinations
import tree_run2

def main(argv):  

    
    
    t = Tree(argv[1])
    save=int(argv[2])
    ts=TreeStyle()
    
    # ts.tree_width = 50
    #t.show(tree_style=ts)
    if(save==1):
        if os.path.exists("crud/static/crud/Tree1.png"):
             os.remove("crud/static/crud/Tree1.png")
        t.render("crud/static/crud/Tree1.png", tree_style=ts)
    else:
        if os.path.exists("crud/static/crud/Tree2.png"):
             os.remove("crud/static/crud/Tree2.png")
        t.render("crud/static/crud/Tree2.png", tree_style=ts)

if __name__ == '__main__':

    main(sys.argv)