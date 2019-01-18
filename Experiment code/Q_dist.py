from ete3 import Tree,TreeStyle
from math import factorial
from ete3 import Tree,TreeStyle
from itertools import combinations, product

def list_def(l_quars,list1, list2, list3):
    #print(list1)
    #print(list2)
    #print(list3)
    gs=list(combinations(list1, 2))
    list_full=[]
    for ele in gs:
        for leaf in list2:
            
            
            temp=ele
            
            temp=temp+(leaf,)
            
            list_full.append(temp)
    list_comp=[]
    for ele in list_full:
        for leaf in list3:
            
            
            temp=ele
            temp=temp+(leaf,)
            #print(sorted(temp))
            list_comp.append(tuple(sorted(temp)))
    l_quars=set(l_quars)-set(list_comp)
           
    return(l_quars)



def calculate_combinations(n, r):
    if(n-r)>=0:return factorial(n) // factorial(r) // factorial(n-r)
    else: return 0
def prepostorder(self):
        _leaf = self.__class__.is_leaf
        to_visit = [self]
        

        while to_visit:
            node = to_visit.pop(-1)
            try:
                node = node[1]
            except TypeError:
              
                yield (False, node)
                if not _leaf(node):
                   
                    to_visit.extend(reversed(node.children + [[1, node]]))
            else:
           
                yield (True, node)
                
                
def path_from_root_to_node(t):
    d_node=dict()
    d_children=dict()
    edge = 0
    for node in t.traverse():
       if not node.is_leaf():
          node.name = edge
          edge += 1


    current_path = [t]
    for postorder, node in prepostorder(t):
        
        
        if postorder:
            
            current_path.pop(-1)
        else:
            if not node.children:
                
                
                d_node[node.name]=[]
                d_children[node.name]=[]
               
                for i in range(1,len(current_path)):  
              
                 
                    if current_path[i] !=0:
                        d_node[node.name].append(current_path[i])
                pass
                
            else:
                current_path.append(node.name)
                d_children[node.name]=[node.children[0].name,node.children[1].name]
    return d_node,d_children
def descendant_iterator(node, d_children, subtree):
    
    if len(d_children[node])!=0:
       
       for child in d_children[node]:
            if(isinteger(child)==False and child is not "[...]"):
                subtree.append(child)
                
            else:
                subtree=descendant_iterator(child, d_children, subtree)
    return subtree
    
def isinteger(a):
    try:
        int(a)
        return True
    except ValueError:
        return False
