#!/usr/bin/python
from ete3 import Tree
import random
from Bio import SeqIO
from Bio.Align.Applications import ClustalOmegaCommandline
import sys
from subprocess import call
from Bio.Align.Applications import MuscleCommandline

rfdist = 0
leaf_num = 0 

def getRandomNode(tree):
    return tree.get_leaf_names()[random.randint(0, len(tree.get_leaves())-1)]
        

def readFasta(fasta_file):
    return list(SeqIO.parse(fasta_file, "fasta"))
                
def check_what_algorithm(alg, in_file, out_file):
    if alg == "CLUSTAL":
        clustalomega_cline = ClustalOmegaCommandline(infile=in_file, outfile = out_file, verbose=True, auto=True)
        return clustalomega_cline
    elif alg.upper() == "KALIGN":
        return 0
     
def main(arg1, arg2):
    
    t1=Tree()
    tree1=Tree(arg1)
    
    tree2=Tree(arg2)

    node_midpoint = getRandomNode(tree1)
   
    tree1.set_outgroup(node_midpoint)
    
    tree2.set_outgroup(node_midpoint)
    
    
    t1, tree2=tree2.get_tree_root().children
    t1, tree1=tree1.get_tree_root().children
    count = 0
    for leaf in tree1.traverse("postorder"):
        if(leaf.name.strip()):
            count += 1
            leaf.add_features(order=count)
            CurrentNode2=tree2&leaf.name
            CurrentNode2.add_features(order=count)
            
        elif(leaf.name!=node_midpoint):
            leaf.name="int"
            
   
    
    for node in tree2.traverse("postorder"):
        if(node.name==""):
            node.name="int"
    
    Num_splits1=0
    Num_splits2=0
    Num_shared=0
    for node in tree1.traverse("postorder"):
       
        if((node.name=="int")):
            Num_splits1+=1
            cmin=float("+inf")     
            cmax=0
            d1,d2=node.get_children()
            subtree=Tree()
            subtree.add_child(d1)
            subtree.add_child(d2)
            
            for leaf in subtree:
            
                if ((leaf.name!="int")):
                    CurrentNode2=tree1&leaf.name
                    cmin=min( CurrentNode2.order, cmin)
                    cmax=max( CurrentNode2.order, cmax)
                    
            if((node.is_root()==False)):
                node.name="["+str(cmin)+":"+str(cmax)+"]" 

    
    for node in tree2.traverse("postorder"):
       
        if((node.name=="int") and (node.is_root()==False)):
            Num_splits2+=1
            cmin=float("+inf")    
            cmax=0
            size=0
            d1,d2=node.get_children()
            subtree2=Tree()
            subtree2.add_child(d1)
            subtree2.add_child(d2)
            
            for leaf in subtree2:
                size+=1
                if ((leaf.name!="int") and (leaf.name!=node_midpoint)):
                    CurrentNode2=tree2&leaf.name
                    cmin=min( CurrentNode2.order, cmin)
                    cmax=max( CurrentNode2.order, cmax)
            if(size==(cmax-cmin+1)):
                node.name="["+str(cmin)+":"+str(cmax)+"]" 
            if(tree1.search_nodes(name=node.name)):
                Num_shared+=1
    global leaf_num 
    leaf_num = len(tree2.get_leaves())    
    

    rf_dist=Num_splits1+Num_splits2-(2*Num_shared)
   

    return rf_dist
   

    

if __name__ == "__main__":
    s1="(((ab, ad), (ac, aa)), (ae, af));"

    s2="((ab, ad), ((ac, (af, ae)), aa));"
    main(s1,s2)