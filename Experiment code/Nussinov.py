import numpy as np
from ete3 import Tree



def score_fun(x,y):
    
    comparison = 0
    if (x == 'C' and y == 'G') or (x== 'G' and y == 'C') or (x == 'A' and y == 'U') or (x == 'U' and y == 'A')or (x == 'U' and y == 'G')or (x == 'G' and y == 'U'):
        comparison = 1
    return comparison
            
def predict(seq):
    seq=seq.upper()
    N = len(seq)
    output = ["."] * N
    Matrix = np.zeros((N,N))

    for n in range(2,N):
        for j in range(n,N):
            i = j-n
            diag = Matrix[i+1,j-1] + score_fun(seq[i],seq[j])
           
            max_v = 0
            for k in range(i,j-1):
                
                max_v=max(Matrix[i,k] + Matrix[k+1,j],max_v)
            Matrix[i,j] = max(Matrix[i+1,j],Matrix[i,j-1],diag,max_v)

    

    path = [0,N-1]

    while path:
        j = path.pop()
        i= path.pop()
        if j - i > 2:
        
            left = Matrix[i,j-1]
            down = Matrix[i+1,j]
            diag = Matrix[i+1,j-1]
            
            match = score_fun(seq[i],seq[j])
            
            if Matrix[i,j] == diag + match and match != 0:
               
                output[i] = "("
                output[j] = ")"
               
                path.append(i+1)
                path.append(j-1) 
                
            elif Matrix[i,j] == left:
                
                path.append(i)
                path.append(j-1) 
            elif Matrix[i,j] == down:
                path.append(i+1)
                path.append(j) 

            else:
               
                max_v = 0
                temp_max = 0
                for k in range(i,j-1):
                    if max_v < Matrix[i,k] + Matrix[k+1,j]:
                        max_v = Matrix[i,k] + Matrix[k+1,j]
                        temp_max = k
                path.append(i)
                path.append(temp_max) 
                path.append(temp_max+1)
                path.append(j) 
          
            
    return  "".join(output)
def main(s):
    top=predict(s)
    top=top+";"
    return(top)