def main(arg1, arg2):              

    s2 =str(arg1)
    s1 =str(arg2) 
    shared=0
    d_node=dict()
    d_path=dict()
    d_children=dict()
    t1 = Tree(s1)
    #print(t1)
    t2 = Tree(s2)
    L=[]
    
    for leaf in t1:
        L.append(leaf.name)
    L=sorted(L)
    d_node,d_children=path_from_root_to_node(t1)
    d_node2,d_children2=path_from_root_to_node(t2)
    #print(d_node,d_children)
    all_comb=list(combinations(L,4))
    
   
    #print(all_comb)
    Red=[]
    Blue=[]
    quars=all_comb
    for node in t1.traverse("levelorder"):
         if not node.is_leaf():
            subtree1=[]
            subtree2=[]
            children=d_children[node.name]
            if(isinteger(children[0])==False):
                subtree1.append(children[0])
               
            if(isinteger(children[1])==False):
                subtree2.append(children[1])
                
            subtree1=descendant_iterator(children[0],d_children,subtree1)
            subtree2=descendant_iterator(children[1],d_children,subtree2)
            subtree3=list(set(L)-set(subtree1)-set(subtree2))
            #print(node.name)
            #print(subtree1)
            #print(subtree2)
            red=subtree1
            blue=subtree2
            green=subtree3
            for node in t2.traverse("levelorder"):
              if not node.is_leaf():
                subtree1=[]
                subtree2=[]
                subtree3=[]
                children=d_children2[node.name]
                if(isinteger(children[0])==False ):
                    subtree1.append(children[0])
                    
                if(isinteger(children[1])==False):
                    subtree2.append(children[1])
                   
                subtree1=descendant_iterator(children[0],d_children2,subtree1)
                subtree2=descendant_iterator(children[1],d_children2,subtree2)
                subtree3=list(set(L)-set(subtree1)-set(subtree2))
                subtree1_blue= list(set(subtree1).intersection(blue))
                subtree1_red=list(set(subtree1).intersection(red))
                subtree1_green=list(set(subtree1).intersection(green))               
                subtree2_blue=list(set(subtree2).intersection(blue))
                subtree2_red =list(set(subtree2).intersection(red))
                subtree2_green=list(set(subtree2).intersection(green))
                subtree3_blue=list(set(subtree3).intersection(blue))
                subtree3_red =list(set(subtree3).intersection(red))
                subtree3_green=list(set(subtree3).intersection(green))
               
                quars=list_def(quars,subtree1_blue,subtree2_green, subtree3_red)
                quars=list_def(quars,subtree1_blue,subtree3_green, subtree2_red)
                quars=list_def(quars,subtree1_red,subtree2_green, subtree3_blue)
                quars=list_def(quars,subtree1_red,subtree3_green, subtree2_blue)
                quars=list_def(quars,subtree1_green,subtree2_red, subtree3_blue)
                quars=list_def(quars,subtree1_green,subtree3_red, subtree2_blue)
                quars=list_def(quars,subtree2_blue,subtree1_green, subtree3_red)
                quars=list_def(quars,subtree2_blue,subtree3_green, subtree1_red)
                quars=list_def(quars,subtree2_red,subtree1_green, subtree3_blue)
                quars=list_def(quars,subtree2_red,subtree3_green, subtree1_blue)
                quars=list_def(quars,subtree2_green,subtree1_red, subtree3_blue)
                quars=list_def(quars,subtree2_green,subtree3_red, subtree1_blue)
                
                quars=list_def(quars,subtree3_blue,subtree1_green, subtree2_red)
                quars=list_def(quars,subtree3_blue,subtree2_green, subtree1_red)
                quars=list_def(quars,subtree3_red,subtree1_green, subtree2_blue)
                quars=list_def(quars,subtree3_red,subtree2_green, subtree1_blue)
                quars=list_def(quars,subtree3_green,subtree1_red, subtree2_blue)
                quars=list_def(quars,subtree3_green,subtree2_red, subtree1_blue)

                sub1_b2= calculate_combinations(len(subtree1_blue),2)#len( list(combinations))
                sub1_r2= calculate_combinations(len(subtree1_red),2)#len( list(combinations(subtree1_red,2)))
                sub1_g2=calculate_combinations(len(subtree1_green),2)#len( list(combinations(subtree1_green,2)))
                sub2_b2= calculate_combinations(len(subtree2_blue),2)#len( list(combinations(subtree2_blue,2)))
                sub2_r2= calculate_combinations(len(subtree2_red),2)#len( list(combinations(subtree2_red,2)))
                sub2_g2= calculate_combinations(len(subtree2_green),2)#len( list(combinations(subtree2_green,2)))
                sub3_b2= calculate_combinations(len(subtree3_blue),2)#len( list(combinations(subtree3_blue,2)))
                sub3_r2= calculate_combinations(len(subtree3_red),2)#len( list(combinations(subtree3_red,2)))
                sub3_g2= calculate_combinations(len(subtree3_green),2)#len( list(combinations(subtree3_green,2)))
                
                shared=shared +sub1_r2*len(subtree2_blue)*len(subtree3_green)
                shared=shared +sub1_r2*len(subtree3_blue)*len(subtree2_green)
                shared=shared +sub1_b2*len(subtree2_red)*len(subtree3_green)
                shared=shared +sub1_b2*len(subtree3_red)*len(subtree2_green)
                shared=shared +sub1_g2*len(subtree2_red)*len(subtree3_blue)
                shared=shared +sub1_g2*len(subtree3_red)*len(subtree2_blue)

                     
                
                shared=shared +sub2_r2*len(subtree1_blue)*len(subtree3_green)
                shared=shared +sub2_r2*len(subtree3_blue)*len(subtree1_green)
                shared=shared +sub2_b2*len(subtree1_red)*len(subtree3_green)
                shared=shared +sub2_b2*len(subtree3_red)*len(subtree1_green)                
                shared=shared +sub2_g2*len(subtree1_red)*len(subtree3_blue)
                shared=shared +sub2_g2*len(subtree3_red)*len(subtree1_blue)
                
                shared=shared +sub3_r2*len(subtree1_blue)*len(subtree2_green)
                shared=shared +sub3_r2*len(subtree2_blue)*len(subtree1_green)
                shared=shared +sub3_b2*len(subtree1_red)*len(subtree2_green)
                shared=shared +sub3_b2*len(subtree2_red)*len(subtree1_green)                
                shared=shared +sub3_g2*len(subtree1_red)*len(subtree2_blue)
                shared=shared +sub3_g2*len(subtree2_red)*len(subtree1_blue)
                
   
    dist=len( list(combinations(L,4)))-shared/2 
    print(len(quars), dist )  
    return dist
 

if __name__ == '__main__':
    s1="(ab, (ad, ((af, (aa, ac)), ae)));"

    s2="(((ad, ab), aa), ((af, ae), ac));"
    main(s1,s2)