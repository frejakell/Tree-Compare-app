#!/usr/bin/python
import ete3
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node,NodeStyle
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
def Reorder(t1):  
    for node in t1.traverse("preorder"):
            
            if node.is_leaf()==False:
                child=node.get_children()
                dict_c={}
                for i in range(len(child)):
                    cc=child[i]
                   # print(cc)
                    ls=[]
                    for leaf in cc :
                        ls.append(leaf.name)
                    ls= sorted(ls)
                    dict_c[i]=ls[0]
                print(dict_c)
                #WantedOutput = sorted(MyDict, key=lambda x : MyDict[x])
                sorted_keys = sorted(dict_c, key=dict_c.get)
                node.remove_child(child[sorted_keys[1]])
                node.add_child(child[sorted_keys[1]])
    return t1
def main(arg1, arg2):
    style1 = NodeStyle()
    style1["fgcolor"] = "#0f0f0f"
    style1["size"] = 0
    style1["hz_line_color"] = "#ff0000"
    style1["hz_line_width"] = 2

    # 0 solid, 1 dashed, 2 dotted

    t1=Tree()
    tree1=Tree(arg1)
    
    tree2=Tree(arg2)

    node_midpoint = getRandomNode(tree1)
   
    tree1.set_outgroup(node_midpoint)
    
    tree2.set_outgroup(node_midpoint)
    
    
   
    count = 0
    for leaf in tree1.get_tree_root().children[1].traverse("postorder"):
        if(leaf.name.strip()):
            count += 1
            leaf.add_features(order=count)
            CurrentNode2=tree2&leaf.name
            CurrentNode2.add_features(order=count)
            
        elif(leaf.name!=node_midpoint):
            leaf.name="int"
            
   
    
    for node in tree2.get_tree_root().children[1].traverse("postorder"):
        if(node.name==""):
            node.name="int"
    
    Num_splits1=0
    Num_splits2=0
    Num_shared=0
    for node in tree1.get_tree_root().children[1].traverse("postorder"):
       
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

    nodes_split=[]
    for node in tree2.get_tree_root().children[1].traverse("postorder"):
       
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
            else: 
                node.name="["+str(cmin)+":"+str(cmax)+"]" 
                nodes_split.append(node.name)
                node.img_style = style1
                #node.children[1].img_style = style1

    global leaf_num 
    leaf_num = len(tree2.get_leaves())    
    
    #t1=Reorder(t1)
    tree2=Reorder(tree2)
    rf_dist=Num_splits1+Num_splits2-(2*Num_shared)
    print(nodes_split)
    ts = TreeStyle()
    ts.show_leaf_name = True
    #tree2.show(tree_style=ts)
    tree2.render("crud/static/crud/Tree3.png", tree_style=ts)
    
    return rf_dist

if __name__ == "__main__":
    s1="((ab, ad), ((ac, (af, ae)), aa));"

    s2="((ae, ((ac, ad), ab)), (af, aa));"
    dist=main(s1,s2)
    dist=main(s2,s1)
    print(dist)
    t1 = Tree(s1 )
    
 
    
   
    #t1.show(tree_style=ts)
    
    '''for node in t1.traverse("preorder"):
         
        if node.is_leaf()==False:
            child=node.get_children()
            dict_c={}
            for i in range(len(child)):
                cc=child[i]
               # print(cc)
                ls=[]
                for leaf in cc :
                    ls.append(leaf.name)
                ls= sorted(ls)
                dict_c[i]=ls[0]
            print(dict_c)
            #WantedOutput = sorted(MyDict, key=lambda x : MyDict[x])
            sorted_keys = sorted(dict_c, key=dict_c.get)
            node.remove_child(child[sorted_keys[1]])
            node.add_child(child[sorted_keys[1]])
            
            #print(ls)'''
    #print("----------------------------------------------------------------------------------------")        
    t2 = Tree(s2 )
    '''for node in t2.traverse("preorder"):
        if node.is_leaf()==False:
            
            node.swap_children()
            
            #print(t2)
    # t2.show(tree_style=ts)'''
    #t1=Reorder(t1)
    #t2=Reorder(t2)
    print(t1)
    print(t2)