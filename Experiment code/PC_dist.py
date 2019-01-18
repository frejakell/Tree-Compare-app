#! /usr/bin/env python3

from collections import defaultdict
from dendropy import Tree
from math import sqrt

import operator as op
from functools import reduce

def ncr(n, k):
    #print("n:" ,n)
    #print("k:" ,k)
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0
    
def label_parent(list_c):
    #print(list_c)
    c=len(list_c)
    label=0
    #print("length is:",c)
    for i in range(0,c):
        n=(list_c[i]+i)
        k=i+1
        label += ncr(n,k)
        #print(label)
    return label


def annotate_rooted_tree(tree):

    assert isinstance(tree, Tree)
    for node in tree.postorder_node_iter():
        if not node.child_nodes():
            node.annotations['CP-label'].value = 1
        else:
            #print((x.annotations['CP-label'].value for x in node.child_nodes()))
            child=[]
            for x in node.child_nodes():
                child.append(x.annotations['CP-label'].value)
            
            child=sorted(child, key=int, reverse=False)
            
            label = label_parent(child)
      
            node.annotations['CP-label'].value = label


def get_root_label(tree):

    r = tree.seed_node.annotations['CP-label'].value
    if r:
        return r
    else:
        annotate_rooted_tree(tree)
        return tree.seed_node.annotations['CP-label'].value


def get_rooted_vector(tree):

    if not tree.seed_node.annotations['CP-label'].value:
        annotate_rooted_tree(tree)
    r = []
    for node in tree.postorder_node_iter():
        r.append(node.annotations['CP-label'].value)
    r = sorted(r)
    return r




def get_neighbours(node):

    r = []
    if node.child_nodes():
        r += [x for x in node.child_nodes()]
    if node.parent_node:
        r.append(node.parent_node)
    return r





def vector_dict(vector):

    r = defaultdict(lambda: 0)
    for element in vector:
        r[element] += 1
    return r


def euclidean(d1, d2):

    square_sum = 0
    s1 = set(d1.keys())
    key_set = s1.union(set(d2.keys()))
    
    for label in key_set:
        square_sum += (d1[label] - d2[label])**2
    return sqrt(square_sum)
def main(arg1,arg2):
    

    t1 = Tree.get(data=arg1, schema='newick')
    t2 = Tree.get(data=arg2, schema='newick')

    return euclidean(vector_dict(get_rooted_vector(t1)),vector_dict(get_rooted_vector(t2)))
 
s1="(1,2,((((((9)),12),14)),(((20)))),(((28,(30),(((((37,38)))),((45)))))),(53));"
s2="(1,2,((((((9)),12),14)),(((20)))),(((28,(30),(((((37,38)))),((45)))))),(53));"

print(main(s1,s2))