from ete3 import Tree, TreeStyle, TextFace, add_face_to_node,NodeStyle


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
        return 1
    
def label_parent(list_c):
    print(list_c)
    c=len(list_c)
    label=0
    #print("length is:",c)
    for i in range(0,c):
        n=list_c[i]+i
        k=i+1
        label += ncr(n,k)
        #print(label)
    return label
    
def main(t1):


    for node in t1.traverse("postorder"):
        if(node.is_leaf()==True):
            node.add_features(label=1)
            print(node.label)
        else:
            
            child=node.children
            c_labels=[]
            for c in child:
                c_labels.append(c.label)
            c_labels=sorted(c_labels, key=int, reverse=False) 
            node.name=label_parent(c_labels)
            node.add_features(label=label_parent(c_labels))
    return t1